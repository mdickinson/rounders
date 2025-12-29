"""Representations of intermediate values."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, replace

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from rounders.modes import RoundingMode

#: Pattern for string representation of an intermediate form value.
_INTERMEDIATE_FORM_PATTERN = re.compile(
    r"""
    (?P<sign>-?)
    (?P<intpart>[0-9]+)
    (\.(?P<fracpart>[0-9]+))?
    (e(?P<exponent>-?[0-9]+))?
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class IntermediateForm:
    """
    Intermediate value for rounding and formatting operations.

    This is essentially a more accessible version of the Decimal type, that only
    supports finite Decimal instances.

    The value represented is (-1)**sign * significand * 10**exponent.
    """

    # 1 for negative, 0 for positive
    sign: int

    # Significand: a nonnegative integer
    significand: int

    # Exponent
    exponent: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        """
        Create an intermediate form from a string.

        This is currently aimed at test convenience rather than users, and so is rather
        strict about input format.
        """
        if (match := _INTERMEDIATE_FORM_PATTERN.fullmatch(s)) is None:
            raise ValueError(f"invalid numeric string: {s}")

        fracpart = match["fracpart"] or ""
        return cls(
            sign=1 if match["sign"] == "-" else 0,
            significand=int(match["intpart"] + fracpart),
            exponent=int(match["exponent"] or 0) - len(fracpart),
        )

    @property
    def figures(self) -> int:
        """
        Number of decimal digits in the significand.

        Returns zero if the significand is zero.
        """
        return len(str(self.significand)) if self.significand != 0 else 0

    @property
    def decade(self) -> int:
        """Return an integer e such that 10**e <= abs(self) < 10**(e+1)."""
        if self.significand == 0:
            raise ValueError(f"zero value {self} has no decade")
        return self.exponent + self.figures - 1

    def is_zero(self) -> bool:
        """Return True if value is zero, else False."""
        return self.significand == 0

    def trim(self, figures: int) -> IntermediateForm:
        """
        Trim to a given number of significant figures by removing trailing zeros.

        Raises ValueError if trimming would involve removing non-zero digits.
        """
        diff = self.figures - figures
        if diff <= 0:
            return self

        new_significand, remainder = divmod(self.significand, 10**diff)
        if remainder:
            raise ValueError("trim would remove nonzero digits")
        return replace(self, significand=new_significand, exponent=self.exponent + diff)

    def round(self, exponent: int, mode: RoundingMode) -> IntermediateForm:
        """Round to the given exponent, using the given rounding mode."""
        diff = self.exponent - exponent
        if diff >= 0:
            # No change in value; just adding zeros.
            return replace(
                self, significand=self.significand * 10**diff, exponent=exponent
            )
        else:
            # Split into kept digits, rounding digit and trailing digits
            ten_diff = 10**~diff
            kept, remainder = divmod(self.significand, 10 * ten_diff)
            rounding, trailing = divmod(remainder, ten_diff)
            # Incorporate trailing into rounding digit
            rounding += trailing and rounding in {0, 5}
            significand = mode.round(self.sign, kept, rounding)
            return IntermediateForm(
                sign=self.sign,
                significand=significand,
                exponent=exponent,
            )

    def force_unsigned_zero(self) -> IntermediateForm:
        """Replace a negative zero with an unsigned zero."""
        return (
            self
            if self.significand != 0
            else IntermediateForm(
                sign=0,
                significand=self.significand,
                exponent=self.exponent,
            )
        )

    def __int__(self) -> int:
        """Convert a value with exponent 0 to an integer."""
        if self.exponent != 0:
            raise ValueError("can only convert a value with exponent 0 to an integer")
        return -self.significand if self.sign else self.significand

    def __str__(self) -> str:
        """Return a simple string representation of an intermediate form."""
        return f"{'-' * self.sign}{self.significand}e{self.exponent}"

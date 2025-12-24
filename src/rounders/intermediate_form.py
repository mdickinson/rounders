"""Representations of intermediate values."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, replace
from typing import cast

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

_5_POW_256 = 5**256

#: Lookup table from bits 9 through 2 of a power of 5 to the matching power.
_5_POW_FROM_LOW_BITS = {(5**e >> 2) & 0xFF: 5**e for e in range(256)}

#: Lookup table from bits 9 through 2 of a power of 5 to the matching exponent.
_5_POW_EXPONENT_FROM_LOW_BITS = {(5**e >> 2) & 0xFF: e for e in range(256)}


def _natural_exponent(d: int) -> int | None:
    """
    Find the largest integer e such that 1/d is a multiple of 10**e.

    Return None if there's no such integer.
    """
    if d <= 0:
        raise ValueError("d must be positive")

    # Count and remove powers of two.
    two_exp = (~(d | -d)).bit_length()
    d >>= two_exp

    # Determine whether d is a power of 5, and if so find its exponent.
    # Note: there are much faster ways of doing this, and if this ever proves to
    # be a performance bottleneck then we should optimize.
    five_exp = 0
    while d % 5 == 0:
        d //= 5
        five_exp += 1
    if d != 1:
        return None

    return -max(two_exp, five_exp)


def log5exact(d: int) -> int:
    """
    Find the exponent of an exact power of 5.

    Returns e if d = 5**e for some nonnegative integer e. Otherwise,
    raises ValueError.
    """
    if d <= 0 or d & 3 != 1:
        raise ValueError(f"{d} is not a power of 5")

    # If d is a power of 5, it's divisible by 5**e where e is determined
    # by the lower order bits of d.
    low_bits = d >> 2 & 0xFF
    d, rem = divmod(d, _5_POW_FROM_LOW_BITS[low_bits])
    if rem:
        raise ValueError(f"{d} is not a power of 5")
    five_exp = _5_POW_EXPONENT_FROM_LOW_BITS[low_bits]

    while True:
        q, r = divmod(d, _5_POW_256)
        if r:
            break
        else:
            d = q
            five_exp += 256
    if d != 1:
        raise ValueError(f"{d} is not a power of 5")

    return five_exp


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

    @classmethod
    def from_signed_fraction(
        cls, *, sign: int, numerator: int, denominator: int, exponent: int | None
    ) -> Self:
        """
        Create from a signed fraction, given a target exponent.

        Creates an IntermediateForm from a quotient of the form ±(n/d) with either the
        target exponent or the natural exponent of the input, using round-for-reround.
        The natural exponent of the input is the largest nonpositive integer e for which
        (n/d) / 10**e is an integer, if any such exists, else None.

        If exponent is None, then the signed fraction must be exactly representable
        in decimal format, otherwise a ValueError will be raised.

        `numerator` and `denominator` must be relatively prime, `denominator` must be
        positive, and `numerator` must be nonnegative.
        """
        if numerator < 0 or denominator <= 0:
            raise ValueError("Invalid signed fraction representation")

        exponents: list[int | None] = [_natural_exponent(denominator), exponent]
        exponent = max([e for e in exponents if e is not None], default=None)
        if exponent is None:
            raise ValueError(
                f"cannot represent fraction {numerator}/{denominator} "
                f"exactly as a decimal"
            )

        if exponent <= 0:
            n, d = numerator * cast(int, 10**-exponent), denominator
        else:
            n, d = numerator, denominator * cast(int, 10**exponent)

        # Round-for-reround
        significand, inexact = divmod(n, d)
        return cls(
            sign=sign,
            significand=significand + (inexact and significand % 5 == 0),
            exponent=exponent,
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

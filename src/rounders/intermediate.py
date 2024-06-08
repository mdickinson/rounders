"""Representations of intermediate values."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Optional, cast

from rounders.modes import RoundingMode


def _smallest_ten_power_multiple(d: int) -> int:
    """
    Find smallest power of 10 that's divisible by a positive integer d.

    Raises ValueError if there's no such power.
    """
    assert d > 0

    two_exp = (d & -d).bit_length() - 1
    d >>= two_exp

    five_exp = 0
    while d % 5 == 0:
        d //= 5
        five_exp += 1

    if d != 1:
        raise ValueError("d is not a divisor of any power of 10")

    return max(two_exp, five_exp)


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

    # Significand
    significand: int

    # Exponent
    exponent: int

    @classmethod
    def from_str(cls, s: str) -> IntermediateForm:
        """
        Create an intermediate form from a string.

        This is currently aimed at test convenience rather than users, and so is rather
        strict about input format.
        """
        # Temporary cheat: use Decimal
        from decimal import Decimal

        sign, digits, exponent = Decimal(s).as_tuple()
        if not isinstance(exponent, int):
            raise ValueError("Invalid representation of an IntermediateForm")
        return cls(
            sign=sign,
            significand=int("".join(map(str, digits))),
            exponent=exponent,
        )

    @classmethod
    def from_signed_fraction(
        cls, *, sign: int, numerator: int, denominator: int, exponent: Optional[int]
    ) -> IntermediateForm:
        """
        Create from a signed fraction, given a target exponent.

        Creates an IntermediateForm from a quotient of the form ±(n/d) with the target
        exponent, using round-for-reround.

        If exponent is None, then the signed fraction must be exactly representable
        in decimal format, otherwise a ValueError will be raised.

        `numerator` and `denominator` must be relatively prime, `denominator` must be
        positive, and `numerator` must be nonnegative.
        """
        if numerator < 0 or denominator <= 0 or math.gcd(numerator, denominator) != 1:
            raise ValueError("Invalid signed fraction representation")

        # Case where exponent is None: convert exactly if possible, else raise
        # a ValueError. We use the largest nonpositive exponent possible.
        if exponent is None:
            e = _smallest_ten_power_multiple(denominator)
            assert 10**e % denominator == 0
            return IntermediateForm(
                sign=sign,
                significand=numerator * (10**e // denominator),
                exponent=-e,
            )

        if exponent <= 0:
            n, d = numerator * cast(int, 10**-exponent), denominator
        else:
            n, d = numerator, denominator * cast(int, 10**exponent)

        # Round-for-reround
        significand, inexact = divmod(n, d)
        return IntermediateForm(
            sign=sign,
            significand=significand + (inexact and significand % 5 == 0),
            exponent=exponent,
        )

    @property
    def figures(self) -> int:
        """
        Number of decimal digits in the significand.

        Returns zero if the significant is zero.
        """
        return len(str(self.significand)) if self.significand != 0 else 0

    @property
    def decade(self) -> Optional[int]:
        """
        Returns an integer e such that 10**e <= abs(self) < 10**(e+1).

        If the value represented is zero, returns None.
        """
        if self.significand == 0:
            return None
        return self.exponent + self.figures - 1

    def nudge(self, figures: int) -> IntermediateForm:
        """Drop a zero in cases where rounding led us to end up with an extra zero."""
        if self.figures <= figures:
            return self

        if self.figures != figures + 1:
            raise ValueError("Can't drop more than one zero")

        new_significand, tenths = divmod(self.significand, 10)
        if tenths:
            raise ValueError(
                "Last digit is nonzero; dropping it would change the value"
            )

        return replace(
            self,
            significand=new_significand,
            exponent=self.exponent + 1,
        )

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

    def __repr__(self) -> str:
        """Return a simple string representation of an intermediate form."""
        return f"{'-' * self.sign}{self.significand}e{self.exponent}"

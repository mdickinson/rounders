"""
Representations of intermediate values.
"""

from dataclasses import dataclass, replace
from typing import cast


@dataclass(frozen=True)
class IntermediateForm:
    """
    Intermediate value for rounding and formatting operations.

    This is essentially a more accessible version of the Decimal type, that only
    supports finite Decimal instances.

    The value represented is (-1)**sign * significand * 10**exponent.
    """

    # True for negative, False for positive
    sign: bool

    # Significand
    significand: int

    # Exponent
    exponent: int

    @classmethod
    def from_signed_fraction(
        cls, *, sign: bool, numerator: int, denominator: int, exponent: int
    ) -> "IntermediateForm":
        """
        Create from a quotient of the form ±(n/d) with the target exponent, using
        round-for-reround.
        """
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

    def to_zero(self) -> "IntermediateForm":
        """
        Drop the least significant digit, rounding towards zero.
        """
        return replace(
            self, significand=self.significand // 10, exponent=self.exponent + 1
        )

    def to_away(self) -> "IntermediateForm":
        """
        Drop the least significant digit, rounding away from zero.
        """
        return replace(
            self, significand=-(-self.significand // 10), exponent=self.exponent + 1
        )

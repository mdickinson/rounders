"""
Representations of intermediate values.
"""

import dataclasses
from typing import cast


@dataclasses.dataclass(frozen=True)
class IntermediateForm:
    """
    Intermediate value for rounding and formatting operations.

    An IntermediateForm represents a value of the form significand * 10**exponent,
    where significand is a quarter integer (i.e., 4*significand is an integer).
    Signed zeros are supported.

    The value represented is (significand + quarters/4) * 10**exponent if sign is False,
    and the negation of that if sign is True.
    """

    # True for negative, False for positive.
    sign: bool

    # Nonnegative integer giving the integral part of the significand.
    significand: int

    # Integer giving the decimal exponent.
    exponent: int

    # Integer in range(4) giving the number of quarters in the significand.
    quarters: int = 0

    @classmethod
    def from_signed_fraction(
        cls, sign: bool, numerator: int, denominator: int, exponent: int
    ) -> "IntermediateForm":
        """
        Create from a quotient of the form ±(n/d).
        """
        if exponent <= 0:
            n, d = numerator * cast(int, 10**-exponent), denominator
        else:
            n, d = numerator, denominator * cast(int, 10**exponent)

        quarters, inexact = divmod(4 * n, d)
        whole, part = divmod(quarters | bool(inexact), 4)
        return IntermediateForm(
            sign=sign, significand=whole, quarters=part, exponent=exponent
        )

    def to_zero(self) -> "IntermediateForm":
        """
        Round towards zero to the nearest value with quarters = 0.
        """
        if not self.quarters:
            return self

        return IntermediateForm(
            sign=self.sign,
            significand=self.significand,
            exponent=self.exponent,
        )

    def to_away(self) -> "IntermediateForm":
        """
        Round away from zero to the nearest value with quarters = 0.
        """
        if not self.quarters:
            return self

        return IntermediateForm(
            sign=self.sign,
            significand=self.significand + 1,
            exponent=self.exponent,
        )

    def as_int(self) -> int:
        """
        Interpret as int, provided that the exponent is zero.
        """
        if self.exponent or self.quarters:
            raise ValueError("Not an exact integer")
        return -self.significand if self.sign else self.significand

    def nudge(self) -> "IntermediateForm":
        """
        Increment the exponent and divide the significand by 10.

        Expected to be used only when the signficand is divisible by 10.
        """
        significand, remainder = divmod(self.significand, 10)
        if remainder or self.quarters:
            raise ValueError("significand not divisible by 10")
        return IntermediateForm(
            sign=self.sign,
            significand=significand,
            exponent=self.exponent + 1,
        )

"""
Representations of intermediate values.
"""

import dataclasses
from typing import cast


@dataclasses.dataclass(frozen=True)
class IntermediateForm:
    """
    Intermediate value for rounding and formatting operations.

    This is essentially a more accessible version of the Decimal type, that only
    supports finite Decimal instances.

    The value represented is (-1)**sign * significand * 10**exponent.
    """

    # True for negative, False for positive.
    sign: bool

    # Significand
    significand: int

    # Exponent
    exponent: int

    @classmethod
    def from_signed_fraction(
        cls, sign: bool, numerator: int, denominator: int, exponent: int
    ) -> "IntermediateForm":
        """
        Create from a quotient of the form ±(n/d).
        """
        if exponent <= 1:
            n, d = numerator * cast(int, 10 ** (1 - exponent)), denominator
        else:
            n, d = numerator, denominator * cast(int, 10 ** (exponent - 1))

        # Round-for-reround
        tenths, inexact = divmod(n, d)
        if tenths % 5 == 0 and inexact:
            tenths += 1

        return IntermediateForm(
            sign=sign,
            significand=tenths,
            exponent=exponent - 1,
        )

    def to_zero(self) -> "IntermediateForm":
        """
        Round towards zero to the nearest value with quarters = 0.
        """
        return IntermediateForm(
            sign=self.sign,
            significand=self.significand // 10,
            exponent=self.exponent + 1,
        )

    def to_away(self) -> "IntermediateForm":
        """
        Round away from zero to the nearest value with quarters = 0.
        """
        return IntermediateForm(
            sign=self.sign,
            significand=-(-self.significand // 10),
            exponent=self.exponent + 1,
        )

    def as_int(self) -> int:
        """
        Interpret as int, provided that the exponent is zero.
        """
        if self.exponent:
            raise ValueError("Not an exact integer")
        return -self.significand if self.sign else self.significand

    def nudge(self) -> "IntermediateForm":
        """
        Increment the exponent and divide the significand by 10.

        Expected to be used only when the signficand is divisible by 10.
        """
        new_significand, remainder = divmod(self.significand, 10)
        if remainder:
            raise ValueError("significand not divisible by 10")
        return IntermediateForm(
            sign=self.sign,
            significand=new_significand,
            exponent=self.exponent + 1,
        )

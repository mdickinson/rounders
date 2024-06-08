"""Representations of intermediate values."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import cast

from rounders.modes import RoundingMode


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
    def from_signed_fraction(
        cls, *, sign: int, numerator: int, denominator: int, exponent: int
    ) -> IntermediateForm:
        """
        Create from a signed fraction, given a target exponent.

        Creates an IntermediateForm from a quotient of the form ±(n/d) with the target
        exponent, using round-for-reround.
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

    def nudge(self, figures: int) -> IntermediateForm:
        """Drop a zero in cases where rounding led us to end up with an extra zero."""
        if len(str(self.significand)) != figures + 1:
            return self

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

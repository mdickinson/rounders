import fractions
from typing import cast

from rounder.generics import decade, is_finite, is_zero, to_quarters, to_type_of
from rounder.intermediate import IntermediateForm


@decade.register(fractions.Fraction)
def _(x: fractions.Fraction) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")

    # We can compute based entirely on the digit strings.
    sn, sd = str(abs(x.numerator)), str(x.denominator)
    return len(sn) - len(sd) - (sn.rstrip("0") < sd.rstrip("0"))


@to_type_of.register(fractions.Fraction)
def _(x: fractions.Fraction, rounded: IntermediateForm) -> fractions.Fraction:
    if rounded.exponent >= 0:
        numerator = rounded.significand * cast(int, 10**rounded.exponent)
        denominator = 1
    else:
        numerator = rounded.significand
        denominator = cast(int, 10**-rounded.exponent)
    return (
        -fractions.Fraction(numerator, denominator)
        if rounded.sign
        else fractions.Fraction(numerator, denominator)
    )


@is_finite.register(fractions.Fraction)
def _(x: fractions.Fraction) -> bool:
    return True


@is_zero.register(fractions.Fraction)
def _(x: fractions.Fraction) -> bool:
    return x == 0


@to_quarters.register(fractions.Fraction)
def _(x: fractions.Fraction, exponent: int) -> IntermediateForm:
    return IntermediateForm.from_signed_fraction(
        sign=x < 0,
        numerator=abs(x.numerator),
        denominator=x.denominator,
        exponent=exponent,
    )

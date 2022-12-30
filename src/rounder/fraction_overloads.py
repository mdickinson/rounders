import fractions

from rounder.core import Rounded
from rounder.generics import is_finite, is_zero, to_type_of


@to_type_of.register(fractions.Fraction)
def _(x: fractions.Fraction, rounded: Rounded) -> fractions.Fraction:
    if rounded.exponent >= 0:
        numerator = rounded.significand * 10**rounded.exponent
        denominator = 1
    else:
        numerator = rounded.significand
        denominator = 10**-rounded.exponent
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

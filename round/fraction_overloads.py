import fractions

from round.generics import is_finite, to_type_of


@to_type_of.register(fractions.Fraction)
def _(x, sign, significand, exponent):
    if exponent >= 0:
        numerator = significand * 10 ** exponent
        denominator = 1
    else:
        numerator = significand
        denominator = 10 ** -exponent
    return (
        -fractions.Fraction(numerator, denominator)
        if sign
        else fractions.Fraction(numerator, denominator)
    )


@is_finite.register(fractions.Fraction)
def _(x):
    return True

"""Single-dispatch overloads for the fractions.Fraction type."""

import fractions
from typing import cast

from rounders.generics import decade, is_finite, is_zero, preround, to_type_of
from rounders.intermediate_form import IntermediateForm
from rounders.reciprocal_as_decimal import reciprocal_as_decimal


@decade.register
def _(x: fractions.Fraction) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")

    # We can compute based entirely on the digit strings.
    sn, sd = str(abs(x.numerator)), str(x.denominator)
    return len(sn) - len(sd) - (sn.rstrip("0") < sd.rstrip("0"))


@to_type_of.register
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


@is_finite.register
def _(x: fractions.Fraction) -> bool:
    return True


@is_zero.register
def _(x: fractions.Fraction) -> bool:
    return x == 0


@preround.register
def _(x: fractions.Fraction, exponent: int | None) -> IntermediateForm:
    # If the input fraction terminates, return a decimal representation of its exact
    # value, with the exponent reflecting termination point.
    try:
        m, e = reciprocal_as_decimal(x.denominator)
    except ValueError:
        pass
    else:
        return IntermediateForm(
            sign=int(x < 0),
            significand=abs(x.numerator) * m,
            exponent=e,
        )

    # Otherwise, if we're requiring an exact representation, raise.
    if exponent is None:
        raise ValueError("cannot represent non-terminating fraction exactly")

    # In all other cases, we need to round. We use a target exponent of exponent - 1
    # for that rounding, with round-for-reround rounding mode (adjust an inexact 0 or 5
    # final digit upwards).
    rounding_exponent = exponent - 1
    if rounding_exponent < 0:
        n, d = abs(x.numerator) * cast(int, 10**-rounding_exponent), x.denominator
    else:
        n, d = abs(x.numerator), x.denominator * cast(int, 10**rounding_exponent)

    significand, inexact = divmod(n, d)
    return IntermediateForm(
        sign=int(x < 0),
        significand=significand + (inexact and significand % 5 == 0),
        exponent=rounding_exponent,
    )

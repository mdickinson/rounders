from typing import cast

from rounder.generics import decade, is_finite, is_zero, preround, to_type_of
from rounder.intermediate import IntermediateForm


@decade.register
def _(x: int) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")
    return len(str(abs(x))) - 1


@to_type_of.register
def _(x: int, rounded: IntermediateForm) -> int:
    if rounded.exponent >= 0:
        significand = rounded.significand * cast(int, 10**rounded.exponent)
    else:
        significand, remainder = divmod(
            rounded.significand, cast(int, 10**-rounded.exponent)
        )
        if remainder:
            raise ValueError("Not representable as an integer")
    return -significand if rounded.sign else significand


@is_finite.register
def _(x: int) -> bool:
    return True


@is_zero.register
def _(x: int) -> bool:
    return x == 0


@preround.register
def _(x: int, exponent: int) -> IntermediateForm:
    return IntermediateForm.from_signed_fraction(
        sign=x < 0,
        numerator=abs(x),
        denominator=1,
        exponent=exponent,
    )

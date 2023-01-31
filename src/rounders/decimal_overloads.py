import dataclasses
import decimal

from rounders.generics import decade, is_finite, is_zero, preround, to_type_of
from rounders.intermediate import IntermediateForm


@to_type_of.register
def _(x: decimal.Decimal, rounded: IntermediateForm) -> decimal.Decimal:
    return decimal.Decimal(
        f"{'-' if rounded.sign else '+'}{rounded.significand}E{rounded.exponent}"
    )


@is_finite.register
def _(x: decimal.Decimal) -> bool:
    return x.is_finite()


@is_zero.register
def _(x: decimal.Decimal) -> bool:
    return x.is_zero()


@preround.register
def _(x: decimal.Decimal, exponent: int) -> IntermediateForm:
    if not x.is_finite():
        raise ValueError("Input must be finite")

    sign, digit_tuple, x_exponent = x.as_tuple()
    rounded = IntermediateForm.from_signed_fraction(
        sign=bool(sign),
        numerator=int("".join(map(str, digit_tuple))),
        denominator=1,
        exponent=exponent - x_exponent,
    )
    return dataclasses.replace(rounded, exponent=exponent)


@decade.register
def _(x: decimal.Decimal) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")
    if not x.is_finite():
        raise ValueError("decade input must be finite")

    return int(x.logb())

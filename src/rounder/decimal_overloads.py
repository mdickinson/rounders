import decimal
from typing import cast

from rounder.generics import decade, is_finite, is_zero, to_quarters, to_type_of
from rounder.intermediate import IntermediateForm


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


@to_quarters.register
def _(x: decimal.Decimal, exponent: int = 0) -> IntermediateForm:
    if not x.is_finite():
        raise ValueError("Input must be finite")

    sign, digit_tuple, x_exponent = x.as_tuple()
    significand = int("".join(map(str, digit_tuple)))

    scale = x_exponent - exponent + 1
    if scale >= 0:
        numerator, denominator = cast(int, 10**scale) * significand, 1
    else:
        numerator, denominator = significand, cast(int, 10**-scale)

    tenths, inexact = divmod(numerator, denominator)
    if tenths % 5 == 0 and inexact:
        tenths += 1

    return IntermediateForm(
        sign=sign == 1,
        significand=tenths,
        exponent=exponent - 1,
    )


@decade.register
def _(x: decimal.Decimal) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")
    if not x.is_finite():
        raise ValueError("decade input must be finite")

    return int(x.logb())

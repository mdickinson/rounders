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

    # We can convert directly to something of type IntermediateForm without changing
    # the value, so we do that, ignoring the incoming 'exponent'.
    sign, digit_tuple, x_exponent = x.as_tuple()
    # since x is finite, x_exponent can't be one of the special strings 'n', 'N', 'F'
    assert isinstance(x_exponent, int)
    significand = int("".join(map(str, digit_tuple)))
    return IntermediateForm(
        sign=sign,
        significand=significand,
        exponent=x_exponent,
    )


@decade.register
def _(x: decimal.Decimal) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")
    if not x.is_finite():
        raise ValueError("decade input must be finite")

    return int(x.logb())

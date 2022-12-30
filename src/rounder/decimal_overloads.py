import decimal

from rounder.core import Rounded, SignedQuarterInt
from rounder.generics import decade, is_finite, is_zero, to_quarters, to_type_of


@to_type_of.register(decimal.Decimal)
def _(x: decimal.Decimal, rounded: Rounded) -> decimal.Decimal:
    return decimal.Decimal(
        f"{'-' if rounded.sign else '+'}{rounded.significand}E{rounded.exponent}"
    )


@is_finite.register(decimal.Decimal)
def _(x: decimal.Decimal) -> bool:
    return x.is_finite()


@is_zero.register(decimal.Decimal)
def _(x: decimal.Decimal) -> bool:
    return x.is_zero()


@to_quarters.register(decimal.Decimal)
def _(x: decimal.Decimal, exponent: int = 0) -> SignedQuarterInt:
    # XXX Tests for non-finite inputs
    # XXX Tests for preservation of sign of zero.

    if not x.is_finite():
        # XXX Is this branch even exercised?
        raise ValueError("Input must be finite")

    sign, digit_tuple, x_exponent = x.as_tuple()
    significand = int("".join(map(str, digit_tuple)))

    if x_exponent >= exponent:
        quarters, rest = 4 * significand * 10 ** (x_exponent - exponent), 0
    else:
        quarters, rest = divmod(4 * significand, 10 ** (exponent - x_exponent))

    whole, quarters = divmod(int(quarters) | bool(rest), 4)
    return SignedQuarterInt(
        sign=sign == 1,
        whole=whole,
        quarters=quarters,
    )


@decade.register(decimal.Decimal)
def _(x: decimal.Decimal) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")
    if not x.is_finite():
        raise ValueError("decade input must be finite")

    return int(x.logb())

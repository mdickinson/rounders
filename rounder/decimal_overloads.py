import decimal

from rounder.core import SignedQuarterInt
from rounder.generics import decade, is_finite, to_quarters, to_type_of


@to_type_of.register(decimal.Decimal)
def _(x, sign_and_significand, exponent):
    sign, significand = sign_and_significand
    return decimal.Decimal(f"{'-' if sign else '+'}{significand}E{exponent}")


@is_finite.register(decimal.Decimal)
def _(x):
    return x.is_finite()


@to_quarters.register(decimal.Decimal)
def _(x: decimal.Decimal, exponent: int = 0):
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
    return SignedQuarterInt(sign == 1, *divmod(int(quarters) | bool(rest), 4))


@decade.register(decimal.Decimal)
def _(x) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")
    if not x.is_finite():
        raise ValueError("decade input must be finite")

    return int(x.logb())

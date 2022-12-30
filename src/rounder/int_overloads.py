from rounder.core import Rounded
from rounder.generics import is_finite, is_zero, to_type_of


@to_type_of.register(int)
def _(x: int, rounded: Rounded) -> int:
    if rounded.exponent >= 0:
        multiplier: int = 10**rounded.exponent
        significand = rounded.significand * multiplier
    else:
        divisor: int = 10**-rounded.exponent
        significand, remainder = divmod(rounded.significand, divisor)
        if remainder:
            raise ValueError("Not representable as an integer")
    return -significand if rounded.sign else significand


@is_finite.register(int)
def _(x: int) -> bool:
    return True


@is_zero.register(int)
def _(x: int) -> bool:
    return x == 0

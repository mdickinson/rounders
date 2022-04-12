from rounder.generics import is_finite, to_type_of


@to_type_of.register(int)
def _(x, rounded):
    if rounded.exponent >= 0:
        significand = rounded.significand * 10**rounded.exponent
    else:
        significand, remainder = divmod(rounded.significand, 10**-rounded.exponent)
        if remainder:
            raise ValueError("Not representable as an integer")
    return -significand if rounded.sign else significand


@is_finite.register(int)
def _(x):
    return True

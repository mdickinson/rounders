from rounder.generics import is_finite, to_type_of


@to_type_of.register(int)
def _(x, sign_and_significand, exponent):
    sign, significand = sign_and_significand
    if exponent >= 0:
        significand *= 10 ** exponent
    else:
        significand, remainder = divmod(significand, 10 ** -exponent)
        if remainder:
            raise ValueError("Not representable as an integer")
    return -significand if sign else significand


@is_finite.register(int)
def _(x):
    return True

"""
Top-level rounding functions.
"""

import fractions
import functools
import math


#: Signatures for to-nearest rounding modes
_TIES_TO_ZERO = [[1, 1], [1, 1]]
_TIES_TO_AWAY = [[2, 2], [2, 2]]
_TIES_TO_PLUS = [[2, 2], [1, 1]]
_TIES_TO_MINUS = [[1, 1], [2, 2]]
_TIES_TO_EVEN = [[1, 2], [1, 2]]
_TIES_TO_ODD = [[2, 1], [2, 1]]

#: Signatures for directed rounding modes
_TO_ZERO = [[0, 0], [0, 0]]
_TO_AWAY = [[3, 3], [3, 3]]
_TO_MINUS = [[0, 0], [3, 3]]
_TO_PLUS = [[3, 3], [0, 0]]
_TO_EVEN = [[0, 3], [0, 3]]
_TO_ODD = [[3, 0], [3, 0]]


@functools.singledispatch
def to_type_of(x, sign, significand, exponent):
    """
    Convert rounding result to type matching that of x.
    """
    raise NotImplementedError("Not implemented for general objects")


@to_type_of.register(int)
def _(x, sign, significand, exponent):
    if exponent >= 0:
        significand *= 10 ** exponent
    else:
        significand, remainder = divmod(significand, 10 ** -exponent)
        if remainder:
            raise ValueError("Not representable as an integer")
    return -significand if sign else significand


@to_type_of.register(float)
def _(x, sign, significand, exponent):
    if exponent >= 0:
        abs_value = float(significand * 10 ** exponent)
    else:
        abs_value = significand / 10 ** -exponent
    return -abs_value if sign else abs_value


@to_type_of.register(fractions.Fraction)
def _(x, sign, significand, exponent):
    if exponent >= 0:
        numerator = significand * 10 ** exponent
        denominator = 1
    else:
        numerator = significand
        denominator = 10 ** -exponent
    return (
        -fractions.Fraction(numerator, denominator)
        if sign
        else fractions.Fraction(numerator, denominator)
    )


@functools.singledispatch
def is_finite(x):
    """
    Determine whether a given object is finite.
    """
    raise NotImplementedError("Not implemented for general objects")


@is_finite.register(int)
def _(x):
    return True


@is_finite.register(fractions.Fraction)
def _(x):
    return True


@is_finite.register(float)
def _(x):
    return math.isfinite(x)


@functools.singledispatch
def to_quarters(x, exponent=0):
    """
    Pre-rounding step for value x, rounding to integer multiple of
    10**exponent, plus two extra bits rounded to odd.
    """
    negative, x = x < 0, fractions.Fraction(abs(x))
    if exponent <= 0:
        quarters, rest = divmod(4 * 10 ** -exponent * x, 1)
    else:
        quarters, rest = divmod(4 * x, 10 ** exponent)
    return negative, int(quarters) | bool(rest)


@to_quarters.register(float)
def _(x: fractions.Fraction, exponent: int = 0):
    # Need to allow for non-finite inputs, and sign of zero.

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    negative, x = math.copysign(1.0, x) < 0.0, fractions.Fraction(abs(x))
    if exponent <= 0:
        quarters, rest = divmod(4 * 10 ** -exponent * x, 1)
    else:
        quarters, rest = divmod(4 * x, 10 ** exponent)
    return negative, int(quarters) | bool(rest)


def _gen_round_to_int(x, *, signature):
    """
    Round the input x to the nearest integer, according to the given signature.
    """
    if not is_finite(x):
        raise ValueError("x must be finiite")

    sign, quarters = to_quarters(x, 0)
    significand = (quarters + signature[sign][quarters & 4 > 0]) // 4
    return -significand if sign else significand


def _gen_round(x, ndigits=None, *, signature):
    """
    Round the input x to the nearest integer, according to the given signature.

    XXX Also rounds to multiples of powers of 10.
    """
    if ndigits is None:
        return _gen_round_to_int(x, signature=signature)

    # Special handling for infinite results.
    if not is_finite(x):
        return x

    exponent = 0 if ndigits is None else -ndigits
    sign, quarters = to_quarters(x, exponent)
    significand = (quarters + signature[sign][quarters & 4 > 0]) // 4
    return to_type_of(x, sign, significand, exponent)


def round_ties_to_away(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties away from zero.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_AWAY)


def round_ties_to_zero(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards zero.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_ZERO)


def round_ties_to_even(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    even integer.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_EVEN)


def round_ties_to_odd(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    odd integer.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_ODD)


def round_ties_to_plus(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards positive
    infinity.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_PLUS)


def round_ties_to_minus(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards negative
    infinity.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_MINUS)


def round_to_away(x, ndigits=None):
    """
    Round the input x to the nearest integer away from zero.
    """
    return _gen_round(x, ndigits, signature=_TO_AWAY)


def round_to_zero(x, ndigits=None):
    """
    Round the input x to the nearest integer towards zero.
    """
    return _gen_round(x, ndigits, signature=_TO_ZERO)


def round_to_plus(x, ndigits=None):
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, ndigits, signature=_TO_PLUS)


def round_to_minus(x, ndigits=None):
    """
    Round the input x to the nearest integer towards negative infinity.
    """
    return _gen_round(x, ndigits, signature=_TO_MINUS)


def round_to_even(x, ndigits=None):
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, ndigits, signature=_TO_EVEN)


def round_to_odd(x, ndigits=None):
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, ndigits, signature=_TO_ODD)

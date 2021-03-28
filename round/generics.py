"""
Generic extensible computation functions that use singledispatch.
"""

import fractions
import functools

#: Useful constants
_TEN = fractions.Fraction(10)


@functools.singledispatch
def decade(x) -> int:
    """
    Determine the decade that a nonzero number is contained in.

    Given nonzero x, return the unique integer e satisfying
    10**e <= abs(x) < 10**(e + 1).
    """
    # General algorithm assumes the existence of an exact conversion to Fraction.
    fx = fractions.Fraction(abs(x))
    if not fx:
        raise ValueError("decade input must be nonzero")

    n, d = fx.numerator, fx.denominator

    e = len(str(n))  # 10**(e-1) <= n < 10**e
    f = len(str(d))  # 10**(f-1) <= d < 10**f
    # Now 10**(e-f-1) < n/d < 10**(e-f+1), so the decade is either
    # e-f or e-f-1, depending on whether fx >= 10**(e-f) or not.
    return e - f if fx >= _TEN ** (e - f) else e - f - 1


@functools.singledispatch
def to_type_of(x, sign, significand, exponent):
    """
    Convert rounding result to type matching that of x.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def is_finite(x):
    """
    Determine whether a given object is finite.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def to_quarters(x, exponent=0):
    """
    Pre-rounding step for value x, rounding to integer multiple of
    10**exponent, plus two extra bits rounded to odd.

    This base implementation works for any value that can be converted
    losslessly to a fraction, and for which signs of zero and special
    values are not a consideration.

    Returns
    -------
    negative : bool
        True for values that should be treated as negative (including
        negative zero for floating-point types), False otherwise.
    inflated_significand : int
        abs(4*x) as an integer multiple of 10**exponent, rounded to an
        integer using the round-to-odd rounding mode.
    """
    negative, x = x < 0, 4 * abs(fractions.Fraction(x))
    if exponent <= 0:
        quarters, rest = divmod(10 ** -exponent * x, 1)
    else:
        quarters, rest = divmod(x, 10 ** exponent)
    return negative, int(quarters) | bool(rest)

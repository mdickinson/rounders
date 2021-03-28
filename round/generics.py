"""
Generic extensible computation functions that use singledispatch.
"""

import fractions
import functools

from round.intermediates import SignedQuarters


@functools.singledispatch
def decade(x) -> int:
    """
    Determine the decade that a nonzero number is contained in.

    Given nonzero finite x, returns the unique integer e satisfying
    10**e <= abs(x) < 10**(e + 1).

    Parameters
    ----------
    x : numeric

    Returns
    -------
    decade : int

    Raises
    ------
    ValueError
        If input is zero.
    """
    # Generic algorithm assumes the existence of an exact conversion to Fraction.
    fx = fractions.Fraction(x)
    if not fx:
        raise ValueError("decade input must be nonzero")

    # The difference in digit counts of n and d gives us either the true decade
    # (as in 561/23, for example), or overestimates the decade by exactly 1 (as
    # in 231/56).
    n, d = abs(fx.numerator), fx.denominator
    trial_decade = len(str(n)) - len(str(d))

    # Is trial_decade an overestimate?
    if trial_decade >= 0:
        too_high = n < 10 ** trial_decade * d
    else:
        too_high = n * 10 ** -trial_decade < d

    return trial_decade - too_high


@functools.singledispatch
def to_type_of(x, sign_and_significand, exponent):
    """
    Convert rounding result to type matching that of x.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def is_finite(x):
    """
    Determine whether a given number is finite.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def is_zero(x):
    """
    Determine whether a given number is zero.

    Parameters
    ----------
    x : numeric

    Returns
    -------
    is_zero : bool
        True if x is zero, else False
    """
    # Generic implementation simply compares with the zero integer.
    return x == 0


@functools.singledispatch
def to_quarters(x, exponent):
    """
    Pre-rounding step for value x.

    Rounds the number x / 10**exponent to the nearest quarter, using the
    round-to-odd rounding mode. Returns the number of quarters.

    The generic implementation works for any value that can be converted
    losslessly to a fraction, and for which signs of zero and special
    values are not a consideration.

    Parameters
    ----------
    x : numeric
    exponent : int

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
    return SignedQuarters(negative, *divmod(int(quarters) | bool(rest), 4))

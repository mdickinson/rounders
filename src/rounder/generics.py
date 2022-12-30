"""
Generic extensible computation functions that use singledispatch.
"""

import fractions
import functools
from typing import Any

from rounder.core import Rounded, SignedQuarterInt


@functools.singledispatch
def decade(x: Any) -> int:
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
    too_high: bool
    if trial_decade >= 0:
        too_high = n < 10**trial_decade * d
    else:
        too_high = n * 10**-trial_decade < d

    return trial_decade - too_high


@functools.singledispatch
def to_type_of(x: Any, rounded: Rounded) -> Any:
    """
    Convert rounding result to type matching that of x.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def is_finite(x: Any) -> bool:
    """
    Determine whether a given number is finite.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def is_zero(x: Any) -> bool:
    """
    Determine whether a given number is zero.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def to_quarters(x: Any, exponent: int) -> SignedQuarterInt:
    """
    Pre-rounding step for value x.

    Rounds the number x / 10**exponent to the nearest quarter, using the
    round-to-odd rounding mode. Returns the number of quarters.

    The generic implementation works for any value that can be converted
    losslessly to a fraction, and for which signs of zero and special
    values are not a consideration.
    """
    negative, x = x < 0, 4 * abs(fractions.Fraction(x))
    if exponent <= 0:
        quarters, rest = divmod(10**-exponent * x, 1)
    else:
        quarters, rest = divmod(x, 10**exponent)

    whole, quarters = divmod(int(quarters) | bool(rest), 4)

    return SignedQuarterInt(
        sign=negative,
        whole=whole,
        quarters=quarters,
    )

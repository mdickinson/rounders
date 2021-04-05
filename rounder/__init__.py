"""
Top-level rounding functions.
"""

import rounder.decimal_overloads  # noqa: F401
import rounder.float_overloads  # noqa: F401
import rounder.fraction_overloads  # noqa: F401
import rounder.int_overloads  # noqa: F401
from rounder.core import Rounded
from rounder.generics import decade, is_finite, is_zero, to_quarters, to_type_of
from rounder.modes import (
    TIES_TO_AWAY,
    TIES_TO_EVEN,
    TIES_TO_MINUS,
    TIES_TO_ODD,
    TIES_TO_PLUS,
    TIES_TO_ZERO,
    TO_AWAY,
    TO_EVEN,
    TO_MINUS,
    TO_ODD,
    TO_PLUS,
    TO_ZERO,
    TO_ZERO_05_AWAY,
)


def round_to_int(x, *, mode=TIES_TO_EVEN):
    """
    Round a value to the nearest integer, using the given rounding mode.

    Parameters
    ----------
    x : numeric
    mode : optional, keyword-only
        Any of the twelve available rounding modes. Defaults to the
        ties-to-even rounding mode.

    Returns
    -------
    rounded : int

    Raises
    ------
    ValueError
        If the value to be rounded is not finite.
    """
    # Raise on infinities and NaNs
    if not is_finite(x):
        raise ValueError("x must be finite")

    exponent = 0
    quarters = to_quarters(x, exponent)
    rounded = Rounded(quarters.sign, quarters.whole + mode(quarters), exponent)
    return to_type_of(0, rounded)


def round_to_places(x, places, *, mode=TIES_TO_EVEN):
    """
    Round a value to a given number of places after the point.

    Parameters
    ----------
    x : numeric
    places : integer
    mode, optional
        Any of the twelve available rounding modes. Defaults to the
        ties-to-even rounding mode.
    """
    # Infinities and nans are returned unchanged.
    if not is_finite(x):
        return x

    exponent = -places
    quarters = to_quarters(x, exponent)
    rounded = Rounded(quarters.sign, quarters.whole + mode(quarters), exponent)
    return to_type_of(x, rounded)


def round_to_figures(x, figures, *, mode=TIES_TO_EVEN):
    """
    Round a value to a given number of significant figures.

    Parameters
    ----------
    x : numeric
    figures : positive integer
    mode, optional
        Any of the twelve available rounding modes. Defaults to the
        ties-to-even rounding mode.
    """
    if figures <= 0:
        raise ValueError(f"figures must be positive; got {figures}")

    # Special handling for infinite results.
    if not is_finite(x):
        return x

    # The choice of exponent for zero is rather arbitrary. The choice
    # here ensures alignment in a table of values expressed in
    # scientific notation, assuming that 0 is represented with
    # an exponent of zero. For example, with figures=3:
    #
    #  4.56e-02
    #  1.23e+02
    #  0.00e+00

    exponent = 1 - figures + (0 if is_zero(x) else decade(x))
    quarters = to_quarters(x, exponent)
    rounded = Rounded(quarters.sign, quarters.whole + mode(quarters), exponent)

    # Adjust if the result has one more significant figure than expected.
    # This can happen when a value at the uppermost end of a decade gets
    # rounded up to the next power of 10: for example, in rounding
    # 99.973 to 100.0.
    if len(str(rounded.significand)) == figures + 1:
        rounded = Rounded(rounded.sign, rounded.significand // 10, rounded.exponent + 1)
    return to_type_of(x, rounded)


# Per-rounding-mode functions, with behaviour matching that of the built-in
# round: round to some number of places, returning a value of the same type
# as the input, or round to the nearest integer, returning an int.


def round_ties_to_away(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties away from zero.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_AWAY)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_AWAY)


def round_ties_to_zero(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards zero.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_ZERO)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_ZERO)


def round_ties_to_even(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    even integer.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_EVEN)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_EVEN)


def round_ties_to_odd(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    odd integer.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_ODD)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_ODD)


def round_ties_to_plus(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards positive
    infinity.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_PLUS)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_PLUS)


def round_ties_to_minus(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards negative
    infinity.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_MINUS)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_MINUS)


def round_to_away(x, ndigits=None):
    """
    Round the input x to the nearest integer away from zero.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_AWAY)
    else:
        return round_to_places(x, ndigits, mode=TO_AWAY)


def round_to_zero(x, ndigits=None):
    """
    Round the input x to the nearest integer towards zero.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_ZERO)
    else:
        return round_to_places(x, ndigits, mode=TO_ZERO)


def round_to_plus(x, ndigits=None):
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_PLUS)
    else:
        return round_to_places(x, ndigits, mode=TO_PLUS)


def round_to_minus(x, ndigits=None):
    """
    Round the input x to the nearest integer towards negative infinity.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_MINUS)
    else:
        return round_to_places(x, ndigits, mode=TO_MINUS)


def round_to_even(x, ndigits=None):
    """
    Round the input x to the nearest even integer.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_EVEN)
    else:
        return round_to_places(x, ndigits, mode=TO_EVEN)


def round_to_odd(x, ndigits=None):
    """
    Round the input x to the nearest odd integer.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_ODD)
    else:
        return round_to_places(x, ndigits, mode=TO_ODD)


def round_to_zero_05_away(x, ndigits=None):
    """
    Round for re-rounding.

    Like round_to_zero, except that if the result of the rounding would end
    in a 0 or a 5, and the rounded result is not equal to the original, then
    the result is rounded away from zero instead, giving something with last
    digit 1 or 6.

    This rounding mode provides a way to avoid double rounding: rounding to
    precision p + 1 using this mode, followed by rounding to precision p using
    any other mode, has the same result as rounding directly to precision p using
    that other mode.

    """
    if ndigits is None:
        return round_to_int(x, mode=TO_ZERO_05_AWAY)
    else:
        return round_to_places(x, ndigits, mode=TO_ZERO_05_AWAY)

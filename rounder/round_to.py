"""
Top-level rounding functions.
"""

from rounder.core import Rounded
from rounder.generics import decade, is_finite, is_zero, to_quarters, to_type_of
from rounder.modes import TIES_TO_EVEN


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


def round_to_places(value, places, *, mode=TIES_TO_EVEN):
    """
    Round a value to a given number of places after the point.

    Parameters
    ----------
    value : number
        value to be rounded
    places : integer
        Number of places to round to, relative to the decimal point.
    mode, optional
        Any of the twelve available rounding modes. Defaults to the
        ties-to-even rounding mode.
    """
    # Infinities and nans are returned unchanged.
    if not is_finite(value):
        return value

    exponent = -places
    quarters = to_quarters(value, exponent)
    rounded = Rounded(quarters.sign, quarters.whole + mode(quarters), exponent)
    return to_type_of(value, rounded)


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


def round(x, ndigits, *, mode=TIES_TO_EVEN):
    """
    Round a value using a given rounding mode.

    Replacement for the built-in round function with configurable rounding mode.

    Parameters
    ----------
    x : number
        Value to be rounded
    ndigits : int
        Number of digits past the point to round to. Can be negative.
    mode : RoundingMode, optional
        Rounding mode. Defaults to TIES_TO_EVEN.
    """
    if ndigits is None:
        return round_to_int(x, mode=mode)
    else:
        return round_to_places(x, ndigits, mode=mode)

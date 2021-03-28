"""
Top-level rounding functions.
"""

import round.decimal_overloads  # noqa: F401
import round.float_overloads  # noqa: F401
import round.fraction_overloads  # noqa: F401
import round.int_overloads  # noqa: F401
from round.generics import decade, is_finite, is_zero, to_quarters, to_type_of
from round.intermediates import SignedQuarters
from round.modes import (
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
)


def round_quarters(quarters: SignedQuarters, *, rounding_mode):

    odd = quarters.whole & 1
    round_up = quarters.quarters + rounding_mode[quarters.sign][odd] >= 4
    return quarters.sign, quarters.whole + round_up


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
    if not is_finite(x):
        raise ValueError("x must be finite")

    quarters = to_quarters(x, exponent=0)
    rounded = round_quarters(quarters, rounding_mode=mode)
    return to_type_of(0, rounded, exponent=0)


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
    # Special handling for infinities and nans.
    if not is_finite(x):
        return x

    # Figure out exponent to round to.
    exponent = -places
    quarters = to_quarters(x, exponent)
    sign, significand = round_quarters(quarters, rounding_mode=mode)
    return to_type_of(x, (sign, significand), exponent)


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
    sign, significand = rounded = round_quarters(quarters, rounding_mode=mode)

    # Adjust if the result has one more significant figure than expected.
    # This can happen when a value at the uppermost end of a decade gets
    # rounded up to the next power of 10: for example, in rounding
    # 99.973 to 100.0.
    if len(str(significand)) == figures + 1:
        assert significand % 10 == 0
        significand //= 10
        exponent += 1
        rounded = sign, significand
    return to_type_of(x, rounded, exponent)


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

"""Top-level rounding functions."""

from typing import Any

from rounders.generics import decade, is_finite, is_zero, preround, to_type_of
from rounders.modes import TIES_TO_EVEN, RoundingMode


def round_to_int(number: Any, *, mode: RoundingMode = TIES_TO_EVEN) -> int:
    """
    Round a value to the nearest integer, using the given rounding mode.

    Parameters
    ----------
    number : numeric
    mode : optional, keyword-only
        Any of the available rounding modes. Defaults to the
        ties-to-even rounding mode.

    Returns
    -------
    rounded : int

    Raises
    ------
    ValueError
        If the value to be rounded is not finite.
    """
    if not is_finite(number):
        raise ValueError("number must be finite")

    rounded = preround(number, 0).round(0, mode)
    return int(rounded)


def round_to_places(
    number: Any, places: int, *, mode: RoundingMode = TIES_TO_EVEN
) -> Any:
    """
    Round a value to a given number of places after the point.

    Parameters
    ----------
    number : number
        value to be rounded
    places : integer
        Number of places to round to, relative to the decimal point.
    mode, optional
        Any of the available rounding modes. Defaults to the
        ties-to-even rounding mode.
    """
    # Infinities and nans are returned unchanged.
    if not is_finite(number):
        return number

    prerounded = preround(number, -places)
    rounded = prerounded.round(-places, mode)
    return to_type_of(number, rounded)


def round_to_figures(
    number: Any, figures: int, *, mode: RoundingMode = TIES_TO_EVEN
) -> Any:
    """
    Round a value to a given number of significant figures.

    Parameters
    ----------
    number : numeric
    figures : positive integer
    mode, optional
        Any of the available rounding modes. Defaults to the
        ties-to-even rounding mode.
    """
    if figures <= 0:
        raise ValueError(f"figures must be positive; got {figures}")

    # Infinities and nans are returned unchanged.
    if not is_finite(number):
        return number

    # The choice of exponent for zero is rather arbitrary. The choice
    # here ensures alignment in a table of values expressed in
    # scientific notation, assuming that 0 is represented with
    # an exponent of zero. For example, with figures=3:
    #
    #  4.56e-02
    #  1.23e+02
    #  0.00e+00

    prerounded = preround(
        number, exponent=None if is_zero(number) else decade(number) + 1 - figures
    )
    exponent = (0 if is_zero(number) else prerounded.decade) + 1 - figures
    rounded = prerounded.round(exponent, mode)

    # Adjust if the result has one more significant figure than expected.
    # This can happen when a value at the uppermost end of a decade gets
    # rounded up to the next power of 10: for example, in rounding
    # 99.973 to 100.0.
    rounded = rounded.trim(figures)
    return to_type_of(number, rounded)


def round(
    number: Any, ndigits: int | None = None, *, mode: RoundingMode = TIES_TO_EVEN
) -> Any:
    """
    Round a value using a given rounding mode.

    Replacement for the built-in round function with configurable rounding mode.

    Parameters
    ----------
    number : number
        Value to be rounded
    ndigits : int
        Number of digits past the point to round to. Can be negative.
    mode : RoundingMode, optional
        Rounding mode. Defaults to TIES_TO_EVEN.
    """
    if ndigits is None:
        return round_to_int(number, mode=mode)
    else:
        return round_to_places(number, ndigits, mode=mode)

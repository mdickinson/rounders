# Per-rounding-mode functions, with behaviour matching that of the built-in
# round: round to some number of places, returning a value of the same type
# as the input, or round to the nearest integer, returning an int.

from typing import Any, Optional

from rounders.modes import (
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
from rounders.round_to import round


def round_ties_to_away(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer, rounding ties away from zero.
    """
    return round(x, ndigits, mode=TIES_TO_AWAY)


def round_ties_to_zero(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer, rounding ties towards zero.
    """
    return round(x, ndigits, mode=TIES_TO_ZERO)


def round_ties_to_even(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    even integer.
    """
    return round(x, ndigits, mode=TIES_TO_EVEN)


def round_ties_to_odd(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    odd integer.
    """
    return round(x, ndigits, mode=TIES_TO_ODD)


def round_ties_to_plus(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer, rounding ties towards positive
    infinity.
    """
    return round(x, ndigits, mode=TIES_TO_PLUS)


def round_ties_to_minus(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer, rounding ties towards negative
    infinity.
    """
    return round(x, ndigits, mode=TIES_TO_MINUS)


def round_to_away(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer away from zero.
    """
    return round(x, ndigits, mode=TO_AWAY)


def round_to_zero(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer towards zero.
    """
    return round(x, ndigits, mode=TO_ZERO)


def round_to_plus(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return round(x, ndigits, mode=TO_PLUS)


def round_to_minus(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest integer towards negative infinity.
    """
    return round(x, ndigits, mode=TO_MINUS)


def round_to_even(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest even integer.
    """
    return round(x, ndigits, mode=TO_EVEN)


def round_to_odd(x: Any, ndigits: Optional[int] = None) -> Any:
    """
    Round the input x to the nearest odd integer.
    """
    return round(x, ndigits, mode=TO_ODD)


def round_to_zero_05_away(x: Any, ndigits: Optional[int] = None) -> Any:
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
    return round(x, ndigits, mode=TO_ZERO_05_AWAY)

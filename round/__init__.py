"""
Top-level rounding functions.
"""

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


def _float_to_quarters(x: float):
    """
    Information needed for rounding a float to the nearest integer.

    Returns
    -------
    negative : bool
        True if negative, False if positive
    to_odd : nonnegative int
        Absolute value of 4 * x, rounded to the nearest integer under
        the round-to-odd rounding mode.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    # XXX We'll actually want to capture the sign of the zero in cases where a
    # float is being returned. But right now that's not affecting anything
    # using this code, so we can't write a behavioural test for it.
    negative, x = x < 0, abs(x)
    quarters, rest = divmod(x, 0.25)
    return (
        negative,
        (4 * int(x) if math.isinf(quarters) else int(quarters)) | bool(rest),
    )


def _gen_round(x: float, signature) -> int:
    """
    Round the input x to the nearest integer, according to the given signature.
    """
    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    negative, quarters = _float_to_quarters(x)
    sum = (quarters + signature[negative][quarters & 4 > 0]) // 4
    return -sum if negative else sum


def round_ties_to_away(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties away from zero.
    """
    return _gen_round(x, _TIES_TO_AWAY)


def round_ties_to_zero(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards zero.
    """
    return _gen_round(x, _TIES_TO_ZERO)


def round_ties_to_even(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    even integer.
    """
    return _gen_round(x, _TIES_TO_EVEN)


def round_ties_to_odd(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    odd integer.
    """
    return _gen_round(x, _TIES_TO_ODD)


def round_ties_to_plus(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards positive
    infinity.
    """
    return _gen_round(x, _TIES_TO_PLUS)


def round_ties_to_minus(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards negative
    infinity.
    """
    return _gen_round(x, _TIES_TO_MINUS)


def round_to_away(x: float) -> int:
    """
    Round the input x to the nearest integer away from zero.
    """
    return _gen_round(x, _TO_AWAY)


def round_to_zero(x: float) -> int:
    """
    Round the input x to the nearest integer towards zero.
    """
    return _gen_round(x, _TO_ZERO)


def round_to_plus(x: float) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, _TO_PLUS)


def round_to_minus(x: float) -> int:
    """
    Round the input x to the nearest integer towards negative infinity.
    """
    return _gen_round(x, _TO_MINUS)


def round_to_even(x: float) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, _TO_EVEN)


def round_to_odd(x: float) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, _TO_ODD)

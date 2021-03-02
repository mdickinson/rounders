"""
Top-level rounding functions.
"""

import fractions
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


def _float_to_quarters(x: float, ndigits: int = 0):
    """
    Information needed for rounding a float.

    Returns
    -------
    negative : bool
        True if negative, False if positive
    to_odd : nonnegative int
        Absolute value of 4 * x, rounded to the nearest integer under
        the round-to-odd rounding mode.
    """
    if not isinstance(x, float):
        raise NotImplementedError(f"x must be a float; got {type(x)}")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    negative, x = math.copysign(1.0, x) < 0.0, fractions.Fraction(abs(x))
    if ndigits >= 0:
        quarters, rest = divmod(4 * 10 ** ndigits * x, 1)
    else:
        quarters, rest = divmod(4 * x, 10 ** -ndigits)
    return negative, int(quarters) | bool(rest)


def _convert_to_int(result):
    sign, significand, exponent = result
    assert exponent == 0
    return -significand if sign else significand


def _convert_to_float(result):
    sign, significand, exponent = result
    if exponent >= 0:
        abs_value = float(significand * 10 ** exponent)
    else:
        abs_value = significand / 10 ** -exponent
    return -abs_value if sign else abs_value


def _gen_round(x: float, ndigits=None, *, signature) -> int:
    """
    Round the input x to the nearest integer, according to the given signature.
    """
    exponent = 0 if ndigits is None else -ndigits

    sign, quarters = _float_to_quarters(x, -exponent)
    significand = (quarters + signature[sign][quarters & 4 > 0]) // 4
    result = sign, significand, exponent

    return _convert_to_int(result) if ndigits is None else _convert_to_float(result)


def round_ties_to_away(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer, rounding ties away from zero.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_AWAY)


def round_ties_to_zero(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards zero.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_ZERO)


def round_ties_to_even(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    even integer.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_EVEN)


def round_ties_to_odd(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    odd integer.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_ODD)


def round_ties_to_plus(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards positive
    infinity.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_PLUS)


def round_ties_to_minus(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards negative
    infinity.
    """
    return _gen_round(x, ndigits, signature=_TIES_TO_MINUS)


def round_to_away(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer away from zero.
    """
    return _gen_round(x, ndigits, signature=_TO_AWAY)


def round_to_zero(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer towards zero.
    """
    return _gen_round(x, ndigits, signature=_TO_ZERO)


def round_to_plus(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, ndigits, signature=_TO_PLUS)


def round_to_minus(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer towards negative infinity.
    """
    return _gen_round(x, ndigits, signature=_TO_MINUS)


def round_to_even(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, ndigits, signature=_TO_EVEN)


def round_to_odd(x: float, ndigits=None) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    return _gen_round(x, ndigits, signature=_TO_ODD)

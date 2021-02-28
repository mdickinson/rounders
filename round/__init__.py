"""
Top-level rounding functions.
"""

import math


def round_ties_to_away(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties away from zero.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_ties_to_away(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part >= 0.5
    return int_part + round_up


def round_ties_to_zero(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards zero.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_ties_to_zero(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part > 0.5
    return int_part + round_up


def round_ties_to_even(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    even integer.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_ties_to_even(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part > 0.5 or frac_part == 0.5 and int_part % 2 == 1
    return int_part + round_up


def round_ties_to_odd(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    odd integer.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_ties_to_odd(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part > 0.5 or frac_part == 0.5 and int_part % 2 == 0
    return int_part + round_up


def round_ties_to_plus(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards positive
    infinity.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_ties_to_minus(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part >= 0.5
    return int_part + round_up


def round_ties_to_minus(x: float) -> int:
    """
    Round the input x to the nearest integer, rounding ties towards negative
    infinity.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_ties_to_plus(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part > 0.5
    return int_part + round_up


def round_to_away(x: float) -> int:
    """
    Round the input x to the nearest integer away from zero.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_to_away(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part > 0.0
    return int_part + round_up


def round_to_zero(x: float) -> int:
    """
    Round the input x to the nearest integer towards zero.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_to_zero(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    return int_part


def round_to_plus(x: float) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_to_minus(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part > 0.0
    return int_part + round_up


def round_to_minus(x: float) -> int:
    """
    Round the input x to the nearest integer towards negative infinity.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_to_plus(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    return int_part


def round_to_even(x: float) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_to_even(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part > 0.0 and int_part % 2 == 1
    return int_part + round_up


def round_to_odd(x: float) -> int:
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    if not isinstance(x, float):
        raise NotImplementedError("Only implemented for floats")

    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    if x < 0:
        return -round_to_odd(-x)

    frac_part, int_part = math.modf(x)
    int_part = int(int_part)

    round_up = frac_part > 0.0 and int_part % 2 == 0
    return int_part + round_up

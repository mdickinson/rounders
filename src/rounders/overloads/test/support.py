"""Helpers for tests under rounders.overloads.test."""

import dataclasses

from rounders.intermediate_form import IntermediateForm


def truncate_and_remainder(
    value: IntermediateForm, exponent: int | None
) -> tuple[IntermediateForm, int]:
    """Truncate value to the given exponent and determine class of the remainder.

    The class of the remainder is an integer in [0, 3] with the following meaning:

    0: No remainder
    1: Remainder less than half
    2: Remainder exactly half
    3: Remainder greater than half
    """
    if exponent is None or value.exponent >= exponent:
        return value, 0

    quarters, remainder = divmod(
        value.significand << 2, 10 ** (exponent - value.exponent)
    )
    return (
        dataclasses.replace(value, significand=quarters >> 2, exponent=exponent),
        (quarters & 3) | bool(remainder),
    )

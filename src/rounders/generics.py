"""
Generic extensible computation functions that use singledispatch.
"""

import functools
from typing import Any

from rounders.intermediate import IntermediateForm


@functools.singledispatch
def decade(x: Any) -> int:
    """
    Determine the decade that a nonzero number is contained in.

    Given nonzero finite x, returns the unique integer e satisfying
    10**e <= abs(x) < 10**(e + 1).
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def to_type_of(x: Any, rounded: IntermediateForm) -> Any:
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
def preround(x: Any, exponent: int) -> IntermediateForm:
    """
    Pre-rounding step for value x.

    Converts the value x to a decimal value y of type IntermediateForm in such a way
    that rounding y to any exponent greater than or equal to `exponent` is equivalent
    to rounding x to that exponent, under any of the standard rounding modes.

    For example, given a value of 22/7=3.142857142857... and an exponent of -3, an
    IntermediateForm element representing the value 3.1428 might be returned. When
    rounded to 3 or fewer decimal places, 3.1428 rounds the same way as 22/7 under
    any of the rounding modes provided by this package.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")

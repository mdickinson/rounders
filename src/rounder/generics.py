"""
Generic extensible computation functions that use singledispatch.
"""

import functools
from typing import Any

from rounder.intermediate import IntermediateForm


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
def to_quarters(x: Any, exponent: int) -> IntermediateForm:
    """
    Pre-rounding step for value x.

    Rounds the number x / 10**exponent to the nearest quarter, using the
    round-to-odd rounding mode. Returns the number of quarters.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")

"""Generic extensible computation functions that use singledispatch."""

import functools
from typing import Any, Optional

from rounders.intermediate import IntermediateForm


@functools.singledispatch
def decade(x: Any) -> int:
    """
    Determine the decade that a nonzero number is contained in.

    The decade of x is the unique integer e satisfying 10**e <= abs(x) < 10**(e + 1).

    Where the decade is expensive to compute, it's enough for the overloads to return a
    lower bound for the decade: an integer e such that 10**e <= abs(x). This causes some
    extra work during rounding.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def to_type_of(x: Any, rounded: IntermediateForm) -> Any:
    """Convert rounding result to type matching that of x."""
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def is_finite(x: Any) -> bool:
    """Determine whether a given number is finite."""
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def is_zero(x: Any) -> bool:
    """Determine whether a given number is zero."""
    raise NotImplementedError(f"No overload available for type {type(x)}")


@functools.singledispatch
def preround(x: Any, exponent: Optional[int]) -> IntermediateForm:
    """
    Pre-rounding step for value x.

    Converts the value x to a decimal value y of type IntermediateForm in such a way
    that rounding y to any exponent greater than or equal to `exponent` is equivalent
    to rounding x to that exponent, under any of the standard rounding modes.

    For values that can be represented exactly in the target IntermediateForm type,
    an exact conversion can be performed, and then `exponent` can be ignored.

    If exponent is None, then this should either perform an exact conversion, or
    raise ValueError if such an exact conversion isn't possible.

    For example, given a value of 22/7=3.142857142857... and an exponent of -3, an
    IntermediateForm element representing the value 3.1428 might be returned. When
    rounded to 3 or fewer decimal places, 3.1428 rounds the same way as 22/7 under
    any of the rounding modes provided by this package.
    """
    raise NotImplementedError(f"No overload available for type {type(x)}")

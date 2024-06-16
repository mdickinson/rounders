"""Single-dispatch overloads for the IntermediateForm type."""

from typing import Optional

from rounders.generics import decade, is_finite, is_zero, preround, to_type_of
from rounders.intermediate import IntermediateForm


@decade.register
def _(x: IntermediateForm) -> int:
    if x.is_zero():
        raise ValueError("decade input must be nonzero")

    return x.decade


@to_type_of.register
def _(x: IntermediateForm, rounded: IntermediateForm) -> IntermediateForm:
    return rounded


@is_finite.register
def _(x: IntermediateForm) -> bool:
    return True


@is_zero.register
def _(x: IntermediateForm) -> bool:
    return x.is_zero()


@preround.register
def _(x: IntermediateForm, exponent: Optional[int]) -> IntermediateForm:
    return x

"""General target format for a rounding operation."""

import dataclasses

from rounders.intermediate_form import IntermediateForm


@dataclasses.dataclass(frozen=True)
class TargetFormat:
    """
    Class representing a target format for a rounding operation.

    This is a parametric description of a (typically infinite) collection of
    IntermediateForm values.
    """

    # Minimum exponent for represented values. If None, all exponents are permitted.
    minimum_exponent: int | None = None

    # Maximum number of significant figures. If None, arbitrarily long significands
    # are permitted.
    maximum_figures: int | None = None

    # Whether to allow negative zeros.
    signed_zero: bool = True

    def __contains__(self, value: IntermediateForm) -> bool:
        """Determine whether a value belongs to this format."""
        return (
            (self.minimum_exponent is None or value.exponent >= self.minimum_exponent)
            and (self.maximum_figures is None or value.figures <= self.maximum_figures)
            and (self.signed_zero or value.sign == 0 or value.significand != 0)
        )

    def minimum_exponent_for_decade(self, decade: int) -> int | None:
        """
        Return the minimum exponent for a representable value in a given decade.

        The decade of a nonzero (finite) value v is the unique integer e satisfying
        10**e <= abs(v) < 10**(e+1).

        Returns None if the exponent can be arbitrarily small. This occurs for zeros if
        the format has no minimum exponent, and for nonzero numbers if the format has
        neither a minimum exponent nor a maximum number of figures.
        """
        exponents: list[int] = []
        if self.minimum_exponent is not None:
            exponents.append(self.minimum_exponent)
        if self.maximum_figures is not None:
            exponents.append(decade + 1 - self.maximum_figures)
        return max(exponents, default=None)

"""Formatting functionality."""

from __future__ import annotations

import dataclasses
import re
from typing import Any, Dict, Optional

from rounders.generics import decade, is_zero, preround
from rounders.intermediate import IntermediateForm
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
    RoundingMode,
)

_PATTERN = re.compile(
    r"""\A
(?P<sign>[-+ ])?
(?P<no_neg_0>z)?
(?P<alt>\#)?
\.
(?P<precision>-?\d+)
(?P<mode>[aemopzAEMOPRZ])?
(?P<type>[ef])
\Z""",
    re.VERBOSE,
)

_MODE_FORMAT_CODES = {
    "m": TIES_TO_MINUS,
    "p": TIES_TO_PLUS,
    "a": TIES_TO_AWAY,
    "e": TIES_TO_EVEN,
    "o": TIES_TO_ODD,
    "z": TIES_TO_ZERO,
    "M": TO_MINUS,
    "P": TO_PLUS,
    "A": TO_AWAY,
    "E": TO_EVEN,
    "O": TO_ODD,
    "Z": TO_ZERO,
    "R": TO_ZERO_05_AWAY,
}


@dataclasses.dataclass(frozen=True)
class FormatSpecification:
    """Description of a format specification."""

    #: The rounding type to use: "e" versus "f". We'll replace
    #: this with something more generic later.
    round_type: str = "f"

    #: The rounding mode to use.
    rounding_mode: RoundingMode = TIES_TO_EVEN

    #: Number of decimal places after the point. May be
    #: zero or negative.
    places: Optional[int] = None

    #: Number of significant figures. If given, must be positive.
    figures: Optional[int] = None

    #: Whether the target format allows negative zeros or not.
    signed_zero: bool = True

    #: Whether to always output in scientific format.
    scientific: bool = False

    #: If True, a decimal point is always included in the formatted
    #: result even when there are no digits following it.
    always_include_point: bool = False

    #: Minimum numbers of digits before and after the point;
    #: these should be nonnegative integers, and to avoid having no
    #: digits at all their sum should be positive.
    min_digits_before_point: int = 1
    min_digits_after_point: int = 0

    #: Character used for zero padding
    zero: str = "0"

    #: Decimal separator.
    decimal_separator: str = "."

    #: String used to introduce the exponent.
    e: str = "e"

    #: Sign to use for negative values.
    negative_sign: str = "-"

    #: Sign to use for positive values.
    positive_sign: str = ""

    #: Exponent to use for zero.
    exponent_for_zero: int = 0

    @classmethod
    def from_string(cls, pattern: str) -> FormatSpecification:
        """
        Create a format specification from a format specification string.

        Parameters
        ----------
        pattern
            The format specification string.

        Returns
        -------
        FormatSpecification
            The format specification object representing the string.
        """
        match = _PATTERN.match(pattern)
        if match is None:
            raise ValueError(f"Invalid pattern: {pattern!r}")

        kwargs: Dict[str, Any] = {}

        round_type = match["type"]
        if round_type == "f":
            places = int(match["precision"])
            kwargs.update(
                places=places,
                exponent_for_zero=-places,
            )
        elif round_type == "e":
            kwargs.update(figures=int(match["precision"]) + 1)
            kwargs.update(scientific=True)
        else:
            raise ValueError("Unhandled round type")

        if (mode_code := match["mode"]) is not None:
            kwargs.update(rounding_mode=_MODE_FORMAT_CODES[mode_code])
        if (sign := match["sign"]) == "+" or sign == " ":
            kwargs.update(positive_sign=sign)
        if match["no_neg_0"]:
            kwargs.update(signed_zero=False)
        if match["alt"] is not None:
            kwargs.update(always_include_point=True)

        return cls(
            round_type=round_type,
            **kwargs,
        )

    @property
    def target_format(self) -> TargetFormat:
        """Get the target format for this format specification."""
        minimum_exponent = None if self.places is None else -self.places
        return TargetFormat(
            minimum_exponent=minimum_exponent,
            maximum_figures=self.figures,
            signed_zero=self.signed_zero,
        )

    def format(self, rounded: IntermediateForm) -> str:
        """
        Format a decimal object in intermediate form using this format specification.

        Parameters
        ----------
        rounded
            The value to be formatted.

        Returns
        -------
        str
            The formatted value.
        """
        # Get digits as a decimal string.
        digits = str(rounded.significand) if rounded.significand else ""

        # Adjust for scientific notation
        use_exponent = self.scientific
        if use_exponent:
            if not rounded.significand:
                # Q: What should the displayed exponent be in this case?
                raise NotImplementedError("later")

            # Nonzero value: place the decimal point after the
            # first digit.
            e_exponent = rounded.exponent + len(digits) - 1
            end_exponent = rounded.exponent - e_exponent
        else:
            end_exponent = rounded.exponent

        # Figure out number-line positions.
        start_exponent = end_exponent + len(digits)

        # Pad with zeros to ensure required minimum number of digits before and
        # after the point.
        if start_exponent < self.min_digits_before_point:
            digits = (
                self.zero * (self.min_digits_before_point - start_exponent) + digits
            )
            start_exponent = self.min_digits_before_point
        if end_exponent >= -self.min_digits_after_point:
            digits = digits + self.zero * (end_exponent + self.min_digits_after_point)
            end_exponent = -self.min_digits_after_point

        # Determine the string to use to represent the sign.
        sign_str = self.negative_sign if rounded.sign else self.positive_sign

        # Assemble the result.
        before_point = digits[:start_exponent]
        after_point = digits[start_exponent:]
        if after_point or self.always_include_point:
            point = self.decimal_separator
        else:
            point = ""
        if use_exponent:
            exponent = self.e + str(e_exponent)
        else:
            exponent = ""

        return sign_str + before_point + point + after_point + exponent


@dataclasses.dataclass(frozen=True)
class TargetFormat:
    """
    Class representing a target format for a rounding operation.

    This is a parametric description of a (typically infinite) collection of
    IntermediateForm values.
    """

    # Minimum exponent for represented values. Every representable value is an integer
    # multiple of 10**minimum_exponent.
    minimum_exponent: Optional[int] = None

    # Maximum number of significant figures in the result.
    maximum_figures: Optional[int] = None

    # Whether the target format has negative zeros.
    signed_zero: bool = True

    def target_exponent(self, decade: Optional[int]) -> Optional[int]:
        """
        Exponent to round to, given the decade of the value being rounded.

        The decade of a nonzero (finite) value v is the unique integer e
        satisfying 10**e <= abs(v) < 10**(e+1). For a zero value, this function
        accepts a decade of `None`.

        A return value of None should be interpreted as -infinity - that is,
        no rounding is permitted, and the value must be unchanged.
        """
        exponents = []
        if self.minimum_exponent is not None:
            exponents.append(self.minimum_exponent)
        if self.maximum_figures is not None:
            if decade is None:
                decade = 0
            exponents.append(decade + 1 - self.maximum_figures)
        return max(exponents, default=None)


def round_for_format(
    x: Any, *, format: TargetFormat, mode: RoundingMode = TIES_TO_EVEN
) -> IntermediateForm:
    """
    Round a value to a given target format, using a given rounding mode.

    Returns an intermediate form, which can then be formatted to a string.
    """
    # Preround if necessary.
    # Shouldn't matter if decade(x) is an underestimate - we just end up computing more
    # digits than necessary. In effect, we're saying that we know that x >= 10**d.

    # We _do_ assume that target_exponent is increasing with increasing decade.
    decade_x = None if is_zero(x) else decade(x)
    target_exponent = format.target_exponent(decade_x)
    prerounded = preround(x, target_exponent)

    actual_target_exponent = format.target_exponent(prerounded.decade)
    assert (
        target_exponent is None
        or actual_target_exponent is not None
        and actual_target_exponent >= target_exponent
    )

    if actual_target_exponent is None:
        return prerounded

    result = prerounded.round(actual_target_exponent, mode)

    # Drop negative sign on zeros.
    if not format.signed_zero:
        result = result.force_unsigned_zero()

    # Adjust in the case that rounding has changed the decade.
    if format.maximum_figures is not None:
        result = result.nudge(format.maximum_figures)

    return result


def format(value: Any, pattern: str) -> str:
    """
    Format a value using the given pattern.

    Parameters
    ----------
    value : number
        Value to be formatted.
    pattern : str
        Pattern describing how to format.

    Returns
    -------
    Formatted string
    """
    format_specification = FormatSpecification.from_string(pattern)

    # Step 1: convert to rounded value.
    rounded2 = round_for_format(
        value,
        format=format_specification.target_format,
        mode=format_specification.rounding_mode,
    )

    # Step 2: convert to string. Only supporting e and f-presentation formats right now.
    return format_specification.format(rounded2)

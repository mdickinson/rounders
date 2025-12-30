"""Formatting functionality."""

from __future__ import annotations

import dataclasses
import re
import sys
from typing import Any

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from rounders.generics import decade, is_zero, preround
from rounders.intermediate_form import IntermediateForm
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
from rounders.target_format import TargetFormat

_PATTERN = re.compile(
    r"""
    (?P<sign>[-+ ])?
    (?P<no_neg_0>z)?
    (?P<alt>\#)?
    \.
    (?P<precision>-?[0-9]+)
    (?P<mode>[aemopzAEMOPRZ])?
    (?P<type>[ef])
    """,
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


@dataclasses.dataclass(frozen=True, kw_only=True)
class FormatSpecification:
    """Description of a format specification."""

    #: The rounding type to use: "e" versus "f". We'll replace
    #: this with something more generic later.
    round_type: str = "f"

    #: The rounding mode to use.
    rounding_mode: RoundingMode = TIES_TO_EVEN

    #: Number of decimal places after the point. May be
    #: zero or negative.
    places: int | None = None

    #: Number of significant figures. If given, must be positive.
    figures: int | None = None

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

    @classmethod
    def from_str(cls, pattern: str) -> Self:
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
        match = _PATTERN.fullmatch(pattern)
        if match is None:
            raise ValueError(f"Invalid pattern: {pattern!r}")

        kwargs: dict[str, Any] = {}

        round_type = match["type"]
        if round_type == "f":
            places = int(match["precision"])
            kwargs.update(places=places)
            kwargs.update(min_digits_after_point=max(0, places))
        elif round_type == "e":
            figures = int(match["precision"]) + 1
            kwargs.update(figures=figures)
            kwargs.update(scientific=True)
            kwargs.update(min_digits_after_point=figures - 1)
        else:
            raise ValueError("Unhandled round type")

        if mode_code := match["mode"]:
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
        # Get necessary attributes.
        digits, low_exponent, sign = rounded.digits, rounded.exponent, rounded.sign
        high_exponent = rounded.exponent + len(digits)

        # Adjust for scientific notation. e_exponent is the value that will appear after
        # the 'e' in the formatted result.
        use_exponent = self.scientific
        if use_exponent and digits:
            e_exponent = low_exponent + len(digits) - 1
        else:
            e_exponent = 0

        # Figure out number-line positions.
        start_exponent = high_exponent - e_exponent
        end_exponent = low_exponent - e_exponent

        # Pad with zeros to ensure required minimum number of digits before and
        # after the point.
        if start_exponent < self.min_digits_before_point:
            digits = (
                self.zero * (self.min_digits_before_point - start_exponent) + digits
            )
            start_exponent = self.min_digits_before_point
        if end_exponent > -self.min_digits_after_point:
            digits = digits + self.zero * (end_exponent + self.min_digits_after_point)
            end_exponent = -self.min_digits_after_point

        # Determine the string to use to represent the sign.
        sign_str = self.negative_sign if sign else self.positive_sign

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


def round_to_format(
    number: Any,
    format: TargetFormat,
    *,
    mode: RoundingMode = TIES_TO_EVEN,
) -> IntermediateForm:
    """
    Round a finite value to a given target format, using a given rounding mode.

    Returns a value in intermediate form.
    """
    # Preround to an appropriate exponent.
    exponent = (
        None if is_zero(number) else format.minimum_exponent_for_decade(decade(number))
    )
    result: IntermediateForm = preround(number, exponent=exponent)

    # Round if necessary (but avoid reducing the exponent unnecessarily).
    if exponent is not None and exponent > result.exponent:
        result = result.round(exponent, mode)

    # Drop negative sign on zeros (even those that arise from rounding nonzero values).
    if not format.signed_zero:
        result = result.force_unsigned_zero()

    # Adjust in the case that rounding has changed the decade.
    if format.maximum_figures is not None:
        result = result.trim(format.maximum_figures)

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
    format_specification = FormatSpecification.from_str(pattern)

    # Step 1: convert to rounded value.
    rounded = round_to_format(
        value,
        format=format_specification.target_format,
        mode=format_specification.rounding_mode,
    )

    # Step 2: convert to string. Only supporting e and f-presentation formats right now.
    return format_specification.format(rounded)

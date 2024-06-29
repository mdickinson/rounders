"""Formatting functionality."""

from __future__ import annotations

import dataclasses
import re
from typing import Any, Dict, Optional

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

    #: Sign to use for negative nonzero values.
    negative_sign: str = "-"

    #: Sign to use for negative zero values.
    negative_zero_sign: str = "-"

    #: Sign to use for positive values.
    positive_sign: str = ""

    #: Sign to use for positive zero values.
    positive_zero_sign: str = ""

    #: Exponent to use for zero.
    exponent_for_zero: int = 0

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

        # Determine the sign.
        iszero = is_zero(rounded)
        if rounded.sign:
            sign_str = self.negative_zero_sign if iszero else self.negative_sign
        else:
            sign_str = self.positive_zero_sign if iszero else self.positive_sign

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
        match = _PATTERN.fullmatch(pattern)
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

        mode_code = match["mode"]
        if mode_code is not None:
            kwargs.update(rounding_mode=_MODE_FORMAT_CODES[mode_code])

        sign = match["sign"]
        if sign == "+" or sign == " ":
            kwargs.update(
                positive_sign=sign,
                positive_zero_sign=sign,
            )
        if match["no_neg_0"]:
            if sign == "+" or sign == " ":
                kwargs.update(negative_zero_sign=sign)
            else:
                kwargs.update(negative_zero_sign="")

        if match["alt"] is not None:
            kwargs.update(always_include_point=True)

        return cls(
            round_type=round_type,
            **kwargs,
        )


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
    bounds = []
    if is_zero(value):
        exponent = format_specification.exponent_for_zero

    else:
        if format_specification.places is not None:
            bounds.append(-format_specification.places)

        if format_specification.figures is not None:
            bounds.append(decade(value) + 1 - format_specification.figures)

        exponent = max(bounds)

    prerounded = preround(value, exponent)
    rounded = prerounded.round(exponent, format_specification.rounding_mode)
    if format_specification.figures is not None:
        # Adjust if necessary.
        rounded = rounded.trim(format_specification.figures)

    # Step 2: convert to string. Only supporting e and f-presentation formats right now.
    return format_specification.format(rounded)

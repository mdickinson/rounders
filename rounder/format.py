"""
Formatting functionality.
"""

import dataclasses
import re
import sys
import typing

from rounder.core import Rounded
from rounder.generics import decade, is_zero, to_quarters
from rounder.modes import (
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

# Provide compatibility for Python versions older than 3.10, which don't support
# kw_only.
if sys.version_info < (3, 10):
    frozen_dataclass = dataclasses.dataclass(frozen=True)
else:
    frozen_dataclass = dataclasses.dataclass(frozen=True, kw_only=True)


#: Class describing a format specification.
@frozen_dataclass
class FormatSpecification:

    #: The rounding type to use: "e" versus "f". We'll replace
    #: this with something more generic later.
    round_type: str = "f"

    #: The rounding mode to use.
    rounding_mode: RoundingMode = TIES_TO_EVEN

    #: Number of decimal places after the point. May be
    #: zero or negative.
    places: typing.Optional[int] = None

    #: Number of significant figures. If given, must be positive.
    figures: typing.Optional[int] = None

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

    def format(self, rounded: Rounded):

        # Step 2: convert to string. Only supporting f-presentation format right now.
        sign = rounded.sign

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
        iszero = rounded.significand == 0
        if rounded.sign:
            sign = self.negative_zero_sign if iszero else self.negative_sign
        else:
            sign = self.positive_zero_sign if iszero else self.positive_sign

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

        return sign + before_point + point + after_point + exponent

    @classmethod
    def from_string(self, pattern):
        match = _PATTERN.match(pattern)
        if match is None:
            raise ValueError(f"Invalid pattern: {pattern!r}")

        kwargs = {}

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

        return FormatSpecification(
            round_type=round_type,
            **kwargs,
        )


def format(value, pattern):
    """
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

    quarters = to_quarters(value, exponent)
    rounded = Rounded(
        quarters.sign,
        quarters.whole + format_specification.rounding_mode(quarters),
        exponent,
    )
    if format_specification.figures is not None:

        # Adjust if necessary.
        if len(str(rounded.significand)) == format_specification.figures + 1:
            rounded = Rounded(
                rounded.sign, rounded.significand // 10, rounded.exponent + 1
            )

    # Step 2: convert to string. Only supporting e and f-presentation formats right now.
    return format_specification.format(rounded)

"""
Formatting functionality.
"""

import dataclasses
import re

from rounder.core import Rounded
from rounder.generics import to_quarters
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
f
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


#: Class describing a format specification.
@dataclasses.dataclass(frozen=True, kw_only=True)
class FormatSpecification:
    #: The rounding mode to use.
    rounding_mode: RoundingMode = TIES_TO_EVEN

    #: Number of decimal places after the point. This can be negative.
    places: int

    #: If True, a decimal point is always included in the formatted
    #: result even when there are no digits following it.
    always_include_point: bool = False

    #: Minimum numbers of digits before and after the point;
    #: these should be nonnegative integers, and to avoid having no
    #: digits at all their sum should be positive.
    min_digits_before_point: int = 1
    min_digits_after_point: int = 0

    #: Decimal separator.
    decimal_separator: str = "."

    #: Sign to use for negative nonzero values.
    negative_sign: str = "-"

    #: Sign to use for negative zero values.
    negative_zero_sign: str = "-"

    #: Sign to use for positive values.
    positive_sign: str = ""

    #: Sign to use for positive zero values.
    positive_zero_sign: str = ""

    def format(self, rounded: Rounded):

        # Step 2: convert to string. Only supporting f-presentation format right now.
        sign = rounded.sign

        # Get digits as a decimal string.
        digits = str(rounded.significand) if rounded.significand else ""

        # Figure out number-line positions.
        end_exponent = rounded.exponent
        start_exponent = end_exponent + len(digits)

        # Pad with zeros to ensure required minimum number of digits before and
        # after the point.
        if start_exponent < self.min_digits_before_point:
            digits = "0" * (self.min_digits_before_point - start_exponent) + digits
            start_exponent = self.min_digits_before_point
        if end_exponent >= -self.min_digits_after_point:
            digits = digits + "0" * (end_exponent + self.min_digits_after_point)
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
        return sign + before_point + point + after_point

    @classmethod
    def from_string(self, pattern):
        match = _PATTERN.match(pattern)
        if match is None:
            raise ValueError(f"Invalid pattern: {pattern!r}")

        precision = int(match.group("precision"))
        mode_code = match.group("mode")
        mode = TIES_TO_EVEN if mode_code is None else _MODE_FORMAT_CODES[mode_code]
        sign = match.group("sign")

        kwargs = {}

        if sign == "+" or sign == " ":
            kwargs.update(
                dict(
                    positive_sign=sign,
                    positive_zero_sign=sign,
                )
            )
        if match.group("no_neg_0"):
            if sign == "+" or sign == " ":
                kwargs.update(dict(negative_zero_sign=sign))
            else:
                kwargs.update(dict(negative_zero_sign=""))

        return FormatSpecification(
            rounding_mode=mode,
            places=precision,
            always_include_point=match.group("alt") is not None,
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
    exponent = -format_specification.places
    quarters = to_quarters(value, exponent)
    rounded = Rounded(
        quarters.sign,
        quarters.whole + format_specification.rounding_mode(quarters),
        exponent,
    )

    # Step 2: convert to string. Only supporting f-presentation format right now.
    return format_specification.format(rounded)

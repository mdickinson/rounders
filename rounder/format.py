"""
Formatting functionality.
"""

import re

from rounder.core import Rounded
from rounder.generics import to_quarters, to_type_of
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
)

_PATTERN = re.compile(
    r"""
    \A\.
    (?P<places>\d*)
    (?P<mode>[aemopzAEMOPRZ])?
    f\Z
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
    import decimal

    match = _PATTERN.match(pattern)
    if match is None:
        raise ValueError(f"Invalid pattern: {pattern!r}")

    places = int(match.group("places"))
    mode_code = match.group("mode")
    mode = TIES_TO_EVEN if mode_code is None else _MODE_FORMAT_CODES[mode_code]

    exponent = -places
    quarters = to_quarters(value, exponent)
    rounded = Rounded(quarters.sign, quarters.whole + mode(quarters), exponent)
    return str(to_type_of(decimal.Decimal(0), rounded))

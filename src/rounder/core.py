"""
Representations of intermediate values.
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class SignedQuarterInt:
    """
    Representation of a quarter-integer with separate sign.

    The value represented is 'whole + quarters/4' if sign is False,
    and -(whole + quarters/4) if sign is True.
    """

    # True for negative, False for positive.
    sign: bool

    # Nonnegative integer giving the whole part of the fraction.
    whole: int

    # Integer in range(4) giving the number of quarters.
    quarters: int


@dataclasses.dataclass(frozen=True)
class Rounded:
    """
    Finite rounded value with sign, significand and exponent.

    The value represented is significand * 10**exponent if sign is False, and
    -(significand * 10**exponent) is sign is True.
    """

    # True for negative, False for positive.
    sign: bool

    # Nonnegative integer giving the coefficient of the rounded result.
    significand: int

    # Integer giving the decimal exponent.
    exponent: int

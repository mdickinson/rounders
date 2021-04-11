"""
Representations of intermediate values.
"""

from collections import namedtuple

#: Representation of a quarter-integer, with separate sign.

# `sign` is a boolean: True for negative, False for positive
# `whole` is a nonnegative int, giving the whole part of the fraction
# `quarters` is a nonnegative int in the range 0 <= quarters < 4,
# representing the fractional part.
#
# The value represented is whole + quarterss/4 if sign is False, and
# -(whole + quarters/4) if sign is True.
SignedQuarterInt = namedtuple("SignedQuarterInt", ["sign", "whole", "quarters"])

#: Representation of a finite rounded value, with sign, significand and exponent.

# `sign` is a boolean: True for negative, False for positive
# `significand` is a nonnegative int, giving the coefficient of the rounded result
# `exponent` is an integer
#
# The value represented is significand * 10**exponent if sign is False, and
# -(significand * 10**exponent) is sign is True.
Rounded = namedtuple("Rounded", ["sign", "significand", "exponent"])

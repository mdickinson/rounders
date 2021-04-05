"""
Representations of intermediate values.
"""

from collections import namedtuple

#: Representation of a quarter-integer, with separate sign.

# `sign` is a boolean: True for negative, False for positive
# `whole` is a nonnegative int, giving the whole part of the fraction
# `quarters` is a nonnegative int in the range 0 <= quarters < 4,
# representing the fractional part.
SignedQuarterInt = namedtuple("SignedQuarterInt", ["sign", "whole", "quarters"])

#: Representation of an integer with sign. Represents the same set of values
#: as a plain int, except that positive and negative zero are distinguished.
SignedInt = namedtuple("SignedInt", ["sign", "magnitude"])

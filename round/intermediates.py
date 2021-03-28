"""
Representations of intermediate values.
"""

from collections import namedtuple


#: Representation of a quarter-integer, with separate sign.

# sign should be a boolean: True for negative, False for positive
# whole is a nonnegative int, giving the whole part of the fraction
# quarters is a nonnegative int in the range 0 <= quarters < 4,
# representing the fractional part.
SignedQuarters = namedtuple("SignedQuarters", ["sign", "whole", "quarters"])

"""
Rounding modes.

A rounding mode is a callable that accepts a quarter integer value (something
of type SignedQuarterInt) and returns a bool indicating whether that value should
be rounded away from zero.
"""


from typing import Callable

from rounder.core import SignedQuarterInt

#: Type for rounding modes.
RoundingMode = Callable[[SignedQuarterInt], bool]


def standard_rounding_mode(signature):
    def round_decide(quarters: SignedQuarterInt) -> bool:
        odd = quarters.whole & 1
        return quarters.quarters + signature[quarters.sign][odd] >= 4

    return round_decide


#: Round for re-round.
def TO_ZERO_05_AWAY(quarters):
    return quarters.quarters > 0 and quarters.whole % 5 == 0


#: To-nearest rounding modes.
TIES_TO_ZERO: RoundingMode = standard_rounding_mode([[1, 1], [1, 1]])
TIES_TO_AWAY: RoundingMode = standard_rounding_mode([[2, 2], [2, 2]])
TIES_TO_MINUS: RoundingMode = standard_rounding_mode([[1, 1], [2, 2]])
TIES_TO_PLUS: RoundingMode = standard_rounding_mode([[2, 2], [1, 1]])
TIES_TO_EVEN: RoundingMode = standard_rounding_mode([[1, 2], [1, 2]])
TIES_TO_ODD: RoundingMode = standard_rounding_mode([[2, 1], [2, 1]])

#: Directed rounding modes.
TO_ZERO: RoundingMode = standard_rounding_mode([[0, 0], [0, 0]])
TO_AWAY: RoundingMode = standard_rounding_mode([[3, 3], [3, 3]])
TO_MINUS: RoundingMode = standard_rounding_mode([[0, 0], [3, 3]])
TO_PLUS: RoundingMode = standard_rounding_mode([[3, 3], [0, 0]])
TO_EVEN: RoundingMode = standard_rounding_mode([[0, 3], [0, 3]])
TO_ODD: RoundingMode = standard_rounding_mode([[3, 0], [3, 0]])

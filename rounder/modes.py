"""
Rounding modes.

A rounding mode is a callable that accepts a quarter integer value (something
of type SignedQuarterInt) and returns a bool indicating whether that value should
be rounded away from zero.

This module implements 13 rounding modes. There are six directed rounding modes,
six to-nearest rounding modes, and one extra rounding mode TO_ZERO_05_AWAY

Directed rounding modes
-----------------------

The six directed rounding modes occur in three opposite pairs, here illustrated by
their actions when rounding a real number to an integer.

To zero: floor(x) for nonnegative x, ceil(x) for negative x

    ⋯→→●→→→●→→→●←←←●←←←●←←←●←←⋯
      -2  -1   0   1   2   3


To away: floor(x) for negative x, ceil(x) for nonnegative x

    ⋯←←●←←←●←←←●→→→●→→→●→→→●→→⋯
      -2  -1   0   1   2   3


To minus: floor(x)

    ⋯←←●←←←●←←←●←←←●←←←●←←←●←←⋯
      -2  -1   0   1   2   3

To plus: ceil(x)

    ⋯→→●→→→●→→→●→→→●→→→●→→→●→→⋯
      -2  -1   0   1   2   3

To even: floor(x) if floor(x) is even, else ceil(x)

    ⋯→→●←←←●→→→●←←←●→→→●←←←●→→⋯
      -2  -1   0   1   2   3

To odd: floor(x) if floor(x) is odd, else ceil(x)

    ⋯←←●→→→●←←←●→→→●←←←●→→→●←←⋯
      -2  -1   0   1   2   3

There are six corresponding round-to-nearest rounding modes: where every input
value x rounds to the nearest integer, and the zero / away / minus / plus / even / odd
rule only applies in halfway cases - numbers of the form n + 0.5 for an integer n.

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

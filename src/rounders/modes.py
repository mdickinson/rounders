"""
Rounding modes.

A rounding mode is an object with a 'round' method. That 'round' method accepts
a value in the form `±(n + d/10)` where n is a nonnegative integer and d is
a single digit integer (0 <= d < 10), and rounds it to the nearest integer.

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

To-nearest rounding modes
-------------------------

The six round-to-nearest rounding modes correspond directly to the directed rounding
modes: in non-halfway cases, an input value x is rounded to the nearest integer. In
halfway cases, the corresponding directed rounding mode is applied, and the value x
is rounded using the zero / away / minus / plus / even / odd rule as appropriate.

"""


import abc
from typing import Tuple


class RoundingMode(abc.ABC):
    @abc.abstractmethod
    def round(self, sign: int, significand: int, tenths: int) -> int:
        """
        Round the value represented by (-1)**sign * (significand + tenths / 10)
        to the nearest integer.
        """


class _StandardRoundingMode(RoundingMode):
    def __init__(self, signature: Tuple[Tuple[int, int], Tuple[int, int]]):
        self._signature = signature

    def round(self, sign: int, significand: int, tenths: int) -> int:
        is_odd = significand % 2
        round_up = tenths + self._signature[sign][is_odd] >= 10
        return significand + round_up


class _RoundForReroundRoundingMode(RoundingMode):
    def round(self, sign: int, significand: int, tenths: int) -> int:
        round_up = tenths > 0 and significand % 5 == 0
        return significand + round_up


#: Round for re-round.
TO_ZERO_05_AWAY: RoundingMode = _RoundForReroundRoundingMode()

#: To-nearest rounding modes.
TIES_TO_ZERO: RoundingMode = _StandardRoundingMode(((4, 4), (4, 4)))
TIES_TO_AWAY: RoundingMode = _StandardRoundingMode(((5, 5), (5, 5)))
TIES_TO_MINUS: RoundingMode = _StandardRoundingMode(((4, 4), (5, 5)))
TIES_TO_PLUS: RoundingMode = _StandardRoundingMode(((5, 5), (4, 4)))
TIES_TO_EVEN: RoundingMode = _StandardRoundingMode(((4, 5), (4, 5)))
TIES_TO_ODD: RoundingMode = _StandardRoundingMode(((5, 4), (5, 4)))

#: Directed rounding modes.
TO_ZERO: RoundingMode = _StandardRoundingMode(((0, 0), (0, 0)))
TO_AWAY: RoundingMode = _StandardRoundingMode(((9, 9), (9, 9)))
TO_MINUS: RoundingMode = _StandardRoundingMode(((0, 0), (9, 9)))
TO_PLUS: RoundingMode = _StandardRoundingMode(((9, 9), (0, 0)))
TO_EVEN: RoundingMode = _StandardRoundingMode(((0, 9), (0, 9)))
TO_ODD: RoundingMode = _StandardRoundingMode(((9, 0), (9, 0)))

"""
Rounding modes.

A rounding mode is a callable that accepts a quarter integer value (something
of type IntermediateForm) and returns a bool indicating whether that value should
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

To-nearest rounding modes
-------------------------

The six round-to-nearest rounding modes correspond directly to the directed rounding
modes: in non-halfway cases, an input value x is rounded to the nearest integer. In
halfway cases, the corresponding directed rounding mode is applied, and the value x
is rounded using the zero / away / minus / plus / even / odd rule as appropriate.

"""


import abc
from typing import Tuple

from rounders.intermediate import IntermediateForm


class RoundingMode(abc.ABC):
    @abc.abstractmethod
    def round(self, intermediate: IntermediateForm) -> IntermediateForm:
        """
        Round using the given rounding mode.
        """
        raise NotImplementedError("Should be implemented in subclasses")


class _StandardRoundingMode(RoundingMode):
    def __init__(self, signature: Tuple[Tuple[int, int], Tuple[int, int]]):
        self._signature = signature

    def round(self, intermediate: IntermediateForm) -> IntermediateForm:
        """
        Round using the given rounding mode.
        """
        is_odd, tenths = divmod(intermediate.significand % 20, 10)
        round_up = tenths + self._signature[intermediate.sign][is_odd] >= 10
        return intermediate.to_away() if round_up else intermediate.to_zero()


class _RoundForReroundRoundingMode(RoundingMode):
    def round(self, intermediate: IntermediateForm) -> IntermediateForm:
        """
        Round using the given rounding mode.
        """
        round_up = intermediate.significand % 50 < 10
        return intermediate.to_away() if round_up else intermediate.to_zero()


#: Round for re-round.
TO_ZERO_05_AWAY = _RoundForReroundRoundingMode()

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

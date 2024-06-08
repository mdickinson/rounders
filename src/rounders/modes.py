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
    """Abstract base class for rounding modes."""

    @abc.abstractmethod
    def round(self, sign: int, significand: int, tenths: int) -> int:
        """
        Round a value with tenths to an integer.

        Rounds the value represented by (-1)**sign * (significand + tenths / 10)
        to an integer.
        """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name for this rounding mode."""

    def __repr__(self) -> str:
        """Representation of this rounding mode."""
        return f"<RoundingMode: {self.name}>"


class _StandardRoundingMode(RoundingMode):
    """
    Standard rounding mode.

    These rounding modes only depend on the parity of the integer part of the
    value to be rounded, and are either directed rounding modes (rounding every
    value between two integers in the same direction), or round-to-nearest rounding
    modes, rounding all non-ties to an integer.
    """

    def __init__(self, signature: Tuple[Tuple[int, int], Tuple[int, int]], name: str):
        self._signature = signature
        self._name = name

    def round(self, sign: int, significand: int, tenths: int) -> int:
        """
        Round a value with tenths to an integer.

        Rounds the value represented by (-1)**sign * (significand + tenths / 10)
        to an integer.
        """
        is_odd = significand % 2
        round_up = tenths + self._signature[sign][is_odd] >= 10
        return significand + round_up

    @property
    def name(self) -> str:
        """Name for this rounding mode."""
        return self._name


class _RoundForReroundRoundingMode(RoundingMode):
    """
    Round for reround.

    This rounding mode is most useful for allowing subsequent roundings with smaller
    precision, while avoiding issues from double rounding.
    """

    def round(self, sign: int, significand: int, tenths: int) -> int:
        """
        Round a value with tenths to an integer.

        Rounds the value represented by (-1)**sign * (significand + tenths / 10)
        to an integer.
        """
        round_up = tenths > 0 and significand % 5 == 0
        return significand + round_up

    @property
    def name(self) -> str:
        """Name for this rounding mode."""
        return "to zero (05 away)"


#: Round for re-round.
TO_ZERO_05_AWAY: RoundingMode = _RoundForReroundRoundingMode()

#: To-nearest rounding modes.
TIES_TO_ZERO: RoundingMode = _StandardRoundingMode(((4, 4), (4, 4)), name="ties to zero")
TIES_TO_AWAY: RoundingMode = _StandardRoundingMode(((5, 5), (5, 5)), name="ties to away")
TIES_TO_MINUS: RoundingMode = _StandardRoundingMode(
    ((4, 4), (5, 5)), name="ties to minus"
)
TIES_TO_PLUS: RoundingMode = _StandardRoundingMode(((5, 5), (4, 4)), name="ties to plus")
TIES_TO_EVEN: RoundingMode = _StandardRoundingMode(((4, 5), (4, 5)), name="ties to even")
TIES_TO_ODD: RoundingMode = _StandardRoundingMode(((5, 4), (5, 4)), name="ties to odd")

#: Directed rounding modes.
TO_ZERO: RoundingMode = _StandardRoundingMode(((0, 0), (0, 0)), name="to zero")
TO_AWAY: RoundingMode = _StandardRoundingMode(((9, 9), (9, 9)), name="to away")
TO_MINUS: RoundingMode = _StandardRoundingMode(((0, 0), (9, 9)), name="to minus")
TO_PLUS: RoundingMode = _StandardRoundingMode(((9, 9), (0, 0)), name="to plus")
TO_EVEN: RoundingMode = _StandardRoundingMode(((0, 9), (0, 9)), name="to even")
TO_ODD: RoundingMode = _StandardRoundingMode(((9, 0), (9, 0)), name="to odd")

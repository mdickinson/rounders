from rounder.core import SignedInt, SignedQuarterInt

#: Signatures for to-nearest rounding modes
TIES_TO_ZERO = [[1, 1], [1, 1]]
TIES_TO_AWAY = [[2, 2], [2, 2]]
TIES_TO_PLUS = [[2, 2], [1, 1]]
TIES_TO_MINUS = [[1, 1], [2, 2]]
TIES_TO_EVEN = [[1, 2], [1, 2]]
TIES_TO_ODD = [[2, 1], [2, 1]]

#: Signatures for directed rounding modes
TO_ZERO = [[0, 0], [0, 0]]
TO_AWAY = [[3, 3], [3, 3]]
TO_MINUS = [[0, 0], [3, 3]]
TO_PLUS = [[3, 3], [0, 0]]
TO_EVEN = [[0, 3], [0, 3]]
TO_ODD = [[3, 0], [3, 0]]

#: Round for re-round
TO_ZERO_05_AWAY = "TO_ZERO_05_AWAY"


def round_decide(quarters: SignedQuarterInt, *, rounding_mode) -> SignedInt:
    """
    Decide whether to round a given value up or not, for a given rounding mode.
    """
    if rounding_mode == TO_ZERO_05_AWAY:
        return quarters.quarters > 0 and quarters.whole % 5 == 0
    else:
        odd = quarters.whole & 1
        return quarters.quarters + rounding_mode[quarters.sign][odd] >= 4


def round_quarters(quarters: SignedQuarterInt, *, rounding_mode) -> SignedInt:
    """
    Round a quarter-integer to an integer using the given rounding mode.
    """
    round_away = round_decide(quarters, rounding_mode=rounding_mode)
    return SignedInt(quarters.sign, quarters.whole + round_away)

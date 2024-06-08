"""Interface for the rounders package."""

import rounders.decimal_overloads  # noqa: F401
import rounders.float_overloads  # noqa: F401
import rounders.fraction_overloads  # noqa: F401
import rounders.int_overloads  # noqa: F401
from rounders.mode_specific import (
    round_ties_to_away,
    round_ties_to_even,
    round_ties_to_minus,
    round_ties_to_odd,
    round_ties_to_plus,
    round_ties_to_zero,
    round_to_away,
    round_to_even,
    round_to_minus,
    round_to_odd,
    round_to_plus,
    round_to_zero,
    round_to_zero_05_away,
)
from rounders.modes import (
    TIES_TO_AWAY,
    TIES_TO_EVEN,
    TIES_TO_MINUS,
    TIES_TO_ODD,
    TIES_TO_PLUS,
    TIES_TO_ZERO,
    TO_AWAY,
    TO_EVEN,
    TO_MINUS,
    TO_ODD,
    TO_PLUS,
    TO_ZERO,
    TO_ZERO_05_AWAY,
    RoundingMode,
)
from rounders.round_to import round, round_to_figures, round_to_int, round_to_places

ceil = round_to_plus
floor = round_to_minus
trunc = round_to_zero

__all__ = [
    # Top-level rounding functions
    "round",
    "round_to_figures",
    "round_to_int",
    "round_to_places",
    # Mode-specific rounding functions - replacements for round
    "round_ties_to_away",
    "round_ties_to_even",
    "round_ties_to_minus",
    "round_ties_to_odd",
    "round_ties_to_plus",
    "round_ties_to_zero",
    "round_to_away",
    "round_to_even",
    "round_to_minus",
    "round_to_odd",
    "round_to_plus",
    "round_to_zero",
    "round_to_zero_05_away",
    # Aliases
    "ceil",
    "floor",
    "trunc",
    # Rounding mode type
    "RoundingMode",
    # Rounding modes - to-nearest
    "TIES_TO_AWAY",
    "TIES_TO_EVEN",
    "TIES_TO_MINUS",
    "TIES_TO_ODD",
    "TIES_TO_PLUS",
    "TIES_TO_ZERO",
    # Rounding modes - directed
    "TO_AWAY",
    "TO_EVEN",
    "TO_MINUS",
    "TO_ODD",
    "TO_PLUS",
    "TO_ZERO",
    # Round for re-round
    "TO_ZERO_05_AWAY",
]

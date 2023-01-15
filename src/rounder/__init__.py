"""
Interface for the rounder package.
"""

import rounder.decimal_overloads  # noqa: F401
import rounder.float_overloads  # noqa: F401
import rounder.fraction_overloads  # noqa: F401
import rounder.int_overloads  # noqa: F401
from rounder.format import format
from rounder.mode_specific import (
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
from rounder.modes import (
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
)
from rounder.round_to import round, round_to_figures, round_to_int, round_to_places

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

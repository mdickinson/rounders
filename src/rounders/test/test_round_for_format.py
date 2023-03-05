"""
Tests for round_for_format.
"""

import dataclasses
import unittest

from rounders.intermediate import IntermediateForm
from rounders.generics import decade, preround
from rounders.modes import TIES_TO_EVEN, TO_AWAY, TO_ZERO

# XXX Test cases where rounding changes the exponent.
# XXX Tests for round to figures when rounding zero.
# XXX Consider implementing __contains__ (possibly as a synonym for is_representable)
# XXX Don't use Decimal in from_str
# XXX Tests for the case where neither maximum_figures not minimum_exponent is supplied.
# XXX Add support for suppressing sign of zero.
# XXX Fix typing issues.
# XXX Later on, we should allow decade to be a lower bound. If it's
#     too small, the only effect is that we do extra work.
# XXX To do: Try testing after deliberately reducing decade by 1 (or 2, or 10)
# XXX To do: rewire round_to_figures to use this function, so that
#     we can benefit from existing tests.
# XXX Decide on signature and preferred calling pattern for IntermediateForm.round
#     - should we always pass by position?
# XXX Rethink IntermediateForm.__repr__.
# XXX Move key classes and functions to their own homes.
# XXX Support keeping the extra zero in the case where we round up to the next
#     power of 10.
# XXX Move decade computation for IntermediateForm to an overload for IntermediateForm.
#     Or possibly a method on IntermediateForm. Or both.
# XXX Test case where prerounding rounds a nonzero value to zero, so that the
#     original value has a valid decade but the prerounded value does not.


from typing import Optional


@dataclasses.dataclass(frozen=True)
class TargetFormat:
    """
    Class representing a target format for a rounding operation.

    This is a parametric description of a (typically infinite) collection of
    IntermediateForm values.
    """

    # Minimum exponent for represented values.
    minimum_exponent: Optional[int] = None

    # Maximum number of significant figures in the result.
    maximum_figures: Optional[int] = None



def round_to_format(x, *, format: TargetFormat, mode=TIES_TO_EVEN):
    if format.maximum_figures is format.minimum_exponent is None:
        raise NotImplementedError()

    min_exps = []
    if format.maximum_figures is not None:
        # decade is allowed to be an underestimate here
        decade_x = decade(x)
        min_exps.append(decade_x + 1 - format.maximum_figures)
    if format.minimum_exponent is not None:
        min_exps.append(format.minimum_exponent)
    prerounded = preround(x, max(min_exps))

    # Note that prerounding _never_ changes the decade. We can therefore
    # get the _true_ decade from prerounded.
    min_exps = []
    if format.maximum_figures is not None:
        actual_decade = prerounded.exponent + len(str(prerounded.significand)) - 1
        min_exps.append(actual_decade + 1 - format.maximum_figures)
    if format.minimum_exponent is not None:
        min_exps.append(format.minimum_exponent)
    return prerounded.round(max(min_exps), mode)




class TestRoundForFormat(unittest.TestCase):
    def test_minimum_exponent(self) -> None:
        format = TargetFormat(minimum_exponent=-3)

        # Pairs (value, mode, expected)
        test_values = [
            (3.14159, TIES_TO_EVEN, "3.142"),
            (3.14159, TO_ZERO, "3.141"),
        ]

        for unrounded, mode, expected in test_values:
            with self.subTest(unrounded=unrounded, mode=mode):
                rounded = round_to_format(unrounded, format=format, mode=mode)
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

    def test_maximum_figures(self) -> None:
        format = TargetFormat(maximum_figures = 3)

        # Pairs (value, mode, expected)
        test_values = [
            (3.14159, TIES_TO_EVEN, "3.14"),
            (3.14159, TO_ZERO, "3.14"),
            (3.14159, TO_AWAY, "3.15"),
            (12345.6, TIES_TO_EVEN, "123e2"),
            (0.00098765, TIES_TO_EVEN, "988e-6"),
            (0.00098765, TO_ZERO, "987e-6"),
        ]

        for unrounded, mode, expected in test_values:
            with self.subTest(unrounded=unrounded, mode=mode):
                rounded = round_to_format(unrounded, format=format, mode=mode)
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

    def test_minimum_exponent_and_maximum_figures(self):
        format = TargetFormat(
            maximum_figures=4,
            minimum_exponent=-2
        )

        # Pairs (value, mode, expected)
        test_values = [
            (3.14159, TIES_TO_EVEN, "3.14"),
            (23.14159, TIES_TO_EVEN, "23.14"),
            (123.14159, TIES_TO_EVEN, "123.1"),
            (6123.14159, TIES_TO_EVEN, "6123"),
        ]

        for unrounded, mode, expected in test_values:
            with self.subTest(unrounded=unrounded, mode=mode):
                rounded = round_to_format(unrounded, format=format, mode=mode)
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

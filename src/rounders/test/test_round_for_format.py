"""
Tests for round_for_format.
"""

import dataclasses
import decimal
import fractions
import math
import unittest
from typing import Any, Optional

from rounders.generics import decade, is_zero, preround
from rounders.intermediate import IntermediateForm, _smallest_ten_power_multiple
from rounders.modes import TIES_TO_EVEN, TO_AWAY, TO_ZERO, RoundingMode

# XXX Consider implementing __contains__ (possibly as a synonym for is_representable)
# XXX Don't use Decimal in from_str
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
# XXX Consider making unsigned zero the default.
# XXX Think about exponent preservation (e.g., for Decimal inputs); what should
#     rounding do?
# XXX Consider format flag requiring particular exponent for zero.
# XXX Remove tests for _smallest_ten_power_multiple
# XXX Make _smallest_ten_power_multiple more efficient


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

    def target_exponent(self, decade: Optional[int]) -> Optional[int]:
        """
        Exponent to round to, given the decade of the value being rounded.

        The decade of a nonzero (finite) value v is the unique integer e
        satisfying 10**e <= abs(v) < 10**(e+1). For a zero value, this function
        accepts a decade of `None`.

        A return value of None should be interpreted as -infinity - that is,
        no rounding is permitted, and the value must be unchanged.
        """
        exponents = []
        if self.minimum_exponent is not None:
            exponents.append(self.minimum_exponent)
        if self.maximum_figures is not None:
            if decade is None:
                # XXX Better heuristic for this; make this configurable.
                decade = 0
            exponents.append(decade + 1 - self.maximum_figures)
        return max(exponents, default=None)


def round_for_format(
    x: Any, *, format: TargetFormat, mode: RoundingMode = TIES_TO_EVEN
) -> IntermediateForm:
    # Preround if necessary.
    # Shouldn't matter if decade(x) is an underestimate - we just end up computing more
    # digits than necessary. In effect, we're saying that we know that x >= 10**d.

    # We _do_ assume that target_exponent is increasing with increasing decade.
    decade_x = None if is_zero(x) else decade(x)
    target_exponent = format.target_exponent(decade_x)
    prerounded = preround(x, target_exponent)

    actual_target_exponent = format.target_exponent(prerounded.decade)
    assert (
        target_exponent is None
        or actual_target_exponent is not None
        and actual_target_exponent >= target_exponent
    )

    if actual_target_exponent is None:
        return prerounded

    result = prerounded.round(actual_target_exponent, mode)

    # Adjust in the case that rounding has changed the decade.
    if format.maximum_figures is not None:
        result = result.nudge(format.maximum_figures)

    return result


class TestRoundForFormat(unittest.TestCase):
    def test_minimum_exponent(self) -> None:
        format = TargetFormat(minimum_exponent=-3)

        # Pairs (value, mode, expected)
        test_values = [
            (3.14159, TIES_TO_EVEN, "3.142"),
            (3.14159, TO_ZERO, "3.141"),
            (9.9999, TIES_TO_EVEN, "10.000"),
            (0.0, TIES_TO_EVEN, "0.000"),
            (-0.0, TIES_TO_EVEN, "-0.000"),
            (0.0, TO_ZERO, "0.000"),
            (-0.0, TO_ZERO, "-0.000"),
            (0.0, TO_AWAY, "0.000"),
            (-0.0, TO_AWAY, "-0.000"),
        ]

        for unrounded, mode, expected in test_values:
            with self.subTest(unrounded=unrounded, mode=mode):
                rounded = round_for_format(unrounded, format=format, mode=mode)
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

    def test_maximum_figures(self) -> None:
        format = TargetFormat(maximum_figures=3)

        # Pairs (value, mode, expected)
        test_values = [
            (3.14159, TIES_TO_EVEN, "3.14"),
            (3.14159, TO_ZERO, "3.14"),
            (3.14159, TO_AWAY, "3.15"),
            (12345.6, TIES_TO_EVEN, "123e2"),
            (0.00098765, TIES_TO_EVEN, "988e-6"),
            (0.00098765, TO_ZERO, "987e-6"),
            # Check that exponent gets bumped down where necessary
            (9.99612, TIES_TO_EVEN, "10.0"),
            # Small integers
            (1.0, TIES_TO_EVEN, "1.00"),
            (2.0, TIES_TO_EVEN, "2.00"),
            (3.0, TIES_TO_EVEN, "3.00"),
            (-1.0, TIES_TO_EVEN, "-1.00"),
            (-2.0, TIES_TO_EVEN, "-2.00"),
            # Zeros; default behaviour is to use the same exponent that other small
            # integers would use.
            (0.0, TIES_TO_EVEN, "0.00"),
            (-0.0, TIES_TO_EVEN, "-0.00"),
            # Some tiny values
            (1e-300, TIES_TO_EVEN, "1.00e-300"),
        ]

        for unrounded, mode, expected in test_values:
            with self.subTest(unrounded=unrounded, mode=mode):
                rounded = round_for_format(unrounded, format=format, mode=mode)
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

    def test_minimum_exponent_and_maximum_figures(self) -> None:
        format = TargetFormat(maximum_figures=4, minimum_exponent=-2)

        # Pairs (value, mode, expected)
        test_values = [
            (3.14159, TIES_TO_EVEN, "3.14"),
            (23.14159, TIES_TO_EVEN, "23.14"),
            (123.14159, TIES_TO_EVEN, "123.1"),
            (6123.14159, TIES_TO_EVEN, "6123"),
            # Zeros: constrained by minimum exponent.
            (0.0, TIES_TO_EVEN, "0.00"),
            (-0.0, TIES_TO_EVEN, "-0.00"),
            # Near zero
            (0.006, TIES_TO_EVEN, "0.01"),
            (0.004, TIES_TO_EVEN, "0.00"),
            (0.0004, TIES_TO_EVEN, "0.00"),
            (4e-10, TIES_TO_EVEN, "0.00"),
            (-0.004, TIES_TO_EVEN, "-0.00"),
        ]

        for unrounded, mode, expected in test_values:
            with self.subTest(unrounded=unrounded, mode=mode):
                rounded = round_for_format(unrounded, format=format, mode=mode)
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

    def test_neither_minimum_exponent_nor_maximum_figures(self) -> None:
        format = TargetFormat()

        test_values = [
            (1.0, TIES_TO_EVEN, "1"),
            (fractions.Fraction(3, 8), TIES_TO_EVEN, "0.375"),
            (fractions.Fraction(3, 40), TIES_TO_EVEN, "0.075"),
            (fractions.Fraction(3, 125), TIES_TO_EVEN, "0.024"),
            (1230, TIES_TO_EVEN, "1230"),
            (decimal.Decimal("123e4"), TIES_TO_EVEN, "123e4"),
        ]

        for unrounded, mode, expected in test_values:
            with self.subTest(unrounded=unrounded, mode=mode):
                rounded = round_for_format(unrounded, format=format, mode=mode)
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

        bad_values = [
            fractions.Fraction(1, 3),
            fractions.Fraction(1, 300),
        ]
        for value in bad_values:
            with self.assertRaises(ValueError):
                round_for_format(value, format=format, mode=TIES_TO_EVEN)

    def test__smallest_ten_power_multiple(self) -> None:
        for etwo in range(100):
            for efive in range(100):
                d = 2**etwo * 5**efive
                self.assertEqual(_smallest_ten_power_multiple(d), max(etwo, efive))

        bad = [n for n in range(2, 1000) if math.gcd(n, 10) == 1]

        for etwo in range(10):
            for efive in range(10):
                for b in bad:
                    d = b * 2**etwo * 5**efive
                    with self.assertRaises(ValueError):
                        _smallest_ten_power_multiple(d)

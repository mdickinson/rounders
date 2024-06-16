"""Tests for round_for_format."""

# To do

# XXX To do: rewire round_to_figures to use this function, so that
#     we can benefit from existing tests.
# XXX Decide on signature and preferred calling pattern for IntermediateForm.round
#     - should we always pass by position?
# XXX Rethink IntermediateForm.__repr__.
# XXX Support keeping the extra zero in the case where we round up to the next
#     power of 10.
# XXX Think about exponent preservation (e.g., for Decimal inputs); what should
#     rounding do?
# XXX Make _smallest_ten_power_multiple more efficient - once we've eliminated
#     powers of two, all we need to do is determine whether the value is a power of
#     five, and if so what its exponent is. The order of 5 modulo 1024 is 256, so
#     a lookup table based on the last ten bits (or even bits 2 through 9 inclusive)
#     could be used. That then leaves a power of 5**256 ...
# XXX Consider format flag requiring particular exponent for zero. Or perhaps
#     just a minimum exponent for zero? Maximum exponent? (Ideally, we want for
#     example a decimal zero to keep its exponent.)
# XXX Make the target decade for zero configurable in TargetFormat.
# XXX When the target format has unsigned zero, allow specifying the sign character
#     to use for zero.
# XXX Rename 'round_for_format' to 'round_to_format'?
# XXX Formatting of infinities and nans?
# XXX Reorganize: group overloads together?
#     Architecture:
#     - Overloads need to know about generics, IntermediateForm
#     - Main exports need the overloads
#     - Don't we end up with circular import problems? Possibly not.
# XXX Rework so that we're not using the decimal type anywhere outside the overloads
#     (except perhaps in dedicated end-to-end tests)
# XXX Add overloads for IntermediateForm, so that we can easily use it in tests
#     in place of decimal.Decimal. (preround would simply return the value unchanged)

# Doing

# Done

# XXX Fix typing issues.
# XXX Add support for suppressing sign of zero.
# XXX Consider making unsigned zero the default.
#     (Considered, but we're not going to do it.)
# XXX Move key classes and functions to their own homes.
# XXX Consolidate: use round_for_format in format.
# XXX Don't use Decimal in from_str
# XXX Test case where prerounding rounds a nonzero value to zero, so that the
#     original value has a valid decade but the prerounded value does not.
# XXX Consider implementing TargetFormat.__contains__ (possibly as a synonym for
#     is_representable).
# XXX Determine exponent to show for zeros.
# XXX Remove tests for _smallest_ten_power_multiple; check coverage.
# XXX Allow decade to be a lower bound. If it's too small, the only effect is that we do
#     extra work.
# XXX Move decade computation for IntermediateForm to an overload for IntermediateForm.
#     Or possibly a method on IntermediateForm. Or both.

import decimal
import fractions
import unittest

from rounders.format import TargetFormat, round_for_format
from rounders.intermediate import IntermediateForm
from rounders.modes import TIES_TO_EVEN, TO_AWAY, TO_ZERO


class TestRoundForFormat(unittest.TestCase):
    """Tests for round_for_format."""

    def test_minimum_exponent(self) -> None:
        format = TargetFormat(minimum_exponent=-3)
        zero_exponent = -3

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
                rounded = round_for_format(
                    unrounded, format=format, mode=mode, zero_exponent=zero_exponent
                )
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

    def test_maximum_figures(self) -> None:
        format = TargetFormat(maximum_figures=3)
        zero_exponent = -2

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
                rounded = round_for_format(
                    unrounded, format=format, mode=mode, zero_exponent=zero_exponent
                )
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

    def test_minimum_exponent_and_maximum_figures(self) -> None:
        format = TargetFormat(maximum_figures=4, minimum_exponent=-2)
        zero_exponent = -2

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
                rounded = round_for_format(
                    unrounded, format=format, mode=mode, zero_exponent=zero_exponent
                )
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

    def test_neither_minimum_exponent_nor_maximum_figures(self) -> None:
        format = TargetFormat()
        zero_exponent = None

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
                rounded = round_for_format(
                    unrounded, format=format, mode=mode, zero_exponent=zero_exponent
                )
                self.assertEqual(rounded, IntermediateForm.from_str(expected))

        bad_values = [
            fractions.Fraction(1, 3),
            fractions.Fraction(1, 300),
        ]
        for value in bad_values:
            with self.assertRaises(ValueError):
                round_for_format(
                    value, format=format, mode=TIES_TO_EVEN, zero_exponent=zero_exponent
                )

    def test_no_negative_zero(self) -> None:
        format = TargetFormat(signed_zero=False, minimum_exponent=-3)
        self.assertEqual(
            round_for_format(3e-4, format=format, zero_exponent=-3),
            IntermediateForm.from_str("0e-3"),
        )
        self.assertEqual(
            round_for_format(-3e-4, format=format, zero_exponent=-3),
            IntermediateForm.from_str("0e-3"),
        )
        self.assertEqual(
            round_for_format(-0.0, format=format, zero_exponent=-3),
            IntermediateForm.from_str("0e-3"),
        )

        format = TargetFormat(signed_zero=False)
        self.assertEqual(
            round_for_format(-0.0, format=format, zero_exponent=None),
            IntermediateForm.from_str("0"),
        )

        format = TargetFormat(signed_zero=True, minimum_exponent=-3)
        self.assertEqual(
            round_for_format(3e-4, format=format, zero_exponent=-3),
            IntermediateForm.from_str("0e-3"),
        )
        self.assertEqual(
            round_for_format(-3e-4, format=format, zero_exponent=-3),
            IntermediateForm.from_str("-0e-3"),
        )
        self.assertEqual(
            round_for_format(-0.0, format=format, zero_exponent=-3),
            IntermediateForm.from_str("-0e-3"),
        )

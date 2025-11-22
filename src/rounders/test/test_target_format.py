"""Tests for the TargetFormat data class."""

import unittest

from rounders.target_format import TargetFormat


class TestTargetFormat(unittest.TestCase):
    """Tests for the TargetFormat data class."""

    def test_minimum_exponent_for_decade_with_figures_and_exponent_bounds(self) -> None:
        # Given
        format = TargetFormat(minimum_exponent=-10, maximum_figures=3)

        # Then
        self.assertEqual(format.minimum_exponent_for_decade(-19), -10)
        self.assertEqual(format.minimum_exponent_for_decade(-9), -10)
        self.assertEqual(format.minimum_exponent_for_decade(-8), -10)
        self.assertEqual(format.minimum_exponent_for_decade(0), -2)
        self.assertEqual(format.minimum_exponent_for_decade(3), 1)

    def test_minimum_exponent_for_decade_with_figures_bound(self) -> None:
        # Given
        format = TargetFormat(maximum_figures=3)

        # Then
        self.assertEqual(format.minimum_exponent_for_decade(-19), -21)
        self.assertEqual(format.minimum_exponent_for_decade(-9), -11)
        self.assertEqual(format.minimum_exponent_for_decade(-8), -10)
        self.assertEqual(format.minimum_exponent_for_decade(0), -2)
        self.assertEqual(format.minimum_exponent_for_decade(3), 1)

    def test_minimum_exponent_for_decade_with_exponent_bound(self) -> None:
        # Given
        format = TargetFormat(minimum_exponent=-10)

        # Then
        self.assertEqual(format.minimum_exponent_for_decade(-19), -10)
        self.assertEqual(format.minimum_exponent_for_decade(-9), -10)
        self.assertEqual(format.minimum_exponent_for_decade(-8), -10)
        self.assertEqual(format.minimum_exponent_for_decade(0), -10)
        self.assertEqual(format.minimum_exponent_for_decade(3), -10)

    def test_minimum_exponent_for_decade_with_no_bounds(self) -> None:
        # Given
        format = TargetFormat()

        # Then
        self.assertIsNone(format.minimum_exponent_for_decade(-19))
        self.assertIsNone(format.minimum_exponent_for_decade(-9))
        self.assertIsNone(format.minimum_exponent_for_decade(-8))
        self.assertIsNone(format.minimum_exponent_for_decade(0))
        self.assertIsNone(format.minimum_exponent_for_decade(3))

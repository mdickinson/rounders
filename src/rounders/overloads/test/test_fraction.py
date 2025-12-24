"""Tests for Fraction overloads."""

import fractions
import unittest

from rounders.generics import preround
from rounders.intermediate_form import IntermediateForm
from rounders.overloads.test.support import truncate_and_remainder


class TestFractionOverloads(unittest.TestCase):
    """Test that preround works for Fraction objects."""

    def test_preround_no_exponent_convertible(self) -> None:
        # Triples (numerator, denominator, expected IntermediateForm as a string)
        test_values: list[tuple[int, int, str]] = [
            (-1000, 1, "-1000"),
            (-10, 1, "-10"),
            (-1, 1, "-1"),
            (0, 1, "0"),
            (1, 1, "1"),
            (5, 1, "5"),
            (10, 1, "10"),
            (73, 1, "73"),
            (20, 1, "20"),
            (50, 1, "50"),
            (100, 1, "100"),
            (1, 10, "0.1"),
            (1, 2, "0.5"),
            (3, 4, "0.75"),
            (2, 5, "0.4"),
            (5, 2, "2.5"),
            (1, 16, "0.0625"),
            (1, 5**4, "0.0016"),
            (1234, 10000, "0.1234"),
        ]

        for numerator, denominator, expected_str in test_values:
            with self.subTest(numerator=numerator, denominator=denominator):
                value = fractions.Fraction(numerator, denominator)
                expected = IntermediateForm.from_str(expected_str)
                self.assertEqual(preround(value, None), expected)

    def test_preround_with_no_exponent_not_convertible(self) -> None:
        test_values: list[fractions.Fraction] = [
            fractions.Fraction(1, 3),
            fractions.Fraction(2, 3),
            fractions.Fraction(1, 6),
            fractions.Fraction(1, 7),
            fractions.Fraction(10, 3),
            fractions.Fraction(123, 700),
        ]

        for value in test_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    preround(value, None)

    def test_preround_with_exponent(self) -> None:
        # Triples (numerator, denominator, exponent, expected IntermediateForm as a string)
        test_values: list[tuple[int, int, int, str]] = [
            (-1000, 1, 0, "-1000"),
            (-10, 1, 0, "-10"),
            (-1, 1, 0, "-1"),
            (0, 1, 0, "0"),
            (1, 1, 0, "1"),
            (5, 1, 0, "5"),
            (10, 1, 0, "10"),
            (73, 1, 0, "73"),
            (20, 1, 0, "20"),
            (50, 1, 0, "50"),
            (100, 1, 0, "100"),
            (1, 10, -1, "0.1"),
            (1, 2, 0, "0.5"),
            (1, 2, -10, "0.5"),
            (3, 4, 0, "0.6"),
            (2, 5, -1, "0.4"),
            (5, 2, 0, "2.5"),
            (1, 16, -3, "0.0625"),
            (1, 5**4, -3, "0.0016"),
            (1234, 10000, -3, "0.1231"),

            # Inexact cases
            (1, 7, -6, "0.1428571"),
            (1, 7, -7, "0.14285711"),
            (1, 7, -8, "0.142857141"),
            (1, 7, -9, "0.1428571426"),
            (1, 7, -10, "0.14285714286"),
            (2, 3, -10, "0.66666666666"),
        ]

        for numerator, denominator, exponent, expected_str in test_values:
            with self.subTest(
                numerator=numerator,
                denominator=denominator,
                exponent=exponent,
            ):
                value = fractions.Fraction(numerator, denominator)
                expected = IntermediateForm.from_str(expected_str)
                actual = preround(value, exponent)
                self.assertEqual(
                    truncate_and_remainder(actual, exponent),
                    truncate_and_remainder(expected, exponent)
                )

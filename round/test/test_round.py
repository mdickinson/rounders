"""
Tests for functions in the 'round' module.
"""

import fractions
import math
import unittest

from round import (
    # Midpoint rounding methods
    round_ties_to_away,
    round_ties_to_zero,
    round_ties_to_plus,
    round_ties_to_minus,
    round_ties_to_even,
    round_ties_to_odd,
    # Directed rounding methods
    round_to_away,
    round_to_zero,
    round_to_plus,
    round_to_minus,
    round_to_even,
    round_to_odd,
)


#: A selection of IEEE 754 binary64 floating-point values used in a wide
#: variety of tests.
ALL_POSITIVE_TEST_VALUES = [
    *[0.25 * n for n in range(100)],  # quarter integers from 0.0 to 24.75
    4503599627370495.5,  # largest representable non-integral half integer
    float.fromhex("0x0.0000000000001p-1022"),  # smallest +ve subnormal
    float.fromhex("0x0.fffffffffffffp-1022"),  # largest +ve subnormal
    float.fromhex("0x1.fffffffffffffp-2"),  # largest value < 0.5
    float.fromhex("0x1.0000000000001p-1"),  # largest value > 0.5
    float.fromhex("0x1.fffffffffffffp+1023"),  # largest finite value
]

ALL_TEST_VALUES = [
    signed_value
    for value in ALL_POSITIVE_TEST_VALUES
    for signed_value in [-value, value]
]

#: Various subsets of the rounding functions
MIDPOINT_ROUNDING_FUNCTIONS = [
    round_ties_to_even,
    round_ties_to_odd,
    round_ties_to_away,
    round_ties_to_zero,
    round_ties_to_plus,
    round_ties_to_minus,
]

DIRECTED_ROUNDING_FUNCTIONS = [
    round_to_even,
    round_to_odd,
    round_to_away,
    round_to_zero,
    round_to_plus,
    round_to_minus,
]

ALL_ROUNDING_FUNCTIONS = MIDPOINT_ROUNDING_FUNCTIONS + DIRECTED_ROUNDING_FUNCTIONS


#: One half, as a fraction constant.
ONE_HALF = fractions.Fraction("1/2")


class TestRound(unittest.TestCase):
    def test_round_ties_to_away_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_away(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_ties_to_zero_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_zero(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_ties_to_even_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_even(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_ties_to_odd_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_odd(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_ties_to_plus_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_plus(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_ties_to_minus_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_minus(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_to_away_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -2),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, -1),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 1),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 2),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_away(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_to_zero_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -1),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, 0),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 0),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 1),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_zero(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_to_plus_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -1),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, 0),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 1),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 2),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_plus(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_to_minus_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -2),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, -1),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 0),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 1),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_minus(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_to_even_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -2),
            (-1.0, -1),
            (-0.75, 0),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 0),
            (1.0, 1),
            (1.25, 2),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_even(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_round_to_odd_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -1),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, -1),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 1),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 1),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_odd(value)
                self.assertIsInstance(actual_result, int)
                self.assertEqual(actual_result, expected_result)

    def test_all_midpoint_rounding_modes_round_to_nearest(self):
        # Difference between rounded value and original value should always
        # at most 0.5 in absolute value.
        for round_function in MIDPOINT_ROUNDING_FUNCTIONS:
            for original_value in ALL_TEST_VALUES:
                rounded_value = round_function(original_value)
                diff = fractions.Fraction(rounded_value) - fractions.Fraction(
                    original_value
                )
                self.assertLessEqual(abs(diff), ONE_HALF)

    def test_all_rounding_modes_round_to_neighbour(self):
        # Difference between rounded value and original value should always
        # be strictly less than 1.0 in absolute value.
        for round_function in ALL_ROUNDING_FUNCTIONS:
            for original_value in ALL_TEST_VALUES:
                rounded_value = round_function(original_value)
                diff = fractions.Fraction(rounded_value) - fractions.Fraction(
                    original_value
                )
                self.assertLessEqual(abs(diff), 1)

    def test_infinities(self):
        for round_function in ALL_ROUNDING_FUNCTIONS:
            for infinity in [math.inf, -math.inf]:
                with self.assertRaises(ValueError):
                    round_function(infinity)

    def test_nan(self):
        for round_function in ALL_ROUNDING_FUNCTIONS:
            with self.assertRaises(ValueError):
                round_function(math.nan)

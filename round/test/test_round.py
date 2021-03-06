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


def sign_bit(x):
    """
    Sign bit of a float: True if negative, False if positive.
    """
    return math.copysign(1.0, x) < 0


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

    def test_round_to_decimal_places(self):
        self.assertFloatsIdentical(round_ties_to_away(66.15, -2), 100.0)
        self.assertFloatsIdentical(round_ties_to_away(66.15, -1), 70.0)
        self.assertFloatsIdentical(round_ties_to_away(2.37, -2), 0.0)
        self.assertFloatsIdentical(round_ties_to_away(2.37, -1), 0.0)
        self.assertFloatsIdentical(round_ties_to_away(-2.37, -1), -0.0)
        self.assertFloatsIdentical(round_ties_to_away(2.37, 0), 2.0)
        self.assertFloatsIdentical(round_ties_to_away(2.37, 1), 2.4)
        self.assertFloatsIdentical(round_ties_to_away(2.37, 2), 2.37)
        self.assertFloatsIdentical(round_ties_to_away(2.553, 2), 2.55)

        self.assertFloatsIdentical(round_ties_to_away(0.0, 1), 0.0)
        self.assertFloatsIdentical(round_ties_to_away(-0.0, 1), -0.0)

    def test_exact_halfway_cases(self):
        self.assertFloatsIdentical(round_ties_to_zero(2.5, 0), 2.0)
        self.assertFloatsIdentical(round_ties_to_away(2.5, 0), 3.0)
        self.assertFloatsIdentical(round_ties_to_plus(2.5, 0), 3.0)
        self.assertFloatsIdentical(round_ties_to_minus(2.5, 0), 2.0)
        self.assertFloatsIdentical(round_ties_to_even(2.5, 0), 2.0)
        self.assertFloatsIdentical(round_ties_to_odd(2.5, 0), 3.0)

        self.assertFloatsIdentical(round_ties_to_zero(3.5, 0), 3.0)
        self.assertFloatsIdentical(round_ties_to_away(3.5, 0), 4.0)
        self.assertFloatsIdentical(round_ties_to_plus(3.5, 0), 4.0)
        self.assertFloatsIdentical(round_ties_to_minus(3.5, 0), 3.0)
        self.assertFloatsIdentical(round_ties_to_even(3.5, 0), 4.0)
        self.assertFloatsIdentical(round_ties_to_odd(3.5, 0), 3.0)

        self.assertFloatsIdentical(round_ties_to_zero(-2.5, 0), -2.0)
        self.assertFloatsIdentical(round_ties_to_away(-2.5, 0), -3.0)
        self.assertFloatsIdentical(round_ties_to_plus(-2.5, 0), -2.0)
        self.assertFloatsIdentical(round_ties_to_minus(-2.5, 0), -3.0)
        self.assertFloatsIdentical(round_ties_to_even(-2.5, 0), -2.0)
        self.assertFloatsIdentical(round_ties_to_odd(-2.5, 0), -3.0)

        self.assertFloatsIdentical(round_ties_to_zero(-3.5, 0), -3.0)
        self.assertFloatsIdentical(round_ties_to_away(-3.5, 0), -4.0)
        self.assertFloatsIdentical(round_ties_to_plus(-3.5, 0), -3.0)
        self.assertFloatsIdentical(round_ties_to_minus(-3.5, 0), -4.0)
        self.assertFloatsIdentical(round_ties_to_even(-3.5, 0), -4.0)
        self.assertFloatsIdentical(round_ties_to_odd(-3.5, 0), -3.0)

    def test_special_floats(self):
        for rounding_function in ALL_ROUNDING_FUNCTIONS:
            with self.subTest(rounding_function=rounding_function):
                self.assertFloatsIdentical(rounding_function(math.nan, 0), math.nan)
                self.assertFloatsIdentical(rounding_function(math.inf, 0), math.inf)
                self.assertFloatsIdentical(rounding_function(-math.inf, 0), -math.inf)

    def test_round_finite_to_overflow(self):
        for rounding_function in MIDPOINT_ROUNDING_FUNCTIONS:
            with self.subTest(rounding_function=rounding_function):
                with self.assertRaises(OverflowError):
                    rounding_function(1.7e308, -308)
                with self.assertRaises(OverflowError):
                    rounding_function(-1.7e308, -308)

    def test_round_integers_places_none(self):
        test_values = [*range(-10, 10), *range(10 ** 100 - 10, 10 ** 100 + 10)]
        for rounding_function in MIDPOINT_ROUNDING_FUNCTIONS:
            for value in test_values:
                rounded_value = rounding_function(value)
                self.assertIsInstance(rounded_value, int)
                self.assertEqual(rounded_value, value)

    def assertFloatsIdentical(self, first, second):
        self.assertIsInstance(first, float)
        self.assertIsInstance(second, float)

        if math.isnan(first) and math.isnan(second):
            return

        self.assertEqual(first, second)
        if first == 0.0:
            self.assertEqual(sign_bit(first), sign_bit(second))

"""Tests for the float overloads."""

import decimal
import unittest

from rounders.generics import preround
from rounders.intermediate_form import IntermediateForm
from rounders.overloads.test.support import truncate_and_remainder


class TestFloatOverloads(unittest.TestCase):
    """Tests for the float overloads."""

    def test_preround_infinity_and_nan(self) -> None:
        """Test that preround raises for infinity and NaN."""
        for value in [float("inf"), float("-inf"), float("nan")]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    preround(value, 0)

    def test_preround_finite(self) -> None:
        # Test values: input, exponent for prerounding, expected result as a string
        test_values: list[tuple[float, int | None, str]] = [
            # Small integers
            (-2.0, 0, "-2"),
            (-1.0, 0, "-1"),
            (-0.0, 0, "-0"),
            (0.0, 0, "0"),
            (1.0, 0, "1"),
            (2.0, 0, "2"),
            (10.0, 0, "10"),
            (1000.0, 0, "1000"),
            (2.0, -1000, "2"),
            (2.0, -3, "2"),
            (2.0, -1, "2"),
            (2.0, 1, "1"),
            (2.0, 2, "1"),
            (2.0, 10, "1"),
            (10.0, -1, "10"),
            (10.0, 1, "1e1"),
            # Fractions
            (0.5, -10, "0.5"),
            (0.5, 0, "0.5"),
            # Tiny
            (5e-324, -10, "1e-11"),
            # Huge
            (float.fromhex("0x1p+1023"), -10, f"{2**1023}"),
            # No exponent
            (1.23456789, None, str(decimal.Decimal(1.23456789)).lower()),
            (123, None, "123"),
            (100, None, "100"),
            (1.2e10, None, str(decimal.Decimal(1.2e10)).lower()),
            (1.2e-10, None, str(decimal.Decimal(1.2e-10)).lower()),
        ]

        for value, exponent, expected_str in test_values:
            with self.subTest(value=value, exponent=exponent):
                expected = IntermediateForm.from_str(expected_str)
                actual = preround(value, exponent)
                self.assertEqual(
                    truncate_and_remainder(actual, exponent),
                    truncate_and_remainder(expected, exponent),
                )

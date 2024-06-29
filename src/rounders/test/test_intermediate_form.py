"""Tests for the IntermediateForm class."""

import math
import unittest

from rounders.intermediate_form import IntermediateForm


class TestIntermediateForm(unittest.TestCase):
    """Tests for the IntermediateForm class."""

    def test_from_str(self) -> None:
        # Tuples (input, sign, significand, exponent)
        cases = [
            ("2e3", 0, 2, 3),
            # Negative value
            ("-2e3", 1, 2, 3),
            # Decimal point in significand
            ("1.234e3", 0, 1234, 0),
            ("0.0001e-3", 0, 1, -7),
            # Safeguard against converting fracpart to an int
            ("1.0234e3", 0, 10234, -1),
            # Negative sign on exponent
            ("78e-3", 0, 78, -3),
            # No exponent
            ("1.234", 0, 1234, -3),
            # Zeros
            ("0e0", 0, 0, 0),
            ("-0e0", 1, 0, 0),
            ("000e0", 0, 0, 0),
            ("000e-3", 0, 0, -3),
            ("-0.000e12", 1, 0, 9),
        ]

        for s, sign, significand, exponent in cases:
            with self.subTest(s=s):
                self.assertEqual(
                    IntermediateForm.from_str(s),
                    IntermediateForm(
                        sign=sign,
                        significand=significand,
                        exponent=exponent,
                    ),
                )

    def test_from_signed_fraction_exponent_none(self) -> None:
        # triples (numerator, denominator, expected result)
        cases = [
            (1, 1, "1"),
            (1, 5, "0.2"),
            (1, 25, "0.04"),
            (1, 2, "0.5"),
            (1, 4, "0.25"),
            (1, 10, "0.1"),
            (1, 40, "0.025"),
        ]
        for numerator, denominator, expected_result in cases:
            # Double check that our test cases satisfy the preconditions
            self.assertEqual(math.gcd(numerator, denominator), 1)
            with self.subTest(numerator=numerator, denominator=denominator):
                self.assertEqual(
                    IntermediateForm.from_signed_fraction(
                        sign=0,
                        numerator=numerator,
                        denominator=denominator,
                        exponent=None,
                    ),
                    IntermediateForm.from_str(expected_result),
                )

    def test_from_signed_fraction_exponent_none_invalid_cases(self) -> None:
        # pairs (numerator, denominator)
        cases = [
            (1, 3),
            (1, 7),
            (1, 6),
            (1, 15),
            (1, 30),
        ]
        for numerator, denominator in cases:
            # Double check that our test cases satisfy the preconditions
            self.assertEqual(math.gcd(numerator, denominator), 1)
            with self.subTest(numerator=numerator, denominator=denominator):
                with self.assertRaises(ValueError):
                    IntermediateForm.from_signed_fraction(
                        sign=0,
                        numerator=numerator,
                        denominator=denominator,
                        exponent=None,
                    )

    def test_is_zero(self) -> None:
        self.assertTrue(IntermediateForm.from_str("0").is_zero())
        self.assertTrue(IntermediateForm.from_str("0e10").is_zero())
        self.assertTrue(IntermediateForm.from_str("0e-10").is_zero())
        self.assertTrue(IntermediateForm.from_str("-0").is_zero())
        self.assertTrue(IntermediateForm.from_str("-0e10").is_zero())
        self.assertTrue(IntermediateForm.from_str("-0e-10").is_zero())

        self.assertFalse(IntermediateForm.from_str("1.23").is_zero())
        self.assertFalse(IntermediateForm.from_str("-1.23").is_zero())

    def test_trim(self) -> None:
        # Triples (input, figures, result)
        test_cases = [
            ("1.230", 3, "1.23"),
            ("0.0001230", 3, "0.000123"),
            ("1230", 3, "123e1"),
            ("1.2", 3, "1.2"),
            ("1.200", 3, "1.20"),
            ("1.2000", 3, "1.20"),
            ("1.2000000", 3, "1.20"),
            ("0.0000", 3, "0.0000"),
        ]
        for input_str, figures, expected_result_str in test_cases:
            with self.subTest(input=input_str, figures=figures):
                input = IntermediateForm.from_str(input_str)
                expected_result = IntermediateForm.from_str(expected_result_str)
                self.assertEqual(input.trim(figures), expected_result)

    def test_trim_invalid(self) -> None:
        # Pairs (input, figures)
        test_cases = [
            ("1.234", 3),
            ("1.2345", 3),
            ("1", 0),
        ]
        for input_str, figures in test_cases:
            with self.subTest(input=input_str, figures=figures):
                input = IntermediateForm.from_str(input_str)
                with self.assertRaises(ValueError):
                    input.trim(figures)

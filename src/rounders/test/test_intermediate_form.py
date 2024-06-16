"""Tests for the IntermediateForm class."""

import math
import unittest

from rounders.intermediate import IntermediateForm


class TestIntermediateForm(unittest.TestCase):
    def test_from_signed_fraction_exponent_none(self):
        # triples (numerator, denominator, expected result)
        cases = [
            (1, 5, "0.2"),
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
                    IntermediateForm.from_str(expected_result)
                )

    def test_from_signed_fraction_exponent_none_invalid_cases(self):
        # TBD
        pass

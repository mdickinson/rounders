"""Tests for the IntermediateForm class."""

import unittest

from rounders.intermediate import IntermediateForm


class TestIntermediateForm(unittest.TestCase):
    """Tests for the IntermediateForm class."""

    def test_from_str(self):
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

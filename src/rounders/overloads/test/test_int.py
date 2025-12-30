"""Tests for the int overloads."""

import unittest


class TestIntOverloads(unittest.TestCase):
    """Tests for the int overloads."""

    def test_preround(self) -> None:
        """Test that preround works for exact integers."""
        from rounders.generics import preround
        from rounders.intermediate_form import IntermediateForm

        test_values: list[int] = [
            -1000,
            -10,
            -1,
            0,
            1,
            5,
            10,
            73,
            1000,
            123456789012345678901234567890,
        ]

        for value in test_values:
            with self.subTest(value=value):
                expected = IntermediateForm(
                    sign=0 if value >= 0 else 1,
                    significand=abs(value),
                    exponent=0,
                )
                self.assertEqual(preround(value, None), expected)
                self.assertEqual(preround(value, -10), expected)
                self.assertEqual(preround(value, 0), expected)
                self.assertEqual(preround(value, 10), expected)

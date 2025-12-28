"""Tests for the log5exact function."""

import unittest

from rounders.log5exact import exponent_from_bit_length, log5exact


class TestLog5exact(unittest.TestCase):
    """Tests for the log5exact function."""

    def test_exponent_from_bit_length(self) -> None:
        for e in range(1000):
            with self.subTest(e=e):
                self.assertEqual(exponent_from_bit_length((5**e).bit_length()), e)

    def test_exponent_from_bit_length_extreme_case(self) -> None:
        # The largest power of 5 with at most 2**64 bits is 5**7944580245325990804.
        # It has a bit length of exactly 2**64.
        self.assertEqual(exponent_from_bit_length(2**64), 7944580245325990804)

    def test_exponent_from_bit_length_small_inputs(self) -> None:
        for b in range(1000):
            with self.subTest(b=b):
                if (e := exponent_from_bit_length(b)) is not None:
                    self.assertEqual((5**e).bit_length(), b)

    def test_log5exact_small_powers_of_5(self) -> None:
        for e in range(1000):
            with self.subTest(e=e):
                self.assertEqual(log5exact(5**e), e)

    def test_log5exact_small_inputs(self) -> None:
        powers_of_five: list[tuple[int, int]] = []
        for d in range(-100, 500):
            try:
                e = log5exact(d)
            except ValueError:
                pass
            else:
                powers_of_five.append((d, e))

        self.assertEqual(powers_of_five, [(1, 0), (5, 1), (25, 2), (125, 3)])

    def test_log5exact_nearby_values(self) -> None:
        for e in range(1, 500):
            p = 5**e
            for delta in [-3, -2, -1, 1, 2, 3]:
                d = p + delta
                with self.subTest(e=e, delta=delta, d=d):
                    with self.assertRaises(ValueError):
                        log5exact(d)

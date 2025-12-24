"""Tests for the log5exact function."""

import unittest

from rounders.log5exact import log5exact


class TestLog5exact(unittest.TestCase):
    """Tests for the log5exact function."""

    def test_log5exact_small_powers_of_5(self) -> None:
        for e in range(256):
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

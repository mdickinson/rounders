"""Tests for extended formatting functionality."""

import decimal
import fractions
import unittest
from typing import List, Tuple

from rounders.format import FormatSpecification, format
from rounders.intermediate import IntermediateForm


class TestFormat(unittest.TestCase):
    """Tests for the 'format' functionality."""

    def test_format_fraction(self) -> None:
        self.assertEqual(format(fractions.Fraction(3, 7), ".3f"), "0.429")
        self.assertEqual(format(fractions.Fraction(3, 7), ".4f"), "0.4286")
        self.assertEqual(format(fractions.Fraction(3, 7), ".5f"), "0.42857")

    def test_format_general_f(self) -> None:
        # Cases that are also expected to work for the
        # built-in format.
        cases = [
            ("-0.00123", ".2f", "-0.00"),
            ("-0.0123", ".2f", "-0.01"),
            ("-0.123", ".2f", "-0.12"),
            ("-1.23", ".2f", "-1.23"),
            ("-12.3", ".2f", "-12.30"),
            ("-123", ".2f", "-123.00"),
            ("-123e1", ".2f", "-1230.00"),
            # Use of alternate form. This has an effect
            # only for zero or negative precision.
            ("1.234", "#.0f", "1."),
            ("1.234", ".0f", "1"),
            # Explicit sign specifier.
            ("1.234", "+.2f", "+1.23"),
            ("1.234", " .2f", " 1.23"),
            ("1.234", "-.2f", "1.23"),
            ("-1.234", "+.2f", "-1.23"),
            ("-1.234", " .2f", "-1.23"),
            ("-1.234", "-.2f", "-1.23"),
            ("0.001", "+.2f", "+0.00"),
            ("0.001", " .2f", " 0.00"),
            ("0.001", "-.2f", "0.00"),
            ("0.0", "+.2f", "+0.00"),
            ("0.0", " .2f", " 0.00"),
            ("0.0", "-.2f", "0.00"),
            ("-0.001", "+.2f", "-0.00"),
            ("-0.001", " .2f", "-0.00"),
            ("-0.001", "-.2f", "-0.00"),
            ("-0.0", "+.2f", "-0.00"),
            ("-0.0", " .2f", "-0.00"),
            ("-0.0", "-.2f", "-0.00"),
            # Combinations using 'z'
            ("1.234", "+z.2f", "+1.23"),
            ("1.234", " z.2f", " 1.23"),
            ("1.234", "-z.2f", "1.23"),
            ("1.234", "z.2f", "1.23"),
            ("-1.234", "+z.2f", "-1.23"),
            ("-1.234", " z.2f", "-1.23"),
            ("-1.234", "-z.2f", "-1.23"),
            ("-1.234", "z.2f", "-1.23"),
            ("0.001", "+z.2f", "+0.00"),
            ("0.001", " z.2f", " 0.00"),
            ("0.001", "-z.2f", "0.00"),
            ("0.001", "z.2f", "0.00"),
            ("0.0", "+z.2f", "+0.00"),
            ("0.0", " z.2f", " 0.00"),
            ("0.0", "-z.2f", "0.00"),
            ("0.0", "z.2f", "0.00"),
            ("-0.001", "+z.2f", "+0.00"),
            ("-0.001", " z.2f", " 0.00"),
            ("-0.001", "-z.2f", "0.00"),
            ("-0.001", "z.2f", "0.00"),
            ("-0.0", "+z.2f", "+0.00"),
            ("-0.0", " z.2f", " 0.00"),
            ("-0.0", "-z.2f", "0.00"),
            ("-0.0", "z.2f", "0.00"),
        ]
        self.check_cases(cases)

    def test_format_general_e(self) -> None:
        # Cases that are also expected to work for the
        # built-in format, for the "e" presentation type.
        cases = [
            ("-0.0012", ".2e", "-1.20e-3"),
            ("-0.00124", ".2e", "-1.24e-3"),
            ("-0.001245", ".2e", "-1.24e-3"),
            ("-0.001245", ".2ae", "-1.25e-3"),
            ("-0.0012451", ".2e", "-1.25e-3"),
            ("0.994", ".1e", "9.9e-1"),
            # Corner case where exponent is adjusted *after*
            # rounding.
            ("0.996", ".1e", "1.0e0"),
            ("3.14159", ".0e", "3e0"),
            ("3.14159", "#.0e", "3.e0"),
        ]
        self.check_cases(cases)

    def test_negative_precision(self) -> None:
        cases = [
            ("31415.926", ".-2f", "31400"),
            ("314159.26", "#.-2f", "314200."),
            ("314159.26", "#.-2Zf", "314100."),
        ]
        self.check_cases(cases)

    def test_format_rounding_mode(self) -> None:
        cases = [
            ("-0.4277", ".3Mf", "-0.428"),
            ("-0.4277", ".3Pf", "-0.427"),
            ("-0.4277", ".3Zf", "-0.427"),
            ("-0.4277", ".3Af", "-0.428"),
            ("-0.4277", ".3Ef", "-0.428"),
            ("-0.4277", ".3Of", "-0.427"),
            ("-0.4277", ".3mf", "-0.428"),
            ("-0.4277", ".3pf", "-0.428"),
            ("-0.4277", ".3zf", "-0.428"),
            ("-0.4277", ".3af", "-0.428"),
            ("-0.4277", ".3ef", "-0.428"),
            ("-0.4277", ".3of", "-0.428"),
            ("+0.4275", ".3Mf", "0.427"),
            ("+0.4275", ".3Pf", "0.428"),
            ("+0.4275", ".3Zf", "0.427"),
            ("+0.4275", ".3Af", "0.428"),
            ("+0.4275", ".3Ef", "0.428"),
            ("+0.4275", ".3Of", "0.427"),
            ("+0.4275", ".3mf", "0.427"),
            ("+0.4275", ".3pf", "0.428"),
            ("+0.4275", ".3zf", "0.427"),
            ("+0.4275", ".3af", "0.428"),
            ("+0.4275", ".3ef", "0.428"),
            ("+0.4275", ".3of", "0.427"),
            ("+0.4277", ".3Mf", "0.427"),
            ("+0.4277", ".3Pf", "0.428"),
            ("+0.4277", ".3Zf", "0.427"),
            ("+0.4277", ".3Af", "0.428"),
            ("+0.4277", ".3Ef", "0.428"),
            ("+0.4277", ".3Of", "0.427"),
            ("+0.4277", ".3mf", "0.428"),
            ("+0.4277", ".3pf", "0.428"),
            ("+0.4277", ".3zf", "0.428"),
            ("+0.4277", ".3af", "0.428"),
            ("+0.4277", ".3ef", "0.428"),
            ("+0.4277", ".3of", "0.428"),
            ("+0.4285", ".3Mf", "0.428"),
            ("+0.4285", ".3Pf", "0.429"),
            ("+0.4285", ".3Zf", "0.428"),
            ("+0.4285", ".3Af", "0.429"),
            ("+0.4285", ".3Ef", "0.428"),
            ("+0.4285", ".3Of", "0.429"),
            ("+0.4285", ".3mf", "0.428"),
            ("+0.4285", ".3pf", "0.429"),
            ("+0.4285", ".3zf", "0.428"),
            ("+0.4285", ".3af", "0.429"),
            ("+0.4285", ".3ef", "0.428"),
            ("+0.4285", ".3of", "0.429"),
            ("+0.4287", ".3Mf", "0.428"),
            ("+0.4287", ".3Pf", "0.429"),
            ("+0.4287", ".3Zf", "0.428"),
            ("+0.4287", ".3Af", "0.429"),
            ("+0.4287", ".3Ef", "0.428"),
            ("+0.4287", ".3Of", "0.429"),
            ("+0.4287", ".3mf", "0.429"),
            ("+0.4287", ".3pf", "0.429"),
            ("+0.4287", ".3zf", "0.429"),
            ("+0.4287", ".3af", "0.429"),
            ("+0.4287", ".3ef", "0.429"),
            ("+0.4287", ".3of", "0.429"),
            ("+0.4200", ".3Rf", "0.420"),
            ("+0.4210", ".3Rf", "0.421"),
            ("+0.4220", ".3Rf", "0.422"),
            ("+0.4230", ".3Rf", "0.423"),
            ("+0.4240", ".3Rf", "0.424"),
            ("+0.4250", ".3Rf", "0.425"),
            ("+0.4260", ".3Rf", "0.426"),
            ("+0.4270", ".3Rf", "0.427"),
            ("+0.4280", ".3Rf", "0.428"),
            ("+0.4290", ".3Rf", "0.429"),
            ("+0.4202", ".3Rf", "0.421"),
            ("+0.4212", ".3Rf", "0.421"),
            ("+0.4222", ".3Rf", "0.422"),
            ("+0.4232", ".3Rf", "0.423"),
            ("+0.4242", ".3Rf", "0.424"),
            ("+0.4252", ".3Rf", "0.426"),
            ("+0.4262", ".3Rf", "0.426"),
            ("+0.4272", ".3Rf", "0.427"),
            ("+0.4282", ".3Rf", "0.428"),
            ("+0.4292", ".3Rf", "0.429"),
            ("+0.4208", ".3Rf", "0.421"),
            ("+0.4218", ".3Rf", "0.421"),
            ("+0.4228", ".3Rf", "0.422"),
            ("+0.4238", ".3Rf", "0.423"),
            ("+0.4248", ".3Rf", "0.424"),
            ("+0.4258", ".3Rf", "0.426"),
            ("+0.4268", ".3Rf", "0.426"),
            ("+0.4278", ".3Rf", "0.427"),
            ("+0.4288", ".3Rf", "0.428"),
            ("+0.4298", ".3Rf", "0.429"),
        ]
        self.check_cases(cases)

    def check_cases(self, cases: List[Tuple[str, str, str]]) -> None:
        for case in cases:
            value_str, pattern, expected_result = case
            with self.subTest(case=case):
                value = decimal.Decimal(value_str)
                actual_result = format(value, pattern)
                self.assertEqual(actual_result, expected_result)


class TestFormatFromSpecification(unittest.TestCase):
    """Tests for conversion of a format string to a FormatSpecification."""

    def test_min_digits_before_point(self) -> None:
        format_specification = FormatSpecification(
            min_digits_before_point=0,
            min_digits_after_point=1,
            places=2,
            figures=None,
        )
        self.assertEqual(
            format_specification.format(
                IntermediateForm(sign=0, significand=23, exponent=-2)
            ),
            ".23",
        )
        self.assertEqual(
            format_specification.format(
                IntermediateForm(sign=0, significand=67, exponent=-3)
            ),
            ".067",
        )

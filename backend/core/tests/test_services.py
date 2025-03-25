"""Test services."""

from decimal import Decimal

from django.test import TestCase
from djmoney.money import Money

from ..services import to_money


class ToMoneyFunctionTest(TestCase):
    """Tests for the to_money function."""

    def test_to_money_with_decimal(self):
        """Test conversion of Decimal to Money."""
        amount = Decimal("100.50")
        result = to_money(amount)
        self.assertIsInstance(result, Money)
        self.assertEqual(result, Money(Decimal("100.50"), "USD"))

    def test_to_money_with_int(self):
        """Test conversion of int to Money."""
        amount = 200
        result = to_money(amount)
        self.assertIsInstance(result, Money)
        self.assertEqual(result, Money(200, "USD"))

    def test_to_money_with_float(self):
        """Test conversion of float to Money."""
        amount = 50.75
        result = to_money(amount)
        self.assertIsInstance(result, Money)
        self.assertEqual(result, Money(Decimal("50.75"), "USD"))

    def test_to_money_with_money_instance(self):
        """Test that Money instance is returned as-is."""
        amount = Money(Decimal("300.00"), "USD")
        result = to_money(amount)
        self.assertIsInstance(result, Money)
        self.assertEqual(result, amount)

    def test_to_money_with_invalid_type_raises_value_error(self):
        """Test that invalid types raise ValueError."""
        invalid_values = ["invalid", None, {"value": 100}, [10, 20], object()]

        for value in invalid_values:
            with self.assertRaises(ValueError) as context:
                to_money(value)

            self.assertIn("Invalid type for amount:", str(context.exception))

"""Core services."""

from decimal import Decimal
from typing import Union

from djmoney.money import Money
from typing_extensions import TypeAlias

Amount: TypeAlias = Union[Decimal, int, float, Money]
CURRENCY = "USD"


def to_money(amount: Amount, currency: str = CURRENCY) -> Money:
    """Convert amount to Money if possible or raise ValueError."""
    if isinstance(amount, (Decimal, int, float)):
        return Money(amount, CURRENCY)
    elif isinstance(amount, Money):
        return amount
    else:
        raise ValueError(f"Invalid type for amount: {type(amount)}")

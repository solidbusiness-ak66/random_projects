
import pytest

from decimal import Decimal
from cli_tracker.expense import Expense


@pytest.fixture
def sample_expense():
    """Provide a reusable expense for tests."""

    return Expense(
        id=1,
        amt =Decimal("150.50"),
        typeof ="Food",
        description="Lunch",
        date="2026-11-07",
    )

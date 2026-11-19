
import json

from decimal import Decimal, InvalidOperation
from pathlib import Path

from .expense import Expense
from .errors import StorageError, InvalidExpenseError


# Locate expenses.json relative to the project root.
DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "expenses.json"
)


def load_expenses() -> list[Expense]:
    """Load expenses from JSON and return Expense objects."""

    # If the file doesn't exist, there are no saved expenses.
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Our JSON file must contain a list.
        if not isinstance(data, list):
            raise StorageError("Expense data must be a list.")

        expenses = []

        for item in data:
            if not isinstance(item, dict):
                raise StorageError("Invalid expense record.")

            expense = Expense(
                id=item["id"],
                amt=Decimal(str(item["amt"])),
                typeof=item["typeof"],
                description=item["description"],
                date=item["date"],
            )

            expenses.append(expense)

        return expenses

    except StorageError:
        raise

    except (
        OSError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
        InvalidOperation,
        InvalidExpenseError,
    ) as error:
        raise StorageError(
            f"Unable to load expenses: {error}"
        ) from error


def save_expenses(expenses: list[Expense]) -> None:
    """Save Expense objects into the JSON file."""

    data = []

    for expense in expenses:
        expense_data = {
            "id": expense.id,
            "amt": str(expense.amt),
            "typeof": expense.typeof,
            "description": expense.description,
            "date": expense.date,
        }

        data.append(expense_data)

    try:
        # Create the data directory if it doesn't exist.
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        raise StorageError(
            f"Unable to save expenses: {error}"
        ) from error

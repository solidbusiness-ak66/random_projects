
import argparse

from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from .import storage
from .expense import Expense
from .errors import (
    InvalidExpenseError,
    ExpenseNotFoundError,
    StorageError,
)


def next_expense_id(expenses: list[Expense]) -> int:
    """Generate an ID greater than every existing expense ID."""

    return max(
        (expense.id for expense in expenses),
        default=0
    ) + 1


def add_expense(args: argparse.Namespace) -> None:
    """Create a new expense and save it."""

    try:
        amt = Decimal(args.amt)

        expenses = storage.load_expenses()

        expense = Expense(
            id=next_expense_id(expenses),
            amt=amt,
            typeof=args.typeof,
            description=args.description,
            date=args.date or date.today().isoformat(),
        )

        expenses.append(expense)

        storage.save_expenses(expenses)

        print(f"Expense added successfully. ID: {expense.id}")

    except InvalidOperation as error:
        raise InvalidExpenseError(
            "amt must be a valid decimal number."
        ) from error


def list_expenses(args: argparse.Namespace) -> None:
    """Display all saved expenses."""

    expenses = storage.load_expenses()

    if not expenses:
        print("No expenses recorded yet.")
        return

    print(
        f"{'ID':<5} {'DATE':<12} "
        f"{'typeof':<16} {'amt':>12}  DESCRIPTION"
    )

    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense.id:<5} "
            f"{expense.date:<12} "
            f"{expense.typeof:<16} "
            f"{expense.amt:>12.2f}  "
            f"{expense.description}"
        )


def delete_expense(args: argparse.Namespace) -> None:
    """Delete an expense using its ID."""

    expenses = storage.load_expenses()

    updated_expenses = [
        expense
        for expense in expenses
        if expense.id != args.id
    ]

    if len(updated_expenses) == len(expenses):
        raise ExpenseNotFoundError(
            f"No expense found with ID {args.id}."
        )

    storage.save_expenses(updated_expenses)

    print(f"Expense {args.id} deleted successfully.")


def show_total(args: argparse.Namespace) -> None:
    """Calculate total expenses, optionally filtering by month."""

    expenses = storage.load_expenses()

    if args.month:
        expenses = [
            expense
            for expense in expenses
            if expense.date.startswith(args.month)
        ]

        print(f"Total expenses for {args.month}:")

    else:
        print("Total expenses:")

    total = sum(
        (expense.amt for expense in expenses),
        Decimal("0.00")
    )

    print(f"₹{total:.2f}")
    print(f"Number of expenses: {len(expenses)}")


def validate_month(value: str) -> str:
    """Validate a month supplied in YYYY-MM format."""

    try:
        parsed = datetime.strptime(value, "%Y-%m")

        if parsed.strftime("%Y-%m") != value:
            raise ValueError

        return value

    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "Month must be in YYYY-MM format, e.g. 2026-11."
        ) from error


def build_parser() -> argparse.ArgumentParser:
    """Create the main parser and its subcommands."""

    parser = argparse.ArgumentParser(
        description="A simple command-line expense tracker."
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True
    )

    # ADD COMMAND
    add_parser = commands.add_parser(
        "add",
        help="Add a new expense."
    )

    add_parser.add_argument(
        "--amt",
        required=True,
        help="Expense amt."
    )

    add_parser.add_argument(
        "--typeof",
        required=True,
        help="Expense typeof."
    )

    add_parser.add_argument(
        "--description",
        required=True,
        help="Expense description."
    )

    add_parser.add_argument(
        "--date",
        help="Expense date in YYYY-MM-DD format."
    )

    add_parser.set_defaults(func=add_expense)

    # LIST COMMAND
    list_parser = commands.add_parser(
        "list",
        help="List all expenses."
    )

    list_parser.set_defaults(func=list_expenses)

    # DELETE COMMAND
    delete_parser = commands.add_parser(
        "delete",
        help="Delete an expense."
    )

    delete_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="ID of the expense to delete."
    )

    delete_parser.set_defaults(func=delete_expense)

    # TOTAL COMMAND
    total_parser = commands.add_parser(
        "total",
        help="Calculate total expenses."
    )

    total_parser.add_argument(
        "--month",
        type=validate_month,
        help="Filter by month using YYYY-MM."
    )

    total_parser.set_defaults(func=show_total)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse the command, execute it and handle application errors."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        args.func(args)
        return 0

    except (
        InvalidExpenseError,
        ExpenseNotFoundError,
        StorageError,
    ) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

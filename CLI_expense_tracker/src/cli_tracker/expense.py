from dataclasses import dataclass
from decimal import Decimal
from datetime import date

from .errors import InvalidExpenseError

from decimal import InvalidOperation


@dataclass
class Expense:
    id: int
    amt: Decimal
    typeof: str
    description: str
    date: str

    def __post_init__(self) -> None:

        """ 2.2 --> Validate and cleanup expense data after object creation."""

        # Validate ID
        if isinstance(self.id, bool) or not isinstance(self.id, int) or self.id <= 0:
            raise InvalidExpenseError("Expense ID must be a positive integer.")

        # Validate amt
        if not isinstance(self.amt, Decimal):
            raise InvalidExpenseError("amt must be a Decimal value.")

        if not self.amt.is_finite() or self.amt <= 0:
            raise InvalidExpenseError("amt must be greater than zero.")

        # Ensure amt has at most two decimal places
        try:
            rounded_amt = self.amt.quantize(Decimal("0.01"))
        except InvalidOperation as error:
            raise InvalidExpenseError("Invalid expense amt.") from error

        if rounded_amt != self.amt:
            raise InvalidExpenseError("amt cannot have more than two decimal places.")

        self.amt = rounded_amt

        # Validate typeof
        if not isinstance(self.typeof, str) or not self.typeof.strip():
            raise InvalidExpenseError("typeof cannot be empty.")

        self.typeof = self.typeof.strip()

        # Validate description
        if not isinstance(self.description, str) or not self.description.strip():
            raise InvalidExpenseError("Description cannot be empty.")

        self.description = self.description.strip()

        # Validate date
        if not isinstance(self.date, str):
            raise InvalidExpenseError("Date must be a string.")

        try:
            parsed_date = date.fromisoformat(self.date)
        except ValueError as error:
            raise InvalidExpenseError(
                "Date must use YYYY-MM-DD format."
            ) from error

        if parsed_date.isoformat() != self.date:
            raise InvalidExpenseError("Date must use YYYY-MM-DD format.")
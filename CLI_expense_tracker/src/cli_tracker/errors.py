class InvalidExpenseError(Exception):
    """Raised when an expense contains invalid data."""


class ExpenseNotFoundError(Exception):
    """Raised when an expense ID does not exist."""

class StorageError(Exception):
    """Raised when reading or writing expense data fails."""

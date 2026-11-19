
from decimal import Decimal

from cli_tracker import main, storage
from cli_tracker.expense import Expense


def test_add_expense(tmp_path, monkeypatch, capsys):
    """Check whether the add command saves an expense."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    result = main.main([
        "add",
        "--amt", "150",
        "--typeof", "Food",
        "--description", "Lunch",
        "--date", "2026-11-07",
    ])

    expenses = storage.load_expenses()

    assert result == 0
    assert len(expenses) == 1
    assert expenses[0].amt == Decimal("150.00")

    assert "Expense added successfully" in capsys.readouterr().out


def test_list_expenses(tmp_path, monkeypatch, sample_expense, capsys):
    """Check whether the list command displays expenses."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    storage.save_expenses([sample_expense])

    result = main.main(["list"])

    output = capsys.readouterr().out

    assert result == 0
    assert "Food" in output
    assert "150.50" in output
    assert "Lunch" in output


def test_list_empty_expenses(tmp_path, monkeypatch, capsys):
    """Check the output when no expenses exist."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    result = main.main(["list"])

    assert result == 0
    assert "No expenses recorded yet." in capsys.readouterr().out


def test_delete_expense(tmp_path, monkeypatch, sample_expense):
    """Check whether an expense can be deleted."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    storage.save_expenses([sample_expense])

    result = main.main(["delete", "--id", "1"])

    assert result == 0
    assert storage.load_expenses() == []


def test_delete_missing_expense(tmp_path, monkeypatch, capsys):
    """Check whether deleting a missing ID produces an error."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    result = main.main(["delete", "--id", "99"])

    assert result == 1
    assert "No expense found with ID 99" in capsys.readouterr().out


def test_total_expenses(tmp_path, monkeypatch, sample_expense, capsys):
    """Check whether the total command calculates correctly."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    second_expense = Expense(
        id=2,
        amt=Decimal("50.00"),
        typeof="Transport",
        description="Bus",
        date="2026-11-07",
    )

    storage.save_expenses([sample_expense, second_expense])

    result = main.main(["total"])

    output = capsys.readouterr().out

    assert result == 0
    assert "₹200.50" in output


def test_monthly_total(tmp_path, monkeypatch, capsys):
    """Check whether the monthly total filters expenses correctly."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    expenses = [
        Expense(
            id=1,
            amt=Decimal("100"),
            typeof="Food",
            description="Lunch",
            date="2026-11-01",
        ),
        Expense(
            id=2,
            amt=Decimal("200"),
            typeof="Shopping",
            description="Notebook",
            date="2026-11-05",
        ),
        Expense(
            id=3,
            amt=Decimal("500"),
            typeof="Travel",
            description="Train",
            date="2026-10-20",
        ),
        Expense(
            id=4,
            amt=Decimal("300"),
            typeof="Food",
            description="Lunch",
            date="2025-11-01",
        ),
    ]

    storage.save_expenses(expenses)

    result = main.main(["total", "--month", "2026-11"])

    output = capsys.readouterr().out

    assert result == 0
    assert "₹300.00" in output
    assert "Number of expenses: 2" in output

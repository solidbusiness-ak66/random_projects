
import json

from decimal import Decimal

import pytest

from cli_tracker import storage
from cli_tracker.expense import Expense
from cli_tracker.errors import StorageError


def test_save_expenses(tmp_path, monkeypatch, sample_expense):
    """Check whether expenses are correctly saved."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    storage.save_expenses([sample_expense])

    assert test_file.exists()

    with test_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert data[0]["id"] == 1
    assert data[0]["amt"] == "150.50"


def test_load_expenses(tmp_path, monkeypatch, sample_expense):
    """Check whether saved expenses can be loaded."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    storage.save_expenses([sample_expense])

    expenses = storage.load_expenses()

    assert len(expenses) == 1
    assert isinstance(expenses[0], Expense)
    assert expenses[0].amt == Decimal("150.50")


def test_load_missing_file(tmp_path, monkeypatch):
    """Check whether a missing file returns an empty list."""

    test_file = tmp_path / "missing.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    expenses = storage.load_expenses()

    assert expenses == []


def test_load_corrupted_json(tmp_path, monkeypatch):
    """Check whether corrupted JSON raises StorageError."""

    test_file = tmp_path / "expenses.json"

    test_file.write_text(
        "{ invalid json }",
        encoding="utf-8"
    )

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    with pytest.raises(StorageError):
        storage.load_expenses()


def test_save_empty_list(tmp_path, monkeypatch):
    """Check whether an empty expense list can be saved."""

    test_file = tmp_path / "expenses.json"

    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    storage.save_expenses([])

    assert json.loads(test_file.read_text()) == []

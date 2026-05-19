"""Tests for cronlens.history module."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from cronlens.history import (
    HistoryEntry,
    clear_history,
    load_history,
    record,
    search_history,
)


@pytest.fixture
def tmp_history(tmp_path: Path) -> Path:
    return tmp_path / "history.json"


NEXT_RUNS = [
    datetime(2024, 6, 1, 12, 0),
    datetime(2024, 6, 1, 13, 0),
]


def test_record_creates_file(tmp_history):
    record("0 * * * *", NEXT_RUNS, path=tmp_history)
    assert tmp_history.exists()


def test_record_returns_entry(tmp_history):
    entry = record("0 * * * *", NEXT_RUNS, path=tmp_history)
    assert isinstance(entry, HistoryEntry)
    assert entry.expression == "0 * * * *"
    assert len(entry.next_runs) == 2


def test_record_with_label(tmp_history):
    entry = record("*/5 * * * *", NEXT_RUNS, label="my-job", path=tmp_history)
    assert entry.label == "my-job"


def test_load_history_empty_when_no_file(tmp_history):
    assert load_history(path=tmp_history) == []


def test_load_history_returns_all_entries(tmp_history):
    record("0 * * * *", NEXT_RUNS, path=tmp_history)
    record("*/5 * * * *", NEXT_RUNS, path=tmp_history)
    entries = load_history(path=tmp_history)
    assert len(entries) == 2


def test_clear_history_returns_count(tmp_history):
    record("0 * * * *", NEXT_RUNS, path=tmp_history)
    record("0 * * * *", NEXT_RUNS, path=tmp_history)
    removed = clear_history(path=tmp_history)
    assert removed == 2


def test_clear_history_empties_file(tmp_history):
    record("0 * * * *", NEXT_RUNS, path=tmp_history)
    clear_history(path=tmp_history)
    assert load_history(path=tmp_history) == []


def test_search_history_filters_by_expression(tmp_history):
    record("0 * * * *", NEXT_RUNS, path=tmp_history)
    record("*/5 * * * *", NEXT_RUNS, path=tmp_history)
    record("0 * * * *", NEXT_RUNS, path=tmp_history)
    results = search_history("0 * * * *", path=tmp_history)
    assert len(results) == 2
    assert all(e.expression == "0 * * * *" for e in results)


def test_load_history_handles_corrupt_file(tmp_history):
    tmp_history.parent.mkdir(parents=True, exist_ok=True)
    tmp_history.write_text("not valid json")
    assert load_history(path=tmp_history) == []


def test_history_entry_iso_format(tmp_history):
    entry = record("0 12 * * *", NEXT_RUNS, path=tmp_history)
    # Should be parseable ISO strings
    for ts in entry.next_runs:
        datetime.fromisoformat(ts)
    datetime.fromisoformat(entry.queried_at)

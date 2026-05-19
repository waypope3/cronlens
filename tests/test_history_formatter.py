"""Tests for cronlens.history_formatter module."""

from __future__ import annotations

from cronlens.history import HistoryEntry
from cronlens.history_formatter import format_entry, format_history


def _make_entry(
    expression: str = "0 * * * *",
    next_runs: list | None = None,
    label: str | None = None,
) -> HistoryEntry:
    if next_runs is None:
        next_runs = ["2024-06-01T12:00:00", "2024-06-01T13:00:00"]
    return HistoryEntry(
        expression=expression,
        queried_at="2024-06-01T11:55:00",
        next_runs=next_runs,
        label=label,
    )


def test_format_entry_contains_expression():
    entry = _make_entry("*/5 * * * *")
    result = format_entry(entry, 1, color=False)
    assert "*/5 * * * *" in result


def test_format_entry_contains_index():
    entry = _make_entry()
    result = format_entry(entry, 7, color=False)
    assert "#7" in result


def test_format_entry_shows_label():
    entry = _make_entry(label="nightly-backup")
    result = format_entry(entry, 1, color=False)
    assert "nightly-backup" in result


def test_format_entry_no_label_no_parens():
    entry = _make_entry(label=None)
    result = format_entry(entry, 1, color=False)
    assert "(" not in result


def test_format_entry_shows_next_runs():
    entry = _make_entry(next_runs=["2024-06-01T12:00:00", "2024-06-01T13:00:00"])
    result = format_entry(entry, 1, color=False)
    assert "2024-06-01 12:00" in result
    assert "2024-06-01 13:00" in result


def test_format_entry_truncates_long_run_list():
    runs = [f"2024-06-01T{h:02d}:00:00" for h in range(6)]
    entry = _make_entry(next_runs=runs)
    result = format_entry(entry, 1, color=False)
    assert "and 3 more" in result


def test_format_history_empty_message():
    result = format_history([], color=False)
    assert "No history" in result


def test_format_history_multiple_entries():
    entries = [_make_entry("0 * * * *"), _make_entry("*/15 * * * *")]
    result = format_history(entries, color=False)
    assert "0 * * * *" in result
    assert "*/15 * * * *" in result


def test_format_history_separator_present():
    entries = [_make_entry(), _make_entry()]
    result = format_history(entries, color=False)
    assert "-" * 10 in result


def test_format_entry_color_codes_present():
    entry = _make_entry()
    result = format_entry(entry, 1, color=True)
    assert "\033[" in result

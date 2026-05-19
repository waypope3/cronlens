"""Tests for cronlens.diff."""

from datetime import datetime

import pytest

from cronlens.diff import compare, format_diff, ScheduleDiff


FIXED_NOW = datetime(2024, 1, 1, 0, 0)


def test_identical_expressions_have_no_diff():
    diff = compare("* * * * *", "* * * * *", from_dt=FIXED_NOW, count=5)
    assert diff.is_identical
    assert diff.only_in_a == []
    assert diff.only_in_b == []


def test_common_runs_populated_for_identical():
    diff = compare("0 * * * *", "0 * * * *", from_dt=FIXED_NOW, count=3)
    assert len(diff.common) == 3


def test_different_expressions_produce_diff():
    diff = compare("0 * * * *", "30 * * * *", from_dt=FIXED_NOW, count=5)
    assert not diff.is_identical
    assert len(diff.only_in_a) > 0
    assert len(diff.only_in_b) > 0


def test_only_in_a_not_in_b():
    diff = compare("0 * * * *", "30 * * * *", from_dt=FIXED_NOW, count=5)
    set_b = set(diff.only_in_b) | set(diff.common)
    for dt in diff.only_in_a:
        assert dt not in set_b


def test_only_in_b_not_in_a():
    diff = compare("0 * * * *", "30 * * * *", from_dt=FIXED_NOW, count=5)
    set_a = set(diff.only_in_a) | set(diff.common)
    for dt in diff.only_in_b:
        assert dt not in set_a


def test_returns_schedule_diff_instance():
    result = compare("* * * * *", "* * * * *", from_dt=FIXED_NOW, count=2)
    assert isinstance(result, ScheduleDiff)


def test_format_diff_contains_expressions():
    diff = compare("0 * * * *", "30 * * * *", from_dt=FIXED_NOW, count=3)
    text = format_diff(diff, "0 * * * *", "30 * * * *")
    assert "0 * * * *" in text
    assert "30 * * * *" in text


def test_format_diff_identical_message():
    diff = compare("* * * * *", "* * * * *", from_dt=FIXED_NOW, count=3)
    text = format_diff(diff, "* * * * *", "* * * * *")
    assert "identical" in text.lower()


def test_format_diff_lists_unique_runs():
    diff = compare("0 * * * *", "30 * * * *", from_dt=FIXED_NOW, count=3)
    text = format_diff(diff, "0 * * * *", "30 * * * *")
    assert "Unique to first" in text or "Unique to second" in text


def test_count_parameter_limits_sample_size():
    diff = compare("* * * * *", "0 * * * *", from_dt=FIXED_NOW, count=5)
    total = len(diff.common) + len(diff.only_in_a) + len(diff.only_in_b)
    # total unique datetimes across both sets must be <= 2*count
    assert total <= 10

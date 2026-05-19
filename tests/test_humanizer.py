"""Tests for the humanizer module."""

import pytest
from cronlens.parser import CronExpression
from cronlens.humanizer import humanize


def test_all_wildcards():
    expr = CronExpression.parse("* * * * *")
    assert humanize(expr) == "Every minute"


def test_specific_time():
    expr = CronExpression.parse("30 9 * * *")
    result = humanize(expr)
    assert "30" in result
    assert "9" in result


def test_hourly():
    expr = CronExpression.parse("0 * * * *")
    result = humanize(expr)
    assert "minute" in result
    assert "0" in result


def test_daily_midnight():
    expr = CronExpression.parse("0 0 * * *")
    result = humanize(expr)
    assert "0" in result


def test_with_day_of_week():
    expr = CronExpression.parse("0 9 * * 1")
    result = humanize(expr)
    assert "Monday" in result


def test_with_month():
    expr = CronExpression.parse("0 0 1 6 *")
    result = humanize(expr)
    assert "June" in result


def test_with_dom():
    expr = CronExpression.parse("0 0 15 * *")
    result = humanize(expr)
    assert "15th" in result


def test_step_minutes():
    expr = CronExpression.parse("*/15 * * * *")
    result = humanize(expr)
    assert "15" in result
    assert "minute" in result


def test_multiple_weekdays():
    expr = CronExpression.parse("0 9 * * 1,3,5")
    result = humanize(expr)
    assert "Monday" in result
    assert "Wednesday" in result
    assert "Friday" in result


def test_month_name_range():
    expr = CronExpression.parse("0 0 * 3-5 *")
    result = humanize(expr)
    assert "March" in result
    assert "May" in result

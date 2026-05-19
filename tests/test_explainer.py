"""Tests for cronlens.explainer."""

import pytest

from cronlens.parser import CronExpression
from cronlens.explainer import explain, FieldExplanation


def _parse(expr: str) -> CronExpression:
    return CronExpression.parse(expr)


def test_returns_five_fields():
    explanations = explain(_parse("* * * * *"))
    assert len(explanations) == 5


def test_field_names_in_order():
    explanations = explain(_parse("* * * * *"))
    labels = [e.field_name for e in explanations]
    assert labels == ["Minute", "Hour", "Day of Month", "Month", "Day of Week"]


def test_wildcard_description():
    explanations = explain(_parse("* * * * *"))
    for e in explanations:
        assert "every" in e.description


def test_specific_minute():
    explanations = explain(_parse("30 * * * *"))
    minute_exp = explanations[0]
    assert minute_exp.raw == "30"
    assert "30" in minute_exp.description


def test_specific_hour():
    explanations = explain(_parse("0 9 * * *"))
    hour_exp = explanations[1]
    assert "9" in hour_exp.description


def test_month_name_expansion():
    explanations = explain(_parse("0 0 1 6 *"))
    month_exp = explanations[3]
    assert "June" in month_exp.description


def test_dow_name_expansion():
    explanations = explain(_parse("0 9 * * 1"))
    dow_exp = explanations[4]
    assert "Monday" in dow_exp.description


def test_range_description():
    explanations = explain(_parse("0 9-17 * * *"))
    hour_exp = explanations[1]
    assert "9" in hour_exp.description
    assert "17" in hour_exp.description


def test_step_description():
    explanations = explain(_parse("*/15 * * * *"))
    minute_exp = explanations[0]
    assert "15" in minute_exp.description


def test_field_explanation_is_dataclass():
    explanations = explain(_parse("* * * * *"))
    assert isinstance(explanations[0], FieldExplanation)


def test_raw_preserved():
    explanations = explain(_parse("5,10,15 * * * *"))
    assert explanations[0].raw == "5,10,15"

"""Tests for cronlens.parser module."""

import pytest
from cronlens.parser import parse, ParseError, CronField, CronExpression


def test_parse_all_wildcards():
    expr = parse("* * * * *")
    assert isinstance(expr, CronExpression)
    assert expr.fields["minute"].values == list(range(0, 60))
    assert expr.fields["hour"].values == list(range(0, 24))


def test_parse_specific_values():
    expr = parse("30 9 * * *")
    assert expr.fields["minute"].values == [30]
    assert expr.fields["hour"].values == [9]


def test_parse_range():
    expr = parse("0 9-17 * * *")
    assert expr.fields["hour"].values == list(range(9, 18))


def test_parse_step():
    expr = parse("*/15 * * * *")
    assert expr.fields["minute"].values == [0, 15, 30, 45]


def test_parse_step_with_start():
    expr = parse("5/10 * * * *")
    assert expr.fields["minute"].values == [5, 15, 25, 35, 45, 55]


def test_parse_comma_list():
    expr = parse("0 8,12,18 * * *")
    assert expr.fields["hour"].values == [8, 12, 18]


def test_parse_day_names():
    expr = parse("0 9 * * mon-fri")
    assert expr.fields["day_of_week"].values == [1, 2, 3, 4, 5]


def test_parse_month_names():
    expr = parse("0 0 1 jan,jun,dec *")
    assert expr.fields["month"].values == [1, 6, 12]


def test_parse_invalid_field_count():
    with pytest.raises(ParseError, match="Expected 5 fields"):
        parse("* * * *")


def test_parse_out_of_range():
    with pytest.raises(ParseError, match="out of range"):
        parse("60 * * * *")


def test_cron_field_attributes():
    expr = parse("0 6 * * 0")
    field = expr.fields["day_of_week"]
    assert isinstance(field, CronField)
    assert field.raw == "0"
    assert field.values == [0]


def test_raw_expression_preserved():
    raw = "*/5 * * * *"
    expr = parse(raw)
    assert expr.raw == raw

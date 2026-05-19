"""Tests for the CLI entry point."""

import pytest
from unittest.mock import patch
from datetime import datetime

from cronlens.cli import main, parse_from_dt, build_parser


FIXED_DT = datetime(2024, 3, 1, 12, 0)


@pytest.fixture(autouse=True)
def fixed_now():
    with patch("cronlens.cli.datetime") as mock_dt:
        mock_dt.now.return_value = FIXED_DT
        mock_dt.strptime.side_effect = datetime.strptime
        yield mock_dt


def test_main_returns_zero_on_valid_expression(capsys):
    result = main(["*/5 * * * *"])
    assert result == 0
    captured = capsys.readouterr()
    assert "*/5 * * * *" in captured.out


def test_main_returns_one_on_invalid_expression(capsys):
    result = main(["not a cron"])
    assert result == 1
    captured = capsys.readouterr()
    assert "parse error" in captured.err


def test_main_count_flag(capsys):
    result = main(["* * * * *", "-n", "3"])
    assert result == 0
    captured = capsys.readouterr()
    # 3 run lines expected
    lines = [l for l in captured.out.splitlines() if "2024" in l]
    assert len(lines) == 3


def test_main_from_flag(capsys):
    result = main(["0 9 * * *", "--from", "2024-06-01 00:00"])
    assert result == 0
    captured = capsys.readouterr()
    assert "2024-06-01" in captured.out or "2024" in captured.out


def test_main_invalid_from_flag(capsys):
    result = main(["* * * * *", "--from", "not-a-date"])
    assert result == 1
    captured = capsys.readouterr()
    assert "Cannot parse" in captured.err


def test_main_no_color_flag(capsys):
    result = main(["* * * * *", "--no-color"])
    assert result == 0


def test_parse_from_dt_formats():
    assert parse_from_dt("2024-01-15 08:00") == datetime(2024, 1, 15, 8, 0)
    assert parse_from_dt("2024-01-15T08:00") == datetime(2024, 1, 15, 8, 0)
    assert parse_from_dt("2024-01-15") == datetime(2024, 1, 15, 0, 0)


def test_parse_from_dt_invalid():
    with pytest.raises(ValueError, match="Cannot parse"):
        parse_from_dt("15/01/2024")


def test_build_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["* * * * *"])
    assert args.count == 5
    assert args.from_dt is None
    assert args.no_color is False

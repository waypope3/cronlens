"""Tests for next_run scheduling logic."""

from datetime import datetime
import pytest
from cronlens.parser import CronExpression
from cronlens.next_run import next_runs, iter_next_runs


BASE = datetime(2024, 1, 15, 12, 0, 0)  # Monday noon


def test_returns_n_results():
    expr = CronExpression.parse("* * * * *")
    results = next_runs(expr, n=5, after=BASE)
    assert len(results) == 5


def test_every_minute_consecutive():
    expr = CronExpression.parse("* * * * *")
    results = next_runs(expr, n=3, after=BASE)
    assert results[1] - results[0] == pytest.approx(60, abs=1)


def test_specific_minute():
    expr = CronExpression.parse("30 * * * *")
    results = next_runs(expr, n=3, after=BASE)
    for dt in results:
        assert dt.minute == 30


def test_specific_hour():
    expr = CronExpression.parse("0 9 * * *")
    results = next_runs(expr, n=3, after=BASE)
    for dt in results:
        assert dt.hour == 9
        assert dt.minute == 0


def test_step_expression():
    expr = CronExpression.parse("*/15 * * * *")
    results = next_runs(expr, n=4, after=BASE)
    for dt in results:
        assert dt.minute % 15 == 0


def test_day_of_week_filter():
    # 1 = Monday in cron (0=Sun)
    expr = CronExpression.parse("0 0 * * 1")
    results = next_runs(expr, n=3, after=BASE)
    for dt in results:
        assert dt.weekday() == 0  # Python Monday = 0


def test_specific_day_of_month():
    expr = CronExpression.parse("0 0 20 * *")
    results = next_runs(expr, n=2, after=BASE)
    for dt in results:
        assert dt.day == 20


def test_results_are_in_future():
    expr = CronExpression.parse("* * * * *")
    after = BASE
    results = next_runs(expr, n=5, after=after)
    for dt in results:
        assert dt > after


def test_iter_is_lazy():
    expr = CronExpression.parse("* * * * *")
    gen = iter_next_runs(expr, after=BASE)
    first = next(gen)
    second = next(gen)
    assert second > first

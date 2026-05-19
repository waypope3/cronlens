"""Compute the next N scheduled run times for a cron expression."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterator, List

from cronlens.parser import CronExpression

_MAX_ITERATIONS = 527_040  # minutes in one year


def _matches(expr: CronExpression, dt: datetime) -> bool:
    """Return True if *dt* satisfies all fields of *expr*."""
    for value, field in [
        (dt.minute, expr.minute),
        (dt.hour, expr.hour),
        (dt.day, expr.day_of_month),
        (dt.month, expr.month),
        (dt.weekday() + 1) % 7, expr.day_of_week),  # 0=Sun
    ]:
        if not field.matches(value):
            return False
    return True


def iter_next_runs(expr: CronExpression, after: datetime | None = None) -> Iterator[datetime]:
    """Yield successive run datetimes for *expr* starting after *after*."""
    if after is None:
        after = datetime.now()
    # Advance to next whole minute
    current = after.replace(second=0, microsecond=0) + timedelta(minutes=1)
    iterations = 0
    while iterations < _MAX_ITERATIONS:
        if _matches(expr, current):
            yield current
        current += timedelta(minutes=1)
        iterations += 1


def next_runs(expr: CronExpression, n: int = 5, after: datetime | None = None) -> List[datetime]:
    """Return the next *n* scheduled datetimes for *expr*."""
    results: List[datetime] = []
    for dt in iter_next_runs(expr, after=after):
        results.append(dt)
        if len(results) >= n:
            break
    return results

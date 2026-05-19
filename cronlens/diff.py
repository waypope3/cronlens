"""Compare two cron expressions and report differences in their schedules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

from .next_run import next_runs
from .parser import CronExpression


@dataclass
class ScheduleDiff:
    only_in_a: List[datetime]
    only_in_b: List[datetime]
    common: List[datetime]

    @property
    def is_identical(self) -> bool:
        return not self.only_in_a and not self.only_in_b


def compare(
    expr_a: str,
    expr_b: str,
    *,
    from_dt: datetime | None = None,
    count: int = 10,
) -> ScheduleDiff:
    """Compare the next *count* run times of two cron expressions.

    Parameters
    ----------
    expr_a, expr_b:
        Raw cron expression strings.
    from_dt:
        Starting point for iteration; defaults to *now*.
    count:
        How many upcoming run times to collect per expression.
    """
    parsed_a = CronExpression.parse(expr_a)
    parsed_b = CronExpression.parse(expr_b)

    from_dt = from_dt or datetime.now().replace(second=0, microsecond=0)

    runs_a: List[datetime] = next_runs(parsed_a, n=count, from_dt=from_dt)
    runs_b: List[datetime] = next_runs(parsed_b, n=count, from_dt=from_dt)

    set_a = set(runs_a)
    set_b = set(runs_b)

    common = sorted(set_a & set_b)
    only_in_a = sorted(set_a - set_b)
    only_in_b = sorted(set_b - set_a)

    return ScheduleDiff(only_in_a=only_in_a, only_in_b=only_in_b, common=common)


def format_diff(diff: ScheduleDiff, expr_a: str, expr_b: str) -> str:
    """Return a human-readable diff report."""
    lines: List[str] = []
    lines.append(f"Comparing: [{expr_a}]  vs  [{expr_b}]")
    lines.append(f"  Common runs   : {len(diff.common)}")
    lines.append(f"  Only in first : {len(diff.only_in_a)}")
    lines.append(f"  Only in second: {len(diff.only_in_b)}")
    if diff.only_in_a:
        lines.append("\n  ← Unique to first:")
        for dt in diff.only_in_a:
            lines.append(f"    {dt.strftime('%Y-%m-%d %H:%M')}")
    if diff.only_in_b:
        lines.append("\n  → Unique to second:")
        for dt in diff.only_in_b:
            lines.append(f"    {dt.strftime('%Y-%m-%d %H:%M')}")
    if diff.is_identical:
        lines.append("\n  ✓ Schedules are identical for the sampled window.")
    return "\n".join(lines)

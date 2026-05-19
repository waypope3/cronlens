"""Terminal formatting utilities for cronlens output."""

from __future__ import annotations

from datetime import datetime
from typing import List

from cronlens.parser import CronExpression
from cronlens.humanizer import humanize
from cronlens.next_run import next_runs

_RESET = "\033[0m"
_BOLD = "\033[1m"
_CYAN = "\033[36m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_DIM = "\033[2m"


def _colorize(text: str, color: str) -> str:
    return f"{color}{text}{_RESET}"


def format_summary(expression: str, n: int = 5, color: bool = True) -> str:
    """Return a formatted terminal string summarising a cron expression."""
    expr = CronExpression.parse(expression)
    description = humanize(expr)
    runs: List[datetime] = next_runs(expr, n=n)

    lines: List[str] = []

    header = f"Expression : {expression}"
    if color:
        header = _colorize("Expression", _BOLD) + f" : {_colorize(expression, _CYAN)}"
    lines.append(header)

    desc_line = f"Meaning    : {description}"
    if color:
        desc_line = _colorize("Meaning", _BOLD) + f"    : {_colorize(description, _YELLOW)}"
    lines.append(desc_line)

    lines.append("")
    next_label = "Next runs  :"
    if color:
        next_label = _colorize("Next runs", _BOLD) + "  :"
    lines.append(next_label)

    for i, dt in enumerate(runs, start=1):
        ts = dt.strftime("%Y-%m-%d %H:%M")
        entry = f"  {i}. {ts}"
        if color:
            entry = f"  {_colorize(str(i) + '.', _DIM)} {_colorize(ts, _GREEN)}"
        lines.append(entry)

    return "\n".join(lines)


def print_summary(expression: str, n: int = 5, color: bool = True) -> None:
    """Print the formatted summary directly to stdout."""
    print(format_summary(expression, n=n, color=color))

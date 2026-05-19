"""Formatting utilities for displaying cron run history in the terminal."""

from __future__ import annotations

from datetime import datetime
from typing import List

from cronlens.history import HistoryEntry

DIM = "\033[2m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def _fmt_dt(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso


def format_entry(entry: HistoryEntry, index: int, *, color: bool = True) -> str:
    """Format a single history entry as a readable string."""
    lines: List[str] = []

    label_part = f" ({entry.label})" if entry.label else ""
    header = f"#{index}  {entry.expression}{label_part}"
    queried = f"Queried at: {_fmt_dt(entry.queried_at)}"

    if color:
        header = f"{BOLD}{CYAN}{header}{RESET}"
        queried = f"{DIM}{queried}{RESET}"

    lines.append(header)
    lines.append(queried)

    if entry.next_runs:
        lines.append("Next runs:")
        for ts in entry.next_runs[:3]:
            run_str = f"  • {_fmt_dt(ts)}"
            if color:
                run_str = f"{YELLOW}{run_str}{RESET}"
            lines.append(run_str)
        if len(entry.next_runs) > 3:
            more = f"  … and {len(entry.next_runs) - 3} more"
            lines.append(f"{DIM}{more}{RESET}" if color else more)

    return "\n".join(lines)


def format_history(entries: List[HistoryEntry], *, color: bool = True) -> str:
    """Format a list of history entries into a terminal-ready block."""
    if not entries:
        msg = "No history recorded yet."
        return f"{DIM}{msg}{RESET}" if color else msg

    blocks = [
        format_entry(entry, i + 1, color=color)
        for i, entry in enumerate(entries)
    ]
    separator = "\n" + ("-" * 40) + "\n"
    return separator.join(blocks)


def print_history(entries: List[HistoryEntry], *, color: bool = True) -> None:
    """Print formatted history to stdout."""
    print(format_history(entries, color=color))

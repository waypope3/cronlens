"""Cron run history tracker — records and retrieves past scheduled runs."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

DEFAULT_HISTORY_PATH = Path.home() / ".cronlens" / "history.json"
MAX_HISTORY_ENTRIES = 500


@dataclass
class HistoryEntry:
    expression: str
    queried_at: str  # ISO format
    next_runs: List[str]  # ISO format datetimes
    label: Optional[str] = None

    @classmethod
    def create(
        cls,
        expression: str,
        next_runs: List[datetime],
        label: Optional[str] = None,
    ) -> "HistoryEntry":
        return cls(
            expression=expression,
            queried_at=datetime.now().isoformat(),
            next_runs=[dt.isoformat() for dt in next_runs],
            label=label,
        )


def _load(path: Path) -> List[HistoryEntry]:
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text())
        return [HistoryEntry(**entry) for entry in raw]
    except (json.JSONDecodeError, TypeError, KeyError):
        return []


def _save(entries: List[HistoryEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    trimmed = entries[-MAX_HISTORY_ENTRIES:]
    path.write_text(json.dumps([asdict(e) for e in trimmed], indent=2))


def record(
    expression: str,
    next_runs: List[datetime],
    label: Optional[str] = None,
    path: Path = DEFAULT_HISTORY_PATH,
) -> HistoryEntry:
    """Append a new history entry and persist to disk."""
    entry = HistoryEntry.create(expression, next_runs, label)
    entries = _load(path)
    entries.append(entry)
    _save(entries, path)
    return entry


def load_history(path: Path = DEFAULT_HISTORY_PATH) -> List[HistoryEntry]:
    """Return all recorded history entries."""
    return _load(path)


def clear_history(path: Path = DEFAULT_HISTORY_PATH) -> int:
    """Delete all history entries. Returns the count removed."""
    entries = _load(path)
    count = len(entries)
    _save([], path)
    return count


def search_history(
    expression: str,
    path: Path = DEFAULT_HISTORY_PATH,
) -> List[HistoryEntry]:
    """Return history entries matching a specific cron expression."""
    return [e for e in _load(path) if e.expression == expression]

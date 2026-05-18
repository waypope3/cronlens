"""Cron expression parser for cronlens."""

from dataclasses import dataclass
from typing import List, Optional


CRON_FIELDS = ["minute", "hour", "day_of_month", "month", "day_of_week"]

FIELD_RANGES = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day_of_month": (1, 31),
    "month": (1, 12),
    "day_of_week": (0, 6),
}

MONTH_NAMES = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

DAY_NAMES = {
    "sun": 0, "mon": 1, "tue": 2, "wed": 3,
    "thu": 4, "fri": 5, "sat": 6,
}


@dataclass
class CronField:
    name: str
    raw: str
    values: List[int]


@dataclass
class CronExpression:
    raw: str
    fields: dict  # field_name -> CronField

    def __getattr__(self, name: str) -> Optional[CronField]:
        if name in CRON_FIELDS:
            return self.fields.get(name)
        raise AttributeError(f"No attribute '{name}'")


class ParseError(ValueError):
    pass


def _resolve_name(value: str, mapping: dict) -> str:
    return str(mapping.get(value.lower(), value))


def _parse_field(raw: str, field_name: str) -> CronField:
    min_val, max_val = FIELD_RANGES[field_name]
    name_map = MONTH_NAMES if field_name == "month" else (DAY_NAMES if field_name == "day_of_week" else {})
    values = set()

    for part in raw.split(","):
        part = _resolve_name(part, name_map)
        if part == "*":
            values.update(range(min_val, max_val + 1))
        elif "/" in part:
            base, step = part.split("/", 1)
            step = int(step)
            start = min_val if base == "*" else int(_resolve_name(base, name_map))
            values.update(range(start, max_val + 1, step))
        elif "-" in part:
            start, end = part.split("-", 1)
            values.update(range(int(_resolve_name(start, name_map)), int(_resolve_name(end, name_map)) + 1))
        else:
            val = int(part)
            if not (min_val <= val <= max_val):
                raise ParseError(f"Value {val} out of range [{min_val}, {max_val}] for field '{field_name}'")
            values.add(val)

    return CronField(name=field_name, raw=raw, values=sorted(values))


def parse(expression: str) -> CronExpression:
    """Parse a standard 5-field cron expression."""
    parts = expression.strip().split()
    if len(parts) != 5:
        raise ParseError(f"Expected 5 fields, got {len(parts)}: '{expression}'")

    fields = {}
    for name, raw in zip(CRON_FIELDS, parts):
        fields[name] = _parse_field(raw, name)

    return CronExpression(raw=expression, fields=fields)

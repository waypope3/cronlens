"""Field-level explanation generator for cron expressions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .parser import CronExpression, CronField


@dataclass
class FieldExplanation:
    field_name: str
    raw: str
    description: str


_FIELD_NAMES = ("minute", "hour", "day_of_month", "month", "day_of_week")
_FIELD_LABELS = {
    "minute": "Minute",
    "hour": "Hour",
    "day_of_month": "Day of Month",
    "month": "Month",
    "day_of_week": "Day of Week",
}
_MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
_DOW_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def _describe_field_verbose(field: CronField, field_name: str) -> str:
    if field.wildcard:
        return f"every {field_name}"

    parts = []
    for item in field.values:
        if isinstance(item, tuple):
            start, stop, step = item
            if field_name == "month":
                s, e = _MONTH_NAMES[start], _MONTH_NAMES[stop]
            elif field_name == "day_of_week":
                s, e = _DOW_NAMES[start % 7], _DOW_NAMES[stop % 7]
            else:
                s, e = str(start), str(stop)
            chunk = f"{s}–{e}"
            if step and step > 1:
                chunk += f" every {step}"
            parts.append(chunk)
        else:
            if field_name == "month" and 1 <= item <= 12:
                parts.append(_MONTH_NAMES[item])
            elif field_name == "day_of_week":
                parts.append(_DOW_NAMES[item % 7])
            else:
                parts.append(str(item))

    return ", ".join(parts)


def explain(expr: CronExpression) -> List[FieldExplanation]:
    """Return a list of per-field explanations for *expr*."""
    result = []
    for name in _FIELD_NAMES:
        field: CronField = getattr(expr, name)
        label = _FIELD_LABELS[name]
        description = _describe_field_verbose(field, name)
        result.append(FieldExplanation(field_name=label, raw=field.raw, description=description))
    return result

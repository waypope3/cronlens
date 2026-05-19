"""Human-readable descriptions for cron expressions."""

from cronlens.parser import CronExpression, CronField

ORDINALS = {
    1: "1st", 2: "2nd", 3: "3rd",
    **{i: f"{i}th" for i in range(4, 32)},
}

DAY_NAMES = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
    4: "Thursday", 5: "Friday", 6: "Saturday",
}

MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}


def _describe_field(field: CronField, unit: str, names: dict = None) -> str:
    """Produce a human-readable description of a single cron field."""
    if field.wildcard:
        return f"every {unit}"

    if field.step and field.values is None:
        start = field.range_start if field.range_start is not None else 0
        label = names.get(start, str(start)) if names else str(start)
        return f"every {field.step} {unit}s starting from {label}"

    if field.range_start is not None and field.range_end is not None:
        s = names.get(field.range_start, str(field.range_start)) if names else str(field.range_start)
        e = names.get(field.range_end, str(field.range_end)) if names else str(field.range_end)
        if field.step:
            return f"every {field.step} {unit}s from {s} through {e}"
        return f"every {unit} from {s} through {e}"

    if field.values:
        labels = [names.get(v, str(v)) if names else str(v) for v in field.values]
        if len(labels) == 1:
            return f"{unit} {labels[0]}"
        return f"{unit}s {', '.join(labels[:-1])} and {labels[-1]}"

    return unit


def humanize(expr: CronExpression) -> str:
    """Return a full human-readable sentence for a CronExpression."""
    minute = _describe_field(expr.minute, "minute")
    hour = _describe_field(expr.hour, "hour")
    dom = _describe_field(expr.day_of_month, "day", ORDINALS)
    month = _describe_field(expr.month, "month", MONTH_NAMES)
    dow = _describe_field(expr.day_of_week, "weekday", DAY_NAMES)

    parts = []

    if expr.minute.wildcard and expr.hour.wildcard:
        parts.append("Every minute")
    elif expr.minute.wildcard:
        parts.append(f"Every minute of {hour}")
    else:
        parts.append(f"At {minute} past {hour}")

    if not expr.day_of_month.wildcard:
        parts.append(f"on the {dom}")
    if not expr.month.wildcard:
        parts.append(f"in {month}")
    if not expr.day_of_week.wildcard:
        parts.append(f"on {dow}")

    return " ".join(parts)

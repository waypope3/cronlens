"""Well-known cron aliases (e.g. @daily, @weekly) and their expansion."""

from __future__ import annotations

from typing import Dict, Optional


_ALIASES: Dict[str, str] = {
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@midnight": "0 0 * * *",
    "@hourly": "0 * * * *",
    "@reboot": None,  # not representable as a standard 5-field expression
}


class AliasNotRepresentable(ValueError):
    """Raised when an alias cannot be expressed as a 5-field cron string."""


def is_alias(expression: str) -> bool:
    """Return True if *expression* is a recognised cron alias."""
    return expression.strip().lower() in _ALIASES


def expand(expression: str) -> str:
    """Expand a cron alias to its 5-field equivalent.

    Raises
    ------
    KeyError
        If *expression* is not a known alias.
    AliasNotRepresentable
        If the alias has no 5-field equivalent (e.g. ``@reboot``).
    """
    key = expression.strip().lower()
    if key not in _ALIASES:
        raise KeyError(f"Unknown alias: {expression!r}")
    expanded = _ALIASES[key]
    if expanded is None:
        raise AliasNotRepresentable(
            f"{expression!r} cannot be represented as a standard 5-field expression."
        )
    return expanded


def resolve(expression: str) -> str:
    """Return the 5-field form of *expression*, expanding aliases transparently."""
    if is_alias(expression):
        return expand(expression)
    return expression


def all_aliases() -> Dict[str, Optional[str]]:
    """Return a copy of the full alias mapping."""
    return dict(_ALIASES)

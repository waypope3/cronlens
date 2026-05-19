"""Configuration and defaults for cronlens CLI output."""

from dataclasses import dataclass, field
from typing import Optional


# Default number of upcoming runs shown when -n is not supplied
DEFAULT_RUN_COUNT: int = 5

# Maximum allowed value for -n to prevent runaway loops
MAX_RUN_COUNT: int = 100

# Date/time format used when displaying next-run timestamps
DISPLAY_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M"

# Accepted input datetime formats for --from flag (tried in order)
INPUT_DATETIME_FORMATS: tuple[str, ...] = (
    "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d",
)


@dataclass(frozen=True)
class OutputConfig:
    """Immutable configuration for terminal output."""

    color: bool = True
    run_count: int = DEFAULT_RUN_COUNT
    datetime_format: str = DISPLAY_DATETIME_FORMAT

    def validate(self) -> None:
        if not (1 <= self.run_count <= MAX_RUN_COUNT):
            raise ValueError(
                f"run_count must be between 1 and {MAX_RUN_COUNT}, "
                f"got {self.run_count}"
            )


# ANSI color codes used by formatter
COLORS: dict[str, str] = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "cyan": "\033[36m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "grey": "\033[90m",
}

"""Tests for cronlens.config."""

import pytest
from cronlens.config import (
    OutputConfig,
    DEFAULT_RUN_COUNT,
    MAX_RUN_COUNT,
    DISPLAY_DATETIME_FORMAT,
    INPUT_DATETIME_FORMATS,
    COLORS,
)


def test_default_run_count_is_positive():
    assert DEFAULT_RUN_COUNT > 0


def test_max_run_count_gte_default():
    assert MAX_RUN_COUNT >= DEFAULT_RUN_COUNT


def test_output_config_defaults():
    cfg = OutputConfig()
    assert cfg.color is True
    assert cfg.run_count == DEFAULT_RUN_COUNT
    assert cfg.datetime_format == DISPLAY_DATETIME_FORMAT


def test_output_config_validate_ok():
    cfg = OutputConfig(run_count=10)
    cfg.validate()  # should not raise


def test_output_config_validate_zero_raises():
    cfg = OutputConfig(run_count=0)
    with pytest.raises(ValueError, match="run_count"):
        cfg.validate()


def test_output_config_validate_exceeds_max_raises():
    cfg = OutputConfig(run_count=MAX_RUN_COUNT + 1)
    with pytest.raises(ValueError, match="run_count"):
        cfg.validate()


def test_output_config_is_immutable():
    cfg = OutputConfig()
    with pytest.raises((AttributeError, TypeError)):
        cfg.color = False  # type: ignore[misc]


def test_input_datetime_formats_non_empty():
    assert len(INPUT_DATETIME_FORMATS) > 0


def test_colors_has_reset():
    assert "reset" in COLORS
    assert COLORS["reset"].startswith("\033[")

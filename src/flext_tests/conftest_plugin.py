"""Pytest plugin wiring the canonical flext-tests fixture modules.

Usage in any project's conftest.py::

    pytest_plugins = ["flext_tests.conftest_plugin"]

This plugin delegates to the shared markdown-validation and test-runtime
fixture modules so projects get one canonical owner for CLI options,
autouse runtime setup, and shared helper fixtures.
"""

from __future__ import annotations

import pytest

pytest_plugins: tuple[str, str] = (
    "flext_tests._fixtures.markdown_validation",
    "flext_tests._fixtures.settings",
)

# NOTE (mro-wkii.17.26, agent: codex): the generated static fixtures package
# imports sibling modules eagerly, so register rewriting before pytest imports it.
pytest.register_assert_rewrite(*pytest_plugins)

# Enforcement dispatcher (flext_tests._fixtures.enforcement) is loaded via
# the ``flext_tests_enforcement`` pytest11 entry point in pyproject.toml —
# re-exporting its hooks here would double-register CLI options when both
# paths are active. The plugin module only delegates to the canonical
# fixture modules so lazy-init sees a single owner for each exported symbol.

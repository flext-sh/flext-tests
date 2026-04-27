"""Pytest plugin providing centralized FlextSettings fixtures and markdown validation.

Usage in any project's conftest.py::

    pytest_plugins = ["flext_tests.conftest_plugin"]

This registers the following auto-use fixtures:
- reset_settings: Resets FlextSettings + FlextContainer singletons between tests

And the following on-demand fixtures:
- settings: Clean FlextSettings with debug=True
- settings_factory: Factory for project-specific settings classes

And the following CLI options:
- the markdown docs option: Validate Python code blocks in .md files
"""

from __future__ import annotations

from flext_tests._fixtures.markdown_validation import (
    MarkdownCodeBlockCollector,
    MarkdownCodeBlockItem,
    MarkdownValidationError,
    pytest_addoption,
    pytest_collect_file,
)
from flext_tests._fixtures.settings import (
    reset_settings,
    settings,
    settings_factory,
)

# Enforcement dispatcher (flext_tests._fixtures.enforcement) is loaded via
# the ``flext_tests_enforcement`` pytest11 entry point in pyproject.toml —
# re-exporting its hooks here would double-register CLI options when both
# paths are active.

_ = (
    reset_settings,
    settings,
    settings_factory,
    pytest_addoption,
    pytest_collect_file,
    MarkdownCodeBlockCollector,
    MarkdownCodeBlockItem,
    MarkdownValidationError,
)

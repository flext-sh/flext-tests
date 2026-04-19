"""Pytest plugin providing centralized FlextSettings fixtures and markdown validation.

Usage in any project's conftest.py::

    pytest_plugins = ["flext_tests.conftest_plugin"]

This registers the following auto-use fixtures:
- reset_settings: Resets FlextSettings + FlextContainer singletons between tests

And the following on-demand fixtures:
- settings: Clean FlextSettings with debug=True
- settings_factory: Factory for project-specific settings classes

And the following CLI options:
- --markdown-docs: Validate Python code blocks in .md files
- --markdown-ruff: Also run ruff on extracted code blocks
"""

from __future__ import annotations

from flext_tests import (
    MarkdownCodeBlockCollector,
    MarkdownCodeBlockItem,
    MarkdownValidationError,
    pytest_addoption,
    pytest_collect_file,
    reset_settings,
    settings,
    settings_factory,
)

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

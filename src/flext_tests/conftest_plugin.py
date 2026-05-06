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

from tests import t

pytest_plugins: t.StrSequence = (
    "flext_tests._fixtures.markdown_validation",
    "flext_tests._fixtures.settings",
)

# Enforcement dispatcher (flext_tests._fixtures.enforcement) is loaded via
# the ``flext_tests_enforcement`` pytest11 entry point in pyproject.toml —
# re-exporting its hooks here would double-register CLI options when both
# paths are active. The plugin module only delegates to the canonical
# fixture modules so lazy-init sees a single owner for each exported symbol.

"""Pytest plugin providing centralized FlextSettings fixtures.

Usage in any project's conftest.py::

    pytest_plugins = ["flext_tests.conftest_plugin"]

This registers the following auto-use fixtures:
- reset_settings: Resets FlextSettings + FlextContainer singletons between tests

And the following on-demand fixtures:
- settings: Clean FlextSettings with debug=True
- settings_factory: Factory for project-specific settings classes
"""

from __future__ import annotations

from flext_tests._fixtures.settings import reset_settings, settings, settings_factory

_ = (reset_settings, settings, settings_factory)

"""Pytest plugin wiring the canonical flext-tests fixture modules.

The installed ``pytest11`` entry point targets ``FlextTestsConftestPlugin``
directly and registers its static hooks before configuration. Shared fixtures
register automatically; projects do not copy plugin wiring.
``session_runtime`` lazily provisions one
physical locked consumer per worker, with exclusive, isolated case leases.
Markdown code blocks are executed by pytest-markdown-docs; there is no local
markdown rule fallback.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

from flext_tests import c

if TYPE_CHECKING:
    import pytest


class FlextTestsConftestPlugin:
    """Native pytest plugin object loaded directly by the installed entry point."""

    @staticmethod
    def pytest_configure(config: pytest.Config) -> None:
        """Register fixture plugins after startup instrumentation is active."""
        # Import at configure time, after pytest-cov starts measuring. The module
        # name avoids the settings fixture shadowing its submodule attribute.
        for fixture_module in c.Tests.FIXTURE_PLUGIN_MODULES:
            config.pluginmanager.import_plugin(fixture_module)
        # Prerequisites skip before fixtures; real service failures stay failures.
        if not config.pluginmanager.hasplugin(c.Tests.CAPABILITY_PLUGIN_MODULE):
            capability = import_module(c.Tests.CAPABILITY_PLUGIN_MODULE)
            config.pluginmanager.register(
                capability.FlextTestsCapabilityPlugin(),
                c.Tests.CAPABILITY_PLUGIN_MODULE,
            )


# Enforcement dispatcher (flext_tests.enforcement_plugin) is loaded via
# the ``flext_tests_enforcement`` pytest11 entry point in pyproject.toml —
# re-exporting its hooks here would double-register CLI options when both
# paths are active. The plugin class registers the canonical fixture modules
# during ``pytest_configure``. It must not expose ``pytest_plugins``: pytest
# processes that declaration while loading the ``pytest11`` entry point,
# before pytest-cov starts measuring the product package.


# The pytest11 object target owns hooks, not the package's public facade.
__all__: list[str] = []

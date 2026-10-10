"""Pytest plugin wiring the canonical flext-tests fixture modules.

Usage in any project's conftest.py::

    pytest_plugins = ["flext_tests.conftest_plugin"]

This plugin registers the shared test-runtime fixture modules so projects get
one canonical owner for autouse runtime setup and shared helper fixtures.
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


def pytest_configure(config: pytest.Config) -> None:
    """Register fixture plugins after startup instrumentation is active."""
    # pytest's own plugin-by-name API imports and registers each fixture module
    # here, after pytest-cov started measuring; loading this pytest11 entry
    # point therefore imports no fixture module. Naming the module (not the
    # package attribute) avoids the ``_fixtures.settings`` fixture function
    # that shadows the submodule of the same name. Registration is idempotent.
    for fixture_module in c.Tests.FIXTURE_PLUGIN_MODULES:
        config.pluginmanager.import_plugin(fixture_module)
    # Connectivity prerequisites skip before fixtures; real service failures fail.
    if not config.pluginmanager.hasplugin(c.Tests.CAPABILITY_PLUGIN_MODULE):
        capability = import_module(c.Tests.CAPABILITY_PLUGIN_MODULE)
        config.pluginmanager.register(
            capability.FlextTestsCapabilityPlugin(),
            c.Tests.CAPABILITY_PLUGIN_MODULE,
        )


# Enforcement dispatcher (flext_tests.enforcement_plugin) is loaded via
# the ``flext_tests_enforcement`` pytest11 entry point in pyproject.toml —
# re-exporting its hooks here would double-register CLI options when both
# paths are active. The plugin module registers the canonical fixture modules
# during ``pytest_configure``. It must not expose ``pytest_plugins``: pytest
# processes that declaration while loading the ``pytest11`` entry point,
# before pytest-cov starts measuring the product package.


__all__: list[str] = ["pytest_configure"]

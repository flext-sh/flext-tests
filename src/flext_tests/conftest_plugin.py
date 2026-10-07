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

from flext_tests._fixtures import (
    connectivity as _fixtures_connectivity,
    scratch_storage as _fixtures_scratch_storage,
)

if TYPE_CHECKING:
    import pytest

# `_fixtures/__init__` exports a fixture function named `settings`, which
# shadows the submodule of the same name: `from ... import settings` binds the
# fixture, and registering a function as a plugin silently registers no
# fixtures at all. The top-level ``import_module`` calls name the modules
# unambiguously without touching the shadowed package attribute.
_SETTINGS_FIXTURE_MODULE = import_module("flext_tests._fixtures.settings")
_NAMESPACE_MODULE = import_module("flext_tests._fixtures.namespace")


def pytest_configure(config: pytest.Config) -> None:
    """Register fixture plugins after startup instrumentation is active."""
    settings = _SETTINGS_FIXTURE_MODULE
    namespace_module = _NAMESPACE_MODULE
    scratch_module = _fixtures_scratch_storage

    if settings not in config.pluginmanager.get_plugins():
        config.pluginmanager.register(settings, settings.__name__)
    if namespace_module not in config.pluginmanager.get_plugins():
        config.pluginmanager.register(namespace_module, namespace_module.__name__)
    if scratch_module not in config.pluginmanager.get_plugins():
        config.pluginmanager.register(scratch_module, scratch_module.__name__)
    # Capability-bound tests are DESELECTED (typed NOT EXECUTED) when their
    # capability is absent; a capable host executes and a service failure is RED.
    connectivity = _fixtures_connectivity.FlextTestsCapabilityPlugin()
    if not config.pluginmanager.hasplugin("flext_tests._fixtures.connectivity"):
        config.pluginmanager.register(
            connectivity,
            "flext_tests._fixtures.connectivity",
        )


# Enforcement dispatcher (flext_tests.enforcement_plugin) is loaded via
# the ``flext_tests_enforcement`` pytest11 entry point in pyproject.toml —
# re-exporting its hooks here would double-register CLI options when both
# paths are active. The plugin module registers the canonical fixture modules
# during ``pytest_configure``. It must not expose ``pytest_plugins``: pytest
# processes that declaration while loading the ``pytest11`` entry point,
# before pytest-cov starts measuring the product package.


__all__: list[str] = ["pytest_configure"]

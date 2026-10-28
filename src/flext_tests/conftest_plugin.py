"""Pytest plugin registering the canonical fixture modules' class objects.

The installed ``pytest11`` entry point targets ``FlextTestsConftestPlugin``
directly and registers its static hooks before configuration. Shared fixtures
register automatically; projects do not copy plugin wiring.
The same plugin applies config-owned slow budgets independently of static
enforcement activation.
``session_runtime`` lazily provisions one
physical locked consumer per worker, with exclusive, isolated case leases.
Markdown code blocks are executed by pytest-markdown-docs; there is no local
markdown rule fallback.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib import import_module
from inspect import getmembers, isclass
from typing import TYPE_CHECKING

from flext_tests import c

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping

    import pytest


class FlextTestsConftestPlugin:
    """Native pytest plugin object loaded directly by the installed entry point."""

    @staticmethod
    def pytest_addoption(parser: pytest.Parser) -> None:
        """Register shared runner configuration before pytest validates it."""
        parser.addini(
            c.Tests.ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION,
            "Config-owned timeout in seconds for items explicitly marked slow.",
            default="",
        )

    @staticmethod
    def pytest_collection_modifyitems(
        config: pytest.Config,
        items: list[pytest.Item],
    ) -> None:
        """Apply the shared slow policy through its existing timing owner."""
        dispatcher = import_module(
            c.Tests.ENFORCEMENT_DISPATCHER_MODULE,
        ).FlextTestsEnforcementDispatcher
        dispatcher.apply_slow_budget(config, items)

    @staticmethod
    def publish[TBinding](
        *,
        module_globals: MutableMapping[str, TBinding],
        bindings: Mapping[str, TBinding],
    ) -> None:
        """Publish explicit class-owned bindings on their original pytest module.

        Called during module execution, before pytest registers the conftest.
        Actual fixture descriptors and hook callables retain their native identity;
        the original module path, not a globally registered class plugin, continues
        to own directory visibility. No members are discovered or copied implicitly.
        """
        module_globals.update(bindings)

    @staticmethod
    def pytest_configure(config: pytest.Config) -> None:
        """Register fixture plugins after startup instrumentation is active.

        Raises:
            ValueError: If a fixture module declares more than one owner or a
                required fixture plugin is blocked from registration.

        """
        # Import at configure time, after pytest-cov starts measuring. The module
        # name avoids the settings fixture shadowing its submodule attribute.
        for fixture_module in c.Tests.FIXTURE_PLUGIN_MODULES:
            module = import_module(fixture_module)
            owners = [
                owner
                for _, owner in getmembers(module, isclass)
                if owner.__module__ == module.__name__
            ]
            if len(owners) != 1:
                msg = (
                    f"{fixture_module} must declare exactly one plugin owner; "
                    f"found {len(owners)}"
                )
                raise ValueError(msg)
            owner = owners[0]
            for attr in owner.__dict__.values():
                if hasattr(attr, "_get_wrapped_function"):
                    wrapped = attr._get_wrapped_function()
                    if isinstance(wrapped, staticmethod):
                        attr._fixture_function = wrapped.__func__
            if config.pluginmanager.get_plugin(fixture_module) is owner:
                continue
            if config.pluginmanager.register(owner, fixture_module) is None:
                msg = f"required fixture plugin is blocked: {fixture_module}"
                raise ValueError(msg)
        # Prerequisites skip before fixtures; real service failures stay failures.
        if not config.pluginmanager.hasplugin(c.Tests.CAPABILITY_PLUGIN_MODULE):
            capability = import_module(c.Tests.CAPABILITY_PLUGIN_MODULE)
            config.pluginmanager.register(
                capability.FlextTestsCapabilityPlugin(),
                c.Tests.CAPABILITY_PLUGIN_MODULE,
            )


# The optional static-enforcement adapter owns its own hooks and options;
# shared timing belongs to this always-loaded plugin. The plugin class registers
# each canonical fixture class during ``pytest_configure``. It must not expose
# ``pytest_plugins``: pytest
# processes that declaration while loading the ``pytest11`` entry point,
# before pytest-cov starts measuring the product package.


# The pytest11 object target owns hooks, not the package's public facade.
__all__: list[str] = []

"""Public facade import regressions.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from importlib import import_module
from importlib.metadata import entry_points
from pathlib import Path

import pytest
from flext_infra import config
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

import flext_tests
from flext_tests import FlextTestsCase, FlextTestsModels, FlextTestsUtilities
from tests import d, e, h, m, r, tf, tk, tm, u, x


class TestsFlextTestsPublicFacade:
    """Tests for ``FlextTestsPublicFacade``."""

    class Tests:
        """flext-tests public facade test namespace."""

    @staticmethod
    def test_models_and_utilities_import_together() -> None:
        """Test models and utilities import together.

        The ``tests`` facade deliberately enriches the public models and
        utilities; the letters must resolve to subclasses of the public
        families, keeping both facades importable side by side.

        """
        tm.that(issubclass(m, FlextTestsModels), eq=True)
        tm.that(issubclass(u, FlextTestsUtilities), eq=True)

    @staticmethod
    def test_selected_enforcement_plugin_uses_its_declared_identity(
        pytestconfig: pytest.Config,
    ) -> None:
        """Test selected enforcement plugin uses its declared identity."""
        plugin = config.Infra.tooling.tools.pytest.enforcement_plugin
        entries = entry_points(group="pytest11", name=plugin)
        tm.that(len(entries), eq=1)
        tm.that(
            pytestconfig.pluginmanager.get_plugin(plugin) is next(iter(entries)).load(),
            eq=True,
        )

    @staticmethod
    def test_plugin_configure_hooks_keep_their_registered_module_owners(
        pytestconfig: pytest.Config,
    ) -> None:
        """Both pytest11 configure hooks run without competing for root exports."""
        entries = {
            entry.name: entry
            for entry in entry_points(group="pytest11")
            if entry.value.startswith(f"{flext_tests.__name__}.")
        }
        configure = {
            hook.plugin_name: hook.plugin
            for hook in pytestconfig.hook.pytest_configure.get_hookimpls()
            if hook.plugin_name in entries
        }
        tm.that(set(configure), eq=set(entries))
        for name, entry in entries.items():
            tm.that(configure[name] is entry.load(), eq=True)
        tm.that("pytest_configure" in flext_tests.__all__, eq=False)

    @staticmethod
    def test_consumer_facade_imports_without_container_lifecycle() -> None:
        """Test consumer facade imports without container lifecycle."""
        for name, exported in (
            ("FlextTestsCase", FlextTestsCase),
            ("d", d),
            ("e", e),
            ("h", h),
            ("r", r),
            ("tf", tf),
            ("tk", tk),
            ("tm", tm),
            ("x", x),
        ):
            tm.that(exported is getattr(flext_tests, name), eq=True)

    @staticmethod
    @pytest.mark.parametrize(
        ("module_name", "distribution_name"),
        [
            ("docker", "docker"),
            ("python_on_whales", "python-on-whales"),
            ("flext_cli", "flext-cli"),
            ("flext_core", "flext-core"),
            ("flext_infra", "flext-infra"),
            ("pydantic_settings", "pydantic-settings"),
            ("pytest", "pytest"),
        ],
    )
    def test_facade_runtime_imports_are_direct_unconditional_dependencies(
        module_name: str,
        distribution_name: str,
    ) -> None:
        """Test facade runtime imports are direct unconditional dependencies."""
        root = Path(__file__).resolve().parents[2]
        document = u.read_project_document_cached(root)
        metadata = u.build_project_metadata(root, document)
        requirements = {
            canonicalize_name(requirement.name): requirement
            for value in metadata.project.dependencies
            for requirement in (Requirement(value),)
        }
        name = canonicalize_name(distribution_name)
        tm.that(name in requirements, eq=True)
        tm.that(requirements[name].marker, eq=None)
        import_module(module_name)
        tm.that(module_name in sys.modules, eq=True)

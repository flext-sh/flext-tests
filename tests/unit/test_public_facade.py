"""Public facade import regressions."""

from __future__ import annotations

from importlib import import_module
from importlib.metadata import entry_points
from pathlib import Path

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from flext_tests import tm


class TestsFlextTestsPublicFacade:
    def test_models_and_utilities_import_together(self) -> None:
        from flext_tests import m, u

        tm.that(m.__name__, eq="FlextTestsModels")
        tm.that(u.__name__, eq="FlextTestsUtilities")

    def test_selected_enforcement_plugin_uses_its_declared_identity(
        self, pytestconfig: pytest.Config
    ) -> None:
        from flext_infra import config

        plugin = config.Infra.tooling.tools.pytest.enforcement_plugin
        entries = entry_points(group="pytest11", name=plugin)
        tm.that(len(entries), eq=1)
        tm.that(
            pytestconfig.pluginmanager.get_plugin(plugin) is next(iter(entries)).load(),
            eq=True,
        )

    def test_consumer_facade_imports_without_container_lifecycle(self) -> None:
        import flext_tests
        from flext_tests import FlextTestsCase, d, e, h, r, tf, tk, tm, tv, x

        for name, exported in (
            ("FlextTestsCase", FlextTestsCase),
            ("d", d),
            ("e", e),
            ("h", h),
            ("r", r),
            ("tf", tf),
            ("tk", tk),
            ("tm", tm),
            ("tv", tv),
            ("x", x),
        ):
            tm.that(exported is getattr(flext_tests, name), eq=True)

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
        self, module_name: str, distribution_name: str
    ) -> None:
        from flext_tests import u

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
        imported = import_module(module_name)
        tm.that(imported.__name__, eq=module_name)


__all__: list[str] = ["TestsFlextTestsPublicFacade"]

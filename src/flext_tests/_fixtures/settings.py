"""Centralized settings fixtures and runtime lifecycle for all consumer suites.

The class object is registered once per worker as a native pytest plugin.
Runtime provisioning remains lazy and session-scoped, not inherited per suite.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import TYPE_CHECKING, Protocol, cast

import pytest
from flext_core import FlextContainer, FlextContext, FlextSettings

import flext_tests
from flext_tests import FlextTestsSettings, t

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from pathlib import Path

    from flext_tests import FlextTestsCase, FlextTestsServiceBase, m, p


class FlextTestsSettingsFixtures:
    """Native shared fixtures and per-item reset/binding hooks."""

    class FixtureNodeRequest(Protocol):
        """Public request boundary with the scope-dependent collection node."""

        @property
        def node(self) -> pytest.Item | pytest.Collector:
            """The item or collector owning the current fixture context."""
            ...

    @staticmethod
    @pytest.fixture(scope="session")
    def session_runtime(
        tmp_path_factory: pytest.TempPathFactory,
        run_namespace: m.Tests.TestNamespace,
    ) -> Iterator[p.Tests.SessionRuntime]:
        """Provide one lazy isolated runtime per worker; close it at session end.

        Pure tests never provision tools. Consumers lease one shared locked seed;
        teardown validates allocation identity before removing its owned area.

        Yields:
            p.Tests.SessionRuntime: One lazy isolated worker runtime.

        """
        directory = tmp_path_factory.mktemp(run_namespace.token)
        runtime = flext_tests.u.Tests.SessionRuntime(directory)
        try:
            yield runtime
        finally:
            runtime.close()

    @staticmethod
    def _reset_runtime_state() -> None:
        """Reset root/test settings singletons and the DI container."""
        FlextSettings.reset_for_testing()
        importlib.import_module("flext_tests").FlextTestsSettings.reset_for_testing()
        FlextContainer.reset_for_testing()

    @staticmethod
    def _bind_runtime_aliases(
        *,
        module: ModuleType,
        instance: FlextTestsCase | None,
    ) -> None:
        """Bind canonical aliases only to package-owned FlextTestsCase instances.

        Raises:
            TypeError: If the package service alias has the wrong base.
            AttributeError: If the package omits a required public alias.

        """
        package_root = module.__package__ or ""
        if not package_root or instance is None:
            return
        canonical_service = importlib.import_module("flext_tests").s
        package_name = package_root.split(".", maxsplit=1)[0]
        tests_package = importlib.import_module(package_name)
        try:
            service_type = tests_package.s
        except AttributeError as exc:
            msg = (
                f"{package_name} must re-export the canonical service alias 's' "
                "from its package root for the shared test runtime"
            )
            raise AttributeError(msg) from exc
        if not isinstance(service_type, type) or not issubclass(
            service_type,
            canonical_service,
        ):
            msg = (
                f"{package_name} declares 's' as {service_type!r}, "
                "which is not a FlextTestsServiceBase subclass"
            )
            raise TypeError(msg)
        service_cls = cast("type[FlextTestsServiceBase]", service_type)
        service = service_cls.fetch_global()
        instance.service = service
        instance.settings = service.fetch_settings()
        instance.logger = service.logger
        for alias_name in ("c", "e", "m", "p", "r", "t", "u"):
            try:
                alias_value = getattr(tests_package, alias_name)
            except AttributeError as exc:
                msg = (
                    f"{package_name} must re-export the canonical facade letter "
                    f"'{alias_name}' from its package root for the shared test runtime"
                )
                raise AttributeError(msg) from exc
            setattr(instance, alias_name, alias_value)

    @staticmethod
    def pytest_runtest_setup(item: pytest.Item) -> None:
        """Reset and bind the canonical runtime before each pytest function."""
        FlextTestsSettingsFixtures._reset_runtime_state()
        if not isinstance(item, pytest.Function):
            return
        module = item.module
        if not isinstance(module, ModuleType):
            return
        instance = item.instance
        FlextTestsSettingsFixtures._bind_runtime_aliases(
            module=module,
            instance=(
                instance
                if instance is not None
                and isinstance(instance, flext_tests.FlextTestsCase)
                else None
            ),
        )

    @staticmethod
    def pytest_runtest_teardown(
        item: pytest.Item, nextitem: pytest.Item | None
    ) -> None:
        """Reset the canonical runtime after each pytest function."""
        _ = item, nextitem
        FlextTestsSettingsFixtures._reset_runtime_state()

    @staticmethod
    @pytest.fixture
    def reset_settings() -> Iterator[None]:
        """Reset settings/container before and after an explicitly requested lease.

        The plugin hooks independently reset all tests, including tests that do not
        request this fixture.
        """
        FlextTestsSettingsFixtures._reset_runtime_state()
        try:
            yield
        finally:
            FlextTestsSettingsFixtures._reset_runtime_state()

    @staticmethod
    @pytest.fixture
    def test_runtime(
        request: FlextTestsSettingsFixtures.FixtureNodeRequest,
        reset_settings: None,
    ) -> None:
        """Bind canonical test runtime aliases after the explicit reset fixture.

        Raises:
            TypeError: If the pytest function does not belong to a Python module.

        """
        _ = reset_settings
        node = request.node
        if not isinstance(node, pytest.Function):
            return
        module = node.module
        if not isinstance(module, ModuleType):
            msg = f"pytest function {node.nodeid} must belong to a Python module"
            raise TypeError(msg)
        instance = node.instance
        FlextTestsSettingsFixtures._bind_runtime_aliases(
            module=module,
            instance=(
                instance
                if instance is not None
                and isinstance(instance, flext_tests.FlextTestsCase)
                else None
            ),
        )

    @staticmethod
    @pytest.fixture
    def settings() -> FlextTestsSettings:
        """Provide clean typed test settings with the existing test defaults.

        Returns:
            FlextTestsSettings: Fresh typed test settings with test defaults.

        """
        settings_type: type[FlextTestsSettings] = importlib.import_module(
            "flext_tests",
        ).FlextTestsSettings
        FlextSettings.reset_for_testing()
        settings_type.reset_for_testing()
        return settings_type(debug=True, trace=False)

    @staticmethod
    def _create[TSettings: FlextSettings](
        settings_cls: type[TSettings],
        **overrides: t.Scalar | None,
    ) -> TSettings:
        """Create project settings after resetting their singleton.

        Returns:
            TSettings: The global settings instance with the filtered overrides.

        """
        settings_cls.reset_for_testing()
        return settings_cls.update_global(**{
            key: value for key, value in overrides.items() if value is not None
        })

    @staticmethod
    @pytest.fixture
    def settings_factory() -> Callable[..., FlextSettings]:
        """Supply the settings factory without wrapping its native callable.

        Returns:
            Callable[..., FlextSettings]: The unwrapped settings factory.

        """
        return FlextTestsSettingsFixtures._create

    @staticmethod
    @pytest.fixture
    def test_context() -> FlextContext:
        """Provide the canonical FlextContext fixture for test runtimes.

        Returns:
            FlextContext: A new canonical test context.

        """
        return FlextContext()

    @staticmethod
    @pytest.fixture
    def clean_container() -> Iterator[p.Container]:
        """Provide isolated container state and reset it even on test failure.

        Yields:
            p.Container: A fresh isolated DI container.

        """
        FlextContainer.reset_for_testing()
        try:
            yield FlextContainer()
        finally:
            FlextContainer.reset_for_testing()

    @staticmethod
    @pytest.fixture
    def temp_dir(tmp_path: Path) -> Path:
        """Provide the canonical temporary directory fixture for tests.

        Returns:
            Path: The per-test temporary directory.

        """
        return tmp_path

    @staticmethod
    @pytest.fixture
    def sample_data() -> t.JsonMapping:
        """Provide the existing canonical JSON payload for generic test cases.

        Returns:
            t.JsonMapping: The canonical generic JSON test payload.

        """
        return {"string": "test_value", "number": 42, "enabled": True}

"""Centralized settings fixtures and runtime lifecycle for all consumer suites.

The class object is registered once per worker as a native pytest plugin.
Runtime provisioning remains lazy and session-scoped, not inherited per suite.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest
from flext_core import FlextContainer, FlextContext, FlextSettings

import flext_tests
from flext_tests import t

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from flext_tests import FlextTestsSettings, m, p


class FlextTestsSettingsFixtures:
    """Native shared fixtures and per-item reset hooks."""

    @pytest.fixture(scope="session")
    @staticmethod
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
        flext_tests.FlextTestsSettings.reset_for_testing()
        FlextContainer.reset_for_testing()

    @staticmethod
    def pytest_runtest_setup(item: pytest.Item) -> None:
        """Reset the canonical runtime before each pytest item."""
        _ = item
        FlextTestsSettingsFixtures._reset_runtime_state()

    @staticmethod
    def pytest_runtest_teardown(
        item: pytest.Item, nextitem: pytest.Item | None
    ) -> None:
        """Reset the canonical runtime after each pytest function."""
        _ = item, nextitem
        FlextTestsSettingsFixtures._reset_runtime_state()

    @pytest.fixture
    @staticmethod
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

    @pytest.fixture
    @staticmethod
    def test_runtime(
        reset_settings: None,
    ) -> None:
        """Lease the reset lifecycle without constructing consumer dependencies."""
        _ = reset_settings

    @pytest.fixture
    @staticmethod
    def settings() -> FlextTestsSettings:
        """Provide the reset typed test settings singleton with the test defaults.

        Returns:
            FlextTestsSettings: The published singleton carrying the test defaults.

        """
        settings_type = flext_tests.FlextTestsSettings
        FlextSettings.reset_for_testing()
        settings_type.reset_for_testing()
        return settings_type.update_global(debug=True, trace=False)

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

    @pytest.fixture
    @staticmethod
    def settings_factory() -> Callable[..., FlextSettings]:
        """Supply the settings factory without wrapping its native callable.

        Returns:
            Callable[..., FlextSettings]: The unwrapped settings factory.

        """
        return FlextTestsSettingsFixtures._create

    @pytest.fixture
    @staticmethod
    def test_context() -> FlextContext:
        """Provide the canonical FlextContext fixture for test runtimes.

        Returns:
            FlextContext: A new canonical test context.

        """
        return FlextContext()

    @pytest.fixture
    @staticmethod
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

    @pytest.fixture
    @staticmethod
    def logging_trace() -> bool:
        """Provide the trace selection ``restore_logging`` applies.

        A module selects trace through pytest's direct parametrization of
        this name: ``pytest.mark.parametrize("logging_trace", [True])``.

        Returns:
            bool: ``False``; trace stays off unless a module selects it.

        """
        return False

    @pytest.fixture
    @staticmethod
    def restore_logging(*, logging_trace: bool) -> Iterator[None]:
        """Select DEBUG logging for one test, then restore the captured policy.

        Yields:
            None: While the DEBUG selection is active.

        """
        tests = flext_tests
        original_settings = tests.u.logging_settings()
        original_options = tests.u.logging_options()
        try:
            selected = tests.u.resolve_logging_settings(
                log_level=tests.c.LogLevel.DEBUG, trace=logging_trace
            )
            tests.u.configure_structlog(
                settings=tests.m.StructlogOptions(async_logging=False),
                runtime_settings=selected,
            )
            yield
        finally:
            tests.u.configure_structlog(
                settings=original_options, runtime_settings=original_settings
            )

    @pytest.fixture
    @staticmethod
    def temp_dir(tmp_path: Path) -> Path:
        """Provide the canonical temporary directory fixture for tests.

        Returns:
            Path: The per-test temporary directory.

        """
        return tmp_path

    @pytest.fixture
    @staticmethod
    def sample_data() -> t.JsonMapping:
        """Provide the existing canonical JSON payload for generic test cases.

        Returns:
            t.JsonMapping: The canonical generic JSON test payload.

        """
        return {"string": "test_value", "number": 42, "enabled": True}


__all__ = ["FlextTestsSettingsFixtures"]

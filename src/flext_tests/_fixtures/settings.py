"""Centralized FlextSettings fixtures for all project test suites.

Provides:
- reset_settings: Auto-use fixture that resets FlextSettings singleton between tests
- settings: Base FlextSettings fixture with test defaults
- settings_factory: Factory fixture for creating project-specific settings

Eliminates duplicated reset_settings_singleton / _reset_instance patterns
found across flext-core, flext-oracle-wms, flext-target-oracle, flext-auth,
flext-cli, and other project conftest.py files.
"""

from __future__ import annotations

import importlib
from collections.abc import (
    Callable,
    Iterator,
)
from pathlib import Path

import pytest

from flext_core import FlextContainer, FlextContext, FlextSettings, p
from flext_tests import c, e, m, r, s, t, u
from flext_tests.settings import FlextTestsSettings


@pytest.fixture(autouse=True)
def reset_settings() -> Iterator[None]:
    """Reset root + test settings singletons and the DI container.

    Prevents state leakage across tests by clearing both the root settings
    singleton, the test-settings singleton, and the container singleton.
    Runs as autouse so every test gets clean state automatically.
    """
    FlextSettings.reset_for_testing()
    FlextTestsSettings.reset_for_testing()
    FlextContainer.reset_for_testing()
    try:
        yield
    finally:
        FlextSettings.reset_for_testing()
        FlextTestsSettings.reset_for_testing()
        FlextContainer.reset_for_testing()


@pytest.fixture(autouse=True)
def test_runtime(request: pytest.FixtureRequest, reset_settings: None) -> None:
    """Bind the canonical FLEXT test runtime aliases onto pytest class instances."""
    _ = reset_settings
    package_name = request.module.__package__.split(".", maxsplit=1)[0]
    tests_package = importlib.import_module(package_name)
    service_type = getattr(tests_package, "s", s)
    if not isinstance(service_type, type) or not issubclass(service_type, s):
        service_type = s
    service = service_type.fetch_global()
    instance = request.instance or getattr(request.node, "instance", None)
    if instance is not None:
        instance.service = service
        instance.settings = service.settings
        instance.logger = service.logger
        for alias_name, fallback in (
            ("c", c),
            ("e", e),
            ("m", m),
            ("p", p),
            ("r", r),
            ("t", t),
            ("u", u),
        ):
            setattr(instance, alias_name, getattr(tests_package, alias_name, fallback))


@pytest.fixture
def settings() -> FlextTestsSettings:
    """Provide a clean FlextTestsSettings instance with test defaults.

    Resets the root/test singletons first, then creates a fresh typed
    tests settings instance with verbose core defaults.
    """
    FlextSettings.reset_for_testing()
    FlextTestsSettings.reset_for_testing()
    return FlextTestsSettings(debug=True, trace=False)


@pytest.fixture
def settings_factory() -> Callable[..., FlextSettings]:
    """Factory fixture for creating project-specific settings in tests.

    Usage in test::

        def test_something(settings_factory):
            settings = settings_factory(FlextApiSettings, base_url="http://test")
            assert settings.base_url == "http://test"

    The factory resets the singleton for the given class before creating
    a new instance, ensuring test isolation.
    """

    def _create[TSettings: FlextSettings](
        settings_cls: type[TSettings],
        **overrides: t.Scalar | None,
    ) -> TSettings:
        settings_cls.reset_for_testing()
        filtered_overrides: t.ScalarMapping = {
            key: value for key, value in overrides.items() if value is not None
        }
        return settings_cls.fetch_global(overrides=filtered_overrides)

    return _create


@pytest.fixture
def test_context() -> FlextContext:
    """Provide the canonical FlextContext fixture for test runtimes."""
    return FlextContext()


@pytest.fixture
def clean_container() -> Iterator[p.Container]:
    """Provide an isolated DI container for tests that mutate registrations."""
    FlextContainer.reset_for_testing()
    try:
        yield FlextContainer()
    finally:
        FlextContainer.reset_for_testing()


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Provide the canonical temporary directory fixture for tests."""
    return tmp_path


@pytest.fixture
def temp_file(temp_dir: Path) -> Path:
    """Provide the canonical temporary file path rooted at ``temp_dir``."""
    return temp_dir / "test_file.txt"


@pytest.fixture
def sample_data() -> t.JsonMapping:
    """Provide a small canonical JSON payload for generic test cases."""
    return {
        "string": "test_value",
        "number": 42,
        "enabled": True,
    }

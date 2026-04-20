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

from collections.abc import (
    Callable,
    Iterator,
)
from typing import TypeVar

import pytest

from flext_core import FlextContainer, FlextSettings

T = TypeVar("T", bound=FlextSettings)


@pytest.fixture(autouse=True)
def reset_settings() -> Iterator[None]:
    """Reset FlextSettings and FlextContainer singletons between tests.

    Prevents state leakage across tests by clearing both the settings
    singleton (which uses __new__ caching) and the container singleton.
    Runs as autouse so every test gets clean state automatically.
    """
    yield
    FlextSettings.reset_for_testing()
    FlextContainer.reset_for_testing()


@pytest.fixture
def settings() -> FlextSettings:
    """Provide a clean FlextSettings instance with test defaults.

    Resets the singleton first, then creates a fresh instance with
    debug=True for verbose test output.
    """
    FlextSettings.reset_for_testing()
    return FlextSettings(debug=True, trace=False)


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

    def _create(settings_cls: type[T], **overrides: str | float | bool | None) -> T:
        settings_cls.reset_for_testing()
        return settings_cls(**{k: v for k, v in overrides.items() if v is not None})

    return _create

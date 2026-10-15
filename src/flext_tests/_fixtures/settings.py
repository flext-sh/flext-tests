"""Centralized FlextSettings fixtures for all project test suites.

Provides:
- reset_settings: Fixture that resets FlextSettings singleton between tests
- settings: Base FlextSettings fixture with test defaults
- settings_factory: Factory fixture for creating project-specific settings

Eliminates duplicated reset_settings_singleton / _reset_instance patterns
found across flext-core, flext-oracle-wms, flext-target-oracle, flext-auth,
flext-cli, and other project conftest.py files.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import TYPE_CHECKING, Protocol, cast

import pytest
from flext_core import FlextContainer, FlextContext, FlextSettings, t

from flext_tests import u
from flext_tests._settings import FlextTestsSettings
from flext_tests.case import FlextTestsCase

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from pathlib import Path

    from flext_tests import m, p
    from flext_tests.base import FlextTestsServiceBase

# pytest registers shared fixture modules at configure time. Their public
# facades may load during registration; reset and binding happen during runtime.


class FixtureNodeRequest(Protocol):
    """Typed fixture-request boundary exposing the owning collection node.

    ``pytest.FixtureRequest.node`` is unannotated upstream and its concrete
    node type depends on the fixture scope; this protocol records the public
    contract the runtime fixture consumes.
    """

    @property
    def node(self) -> pytest.Item | pytest.Collector:
        """The item or collector owning the current fixture context."""
        ...


@pytest.fixture(scope="session")
def session_runtime(
    tmp_path_factory: pytest.TempPathFactory,
    run_namespace: m.Tests.TestNamespace,
) -> Iterator[p.Tests.SessionRuntime]:
    """Provide every installed consumer a lazy, isolated worker-session runtime.

    Pure tests never provision tools. Consumers lease one shared locked seed;
    Pytest teardown validates allocation identity before removing its owned area.
    Each xdist worker creates its own area, never borrowing another environment.

    Args:
        tmp_path_factory: Pytest temporary path factory for creating isolated
          directories.
        run_namespace: The test run namespace containing the unique token for this
          session.

    Yields:
        An instance of ``p.Tests.SessionRuntime`` representing the isolated session
          runtime.

    """
    directory = tmp_path_factory.mktemp(run_namespace.token)
    runtime = u.Tests.SessionRuntime(directory)
    try:
        yield runtime
    finally:
        runtime.close()


def _reset_runtime_state() -> None:
    """Reset root/test settings singletons and the DI container."""
    FlextSettings.reset_for_testing()
    importlib.import_module("flext_tests").FlextTestsSettings.reset_for_testing()
    FlextContainer.reset_for_testing()


def _bind_runtime_aliases(
    *,
    module: ModuleType,
    instance: FlextTestsCase | None,
) -> None:
    """Bind canonical FLEXT runtime aliases onto pytest class instances.

    Raises:
        TypeError: If ``not isinstance(service_type, type) or not
            issubclass(service_type, s)``.
        AttributeError: If a ``AttributeError`` is caught.

    """
    # A bare top-level module (e.g. a pytester probe file) has no package
    # contract: there is no package root to resolve aliases from, so the
    # binding scope does not apply. Package-based suites always enforce.
    package_root = module.__package__ or ""
    if not package_root:
        return
    # Function-style tests and plain-class suites obtain their state through
    # the fixtures alone, so the package alias contract is out of scope when
    # there is no runtime instance to bind: enforcing it here would reject
    # suites whose root package does not re-export the facade letters (e.g.
    # lazy generated component packages).
    if instance is None:
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


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Reset and bind the canonical runtime before each pytest function."""
    _reset_runtime_state()
    if not isinstance(item, pytest.Function):
        return
    module = item.module
    if not isinstance(module, ModuleType):
        return
    instance = item.instance
    _bind_runtime_aliases(
        module=module,
        instance=instance if isinstance(instance, FlextTestsCase) else None,
    )


def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item | None) -> None:
    """Reset the canonical runtime after each pytest function."""
    _ = item, nextitem
    _reset_runtime_state()


@pytest.fixture
def reset_settings() -> Iterator[None]:
    """Reset root + test settings singletons and the DI container.

    Prevents state leakage across tests by clearing both the root settings
    singleton, the test-settings singleton, and the container singleton.
    Runs as autouse so every test gets clean state automatically.
    """
    _reset_runtime_state()
    try:
        yield
    finally:
        _reset_runtime_state()


@pytest.fixture
def test_runtime(request: FixtureNodeRequest, reset_settings: None) -> None:
    """Bind the canonical FLEXT test runtime aliases onto pytest class instances.

    Args:
        request: The typed fixture request exposing the owning collection node.
        reset_settings: The autouse reset fixture sequencing runtime state.

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
    _bind_runtime_aliases(
        module=module,
        instance=instance if isinstance(instance, FlextTestsCase) else None,
    )


@pytest.fixture
def settings() -> FlextTestsSettings:
    """Provide a clean FlextTestsSettings instance with test defaults.

    Resets the root/test singletons first, then creates a fresh typed
    tests settings instance with verbose core defaults.

    Returns:
        The resulting ``FlextTestsSettings``.

    """
    settings_type: type[FlextTestsSettings] = importlib.import_module(
        "flext_tests",
    ).FlextTestsSettings
    FlextSettings.reset_for_testing()
    settings_type.reset_for_testing()
    return settings_type(debug=True, trace=False)


@pytest.fixture
def settings_factory() -> Callable[..., FlextSettings]:
    """Create project-specific settings instances in tests.

    Usage in test::

        def test_something(settings_factory):
            settings = settings_factory(FlextApiSettings, base_url="http://test")
            assert settings.base_url == "http://test"

    The factory resets the singleton for the given class before creating
    a new instance, ensuring test isolation.

    Returns:
        The resulting ``Callable[..., FlextSettings]``.

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
    """Provide the canonical FlextContext fixture for test runtimes.

    Returns:
        The resulting ``FlextContext``.

    """
    return FlextContext()


@pytest.fixture
def clean_container() -> Iterator[p.Container]:
    """Provide an isolated DI container for tests that mutate registrations.

    Yields:
        Each ``p.Container``.

    """
    FlextContainer.reset_for_testing()
    try:
        yield FlextContainer()
    finally:
        FlextContainer.reset_for_testing()


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Provide the canonical temporary directory fixture for tests.

    Returns:
        The resulting ``Path``.

    """
    return tmp_path


@pytest.fixture
def temp_file(temp_dir: Path) -> Path:
    """Provide the canonical temporary file path rooted at ``temp_dir``.

    Returns:
        The resulting ``Path``.

    """
    return temp_dir / "test_file.txt"


@pytest.fixture
def sample_data() -> t.JsonMapping:
    """Provide a small canonical JSON payload for generic test cases.

    Returns:
        The resulting ``t.JsonMapping``.

    """
    return {"string": "test_value", "number": 42, "enabled": True}

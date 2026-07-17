"""Structural contracts for Docker test models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from pathlib import Path

    from flext_tests import t


class FlextTestsDockerProtocolsMixin:
    """Read-only Docker contracts published under ``p.Tests``."""

    @runtime_checkable
    class ContainerConfig(Protocol):
        """Resolved Docker target configuration."""

        @property
        def container_name(self) -> str | None: ...

        @property
        def compose_file(self) -> Path | None: ...

        @property
        def service(self) -> str: ...

        @property
        def host(self) -> str: ...

        @property
        def port(self) -> int | None: ...

        @property
        def startup_timeout(self) -> int: ...

        @property
        def force_recreate(self) -> bool: ...

        def model_copy(
            self,
            *,
            update: t.MappingKV[str, t.JsonPayload] | None = None,
            deep: bool = False,
        ) -> FlextTestsDockerProtocolsMixin.ContainerConfig: ...

    @runtime_checkable
    class User(Protocol):
        """Test user data."""

        @property
        def id(self) -> str: ...

        @property
        def unique_id(self) -> str | None: ...

        @property
        def name(self) -> str: ...

        @property
        def email(self) -> str: ...

        @property
        def active(self) -> bool: ...

    @runtime_checkable
    class Config(Protocol):
        """Generic test configuration."""

        @property
        def service_type(self) -> str: ...

        @property
        def environment(self) -> str: ...

        @property
        def debug(self) -> bool: ...

        @property
        def log_level(self) -> str: ...

        @property
        def timeout(self) -> int: ...

        @property
        def max_retries(self) -> int: ...


__all__: tuple[str, ...] = ("FlextTestsDockerProtocolsMixin",)

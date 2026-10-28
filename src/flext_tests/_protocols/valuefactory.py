"""Protocols extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from contextlib import AbstractContextManager
    from pathlib import Path

    from flext_tests._typings.base import FlextTestsTypesBase


class FlextTestsProtocolsValueFactory:
    @runtime_checkable
    class RuntimeProvision(Protocol):
        """Provision one locked consumer through its canonical Make lifecycle."""

        def __call__(self, parent: Path) -> Path:
            """Return the physical checkout provisioned inside ``parent``."""
            ...

    @runtime_checkable
    class SessionRuntime(Protocol):
        """One lazy physical runtime per pytest session and worker."""

        directory: Path

        def lease(
            self,
            provision: FlextTestsProtocolsValueFactory.RuntimeProvision,
            *,
            mutable_environment: bool = False,
        ) -> AbstractContextManager[Path]:
            """Lease the stable source root; restore case changes on exit."""
            ...

    @runtime_checkable
    class EntityFactory[TEntity](Protocol):
        """Factory protocol that builds entity instances for test helpers.

        Methods:
            __call__: build a typed entity given name and value.

        """

        def __call__(
            self,
            *,
            name: str,
            value: FlextTestsTypesBase.Testobject,
        ) -> TEntity:
            """Build a typed entity instance."""
            ...

    @runtime_checkable
    class ValueFactory[TValue](Protocol):
        """Factory protocol that builds value objects for test helpers.

        Methods:
            __call__: build a typed value instance given data and count.

        """

        def __call__(self, *, data: str, count: int) -> TValue:
            """Build a typed value instance."""
            ...


__all__: list[str] = ["FlextTestsProtocolsValueFactory"]

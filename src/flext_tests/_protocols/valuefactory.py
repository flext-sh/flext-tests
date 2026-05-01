"""Protocols extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsValueFactoryProtocolsMixin:
    class EntityFactory[TEntity](Protocol):
        """Factory protocol that builds entity instances for test helpers.

        Methods:
            __call__: build a typed entity given name and value.

        """

        def __call__(
            self,
            *,
            name: str,
            value: t.Tests.Testobject,
        ) -> TEntity:
            """Build a typed entity instance."""
            ...

    class ValueFactory[TValue](Protocol):
        """Factory protocol that builds value objects for test helpers.

        Methods:
            __call__: build a typed value instance given data and count.

        """

        def __call__(self, *, data: str, count: int) -> TValue:
            """Build a typed value instance."""
            ...

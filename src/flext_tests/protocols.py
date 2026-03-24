"""Protocol definitions for FLEXT tests.

Provides FlextTestsProtocols, extending FlextProtocols with test-specific protocol
definitions. Currently serves as MRO parent for consumer project protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, TypeVar

from flext_core import FlextProtocols

from flext_tests import t

TEntity = TypeVar("TEntity")
TValue = TypeVar("TValue")


class FlextTestsProtocols(FlextProtocols):
    """Protocol definitions for FLEXT tests - extends FlextProtocols.

    Architecture: Extends FlextProtocols with test-specific protocol definitions.
    All base protocols from FlextProtocols are available through inheritance pattern.
    Protocols cannot import models - only other protocols and types.
    """

    class EntityFactory[TEntity](Protocol):
        """Factory protocol that builds test entity objects.

        Methods:
            __call__: build an entity instance given name/value.

        """

        def __call__(self, *, name: str, value: t.Tests.Testobject) -> TEntity:
            """Build an entity instance."""
            ...

    class ValueFactory[TValue](Protocol):
        """Factory protocol that builds value objects for test helpers.

        Methods:
            __call__: build a typed value instance given data and count.

        """

        def __call__(self, *, data: str, count: int) -> TValue:
            """Build a typed value instance."""
            ...

    class Tests:
        """Test-specific protocol definitions namespace.

        Protocol classes are defined on-demand as consumer projects require them.
        Base protocols from FlextProtocols.* are inherited automatically.
        """


p = FlextTestsProtocols
# Module-level aliases required by __init__.py lazy loading
EntityFactory = FlextTestsProtocols.EntityFactory
ValueFactory = FlextTestsProtocols.ValueFactory
__all__ = ["EntityFactory", "FlextTestsProtocols", "ValueFactory", "p"]

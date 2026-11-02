# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tests/_protocols/spec
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_tests._protocols import FlextTestsProtocolsDocker


class FlextTestsProtocolsSpec:
    """Own the structural model contracts declared by this module."""

    @runtime_checkable
    class ContainerSpec(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def containers(
            self,
        ) -> MutableMapping[str, FlextTestsProtocolsDocker.ContainerConfig]: ...
        @property
        def initializer_command(self) -> str | None: ...


__all__: list[str] = [
    "FlextTestsProtocolsSpec",
]

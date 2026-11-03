# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tests/_protocols/spec
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_tests._protocols import FlextTestsProtocolsDocker


class FlextTestsProtocolsSpec:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ContainerSpec(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def containers(self) -> Mapping[str, FlextTestsProtocolsDocker.ContainerConfig]:
            """Structural member projected from the owning model.

            Target name → container config; the target name is what CLI --target and
            the in-session plugin resolve.
            """
            ...

        @property
        def initializer_command(self) -> str | None:
            """Structural member projected from the owning model.

            Optional shell command run once after ensure, receiving the container
            environment readback as env vars.
            """
            ...


__all__: list[str] = [
    "FlextTestsProtocolsSpec",
]

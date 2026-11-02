"""Hook contracts of the Docker test lifecycle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import p

if TYPE_CHECKING:
    from flext_tests import c


class FlextTestsProtocolsDocker:
    """Callables the lifecycle invokes around one container."""

    @runtime_checkable
    class ContainerInitializer(Protocol):
        """Prepare a container the lifecycle has just created.

        Runs once per created container, under the exclusive lease, before the
        record is sealed. A failure leaves the record unsealed, so the next
        ensure recreates the container instead of reusing a partial one.
        """

        def __call__(self, info: p.Tests.ContainerInfo) -> p.Result[bool]:
            """Initialize the created container."""
            ...

    @runtime_checkable
    class ReadinessProbe(Protocol):
        """Report whether a container serves its callers.

        Polled until it succeeds with ``True`` or the target's
        ``startup_timeout`` passes; the last failure explains a timeout.
        """

        def __call__(self, info: p.Tests.ContainerInfo) -> p.Result[bool]:
            """Probe the container once."""
            ...

    @runtime_checkable
    class ContainerConfig(Protocol):
        """Structural data contract projected from the owning model."""

        container_name: str | None
        compose_file: Path | None
        service: str
        host: str
        port: int | None
        startup_timeout: int
        force_recreate: bool
        project_name: str | None
        fingerprint_inputs: tuple[Path, ...]
        secret_keys: tuple[str, ...]
        lock_timeout_seconds: float

    @runtime_checkable
    class ContainerInfo(Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        status: c.Tests.ContainerStatus
        ports: Mapping[str, str]
        image: str
        container_id: str
        image_id: str
        health: c.Tests.ContainerHealth

    @runtime_checkable
    class ContainerInspectHealth(Protocol):
        """Structural data contract projected from the owning model."""

        status: c.Tests.ContainerHealth

    @runtime_checkable
    class ContainerInspectState(Protocol):
        """Structural data contract projected from the owning model."""

        status: c.Tests.ContainerStatus
        health: p.Tests.ContainerInspectHealth | None

    @runtime_checkable
    class ContainerInspectConfig(Protocol):
        """Structural data contract projected from the owning model."""

        image: str
        env: Sequence[str] | None

    @runtime_checkable
    class ContainerInspectBinding(Protocol):
        """Structural data contract projected from the owning model."""

        host_port: str

    @runtime_checkable
    class ContainerInspectNetwork(Protocol):
        """Structural data contract projected from the owning model."""

        ports: Mapping[str, Sequence[p.Tests.ContainerInspectBinding] | None] | None

    @runtime_checkable
    class ContainerInspect(Protocol):
        """Structural data contract projected from the owning model."""

        id: str
        image_id: str
        state: p.Tests.ContainerInspectState
        config: p.Tests.ContainerInspectConfig
        network_settings: p.Tests.ContainerInspectNetwork

    @runtime_checkable
    class ContainerState(Protocol):
        """Structural data contract projected from the owning model."""

        container_name: str
        container_id: str
        fingerprint: str
        dirty: bool
        sealed: bool

    @runtime_checkable
    class User(Protocol):
        """Structural data contract projected from the owning model."""

        id: str
        unique_id: str | None
        name: str
        email: str
        active: bool

    @runtime_checkable
    class Config(Protocol):
        """Structural data contract projected from the owning model."""

        service_type: str
        environment: str
        debug: bool
        log_level: str
        timeout: int
        max_retries: int


__all__: list[str] = ["FlextTestsProtocolsDocker"]

"""Hook contracts of the Docker test lifecycle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from flext_cli import p

    from flext_tests._constants import FlextTestsConstantsDocker


class FlextTestsProtocolsDocker:
    """Callables the lifecycle invokes around one container."""

    @runtime_checkable
    class ContainerInitializer(Protocol):
        """Prepare a container the lifecycle has just created.

        Runs once per created container, under the exclusive lease, before the
        record is sealed. A failure leaves the record unsealed, so the next
        ensure recreates the container instead of reusing a partial one.
        """

        def __call__(
            self, info: (FlextTestsProtocolsDocker.ContainerInfo)
        ) -> p.Result[bool]:
            """Initialize the created container."""
            ...

    @runtime_checkable
    class ReadinessProbe(Protocol):
        """Report whether a container serves its callers.

        Polled until it succeeds with ``True`` or the target's
        ``startup_timeout`` passes; the last failure explains a timeout.
        """

        def __call__(
            self, info: (FlextTestsProtocolsDocker.ContainerInfo)
        ) -> p.Result[bool]:
            """Probe the container once."""
            ...

    @runtime_checkable
    class ContainerConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def container_name(self) -> str | None:
            """Optional managed container name for inspection."""
            ...

        @property
        def compose_file(self) -> Path | None:
            """Resolved docker-compose file path."""
            ...

        @property
        def service(self) -> str:
            """Compose service name to start."""
            ...

        @property
        def host(self) -> str:
            """Host used for readiness checks."""
            ...

        @property
        def port(self) -> int | None:
            """Structural member projected from the owning model.

            Container port the service listens on; its published host port is
            resolved from the running container.
            """
            ...

        @property
        def startup_timeout(self) -> int:
            """Bound for compose --wait and for readiness polling."""
            ...

        @property
        def force_recreate(self) -> bool:
            """Whether execute should recreate the target stack."""
            ...

        @property
        def project_name(self) -> str | None:
            """Compose project; the compose file stem when absent."""
            ...

        @property
        def fingerprint_inputs(self) -> tuple[Path, ...]:
            """Files hashed with the compose file into the seal."""
            ...

        @property
        def secret_keys(self) -> tuple[str, ...]:
            """Structural member projected from the owning model.

            Creation variables generated once per container and read back from it
            whenever compose runs again.
            """
            ...

        @property
        def lock_timeout_seconds(self) -> float:
            """Bound on waiting for other sessions' leases to mutate."""
            ...

    @runtime_checkable
    class ContainerInfo(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> str:
            """Container name."""
            ...

        @property
        def status(self) -> FlextTestsConstantsDocker.ContainerStatus:
            """Runtime lifecycle status."""
            ...

        @property
        def ports(self) -> Mapping[str, str]:
            """Published ports: '<port>/<proto>' to host port."""
            ...

        @property
        def image(self) -> str:
            """Configured image reference; may be empty."""
            ...

        @property
        def container_id(self) -> str:
            """Docker-assigned container identifier."""
            ...

        @property
        def image_id(self) -> str:
            """Resolved image identifier."""
            ...

        @property
        def health(self) -> FlextTestsConstantsDocker.ContainerHealth:
            """Healthcheck state; UNKNOWN without a check."""
            ...

    @runtime_checkable
    class ContainerInspectHealth(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def status(self) -> FlextTestsConstantsDocker.ContainerHealth:
            """Healthcheck status."""
            ...

    @runtime_checkable
    class ContainerInspectState(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def status(self) -> FlextTestsConstantsDocker.ContainerStatus:
            """Container lifecycle status."""
            ...

        @property
        def health(self) -> FlextTestsProtocolsDocker.ContainerInspectHealth | None:
            """Present when a check is set."""
            ...

    @runtime_checkable
    class ContainerInspectConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        image: str
        env: Sequence[str] | None

    @runtime_checkable
    class ContainerInspectBinding(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        host_port: str

    @runtime_checkable
    class ContainerInspectNetwork(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def ports(
            self,
        ) -> (
            Mapping[
                str, Sequence[FlextTestsProtocolsDocker.ContainerInspectBinding] | None
            ]
            | None
        ):
            """Bindings per '<port>/<proto>'."""
            ...

    @runtime_checkable
    class ContainerInspect(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        id: str
        image_id: str

        @property
        def state(self) -> FlextTestsProtocolsDocker.ContainerInspectState:
            """Lifecycle state."""
            ...

        @property
        def config(self) -> FlextTestsProtocolsDocker.ContainerInspectConfig:
            """Creation configuration."""
            ...

        @property
        def network_settings(self) -> FlextTestsProtocolsDocker.ContainerInspectNetwork:
            """Published ports."""
            ...

    @runtime_checkable
    class ContainerState(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def container_name(self) -> str:
            """Docker container name; also the record file stem."""
            ...

        @property
        def container_id(self) -> str:
            """Container id the lifecycle sealed; empty if none."""
            ...

        @property
        def fingerprint(self) -> str:
            """Declared-input fingerprint sealed with the id."""
            ...

        @property
        def dirty(self) -> bool:
            """A session reported the container unusable."""
            ...

        @property
        def sealed(self) -> bool:
            """Creation and initialization completed for the id."""
            ...

    @runtime_checkable
    class User(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> str:
            """Opaque user identifier."""
            ...

        @property
        def unique_id(self) -> str | None:
            """Optional unique user identifier."""
            ...

        @property
        def name(self) -> str:
            """Display name."""
            ...

        @property
        def email(self) -> str:
            """Primary email address."""
            ...

        @property
        def active(self) -> bool:
            """True when the account is active."""
            ...

    @runtime_checkable
    class Config(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def service_type(self) -> str:
            """Service kind under test."""
            ...

        @property
        def environment(self) -> str:
            """Target environment label."""
            ...

        @property
        def debug(self) -> bool:
            """Enable verbose debug output."""
            ...

        @property
        def log_level(self) -> str:
            """Logging level name."""
            ...

        @property
        def timeout(self) -> int:
            """Request timeout in seconds."""
            ...

        @property
        def max_retries(self) -> int:
            """Retry budget on transient failure."""
            ...


__all__: list[str] = ["FlextTestsProtocolsDocker"]

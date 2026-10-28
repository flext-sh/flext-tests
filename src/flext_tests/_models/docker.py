"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from flext_cli import m

from flext_tests import c, t


class FlextTestsModelsDocker:
    class ContainerConfig(m.Value):
        """Resolved Docker target configuration used by the public DSL."""

        container_name: Annotated[
            str | None,
            m.Field(description="Optional managed container name for inspection."),
        ] = None
        compose_file: Annotated[
            Path | None,
            m.Field(description="Resolved docker-compose file path."),
        ] = None
        service: Annotated[
            str,
            m.Field(description="Compose service name to start."),
        ] = ""
        host: Annotated[
            str,
            m.Field(min_length=1, description="Host used for readiness checks."),
        ] = c.LOCALHOST
        port: Annotated[
            int | None,
            m.Field(
                description=(
                    "Container port the service listens on; its published host "
                    "port is resolved from the running container."
                ),
            ),
        ] = None
        startup_timeout: Annotated[
            int,
            m.Field(
                ge=1,
                description="Bound for compose --wait and for readiness polling.",
            ),
        ] = 30
        force_recreate: Annotated[
            bool,
            m.Field(description="Whether execute should recreate the target stack."),
        ] = False
        project_name: Annotated[
            str | None,
            m.Field(description="Compose project; the compose file stem when absent."),
        ] = None
        fingerprint_inputs: Annotated[
            tuple[Path, ...],
            m.Field(description="Files hashed with the compose file into the seal."),
        ] = ()
        secret_keys: Annotated[
            tuple[str, ...],
            m.Field(
                description=(
                    "Creation variables generated once per container and read "
                    "back from it whenever compose runs again."
                ),
            ),
        ] = ()
        lock_timeout_seconds: Annotated[
            float,
            m.Field(
                gt=0,
                description="Bound on waiting for other sessions' leases to mutate.",
            ),
        ] = c.Tests.DOCKER_LEASE_TIMEOUT_SECONDS

    class ContainerInfo(m.Value):
        """Container information model."""

        name: Annotated[str, m.Field(min_length=1, description="Container name.")]
        status: Annotated[
            c.Tests.ContainerStatus,
            m.Field(description="Runtime lifecycle status."),
        ]
        ports: Annotated[
            t.StrMapping,
            m.Field(description="Published ports: '<port>/<proto>' to host port."),
        ]
        image: Annotated[
            str,
            m.Field(description="Configured image reference; may be empty."),
        ]
        container_id: Annotated[
            str,
            m.Field(description="Docker-assigned container identifier."),
        ] = ""
        image_id: Annotated[str, m.Field(description="Resolved image identifier.")] = ""
        health: Annotated[
            c.Tests.ContainerHealth,
            m.Field(description="Healthcheck state; UNKNOWN without a check."),
        ] = c.Tests.ContainerHealth.UNKNOWN

    class ContainerInspectHealth(m.FlexibleModel):
        """``State.Health`` of ``docker inspect``."""

        status: Annotated[
            c.Tests.ContainerHealth,
            m.Field(alias="Status", description="Healthcheck status."),
        ]

    class ContainerInspectState(m.FlexibleModel):
        """``State`` of ``docker inspect``."""

        status: Annotated[
            c.Tests.ContainerStatus,
            m.Field(alias="Status", description="Container lifecycle status."),
        ]
        health: Annotated[
            FlextTestsModelsDocker.ContainerInspectHealth | None,
            m.Field(alias="Health", description="Present when a check is set."),
        ] = None

    class ContainerInspectConfig(m.FlexibleModel):
        """``Config`` of ``docker inspect``."""

        image: Annotated[
            str,
            m.Field(alias="Image", description="Configured image reference."),
        ] = ""
        env: Annotated[
            t.StrSequence | None,
            m.Field(alias="Env", description="Environment as KEY=VALUE entries."),
        ] = None

    class ContainerInspectBinding(m.FlexibleModel):
        """One host binding of a published container port."""

        host_port: Annotated[
            str,
            m.Field(alias="HostPort", description="Published host port."),
        ] = ""

    class ContainerInspectNetwork(m.FlexibleModel):
        """``NetworkSettings`` of ``docker inspect``."""

        ports: Annotated[
            t.MappingKV[
                str,
                t.SequenceOf[FlextTestsModelsDocker.ContainerInspectBinding] | None,
            ]
            | None,
            m.Field(alias="Ports", description="Bindings per '<port>/<proto>'."),
        ] = None

    class ContainerInspect(m.FlexibleModel):
        """The subset of ``docker inspect`` the lifecycle reads."""

        id: Annotated[str, m.Field(alias="Id", description="Container id.")]
        image_id: Annotated[
            str,
            m.Field(alias="Image", description="Resolved image id."),
        ]
        state: Annotated[
            FlextTestsModelsDocker.ContainerInspectState,
            m.Field(alias="State", description="Lifecycle state."),
        ]
        config: Annotated[
            FlextTestsModelsDocker.ContainerInspectConfig,
            m.Field(alias="Config", description="Creation configuration."),
        ]
        network_settings: Annotated[
            FlextTestsModelsDocker.ContainerInspectNetwork,
            m.Field(alias="NetworkSettings", description="Published ports."),
        ]

    class ContainerState(m.Value):
        """Host-scoped lifecycle record of one shared test container.

        A name without a record is unprovisioned: no id, no fingerprint, clean
        and unsealed. Every checkout of the host reads the same record.
        """

        container_name: Annotated[
            str,
            m.Field(
                pattern=c.Tests.DOCKER_CONTAINER_NAME_PATTERN,
                description="Docker container name; also the record file stem.",
            ),
        ]
        container_id: Annotated[
            str,
            m.Field(description="Container id the lifecycle sealed; empty if none."),
        ] = ""
        fingerprint: Annotated[
            str,
            m.Field(description="Declared-input fingerprint sealed with the id."),
        ] = ""
        dirty: Annotated[
            bool,
            m.Field(description="A session reported the container unusable."),
        ] = False
        sealed: Annotated[
            bool,
            m.Field(description="Creation and initialization completed for the id."),
        ] = False

    class User(m.Value):
        """Test user model - immutable value object."""

        id: Annotated[str, m.Field(description="Opaque user identifier.")]
        unique_id: Annotated[
            str | None,
            m.Field(description="Optional unique user identifier."),
        ] = None
        name: Annotated[str, m.Field(description="Display name.")]
        email: Annotated[str, m.Field(description="Primary email address.")]
        active: Annotated[
            bool,
            m.Field(description="True when the account is active."),
        ] = True

    class Config(m.Value):
        """Test configuration model - immutable value object."""

        service_type: Annotated[
            str,
            m.Field(description="Service kind under test."),
        ] = "api"
        environment: Annotated[
            str,
            m.Field(description="Target environment label."),
        ] = "test"
        debug: Annotated[bool, m.Field(description="Enable verbose debug output.")] = (
            True
        )
        log_level: Annotated[str, m.Field(description="Logging level name.")] = "DEBUG"
        timeout: Annotated[int, m.Field(description="Request timeout in seconds.")] = 30
        max_retries: Annotated[
            int,
            m.Field(description="Retry budget on transient failure."),
        ] = 3


__all__: list[str] = ["FlextTestsModelsDocker"]

"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from flext_infra import m, u

from flext_tests import c, t


class FlextTestsDockerModelsMixin:
    class ContainerConfig(m.Value):
        """Resolved Docker target configuration used by the public DSL."""

        container_name: Annotated[
            str | None,
            u.Field(description="Optional managed container name for inspection."),
        ] = None
        compose_file: Annotated[
            Path | None,
            u.Field(description="Resolved docker-compose file path."),
        ] = None
        service: Annotated[
            str,
            u.Field(description="Compose service name to start."),
        ] = ""
        host: Annotated[
            str,
            u.Field(min_length=1, description="Host used for readiness checks."),
        ] = c.LOCALHOST
        port: Annotated[
            int | None,
            u.Field(
                description=(
                    "Container port the service listens on; its published host "
                    "port is resolved from the running container."
                ),
            ),
        ] = None
        startup_timeout: Annotated[
            int,
            u.Field(
                ge=1,
                description="Bound for compose --wait and for readiness polling.",
            ),
        ] = 30
        force_recreate: Annotated[
            bool,
            u.Field(description="Whether execute should recreate the target stack."),
        ] = False
        project_name: Annotated[
            str | None,
            u.Field(description="Compose project; the compose file stem when absent."),
        ] = None
        fingerprint_inputs: Annotated[
            t.VariadicTuple[Path],
            u.Field(description="Files hashed with the compose file into the seal."),
        ] = ()
        lock_timeout_seconds: Annotated[
            float,
            u.Field(
                gt=0,
                description="Bound on waiting for other sessions' leases to mutate.",
            ),
        ] = c.Tests.DOCKER_LEASE_TIMEOUT_SECONDS

    class ContainerInfo(m.Value):
        """Container information model."""

        name: Annotated[str, u.Field(min_length=1, description="Container name.")]
        status: Annotated[
            c.Tests.ContainerStatus,
            u.Field(description="Runtime lifecycle status."),
        ]
        ports: Annotated[
            t.StrMapping,
            u.Field(description="Published ports: '<port>/<proto>' to host port."),
        ]
        image: Annotated[
            str,
            u.Field(description="Configured image reference; may be empty."),
        ]
        container_id: Annotated[
            str,
            u.Field(description="Docker-assigned container identifier."),
        ] = ""
        image_id: Annotated[str, u.Field(description="Resolved image identifier.")] = ""
        health: Annotated[
            c.Tests.ContainerHealth,
            u.Field(description="Healthcheck state; UNKNOWN without a check."),
        ] = c.Tests.ContainerHealth.UNKNOWN

    class ContainerInspectHealth(m.FlexibleModel):
        """``State.Health`` of ``docker inspect``."""

        status: Annotated[
            c.Tests.ContainerHealth,
            u.Field(alias="Status", description="Healthcheck status."),
        ]

    class ContainerInspectState(m.FlexibleModel):
        """``State`` of ``docker inspect``."""

        status: Annotated[
            c.Tests.ContainerStatus,
            u.Field(alias="Status", description="Container lifecycle status."),
        ]
        health: Annotated[
            FlextTestsDockerModelsMixin.ContainerInspectHealth | None,
            u.Field(alias="Health", description="Present when a check is set."),
        ] = None

    class ContainerInspectConfig(m.FlexibleModel):
        """``Config`` of ``docker inspect``."""

        image: Annotated[
            str,
            u.Field(alias="Image", description="Configured image reference."),
        ] = ""
        env: Annotated[
            t.StrSequence | None,
            u.Field(alias="Env", description="Environment as KEY=VALUE entries."),
        ] = None

    class ContainerInspectBinding(m.FlexibleModel):
        """One host binding of a published container port."""

        host_port: Annotated[
            str,
            u.Field(alias="HostPort", description="Published host port."),
        ] = ""

    class ContainerInspectNetwork(m.FlexibleModel):
        """``NetworkSettings`` of ``docker inspect``."""

        ports: Annotated[
            t.MappingKV[
                str,
                t.SequenceOf[FlextTestsDockerModelsMixin.ContainerInspectBinding]
                | None,
            ]
            | None,
            u.Field(alias="Ports", description="Bindings per '<port>/<proto>'."),
        ] = None

    class ContainerInspect(m.FlexibleModel):
        """The subset of ``docker inspect`` the lifecycle reads."""

        id: Annotated[str, u.Field(alias="Id", description="Container id.")]
        image_id: Annotated[
            str,
            u.Field(alias="Image", description="Resolved image id."),
        ]
        state: Annotated[
            FlextTestsDockerModelsMixin.ContainerInspectState,
            u.Field(alias="State", description="Lifecycle state."),
        ]
        config: Annotated[
            FlextTestsDockerModelsMixin.ContainerInspectConfig,
            u.Field(alias="Config", description="Creation configuration."),
        ]
        network_settings: Annotated[
            FlextTestsDockerModelsMixin.ContainerInspectNetwork,
            u.Field(alias="NetworkSettings", description="Published ports."),
        ]

    class ContainerState(m.Value):
        """Host-scoped lifecycle record of one shared test container.

        A name without a record is unprovisioned: no id, no fingerprint, clean
        and unsealed. Every checkout of the host reads the same record.
        """

        container_name: Annotated[
            str,
            u.Field(
                pattern=c.Tests.DOCKER_CONTAINER_NAME_PATTERN,
                description="Docker container name; also the record file stem.",
            ),
        ]
        container_id: Annotated[
            str,
            u.Field(description="Container id the lifecycle sealed; empty if none."),
        ] = ""
        fingerprint: Annotated[
            str,
            u.Field(description="Declared-input fingerprint sealed with the id."),
        ] = ""
        dirty: Annotated[
            bool,
            u.Field(description="A session reported the container unusable."),
        ] = False
        sealed: Annotated[
            bool,
            u.Field(description="Creation and initialization completed for the id."),
        ] = False

    class User(m.Value):
        """Test user model - immutable value object."""

        id: Annotated[str, u.Field(description="Opaque user identifier.")]
        unique_id: Annotated[
            str | None,
            u.Field(description="Optional unique user identifier."),
        ] = None
        name: Annotated[str, u.Field(description="Display name.")]
        email: Annotated[str, u.Field(description="Primary email address.")]
        active: Annotated[
            bool,
            u.Field(description="True when the account is active."),
        ] = True

    class Config(m.Value):
        """Test configuration model - immutable value object."""

        service_type: Annotated[
            str,
            u.Field(description="Service kind under test."),
        ] = "api"
        environment: Annotated[
            str,
            u.Field(description="Target environment label."),
        ] = "test"
        debug: Annotated[bool, u.Field(description="Enable verbose debug output.")] = (
            True
        )
        log_level: Annotated[str, u.Field(description="Logging level name.")] = "DEBUG"
        timeout: Annotated[int, u.Field(description="Request timeout in seconds.")] = 30
        max_retries: Annotated[
            int,
            u.Field(description="Retry budget on transient failure."),
        ] = 3

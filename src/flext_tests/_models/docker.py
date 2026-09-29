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
            Path | None, u.Field(description="Resolved docker-compose file path.")
        ] = None
        service: Annotated[
            str, u.Field(description="Compose service name to start.")
        ] = ""
        host: Annotated[
            str, u.Field(min_length=1, description="Host used for readiness checks.")
        ] = c.LOCALHOST
        port: Annotated[
            int | None,
            u.Field(description="Optional host port used for readiness checks."),
        ] = None
        startup_timeout: Annotated[
            int, u.Field(ge=1, description="Maximum wait time for readiness checks.")
        ] = 30
        force_recreate: Annotated[
            bool,
            u.Field(description="Whether execute should recreate the target stack."),
        ] = False

    class ContainerInfo(m.Value):
        """Container information model."""

        name: Annotated[str, u.Field(min_length=1, description="Container name.")]
        status: Annotated[
            c.Tests.ContainerStatus, u.Field(description="Runtime lifecycle status.")
        ]
        ports: Annotated[
            t.StrMapping, u.Field(description="Port mapping (internal → external).")
        ]
        image: Annotated[str, u.Field(min_length=1, description="Source image tag.")]
        container_id: Annotated[
            str, u.Field(description="Docker-assigned container identifier.")
        ] = ""

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
            str, u.Field(description="Declared-input fingerprint sealed with the id.")
        ] = ""
        dirty: Annotated[
            bool, u.Field(description="A session reported the container unusable.")
        ] = False
        sealed: Annotated[
            bool,
            u.Field(description="Creation and initialization completed for the id."),
        ] = False

    class User(m.Value):
        """Test user model - immutable value object."""

        id: Annotated[str, u.Field(description="Opaque user identifier.")]
        unique_id: Annotated[
            str | None, u.Field(description="Optional unique user identifier.")
        ] = None
        name: Annotated[str, u.Field(description="Display name.")]
        email: Annotated[str, u.Field(description="Primary email address.")]
        active: Annotated[
            bool, u.Field(description="True when the account is active.")
        ] = True

    class Config(m.Value):
        """Test configuration model - immutable value object."""

        service_type: Annotated[
            str, u.Field(description="Service kind under test.")
        ] = "api"
        environment: Annotated[
            str, u.Field(description="Target environment label.")
        ] = "test"
        debug: Annotated[bool, u.Field(description="Enable verbose debug output.")] = (
            True
        )
        log_level: Annotated[str, u.Field(description="Logging level name.")] = "DEBUG"
        timeout: Annotated[int, u.Field(description="Request timeout in seconds.")] = 30
        max_retries: Annotated[
            int, u.Field(description="Retry budget on transient failure.")
        ] = 3

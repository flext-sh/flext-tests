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
        project_name: Annotated[
            str | None,
            u.Field(
                description=(
                    "Optional compose project name; derived from the compose "
                    "file stem when omitted."
                )
            ),
        ] = None
        fingerprint_inputs: Annotated[
            t.StrSequence,
            u.Field(
                description=(
                    "Tracked inputs (compose file plus optional extra paths) "
                    "hashed into the container-state fingerprint."
                )
            ),
        ] = ()
        lock_timeout_seconds: Annotated[
            float,
            u.Field(
                gt=0,
                description=(
                    "Bounded wait for the container host lock before failing."
                ),
            ),
        ] = 120.0

    class ContainerState(m.Value):
        """Host-scoped persistent state of one managed container.

        One JSON file per container under ``~/.flext/docker/`` carries this
        state; all checkouts on the host share it (the container is shared,
        so its state is too). ``sealed`` marks a container that came up
        healthy against a known fingerprint; ``dirty`` marks one a failing
        test run must not reuse.
        """

        container_name: Annotated[
            str, u.Field(min_length=1, description="Managed container name.")
        ]
        container_id: Annotated[
            str, u.Field(description="Docker container id at seal time.")
        ] = ""
        fingerprint: Annotated[
            str, u.Field(description="Tracked-inputs fingerprint at seal time.")
        ] = ""
        sealed: Annotated[
            bool, u.Field(description="True once verified healthy and sealed.")
        ] = False
        dirty: Annotated[
            bool, u.Field(description="True when a run marked the container dirty.")
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
        health: Annotated[
            str, u.Field(description="Healthcheck verdict (healthy/unhealthy/none).")
        ] = ""
        image_id: Annotated[
            str, u.Field(description="Docker-resolved image identifier.")
        ] = ""

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

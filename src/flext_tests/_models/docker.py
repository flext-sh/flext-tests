"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, override

from flext_core import FlextModels, u
from flext_tests import c, t


class FlextTestsDockerModelsMixin:
    class ContainerInfo(FlextModels.Value):
        """Container information model."""

        name: Annotated[
            str,
            u.Field(min_length=1, description="Container name."),
        ]
        status: Annotated[
            c.Tests.ContainerStatus,
            u.Field(description="Runtime lifecycle status."),
        ]
        ports: Annotated[
            t.StrMapping,
            u.Field(description="Port mapping (internal → external)."),
        ]
        image: Annotated[
            str,
            u.Field(min_length=1, description="Source image tag."),
        ]
        container_id: Annotated[
            str,
            u.Field(description="Docker-assigned container identifier."),
        ] = ""

    class ContainerConfig(FlextModels.Value):
        """Container configuration model."""

        compose_file: Annotated[
            Path,
            u.Field(description="Path to the docker-compose file."),
        ]
        service: Annotated[
            str,
            u.Field(min_length=1, description="Compose service name to target."),
        ]
        port: Annotated[
            int,
            u.Field(
                ge=c.DEFAULT_RETRY_DELAY_SECONDS,
                le=c.MAX_PORT,
                description="Host-side port exposed by the service.",
            ),
        ]

        @override
        def model_post_init(self, __context: t.JsonValue | None, /) -> None:
            """Validate compose-file path exists (file-system check)."""
            super().model_post_init(__context)
            if not self.compose_file.exists():
                msg = f"Compose file not found: {self.compose_file}"
                raise ValueError(msg)

    class ContainerState(FlextModels.Value):
        """Container state tracking model."""

        container_name: Annotated[
            str,
            u.Field(description="Container name being tracked."),
        ]
        is_dirty: Annotated[
            bool,
            u.Field(description="True when test state has mutated the container."),
        ]
        worker_id: Annotated[
            str,
            u.Field(description="Pytest-xdist worker that owns the state."),
        ]
        last_updated: Annotated[
            str | None,
            u.Field(description="ISO timestamp of last state change."),
        ] = None

    class User(FlextModels.Value):
        """Test user model - immutable value object."""

        id: Annotated[str, u.Field(description="Opaque user identifier.")]
        name: Annotated[str, u.Field(description="Display name.")]
        email: Annotated[str, u.Field(description="Primary email address.")]
        active: Annotated[
            bool,
            u.Field(description="True when the account is active."),
        ] = True

    class Config(FlextModels.Value):
        """Test configuration model - immutable value object."""

        service_type: Annotated[
            str,
            u.Field(description="Service kind under test."),
        ] = "api"
        environment: Annotated[
            str,
            u.Field(description="Target environment label."),
        ] = "test"
        debug: Annotated[
            bool,
            u.Field(description="Enable verbose debug output."),
        ] = True
        log_level: Annotated[
            str,
            u.Field(description="Logging level name."),
        ] = "DEBUG"
        timeout: Annotated[
            int,
            u.Field(description="Request timeout in seconds."),
        ] = 30
        max_retries: Annotated[
            int,
            u.Field(description="Retry budget on transient failure."),
        ] = 3

    class Service(FlextModels.Value):
        """Test service model - immutable value object."""

        id: Annotated[str, u.Field(description="Opaque service identifier.")]
        type: Annotated[
            str,
            u.Field(description="Service classification."),
        ] = "api"
        name: Annotated[
            str,
            u.Field(description="Human-readable service name."),
        ] = ""
        status: Annotated[
            str,
            u.Field(description="Lifecycle status."),
        ] = "active"

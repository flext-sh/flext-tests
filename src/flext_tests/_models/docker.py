"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_tests import c, t


class FlextTestsDockerModelsMixin:
    class ContainerInfo(FlextModels.Value):
        """Container information model."""

        name: str
        status: c.Tests.Docker.ContainerStatus
        ports: t.StrMapping
        image: str
        container_id: str = ""

        @override
        def model_post_init(self, __context: t.Container | None, /) -> None:
            """Validate container info after initialization."""
            super().model_post_init(__context)
            if not self.name:
                msg = "Container name cannot be empty"
                raise ValueError(msg)
            if not self.image:
                msg = "Container image cannot be empty"
                raise ValueError(msg)

    class ContainerConfig(FlextModels.Value):
        """Container configuration model."""

        compose_file: Path
        service: str
        port: int

        @override
        def model_post_init(self, __context: t.Container | None, /) -> None:
            """Validate container config after initialization."""
            super().model_post_init(__context)
            if not self.compose_file.exists():
                msg = f"Compose file not found: {self.compose_file}"
                raise ValueError(msg)
            if not self.service:
                msg = "Service name cannot be empty"
                raise ValueError(msg)
            if not (c.DEFAULT_RETRY_DELAY_SECONDS <= self.port <= c.MAX_PORT):
                msg = f"Port {self.port} out of valid range"
                raise ValueError(msg)

    class ContainerState(FlextModels.Value):
        """Container state tracking model."""

        container_name: str
        is_dirty: bool
        worker_id: str
        last_updated: str | None = None

    class User(FlextModels.Value):
        """Test user model - immutable value t.NormalizedValue."""

        id: str
        name: str
        email: str
        active: bool = True

    class Config(FlextModels.Value):
        """Test configuration model - immutable value t.NormalizedValue."""

        service_type: str = "api"
        environment: str = "test"
        debug: bool = True
        log_level: str = "DEBUG"
        timeout: int = 30
        max_retries: int = 3

    class Service(FlextModels.Value):
        """Test service model - immutable value t.NormalizedValue."""

        id: str
        type: str = "api"
        name: str = ""
        status: str = "active"

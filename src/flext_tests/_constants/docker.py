"""Docker test infrastructure constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from enum import StrEnum, unique
from typing import Final

from flext_tests import t


class FlextTestsDockerConstantsMixin:
    """Docker test infrastructure constants mixin."""

    SHARED_CONTAINERS: Final[Mapping[str, t.HeaderMapping]] = {
        "flext-oracle-db-test": {
            "compose_file": "docker/docker-compose.oracle-db.yml",
            "service": "oracle-db",
            "port": 1522,
            "host": "localhost",
            "container_name": "flext-oracle-db-test",
        },
    }

    @unique
    class ContainerStatus(StrEnum):
        """Container status enumeration for test infrastructure."""

        RUNNING = "running"
        STOPPED = "stopped"
        NOT_FOUND = "not_found"
        ERROR = "error"
        STARTING = "starting"
        STOPPING = "stopping"
        RESTARTING = "restarting"

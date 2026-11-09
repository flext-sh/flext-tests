"""Host-scoped leases and private Docker creation artifacts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import c


class FlextTestsUtilitiesDockerState:
    """Resolve the native assets and host service lease paths."""

    @staticmethod
    def docker_state_dir() -> Path:
        """Return the host directory for leases and private creation artifacts."""
        return Path.home().joinpath(*c.Tests.DOCKER_STATE_DIR_PARTS)

    @staticmethod
    def docker_shared_assets_dir() -> Path:
        """Return the packaged root the shared-container compose files resolve from."""
        return Path(__file__).resolve().parents[1] / c.Tests.DOCKER_SHARED_ASSETS_DIR

    @staticmethod
    def docker_lease_lock_file(state_dir: Path, container_name: str) -> Path:
        """Return the lock shared by the sessions that use one container."""
        return state_dir / f"{container_name}{c.Tests.DOCKER_LEASE_LOCK_SUFFIX}"


__all__: list[str] = ["FlextTestsUtilitiesDockerState"]

"""Docker container control facade for FLEXT test infrastructure."""

from __future__ import annotations

from flext_tests._docker_parts.docker_part_05 import (
    FlextTestsDocker as FlextTestsDockerPart05,
)


class FlextTestsDocker(FlextTestsDockerPart05):
    """Manage Docker containers for FLEXT tests."""


tk = FlextTestsDocker

__all__: list[str] = ["FlextTestsDocker", "tk"]

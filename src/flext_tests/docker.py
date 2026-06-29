"""Docker container control facade for FLEXT test infrastructure."""

from __future__ import annotations

from flext_tests._docker_parts.docker_part_06 import (
    FlextTestsDocker as FlextTestsDockerPart06,
)


class FlextTestsDocker(FlextTestsDockerPart06):
    """Manage Docker containers for FLEXT tests."""


tk = FlextTestsDocker

__all__: list[str] = ["FlextTestsDocker", "tk"]

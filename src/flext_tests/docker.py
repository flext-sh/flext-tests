"""Docker container control facade for FLEXT test infrastructure."""

from __future__ import annotations

from flext_tests._docker_parts.docker_part_06 import (
    FlextTestsDocker as FlextTestsDockerPart06,
)


class FlextTestsDocker(FlextTestsDockerPart06):
    """Manage Docker containers for FLEXT tests."""


# Resolve forward references now that the full MRO (incl. the runtime
# DockerSDKClient field type) is imported, so consumer packages can
# instantiate the service without a PydanticUserError.
FlextTestsDocker.model_rebuild()

tk = FlextTestsDocker

__all__: list[str] = ["FlextTestsDocker", "tk"]

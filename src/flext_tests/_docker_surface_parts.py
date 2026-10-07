"""Public Docker-surface verbs for FlextTestsDocker.

The verbs are composed into ``FlextTestsDocker`` as a parts mixin so the
public method count stays within the configured cap; the public surface is
unchanged.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_tests import r, u

if TYPE_CHECKING:
    from flext_tests import m, p, t


class _DockerFacadeInternals:
    """The facade-own internals the surface verbs delegate to.

    Declared unconditionally: annotations resolve lazily (PEP 563), so the
    TYPE_CHECKING-only ``m``/``p``/``t`` names never evaluate at runtime, and
    the audit's base walker demands class declarations outside conditionals.
    """

    def _compose_path(self, compose_file: str) -> Path: ...

    def _compose_down(self, compose_path: Path, project: str) -> p.Result[str]: ...

    def _compose_up(
        self,
        compose_path: Path,
        project: str,
        service: str | None,
        *,
        force_recreate: bool,
    ) -> p.Result[str]: ...

    def _inspect(
        self,
        container_name: str,
    ) -> p.Result[m.Tests.ContainerInspect]: ...


if TYPE_CHECKING:
    _PartsBase = _DockerFacadeInternals
else:
    _PartsBase = object


class FlextTestsDockerSurfaceParts(_PartsBase):
    """Public compose and container verbs of the Docker facade."""

    def compose_down(self, compose_file: str) -> p.Result[str]:
        """Remove the project of one compose file with its volumes.

        Returns:
            The resulting ``p.Result[str]``.
        """
        compose_path = self._compose_path(compose_file)
        return self._compose_down(
            compose_path,
            u.Tests.docker_compose_project(compose_path),
        )

    def compose_up(
        self,
        compose_file: str,
        service: str | None = None,
        *,
        force_recreate: bool = False,
    ) -> p.Result[str]:
        """Start the project of one compose file and wait for its health.

        Returns:
            The resulting ``p.Result[str]``.
        """
        compose_path = self._compose_path(compose_file)
        return self._compose_up(
            compose_path,
            u.Tests.docker_compose_project(compose_path),
            service,
            force_recreate=force_recreate,
        )

    def fetch_container_info(
        self,
        container_name: str,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Inspect one container; an absent one fails NOT_PROVISIONED.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.
        """
        return self._inspect(container_name).map(
            lambda inspect: u.Tests.container_info(container_name, inspect),
        )

    def fetch_container_status(
        self,
        container_name: str,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch container status.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.
        """
        return self.fetch_container_info(container_name)

    def fetch_container_environment(
        self,
        container_name: str,
        keys: t.StrSequence,
    ) -> p.Result[t.MappingKV[str, t.SecretStr]]:
        """Read named creation variables of a container as secrets.

        A key the container does not carry fails ``ENVIRONMENT_MISSING``,
        naming the key and never a value.

        Returns:
            The resulting ``p.Result[t.MappingKV[str, t.SecretStr]]``.
        """
        return self._inspect(container_name).flat_map(
            lambda inspect: u.Tests.container_environment(
                container_name,
                inspect,
                keys,
            ),
        )

    def start_compose_stack(
        self,
        compose_file: str,
        network_name: str | None = None,
    ) -> p.Result[str]:
        """Start a Docker Compose stack.

        Returns:
            The resulting ``p.Result[str]``.
        """
        _ = network_name
        result = self.compose_up(compose_file)
        if result.failure:
            return result.map_error(lambda error: f"Stack start failed: {error}")
        return r[str].ok("Stack started successfully")


__all__: list[str] = ["FlextTestsDockerSurfaceParts"]

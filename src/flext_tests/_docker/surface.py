"""Public Docker-surface verbs for FlextTestsDocker.

The verbs are composed into ``FlextTestsDocker`` as a parts mixin so the
public method count stays within the configured cap; the public surface is
unchanged.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from flext_tests import u

if TYPE_CHECKING:
    from flext_tests import p, t


class FlextTestsDockerSurface(ABC):
    """Public Docker verbs and the operations their concrete owner supplies."""

    @abstractmethod
    def _compose_path(self, _compose_file: str, /) -> Path:
        """Resolve the declared compose file."""

    @abstractmethod
    def _compose_down(self, _compose_path: Path, _project: str, /) -> p.Result[str]:
        """Remove the specified compose project."""

    @abstractmethod
    def _inspect(
        self,
        _container_name: str,
        /,
    ) -> p.Result[p.Tests.ContainerInspect]:
        """Read the container's inspect record."""

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

    def fetch_container_info(
        self,
        container_name: str,
    ) -> p.Result[p.Tests.ContainerInfo]:
        """Inspect one container; an absent one fails NOT_PROVISIONED.

        Returns:
            The resulting ``p.Result[p.Tests.ContainerInfo]``.

        """
        return self._inspect(container_name).map(
            lambda inspect: u.Tests.container_info(container_name, inspect),
        )

    def fetch_container_environment(
        self,
        container_name: str,
        keys: Sequence[str],
    ) -> p.Result[Mapping[str, t.SecretStr]]:
        """Read named creation variables of a container as secrets.

        A key the container does not carry fails ``ENVIRONMENT_MISSING``,
        naming the key and never a value.

        Returns:
            The resulting ``p.Result[Mapping[str, t.SecretStr]]``.

        """
        return self._inspect(container_name).flat_map(
            lambda inspect: u.Tests.container_environment(
                container_name,
                inspect,
                keys,
            ),
        )


__all__: list[str] = ["FlextTestsDockerSurface"]

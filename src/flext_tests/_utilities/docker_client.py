"""Docker SDK and compose client owner of the test container lifecycle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from pathlib import Path

from docker import DockerClient
from docker.constants import DEFAULT_DOCKER_API_VERSION
from docker.errors import DockerException, NotFound
from docker.utils import kwargs_from_env
from flext_cli import u
from python_on_whales import DockerClient as ComposeDockerClient

from flext_tests import c, m, p, r, t
from flext_tests._utilities import FlextTestsDockerLifecycleUtilitiesMixin


class FlextTestsDockerClientUtilitiesMixin:
    """One endpoint, chosen before connecting; failures keep their cause."""

    @staticmethod
    def docker_endpoint() -> str:
        """Resolve the daemon endpoint before any connection.

        ``DOCKER_HOST`` when configured, otherwise this user's rootless socket
        when present, otherwise the system socket.

        Returns:
            The endpoint URL every Docker client of the test run uses.

        """
        configured = kwargs_from_env().get("base_url")
        if configured is not None:
            return configured
        rootless = Path(f"/run/user/{os.getuid()}/docker.sock")
        if rootless.exists():
            return f"unix://{rootless}"
        return c.Tests.DOCKER_SYSTEM_HOST

    @staticmethod
    def docker_environment_file(directory: Path) -> Path:
        """Write the isolated test environment of Docker-provisioned tests.

        The file is generated per test, never the developer's untracked
        ``.env``: it declares the resolved daemon endpoint so every client
        the test starts talks to the same Docker.

        Returns:
            The written ``.env`` path inside ``directory``.

        """
        env_file = directory / ".env"
        endpoint = FlextTestsDockerClientUtilitiesMixin.docker_endpoint()
        _ = env_file.write_text(
            f"{c.Tests.DOCKER_HOST_VARIABLE}{c.Tests.DOCKER_ENV_SEPARATOR}{endpoint}\n",
            encoding="utf-8",
        )
        env_file.chmod(c.Tests.DOCKER_ENV_FILE_MODE)
        return env_file

    @staticmethod
    def docker_sdk_client() -> p.Result[t.Tests.DockerSdkClient]:
        """Connect to the resolved endpoint and prove the daemon answers a ping.

        Returns:
            The connected client, or a failure carrying the daemon error.

        """
        try:
            client = DockerClient(
                base_url=FlextTestsDockerClientUtilitiesMixin.docker_endpoint(),
                tls=kwargs_from_env().get("tls", False),
                version=DEFAULT_DOCKER_API_VERSION,
            )
        except DockerException as exc:
            return r[t.Tests.DockerSdkClient].fail_op("Connect Docker", exc)
        try:
            _ = client.ping()
        except (DockerException, OSError) as exc:
            client.close()
            return r[t.Tests.DockerSdkClient].fail_op("Ping Docker", exc)
        return r[t.Tests.DockerSdkClient].ok(client)

    @staticmethod
    def docker_inspect(
        client: t.Tests.DockerSdkClient,
        container_name: str,
    ) -> p.Result[m.Tests.ContainerInspect]:
        """Inspect one container; an absent one fails ``NOT_PROVISIONED``.

        Returns:
            The validated inspect payload, or the typed failure.

        """
        try:
            container = client.containers.get(container_name)
        except NotFound as exc:
            return r[m.Tests.ContainerInspect].fail(
                c.Tests.ERR_DOCKER_NOT_PROVISIONED.format(name=container_name),
                error_code=c.Tests.DockerErrorCode.NOT_PROVISIONED,
                exception=exc,
            )
        except (DockerException, OSError) as exc:
            return r[m.Tests.ContainerInspect].fail_op("Inspect container", exc)
        return u.try_(
            lambda: m.Tests.ContainerInspect.model_validate(container.attrs),
            catch=c.EXC_VALIDATION_VALUE,
            op_name=f"Parse docker inspect of {container_name}",
        )

    @staticmethod
    def docker_compose_client(
        compose_file: Path,
        project: str,
        env_files: t.VariadicTuple[Path] = (),
    ) -> t.Tests.ComposeClient:
        """Bind one compose file, its project and its env files to a client.

        Returns:
            The compose client for that project.

        """
        return ComposeDockerClient(
            client_type="docker",
            compose_files=[compose_file],
            compose_project_name=project,
            compose_env_files=list(env_files),
        )

    @staticmethod
    def docker_compose_up(
        target: m.Tests.ContainerConfig,
        env_files: t.VariadicTuple[Path],
        *,
        recreate: bool,
    ) -> p.Result[bool]:
        """Run compose up with --wait bounded by the target's startup timeout.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        compose_file = target.compose_file
        if compose_file is None:
            return r[bool].fail(c.Tests.ERR_DOCKER_TARGET_NOT_INSPECTABLE)
        client = FlextTestsDockerClientUtilitiesMixin.docker_compose_client(
            compose_file,
            target.project_name
            or FlextTestsDockerLifecycleUtilitiesMixin.docker_compose_project(
                compose_file,
            ),
            env_files,
        )
        try:
            if recreate:
                client.compose.down(remove_orphans=True, volumes=True)
            client.compose.up(
                services=[target.service] if target.service else None,
                detach=True,
                remove_orphans=True,
                recreate=recreate,
                wait=True,
                wait_timeout=target.startup_timeout,
                quiet=True,
            )
        except c.Tests.DOCKER_COMPOSE_ERRORS as exc:
            return r[bool].fail_op("Compose up", exc)
        return r[bool].ok(value=True)


__all__: list[str] = ["FlextTestsDockerClientUtilitiesMixin"]

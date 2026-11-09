"""Decisions and projections of the Docker test lifecycle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import secrets
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path

from flext_tests import c, m, p, r, t
from flext_tests._utilities import FlextTestsUtilitiesConfigHelpers


class FlextTestsUtilitiesDockerLifecycle:
    """Pure lifecycle rules over what Docker reports and what the host recorded."""

    @staticmethod
    def docker_compose_project(compose_file: Path) -> str:
        """Derive one compose project per compose file.

        Compose derives the project from the directory when none is given, so
        every file under a shared ``docker/`` directory would land in one
        project, and ``remove_orphans`` would delete a sibling suite's
        containers. Binding each file to its own project keeps
        ``remove_orphans`` scoped to the services that file declares.

        Returns:
            The resulting ``str``.

        """
        return compose_file.stem.replace(".", "-").replace("_", "-")

    @staticmethod
    def resolve_host_port(
        info: p.Tests.ContainerInfo,
        container_port: int,
    ) -> p.Result[int]:
        """Return the host port Docker published for a container TCP port."""
        host_port = info.ports.get(
            f"{container_port}{c.Tests.DOCKER_TCP_PORT_SUFFIX}",
            "",
        )
        if host_port.isdigit():
            return r[int].ok(int(host_port))
        return r[int].fail(
            c.Tests.ERR_DOCKER_PORT_NOT_PUBLISHED.format(
                name=info.name,
                port=container_port,
            ),
            error_code=c.Tests.DockerErrorCode.PORT_NOT_PUBLISHED,
        )

    @staticmethod
    def container_info(
        container_name: str,
        inspect: p.Tests.ContainerInspect,
    ) -> p.Tests.ContainerInfo:
        """Project ``docker inspect`` onto the lifecycle's container view.

        Returns:
            The resulting ``m.Tests.ContainerInfo``.

        """
        bindings = inspect.network_settings.ports or {}
        return m.Tests.ContainerInfo(
            name=container_name,
            status=c.Tests.ContainerStatus(inspect.state.status),
            ports={
                container_port: published[0].host_port
                for container_port, published in bindings.items()
                if published and published[0].host_port
            },
            image=inspect.config.image,
            container_id=inspect.id,
            image_id=inspect.image_id,
            health=c.Tests.ContainerHealth(
                inspect.state.health.status
                if inspect.state.health is not None
                else c.Tests.ContainerHealth.UNKNOWN,
            ),
        )

    @staticmethod
    def container_environment(
        container_name: str,
        inspect: p.Tests.ContainerInspect,
        keys: Sequence[str],
    ) -> p.Result[Mapping[str, t.SecretStr]]:
        """Read named variables from a container's creation environment.

        Returns:
            The resulting ``p.Result[Mapping[str, t.SecretStr]]``.

        """
        entries = dict(
            entry.split(c.Tests.DOCKER_ENV_SEPARATOR, 1)
            for entry in inspect.config.env or ()
            if c.Tests.DOCKER_ENV_SEPARATOR in entry
        )
        missing = [key for key in keys if key not in entries]
        if missing:
            return r[Mapping[str, t.SecretStr]].fail(
                c.Tests.ERR_DOCKER_ENVIRONMENT_MISSING.format(
                    name=container_name,
                    keys=", ".join(missing),
                ),
                error_code=c.Tests.DockerErrorCode.ENVIRONMENT_MISSING,
            )
        return r[Mapping[str, t.SecretStr]].ok({
            key: t.SecretStr(entries[key]) for key in keys
        })

    @staticmethod
    def generate_creation_secrets(
        keys: Sequence[str],
    ) -> Mapping[str, t.SecretStr]:
        """Generate one fresh secret per declared creation key.

        Returns:
            The resulting ``Mapping[str, t.SecretStr]``.

        """
        return {
            key: t.SecretStr(secrets.token_urlsafe(c.Tests.DOCKER_SECRET_BYTES))
            for key in keys
        }

    @staticmethod
    def validate_creation_environment(
        environment: Mapping[str, t.SecretStr],
    ) -> p.Result[bool]:
        """Reject a creation value a compose env file cannot carry literally.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        for key, secret in environment.items():
            value = secret.get_secret_value()
            if any(mark in value for mark in c.Tests.DOCKER_ENV_FORBIDDEN_MARKS):
                return r[bool].fail(c.Tests.ERR_DOCKER_ENV_VALUE.format(key=key))
        return r[bool].ok(value=True)

    @staticmethod
    @contextmanager
    def creation_env_file(
        state_dir: Path,
        container_name: str,
        environment: Mapping[str, t.SecretStr],
    ) -> Generator[tuple[Path, ...]]:
        """Expose creation-only values to compose through a private env file.

        The file is created 0600 next to the host records, exists only inside
        the block and is removed on exit. A leftover file from an interrupted
        run fails the creation instead of being overwritten. Yields the env
        files to pass to compose: none when there is nothing to expose.

        Yields:
            Each ``tuple[Path, ...]``.

        Raises:
            OSError: If ``failure is None``.

        """
        if not environment:
            yield ()
            return
        _ = FlextTestsUtilitiesDockerLifecycle.validate_creation_environment(
            environment,
        ).unwrap()
        lines = [
            f"{key}='{secret.get_secret_value()}'"
            for key, secret in environment.items()
        ]
        env_file = state_dir / f"{container_name}{c.Tests.DOCKER_ENV_FILE_SUFFIX}"
        state_dir.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(
            env_file,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            c.Tests.DOCKER_ENV_FILE_MODE,
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            _ = handle.write("".join(f"{line}\n" for line in lines))
        failure: BaseException | None = None
        try:
            with FlextTestsUtilitiesConfigHelpers.env_vars_context({
                key: secret.get_secret_value() for key, secret in environment.items()
            }):
                yield (env_file,)
        except BaseException as exc:
            failure = exc
            raise
        finally:
            try:
                env_file.unlink()
            except OSError as cleanup_error:
                if failure is None:
                    raise
                failure.add_note(f"creation env file cleanup failed: {cleanup_error}")


__all__: list[str] = ["FlextTestsUtilitiesDockerLifecycle"]

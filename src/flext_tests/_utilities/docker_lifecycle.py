"""Decisions and projections of the Docker test lifecycle."""

from __future__ import annotations

import hashlib
import os
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from flext_infra import u

from flext_core import r
from flext_tests import c, m, p, t


class FlextTestsDockerLifecycleUtilitiesMixin:
    """Pure lifecycle rules over what Docker reports and what the host recorded."""

    @staticmethod
    def docker_action(
        info: m.Tests.ContainerInfo | None,
        state: m.Tests.ContainerState,
        *,
        fingerprint: str,
    ) -> c.Tests.ContainerAction:
        """Decide what an ensure does with a container and its host record.

        A missing container is created. A dirty, unsealed, unhealthy or foreign
        container, or one sealed for other declared inputs, is recreated. A
        stopped container that matches its seal is started. A running one that
        matches is reused, including while its healthcheck is still starting:
        the ensure then waits for the check to settle.
        """
        if info is None:
            return c.Tests.ContainerAction.CREATE
        if (
            state.dirty
            or not state.sealed
            or state.fingerprint != fingerprint
            or state.container_id != info.container_id
            or info.health == c.Tests.ContainerHealth.UNHEALTHY
        ):
            return c.Tests.ContainerAction.RECREATE
        if info.status == c.Tests.ContainerStatus.RUNNING:
            return c.Tests.ContainerAction.REUSE
        if info.status in {
            c.Tests.ContainerStatus.EXITED,
            c.Tests.ContainerStatus.CREATED,
        }:
            return c.Tests.ContainerAction.START
        return c.Tests.ContainerAction.RECREATE

    @staticmethod
    def docker_verify(
        info: m.Tests.ContainerInfo | None,
        state: m.Tests.ContainerState,
        *,
        fingerprint: str,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Check without effects that the running container is the sealed one."""
        codes = c.Tests.DockerErrorCode
        name = state.container_name
        if info is None:
            return r[m.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_NOT_PROVISIONED.format(name=name),
                error_code=codes.NOT_PROVISIONED,
            )
        if state.dirty:
            return r[m.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_DIRTY.format(name=name), error_code=codes.DIRTY
            )
        if not state.sealed or state.container_id != info.container_id:
            return r[m.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_UNSEALED.format(
                    name=name, container_id=info.container_id
                ),
                error_code=codes.UNSEALED,
            )
        if state.fingerprint != fingerprint:
            return r[m.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_FINGERPRINT_MISMATCH.format(
                    name=name, sealed=state.fingerprint, current=fingerprint
                ),
                error_code=codes.FINGERPRINT_MISMATCH,
            )
        if info.status != c.Tests.ContainerStatus.RUNNING or info.health not in {
            c.Tests.ContainerHealth.HEALTHY,
            c.Tests.ContainerHealth.UNKNOWN,
        }:
            return r[m.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_UNHEALTHY.format(
                    name=name, status=info.status, health=info.health
                ),
                error_code=codes.UNHEALTHY,
            )
        return r[m.Tests.ContainerInfo].ok(info)

    @staticmethod
    def docker_compose_project(compose_file: Path) -> str:
        """Derive one compose project per compose file.

        Compose derives the project from the directory when none is given, so
        every file under a shared ``docker/`` directory would land in one
        project, and ``remove_orphans`` would delete a sibling suite's
        containers. Binding each file to its own project keeps
        ``remove_orphans`` scoped to the services that file declares.
        """
        return compose_file.stem.replace(".", "-").replace("_", "-")

    @staticmethod
    def docker_fingerprint(target: m.Tests.ContainerConfig) -> p.Result[str]:
        """Hash the declared inputs of a target: project, service and file bytes.

        The process environment is never an input: two checkouts that declare
        the same files compute the same fingerprint.
        """
        compose_file = target.compose_file
        if compose_file is None:
            return r[str].fail(c.Tests.ERR_DOCKER_TARGET_NOT_INSPECTABLE)
        digest = hashlib.sha256()
        project = target.project_name or (
            FlextTestsDockerLifecycleUtilitiesMixin.docker_compose_project(compose_file)
        )
        for part in (project, target.service):
            digest.update(part.encode())
            digest.update(c.Tests.DOCKER_FINGERPRINT_SEPARATOR)
        for input_file in (compose_file, *target.fingerprint_inputs):
            read = u.Cli.files_read_binary(input_file)
            if read.failure:
                return r[str].from_failure(read)
            digest.update(
                len(read.value).to_bytes(c.Tests.DOCKER_FINGERPRINT_SIZE_BYTES)
            )
            digest.update(read.value)
        return r[str].ok(digest.hexdigest())

    @staticmethod
    def resolve_host_port(
        info: m.Tests.ContainerInfo, container_port: int
    ) -> p.Result[int]:
        """Return the host port Docker published for a container TCP port."""
        host_port = info.ports.get(
            f"{container_port}{c.Tests.DOCKER_TCP_PORT_SUFFIX}", ""
        )
        if host_port.isdigit():
            return r[int].ok(int(host_port))
        return r[int].fail(
            c.Tests.ERR_DOCKER_PORT_NOT_PUBLISHED.format(
                name=info.name, port=container_port
            ),
            error_code=c.Tests.DockerErrorCode.PORT_NOT_PUBLISHED,
        )

    @staticmethod
    def container_info(
        container_name: str, inspect: m.Tests.ContainerInspect
    ) -> m.Tests.ContainerInfo:
        """Project ``docker inspect`` onto the lifecycle's container view."""
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
                else c.Tests.ContainerHealth.UNKNOWN
            ),
        )

    @staticmethod
    def container_environment(
        container_name: str, inspect: m.Tests.ContainerInspect, keys: t.StrSequence
    ) -> p.Result[t.MappingKV[str, t.SecretStr]]:
        """Read named variables from a container's creation environment."""
        entries = dict(
            entry.split(c.Tests.DOCKER_ENV_SEPARATOR, 1)
            for entry in inspect.config.env or ()
            if c.Tests.DOCKER_ENV_SEPARATOR in entry
        )
        missing = [key for key in keys if key not in entries]
        if missing:
            return r[t.MappingKV[str, t.SecretStr]].fail(
                c.Tests.ERR_DOCKER_ENVIRONMENT_MISSING.format(
                    name=container_name, keys=", ".join(missing)
                ),
                error_code=c.Tests.DockerErrorCode.ENVIRONMENT_MISSING,
            )
        return r[t.MappingKV[str, t.SecretStr]].ok({
            key: t.SecretStr(entries[key]) for key in keys
        })

    @staticmethod
    def validate_creation_environment(
        environment: t.MappingKV[str, t.SecretStr],
    ) -> p.Result[bool]:
        """Reject a creation value a compose env file cannot carry literally."""
        for key, secret in environment.items():
            value = secret.get_secret_value()
            if any(mark in value for mark in c.Tests.DOCKER_ENV_FORBIDDEN_MARKS):
                return r[bool].fail(c.Tests.ERR_DOCKER_ENV_VALUE.format(key=key))
        return r[bool].ok(True)

    @staticmethod
    @contextmanager
    def creation_env_file(
        state_dir: Path, container_name: str, environment: t.MappingKV[str, t.SecretStr]
    ) -> Generator[t.VariadicTuple[Path]]:
        """Expose creation-only values to compose through a private env file.

        The file is created 0600 next to the host records, exists only inside
        the block and is removed on exit. A leftover file from an interrupted
        run fails the creation instead of being overwritten. Yields the env
        files to pass to compose: none when there is nothing to expose.
        """
        if not environment:
            yield ()
            return
        _ = FlextTestsDockerLifecycleUtilitiesMixin.validate_creation_environment(
            environment
        ).unwrap()
        lines = [
            f"{key}='{secret.get_secret_value()}'"
            for key, secret in environment.items()
        ]
        env_file = state_dir / f"{container_name}{c.Tests.DOCKER_ENV_FILE_SUFFIX}"
        state_dir.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(
            env_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, c.Tests.DOCKER_ENV_FILE_MODE
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            _ = handle.write("".join(f"{line}\n" for line in lines))
        failure: BaseException | None = None
        try:
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

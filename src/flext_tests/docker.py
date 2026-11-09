"""Docker container control facade for FLEXT test infrastructure.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
import time
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated, Self, override

from flext_tests import c, m, p, r, s, t, u
from flext_tests._docker import FlextTestsDockerSurface


class FlextTestsDocker(FlextTestsDockerSurface, s[p.Tests.ContainerInfo]):
    """Prepare explicitly selected services without replacing existing data.

    Native Compose and live inspection own runtime identity. The host directory
    holds only leases and private creation artifacts; no cache authorizes reset.
    """

    repository_root: Annotated[
        Path,
        m.Field(description="Workspace root used to resolve compose files."),
    ] = m.Field(default_factory=Path.cwd)

    state_dir: Annotated[
        Path,
        m.Field(
            description="Host directory for leases and private creation artifacts."
        ),
    ] = m.Field(default_factory=u.Tests.docker_state_dir)

    docker_client: Annotated[
        t.Port[t.Tests.DockerSdkClient] | None,
        m.Field(exclude=True, description="Cached Docker SDK client instance."),
    ] = None

    target_config: Annotated[
        m.Tests.ContainerConfig | None,
        m.Field(description="Configured Docker target used by the public DSL."),
    ] = None

    @staticmethod
    def shared_target_config(
        container_name: str,
    ) -> p.Tests.ContainerConfig:
        """Resolve one shared-container entry into the canonical target config.

        Its compose file resolves from the packaged shared assets, never from
        the caller's checkout.

        Returns:
            The resulting ``m.Tests.ContainerConfig``.

        Raises:
            ValueError: If Unknown shared container; or if Shared container.

        """
        settings = c.Tests.SHARED_CONTAINERS.get(container_name)
        if settings is None:
            msg = f"Unknown shared container: {container_name}"
            raise ValueError(msg)
        compose_file_raw = settings.get("compose_file")
        if not compose_file_raw:
            msg = f"Shared container '{container_name}' missing compose_file"
            raise ValueError(msg)
        target = m.Tests.ContainerConfig.model_validate({
            **settings,
            "compose_file": Path(str(compose_file_raw)),
        })
        compose_path = u.Tests.docker_shared_assets_dir() / str(compose_file_raw)
        return target.model_copy(
            update={"container_name": container_name, "compose_file": compose_path},
        )

    @property
    def client(self) -> p.Result[t.Tests.DockerSdkClient]:
        """Docker client connected on first use through ``u.Tests.docker_sdk_client``.

        Returns:
            The connected client, or the daemon failure with its cause.

        """
        if self.docker_client is None:
            connected = u.Tests.docker_sdk_client()
            if connected.failure:
                return connected
            self.docker_client = connected.value
        return r[t.Tests.DockerSdkClient].ok(self.docker_client)

    @override
    def _compose_path(self, compose_file: str) -> Path:
        """Resolve a compose path against the configured workspace root.

        Returns:
            The resulting ``Path``.

        """
        compose_path = Path(compose_file)
        return (
            compose_path
            if compose_path.is_absolute()
            else self.repository_root / compose_file
        )

    @override
    def _compose_down(self, compose_path: Path, project: str) -> p.Result[str]:
        """Remove one compose project with its volumes.

        Returns:
            The resulting ``p.Result[str]``.

        """
        client = u.Tests.docker_compose_client(compose_path, project)
        try:
            client.compose.down(volumes=True, remove_orphans=True)
        except c.Tests.DOCKER_COMPOSE_ERRORS as exc:
            return r[str].fail_op("Compose down", exc)
        return r[str].ok("Compose down successful")

    def _compose_up(
        self,
        compose_path: Path,
        project: str,
        service: str | None,
    ) -> p.Result[str]:
        """Start one compose project and wait for its health.

        Returns:
            The resulting ``p.Result[str]``.

        """
        client = u.Tests.docker_compose_client(compose_path, project)
        try:
            # An EMPTY service list is a python-on-whales no-op; None is every
            # service. `wait` returns only once started services are healthy
            # (or running without a healthcheck); `quiet` keeps compose output
            # in the raised exception.
            client.compose.up(
                services=[service] if service else None,
                detach=True,
                recreate=False,
                wait=True,
                quiet=True,
            )
        except c.Tests.DOCKER_COMPOSE_ERRORS as exc:
            self.logger.exception("Compose up failed")
            return r[str].fail_op("Compose up", exc)
        return r[str].ok("Compose up successful")

    @override
    def _inspect(self, container_name: str) -> p.Result[p.Tests.ContainerInspect]:
        """Inspect one container; an absent one fails NOT_PROVISIONED.

        Returns:
            The resulting ``p.Result[p.Tests.ContainerInspect]``.

        """
        client = self.client
        if client.failure:
            return r[p.Tests.ContainerInspect].from_failure(client)
        return u.Tests.docker_inspect(client.value, container_name)

    @staticmethod
    def wait_for_port_ready(
        host: str,
        port: int,
        max_wait: float | None = None,
    ) -> p.Result[bool]:
        """Poll until a TCP port accepts connections or the bound passes.

        The bound is wall-clock, so connection attempts count against it.
        Without ``max_wait`` the ``DOCKER_PROBE_MAX_WAIT_SECONDS`` budget applies.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        probe_budget = (
            max_wait if max_wait is not None else c.Tests.DOCKER_PROBE_MAX_WAIT_SECONDS
        )
        deadline = time.monotonic() + probe_budget
        while True:
            try:
                with socket.create_connection(
                    (host, port),
                    timeout=c.Tests.DOCKER_TCP_CONNECT_TIMEOUT_SECONDS,
                ):
                    return r[bool].ok(value=True)
            except OSError as exc:
                if time.monotonic() >= deadline:
                    return r[bool].fail(
                        f"TCP {host}:{port} not ready within {probe_budget}s: {exc}",
                        exception=exc,
                    )
            time.sleep(c.Tests.DOCKER_HEALTH_POLL_SECONDS)

    @classmethod
    def shared(
        cls,
        container_name: str,
        *,
        repository_root: Path | None = None,
        state_dir: Path | None = None,
    ) -> Self:
        """Build a DSL-configured service from a shared container constant.

        Returns:
            The resulting ``Self``.

        """
        return cls(
            repository_root=repository_root or Path.cwd(),
            state_dir=state_dir or u.Tests.docker_state_dir(),
            target_config=cls.shared_target_config(container_name),
        )

    @classmethod
    def compose(
        cls,
        compose_file: str | Path,
        *,
        target: p.Tests.ContainerConfig | None = None,
        repository_root: Path | None = None,
        state_dir: Path | None = None,
    ) -> Self:
        """Build a DSL-configured service for an explicit compose target.

        Returns:
            The resulting ``Self``.

        """
        resolved_root = repository_root or Path.cwd()
        compose_path = Path(compose_file)
        if not compose_path.is_absolute():
            compose_path = resolved_root / compose_path
        base_target = target or m.Tests.ContainerConfig()
        return cls(
            repository_root=resolved_root,
            state_dir=state_dir or u.Tests.docker_state_dir(),
            target_config=base_target.model_copy(update={"compose_file": compose_path}),
        )

    @classmethod
    def stack(
        cls,
        compose_file: str | Path,
        *,
        target: p.Tests.ContainerConfig | None = None,
        repository_root: Path | None = None,
        state_dir: Path | None = None,
    ) -> Self:
        """Build a DSL-configured service for a compose stack target.

        Returns:
            The resulting ``Self``.

        """
        return cls.compose(
            compose_file,
            target=target,
            repository_root=repository_root,
            state_dir=state_dir,
        )

    def up(self) -> p.Result[str]:
        """Start the configured compose target using the DSL state.

        Returns:
            The resulting ``p.Result[str]``.

        """
        target = self.target_config
        if target is None:
            return r[str].fail(c.Tests.ERR_DOCKER_TARGET_MISSING)
        if target.compose_file is None:
            return r[str].fail("Docker target has no compose file configured.")
        return self._compose_up(
            target.compose_file,
            target.project_name or u.Tests.docker_compose_project(target.compose_file),
            target.service or None,
        )

    def down(self) -> p.Result[str]:
        """Stop the configured compose target using the DSL state.

        Returns:
            The resulting ``p.Result[str]``.

        """
        target = self.target_config
        if target is None:
            return r[str].fail(c.Tests.ERR_DOCKER_TARGET_MISSING)
        if target.compose_file is None:
            return r[str].fail("Docker target has no compose file configured.")
        return self._compose_down(
            target.compose_file,
            target.project_name or u.Tests.docker_compose_project(target.compose_file),
        )

    def ready(
        self,
        *,
        port: int | None = None,
        max_wait: int | None = None,
    ) -> p.Result[bool]:
        """Probe the configured host and port, as given, until it accepts TCP.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        target = self.target_config
        if target is None:
            return r[bool].fail(c.Tests.ERR_DOCKER_TARGET_MISSING)
        resolved_port = target.port if port is None else port
        if resolved_port is None:
            return r[bool].fail(
                f"Docker target {target.container_name} has no configured "
                f"readiness port.",
            )
        return self.wait_for_port_ready(
            target.host,
            resolved_port,
            max_wait=target.startup_timeout if max_wait is None else max_wait,
        )

    def _target_error(self) -> str | None:
        """Explain why the configured target cannot run the lifecycle.

        Returns:
            The resulting ``str | None``.

        """
        target = self.target_config
        if target is None:
            return c.Tests.ERR_DOCKER_TARGET_MISSING
        if not target.container_name or target.compose_file is None:
            return c.Tests.ERR_DOCKER_TARGET_NOT_INSPECTABLE
        if not target.service:
            return "Docker target has no selected Compose service"
        return None

    @contextmanager
    def lease(self) -> Generator[None]:
        """Hold the shared session lease of the configured container.

        Sessions that use a container hold its lease; a recreation waits for
        every lease to be released, up to the target's lock timeout. An
        ``execute`` that must mutate cannot run inside its own session's
        lease: ensure first, then lease.

        Raises:
            ValueError: If ``target is None or target.container_name is None or error is
                not None``.

        """
        target = self.target_config
        error = self._target_error()
        if target is None or target.container_name is None or error is not None:
            raise ValueError(error)
        with u.Tests.FileLock(
            u.Tests.docker_lease_lock_file(self.state_dir, target.container_name),
            shared=True,
            timeout_seconds=target.lock_timeout_seconds,
        ):
            yield

    @override
    def execute(
        self,
        *,
        initializer: p.Tests.ContainerInitializer | None = None,
        readiness_probe: p.Tests.ReadinessProbe | None = None,
        creation_environment: Mapping[str, t.SecretStr] | None = None,
    ) -> p.Result[p.Tests.ContainerInfo]:
        """Create a missing selected service and preserve an existing container.

        Creation and start use Compose with --no-recreate under the exclusive
        lease. Drift and unhealthy services fail without resetting their data.
        ``creation_environment`` is used only when the service is absent.

        Returns:
            The resulting ``p.Result[p.Tests.ContainerInfo]``.

        """
        target = self.target_config
        error = self._target_error()
        if target is None or target.container_name is None or error is not None:
            return r[p.Tests.ContainerInfo].fail(error)
        environment = creation_environment or {}
        owned = sorted(set(environment).intersection(target.secret_keys))
        if owned:
            return r[p.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_GENERATED_KEYS.format(
                    name=target.container_name,
                    keys=", ".join(owned),
                ),
            )
        validated = u.Tests.validate_creation_environment(environment)
        if validated.failure:
            return r[p.Tests.ContainerInfo].from_failure(validated)
        try:
            with u.Tests.FileLock(
                u.Tests.docker_lease_lock_file(self.state_dir, target.container_name),
                timeout_seconds=target.lock_timeout_seconds,
            ):
                return self._ensure_present(target, initializer, environment).flat_map(
                    lambda info: self._serve(target, info, readiness_probe),
                )
        except TimeoutError as exc:
            return r[p.Tests.ContainerInfo].fail(
                str(exc),
                error_code=c.Tests.DockerErrorCode.LOCK_TIMEOUT,
                exception=exc,
            )

    def _ensure_present(
        self,
        target: p.Tests.ContainerConfig,
        initializer: p.Tests.ContainerInitializer | None,
        environment: Mapping[str, t.SecretStr],
    ) -> p.Result[p.Tests.ContainerInfo]:
        """Create only an absent selected service; preserve an existing identity.

        Returns:
            The inspected container or its original preparation failure.

        """
        name = target.container_name or ""
        fetched = self.fetch_container_info(name)
        if (
            fetched.failure
            and fetched.error_code == c.Tests.DockerErrorCode.NOT_PROVISIONED
        ):
            fetched = self._create_selected(target, initializer, environment)
        if fetched.failure:
            return fetched
        checked = self._check_declaration(target, fetched.value)
        if checked.failure:
            return r[p.Tests.ContainerInfo].from_failure(checked)
        if fetched.value.status in {
            c.Tests.ContainerStatus.EXITED,
            c.Tests.ContainerStatus.CREATED,
        }:
            return self._start_existing(target, name)
        return fetched

    def _create_selected(
        self,
        target: p.Tests.ContainerConfig,
        initializer: p.Tests.ContainerInitializer | None,
        environment: Mapping[str, t.SecretStr],
    ) -> p.Result[p.Tests.ContainerInfo]:
        """Prepare the selected absent service with native creation secrets.

        Returns:
            Its inspected identity after the creation-only initializer.

        """
        name = target.container_name or ""
        with u.Tests.creation_env_file(
            self.state_dir,
            name,
            {**environment, **u.Tests.generate_creation_secrets(target.secret_keys)},
        ) as env_files:
            created = u.Tests.docker_compose_up(target, env_files)
        if created.failure:
            return r[p.Tests.ContainerInfo].from_failure(created)
        fetched = self.fetch_container_info(name)
        if fetched.failure or initializer is None:
            return fetched
        return initializer(fetched.value).map(lambda _: fetched.value)

    def _start_existing(
        self,
        target: p.Tests.ContainerConfig,
        container_name: str,
    ) -> p.Result[p.Tests.ContainerInfo]:
        """Start a stopped existing container with the secrets it was created with.

        Compose recreates a container whose declared values differ, so the
        start passes back exactly the values read from the container.

        Returns:
            The resulting ``p.Result[p.Tests.ContainerInfo]``.

        """
        kept = self.fetch_container_environment(container_name, target.secret_keys)
        if kept.failure:
            return r[p.Tests.ContainerInfo].from_failure(kept)
        with u.Tests.creation_env_file(
            self.state_dir,
            container_name,
            kept.value,
        ) as env_files:
            started = u.Tests.docker_compose_up(target, env_files)
        return started.flat_map(lambda _: self.fetch_container_info(container_name))

    def _check_declaration(
        self,
        target: p.Tests.ContainerConfig,
        info: p.Tests.ContainerInfo,
    ) -> p.Result[bool]:
        """Compare Compose's resolved declaration with the existing runtime.

        Returns:
            Success or the drift facet, without exposing environment values.

        """
        compose_file = target.compose_file
        if compose_file is None:
            return r[bool].fail(c.Tests.ERR_DOCKER_TARGET_NOT_INSPECTABLE)
        inspected = self._inspect(info.name)
        if inspected.failure:
            return r[bool].from_failure(inspected)
        environment = dict(
            entry.split("=", 1)
            for entry in inspected.value.config.env or ()
            if "=" in entry
        )
        with u.Tests.env_vars_context(environment):
            client = u.Tests.docker_compose_client(
                compose_file,
                target.project_name or u.Tests.docker_compose_project(compose_file),
            )
            try:
                declared = client.compose.config()
            except c.Tests.DOCKER_COMPOSE_ERRORS as exc:
                return r[bool].fail_op("Resolve Compose declaration", exc)
        service = (declared.services or {}).get(target.service)
        if service is None:
            return r[bool].fail(f"Compose service is not declared: {target.service}")
        return u.Tests.docker_declaration_matches(service, info, inspected.value)

    def _serve(
        self,
        target: p.Tests.ContainerConfig,
        info: p.Tests.ContainerInfo,
        readiness_probe: p.Tests.ReadinessProbe | None,
    ) -> p.Result[p.Tests.ContainerInfo]:
        """Wait, within startup_timeout, for health, the published port and probe.

        Returns:
            The resulting ``p.Result[p.Tests.ContainerInfo]``.

        """
        deadline = time.monotonic() + target.startup_timeout
        settled = self._await_health(info, deadline, target.startup_timeout)
        if settled.failure:
            return settled
        current = settled.value
        if current.status != c.Tests.ContainerStatus.RUNNING or current.health not in {
            c.Tests.ContainerHealth.HEALTHY,
            c.Tests.ContainerHealth.UNKNOWN,
        }:
            return r[p.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_UNHEALTHY.format(
                    name=current.name,
                    status=current.status,
                    health=current.health,
                ),
                error_code=c.Tests.DockerErrorCode.UNHEALTHY,
            )
        if target.port is not None:
            listening = self._await_port(target, current, deadline)
            if listening.failure:
                return r[p.Tests.ContainerInfo].from_failure(listening)
        if readiness_probe is not None:
            probed = self._poll_readiness(
                current,
                readiness_probe,
                deadline,
                target.startup_timeout,
            )
            if probed.failure:
                return r[p.Tests.ContainerInfo].from_failure(probed)
        return r[p.Tests.ContainerInfo].ok(current)

    def _await_port(
        self,
        target: p.Tests.ContainerConfig,
        info: p.Tests.ContainerInfo,
        deadline: float,
    ) -> p.Result[bool]:
        """Wait for the published host port of the target's container port.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        host_port = u.Tests.resolve_host_port(info, target.port or 0)
        if host_port.failure:
            return r[bool].from_failure(host_port)
        listening = self.wait_for_port_ready(
            target.host,
            host_port.value,
            max_wait=deadline - time.monotonic(),
        )
        if listening.failure:
            return r[bool].fail(
                c.Tests.ERR_DOCKER_READINESS_TIMEOUT.format(
                    name=info.name,
                    timeout=target.startup_timeout,
                    detail=listening.error,
                ),
                error_code=c.Tests.DockerErrorCode.READINESS_TIMEOUT,
                exception=listening.exception,
            )
        return listening

    def _await_health(
        self,
        info: p.Tests.ContainerInfo,
        deadline: float,
        timeout: int,
    ) -> p.Result[p.Tests.ContainerInfo]:
        """Poll a starting healthcheck until it settles or the deadline passes.

        Returns:
            The resulting ``p.Result[p.Tests.ContainerInfo]``.

        """
        current = info
        while current.health == c.Tests.ContainerHealth.STARTING:
            if time.monotonic() >= deadline:
                return r[p.Tests.ContainerInfo].fail(
                    c.Tests.ERR_DOCKER_READINESS_TIMEOUT.format(
                        name=current.name,
                        timeout=timeout,
                        detail="healthcheck still starting",
                    ),
                    error_code=c.Tests.DockerErrorCode.READINESS_TIMEOUT,
                )
            time.sleep(c.Tests.DOCKER_HEALTH_POLL_SECONDS)
            refreshed = self.fetch_container_info(current.name)
            if refreshed.failure:
                return refreshed
            current = refreshed.value
        return r[p.Tests.ContainerInfo].ok(current)

    @staticmethod
    def _poll_readiness(
        info: p.Tests.ContainerInfo,
        readiness_probe: p.Tests.ReadinessProbe,
        deadline: float,
        timeout: int,
    ) -> p.Result[bool]:
        """Poll a readiness probe until it reports True or the deadline passes.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        while True:
            probed = readiness_probe(info)
            if probed.success and probed.value:
                return r[bool].ok(value=True)
            detail = probed.error if probed.failure else "probe reported not ready"
            if time.monotonic() >= deadline:
                return r[bool].fail(
                    c.Tests.ERR_DOCKER_READINESS_TIMEOUT.format(
                        name=info.name,
                        timeout=timeout,
                        detail=detail,
                    ),
                    error_code=c.Tests.DockerErrorCode.READINESS_TIMEOUT,
                )
            time.sleep(c.Tests.DOCKER_HEALTH_POLL_SECONDS)

    def verify(
        self,
        *,
        readiness_probe: p.Tests.ReadinessProbe | None = None,
        required_environment: Sequence[str] = (),
    ) -> p.Result[p.Tests.ContainerInfo]:
        """Check, without changing anything, that the container is usable.

        Reports native declaration drift, readiness and environment failures.
        Verification never creates, starts or replaces a service.

        Returns:
            The resulting ``p.Result[p.Tests.ContainerInfo]``.

        """
        target = self.target_config
        error = self._target_error()
        if target is None or target.container_name is None or error is not None:
            return r[p.Tests.ContainerInfo].fail(error)
        try:
            with self.lease():
                return self.fetch_container_info(target.container_name).flat_map(
                    lambda info: (
                        self
                        ._check_declaration(target, info)
                        .flat_map(
                            lambda _: self.fetch_container_environment(
                                info.name, required_environment
                            )
                        )
                        .flat_map(lambda _: self._serve(target, info, readiness_probe))
                    ),
                )
        except TimeoutError as exc:
            return r[p.Tests.ContainerInfo].fail(
                str(exc),
                error_code=c.Tests.DockerErrorCode.LOCK_TIMEOUT,
                exception=exc,
            )


tk: type[FlextTestsDocker] = FlextTestsDocker
"""Docker container control facade alias for flext_tests."""

__all__: list[str] = ["FlextTestsDocker", "tk"]

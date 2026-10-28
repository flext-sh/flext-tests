"""Docker container control facade for FLEXT test infrastructure.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import socket
import time
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated, Self, override

from flext_infra import config as infra_config, settings as infra_settings

from flext_tests import FlextTestsDockerSurface, c, m, p, r, s, t, u


class FlextTestsDocker(FlextTestsDockerSurface, s[m.Tests.ContainerInfo]):
    """Manage the Docker containers FLEXT tests share.

    One container per name serves the whole host. Its record under
    ``state_dir`` says which container the lifecycle created and sealed, for
    which declared inputs, and whether a session reported it unusable.
    ``execute`` decides under a shared lease and mutates only under the
    exclusive one; ``verify`` checks without effects. Under the Make CI token
    every Docker effect fails with ``DISABLED_BY_CI``.
    """

    repository_root: Annotated[
        Path,
        m.Field(description="Workspace root used to resolve compose files."),
    ] = m.Field(default_factory=Path.cwd)

    state_dir: Annotated[
        Path,
        m.Field(description="Host directory of the container state records."),
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
    def ci_disables_docker() -> bool:
        """Return True when the Make CI token (not GitHub's CI=true) is active.

        Returns:
            The resulting ``bool``.

        """
        ci = infra_config.Infra.codegen.make.ci
        return (infra_settings.env_lookup(ci.variable) or "").strip() == ci.value

    @classmethod
    def lifecycle_enabled(cls) -> p.Result[bool]:
        """Gate every Docker effect: fail ``DISABLED_BY_CI`` under the CI token.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        if not cls.ci_disables_docker():
            return r[bool].ok(value=True)
        ci = infra_config.Infra.codegen.make.ci
        return r[bool].fail(
            c.Tests.ERR_DOCKER_DISABLED_BY_CI.format(
                variable=ci.variable,
                value=ci.value,
            ),
            error_code=c.Tests.DockerErrorCode.DISABLED_BY_CI,
        )

    @staticmethod
    def shared_target_config(
        container_name: str,
    ) -> m.Tests.ContainerConfig:
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

    @property
    def dirty_containers(self) -> Sequence[str]:
        """Names of the host's containers marked dirty, in name order."""
        states = u.Tests.list_container_states(self.state_dir).unwrap()
        return tuple(state.container_name for state in states if state.dirty)

    def mark_container_clean(self, container_name: str) -> p.Result[bool]:
        """Mark a container clean in the host record.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        return self._record_dirty(container_name, dirty=False)

    def mark_container_dirty(self, container_name: str) -> p.Result[bool]:
        """Mark a container dirty so the next ensure recreates it.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        return self._record_dirty(container_name, dirty=True)

    def _record_dirty(self, container_name: str, *, dirty: bool) -> p.Result[bool]:
        """Rewrite the dirty flag of one host record.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        updated = u.Tests.update_container_state(
            self.state_dir,
            container_name,
            lambda state: state.model_copy(update={"dirty": dirty}),
        )
        if updated.failure:
            return r[bool].from_failure(updated)
        self.logger.info(
            "Container dirty flag set",
            container=container_name,
            dirty=dirty,
        )
        return r[bool].ok(value=True)

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
        enabled = self.lifecycle_enabled()
        if enabled.failure:
            return r[str].from_failure(enabled)
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
        *,
        force_recreate: bool,
    ) -> p.Result[str]:
        """Start one compose project and wait for its health.

        Returns:
            The resulting ``p.Result[str]``.

        """
        enabled = self.lifecycle_enabled()
        if enabled.failure:
            return r[str].from_failure(enabled)
        client = u.Tests.docker_compose_client(compose_path, project)
        try:
            if force_recreate:
                client.compose.down(remove_orphans=True, volumes=True)
            # An EMPTY service list is a python-on-whales no-op; None is every
            # service. `wait` returns only once started services are healthy
            # (or running without a healthcheck); `quiet` keeps compose output
            # in the raised exception.
            client.compose.up(
                services=[service] if service else None,
                detach=True,
                remove_orphans=True,
                wait=True,
                quiet=True,
            )
        except c.Tests.DOCKER_COMPOSE_ERRORS as exc:
            self.logger.exception("Compose up failed")
            return r[str].fail_op("Compose up", exc)
        return r[str].ok("Compose up successful")

    @override
    def _inspect(self, container_name: str) -> p.Result[m.Tests.ContainerInspect]:
        """Inspect one container; an absent one fails NOT_PROVISIONED.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInspect]``.

        """
        client = self.client
        if client.failure:
            return r[m.Tests.ContainerInspect].from_failure(client)
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
        target: m.Tests.ContainerConfig | None = None,
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
        target: m.Tests.ContainerConfig | None = None,
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
            force_recreate=target.force_recreate,
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

    def cleanup_dirty_containers(self) -> p.Result[Sequence[str]]:
        """Recreate every dirty shared container of the host.

        Each one goes through the same locked lifecycle as ``execute``. A dirty
        record whose name is not a declared shared container belongs to the
        lifecycle that declares it and is left untouched. The first failure is
        returned.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        enabled = self.lifecycle_enabled()
        if enabled.failure:
            return r[Sequence[str]].from_failure(enabled)
        cleaned: list[str] = []
        for container_name in self.dirty_containers:
            if container_name not in c.Tests.SHARED_CONTAINERS:
                continue
            self.logger.info("Recreating dirty container", container=container_name)
            recreated = FlextTestsDocker.shared(
                container_name,
                repository_root=self.repository_root,
                state_dir=self.state_dir,
            ).execute()
            if recreated.failure:
                return r[Sequence[str]].from_failure(recreated)
            cleaned.append(container_name)
        return r[Sequence[str]].ok(tuple(cleaned))

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
        return None

    def fingerprint(
        self,
        target: m.Tests.ContainerConfig | None = None,
    ) -> p.Result[str]:
        """Fingerprint a target's declared inputs; the configured one by default.

        Returns:
            The resulting ``p.Result[str]``.

        """
        resolved = target or self.target_config
        if resolved is None:
            return r[str].fail(c.Tests.ERR_DOCKER_TARGET_MISSING)
        return u.Tests.docker_fingerprint(resolved)

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

    def _observe(
        self,
        container_name: str,
    ) -> p.Result[tuple[m.Tests.ContainerInfo | None, m.Tests.ContainerState]]:
        """Read the container (absent is None) and its host record.

        Returns:
            The resulting ``p.Result[tuple[m.Tests.ContainerInfo | None,
                m.Tests.ContainerState]]``.

        """
        state = u.Tests.read_container_state(self.state_dir, container_name)
        if state.failure:
            return r[
                tuple[m.Tests.ContainerInfo | None, m.Tests.ContainerState]
            ].from_failure(state)
        info = self.fetch_container_info(container_name)
        if info.success:
            return r[tuple[m.Tests.ContainerInfo | None, m.Tests.ContainerState]].ok((
                info.value,
                state.value,
            ))
        if info.error_code == c.Tests.DockerErrorCode.NOT_PROVISIONED:
            return r[tuple[m.Tests.ContainerInfo | None, m.Tests.ContainerState]].ok((
                None,
                state.value,
            ))
        return r[
            tuple[m.Tests.ContainerInfo | None, m.Tests.ContainerState]
        ].from_failure(info)

    @override
    def execute(
        self,
        *,
        initializer: p.Tests.ContainerInitializer | None = None,
        readiness_probe: p.Tests.ReadinessProbe | None = None,
        creation_environment: Mapping[str, t.SecretStr] | None = None,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Ensure the configured container exists, is sealed, healthy and ready.

        Decides under a shared lease and reuses a matching container there. To
        create, start or recreate it takes the exclusive lease (waiting at most
        ``lock_timeout_seconds`` for other sessions), decides again, runs
        compose with ``--wait``, runs ``initializer`` once on a created
        container, seals the record and then waits for readiness.
        ``creation_environment`` reaches compose only while it creates.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

        """
        target = self.target_config
        error = self._target_error()
        if target is None or target.container_name is None or error is not None:
            return r[m.Tests.ContainerInfo].fail(error)
        environment = creation_environment or {}
        owned = sorted(set(environment).intersection(target.secret_keys))
        if owned:
            return r[m.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_GENERATED_KEYS.format(
                    name=target.container_name,
                    keys=", ".join(owned),
                ),
            )
        preflight = (
            self
            .lifecycle_enabled()
            .flat_map(lambda _: u.Tests.validate_creation_environment(environment))
            .flat_map(lambda _: u.Tests.docker_fingerprint(target))
        )
        if preflight.failure:
            return r[m.Tests.ContainerInfo].from_failure(preflight)
        fingerprint = preflight.value
        try:
            return self._ensure_leased(
                fingerprint,
                initializer,
                readiness_probe,
                environment,
            )
        except TimeoutError as exc:
            return r[m.Tests.ContainerInfo].fail(
                str(exc),
                error_code=c.Tests.DockerErrorCode.LOCK_TIMEOUT,
                exception=exc,
            )

    def _ensure_leased(
        self,
        fingerprint: str,
        initializer: p.Tests.ContainerInitializer | None,
        readiness_probe: p.Tests.ReadinessProbe | None,
        environment: Mapping[str, t.SecretStr],
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Reuse under the shared lease, otherwise converge under the exclusive one.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

        """
        target = self.target_config
        error = self._target_error()
        if target is None or target.container_name is None or error is not None:
            return r[m.Tests.ContainerInfo].fail(error)
        container_name = target.container_name
        lease_file = u.Tests.docker_lease_lock_file(self.state_dir, container_name)
        with u.Tests.FileLock(
            lease_file,
            shared=True,
            timeout_seconds=target.lock_timeout_seconds,
        ):
            observed = self._observe(container_name)
            if observed.failure:
                return r[m.Tests.ContainerInfo].from_failure(observed)
            info, state = observed.value
            action = u.Tests.docker_action(info, state, fingerprint=fingerprint)
            if (
                info is not None
                and action == c.Tests.ContainerAction.REUSE
                and not target.force_recreate
            ):
                return self._serve(target, info, readiness_probe)
        with u.Tests.FileLock(lease_file, timeout_seconds=target.lock_timeout_seconds):
            converged = self._converge(
                target,
                container_name,
                fingerprint,
                initializer,
                environment,
            )
            if converged.failure:
                return converged
            return self._serve(target, converged.value, readiness_probe)

    def _start_sealed(
        self,
        target: m.Tests.ContainerConfig,
        container_name: str,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Start a stopped sealed container with the secrets it was created with.

        Compose recreates a container whose declared values differ, so the
        start passes back exactly the values read from the container.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

        """
        kept = self.fetch_container_environment(container_name, target.secret_keys)
        if kept.failure:
            return r[m.Tests.ContainerInfo].from_failure(kept)
        with u.Tests.creation_env_file(
            self.state_dir,
            container_name,
            kept.value,
        ) as env_files:
            started = u.Tests.docker_compose_up(target, env_files, recreate=False)
        return started.flat_map(lambda _: self.fetch_container_info(container_name))

    def _converge(
        self,
        target: m.Tests.ContainerConfig,
        container_name: str,
        fingerprint: str,
        initializer: p.Tests.ContainerInitializer | None,
        environment: Mapping[str, t.SecretStr],
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Under the exclusive lease, decide again and apply the decision.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

        """
        observed = self._observe(container_name)
        if observed.failure:
            return r[m.Tests.ContainerInfo].from_failure(observed)
        info, state = observed.value
        action = (
            c.Tests.ContainerAction.RECREATE
            if target.force_recreate and info is not None
            else u.Tests.docker_action(info, state, fingerprint=fingerprint)
        )
        if info is not None and action == c.Tests.ContainerAction.REUSE:
            return r[m.Tests.ContainerInfo].ok(info)
        if action == c.Tests.ContainerAction.START:
            return self._start_sealed(target, container_name)
        unsealed = u.Tests.update_container_state(
            self.state_dir,
            container_name,
            lambda _: m.Tests.ContainerState(container_name=container_name),
        )
        if unsealed.failure:
            return r[m.Tests.ContainerInfo].from_failure(unsealed)
        with u.Tests.creation_env_file(
            self.state_dir,
            container_name,
            {
                **environment,
                **u.Tests.generate_creation_secrets(target.secret_keys),
            },
        ) as env_files:
            created = u.Tests.docker_compose_up(
                target,
                env_files,
                recreate=action == c.Tests.ContainerAction.RECREATE,
            )
        if created.failure:
            return r[m.Tests.ContainerInfo].from_failure(created)
        return self._seal_created_container(container_name, fingerprint, initializer)

    def _seal_created_container(
        self,
        container_name: str,
        fingerprint: str,
        initializer: p.Tests.ContainerInitializer | None,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch the created container, run its initializer once, and seal it.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

        """
        fetched = self.fetch_container_info(container_name)
        if fetched.failure:
            return fetched
        if initializer is not None:
            initialized = initializer(fetched.value)
            if initialized.failure:
                return r[m.Tests.ContainerInfo].from_failure(initialized)
        created_id = fetched.value.container_id
        sealed = u.Tests.update_container_state(
            self.state_dir,
            container_name,
            lambda state: state.model_copy(
                update={
                    "container_id": created_id,
                    "fingerprint": fingerprint,
                    "dirty": False,
                    "sealed": True,
                },
            ),
        )
        if sealed.failure:
            return r[m.Tests.ContainerInfo].from_failure(sealed)
        return fetched

    def _serve(
        self,
        target: m.Tests.ContainerConfig,
        info: m.Tests.ContainerInfo,
        readiness_probe: p.Tests.ReadinessProbe | None,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Wait, within startup_timeout, for health, the published port and probe.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

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
            return r[m.Tests.ContainerInfo].fail(
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
                return r[m.Tests.ContainerInfo].from_failure(listening)
        if readiness_probe is not None:
            probed = self._poll_readiness(
                current,
                readiness_probe,
                deadline,
                target.startup_timeout,
            )
            if probed.failure:
                return r[m.Tests.ContainerInfo].from_failure(probed)
        return r[m.Tests.ContainerInfo].ok(current)

    def _await_port(
        self,
        target: m.Tests.ContainerConfig,
        info: m.Tests.ContainerInfo,
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
        info: m.Tests.ContainerInfo,
        deadline: float,
        timeout: int,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Poll a starting healthcheck until it settles or the deadline passes.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

        """
        current = info
        while current.health == c.Tests.ContainerHealth.STARTING:
            if time.monotonic() >= deadline:
                return r[m.Tests.ContainerInfo].fail(
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
        return r[m.Tests.ContainerInfo].ok(current)

    @staticmethod
    def _poll_readiness(
        info: m.Tests.ContainerInfo,
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
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Check, without changing anything, that the container is usable.

        Fails typed: NOT_PROVISIONED, DIRTY, UNSEALED, FINGERPRINT_MISMATCH,
        UNHEALTHY, LOCK_TIMEOUT (a recreation holds the lease),
        ENVIRONMENT_MISSING, PORT_NOT_PUBLISHED or READINESS_TIMEOUT.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

        """
        target = self.target_config
        error = self._target_error()
        if target is None or target.container_name is None or error is not None:
            return r[m.Tests.ContainerInfo].fail(error)
        container_name = target.container_name
        preflight = self.lifecycle_enabled().flat_map(
            lambda _: u.Tests.docker_fingerprint(target),
        )
        if preflight.failure:
            return r[m.Tests.ContainerInfo].from_failure(preflight)
        fingerprint = preflight.value
        try:
            with u.Tests.FileLock(
                u.Tests.docker_lease_lock_file(self.state_dir, container_name),
                shared=True,
                timeout_seconds=target.lock_timeout_seconds,
            ):
                return self._verify_leased(
                    target,
                    container_name,
                    fingerprint,
                    readiness_probe,
                    required_environment,
                )
        except TimeoutError as exc:
            return r[m.Tests.ContainerInfo].fail(
                str(exc),
                error_code=c.Tests.DockerErrorCode.LOCK_TIMEOUT,
                exception=exc,
            )

    def _verify_leased(
        self,
        target: m.Tests.ContainerConfig,
        container_name: str,
        fingerprint: str,
        readiness_probe: p.Tests.ReadinessProbe | None,
        required_environment: Sequence[str],
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Verify under a held shared lease.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.

        """
        observed = self._observe(container_name)
        if observed.failure:
            return r[m.Tests.ContainerInfo].from_failure(observed)
        info, state = observed.value
        if info is not None:
            deadline = time.monotonic() + target.startup_timeout
            settled = self._await_health(info, deadline, target.startup_timeout)
            if settled.failure:
                return settled
            info = settled.value
        checked = u.Tests.docker_verify(info, state, fingerprint=fingerprint)
        if checked.failure:
            return checked
        if required_environment:
            environment = self.fetch_container_environment(
                container_name,
                required_environment,
            )
            if environment.failure:
                return r[m.Tests.ContainerInfo].from_failure(environment)
        return self._serve(target, checked.value, readiness_probe)


tk: type[FlextTestsDocker] = FlextTestsDocker
"""Docker container control facade alias for flext_tests."""

__all__: list[str] = ["FlextTestsDocker", "tk"]

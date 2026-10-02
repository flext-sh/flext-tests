"""Host-scoped container state records of the Docker test lifecycle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from flext_infra import u

from flext_core import r
from flext_tests import c, m, p, t

from .testcontext import FlextTestsTestContextUtilitiesMixin


class FlextTestsDockerStateUtilitiesMixin:
    """One JSON record per container name, shared by every checkout of the host.

    A record is rewritten atomically while ``<name>.state.lock`` is held, so a
    reader always sees one complete record. A missing record is the
    unprovisioned state; an unreadable or invalid record fails with its cause
    and is never replaced by that default.
    """

    @staticmethod
    def docker_state_dir() -> Path:
        """Return the host directory that holds every container record."""
        return Path.home().joinpath(*c.Tests.DOCKER_STATE_DIR_PARTS)

    @staticmethod
    def docker_state_file(state_dir: Path, container_name: str) -> Path:
        """Return the JSON record of one container."""
        return state_dir / f"{container_name}{c.Tests.DOCKER_STATE_FILE_SUFFIX}"

    @staticmethod
    def docker_state_lock_file(state_dir: Path, container_name: str) -> Path:
        """Return the lock serializing rewrites of one container record."""
        return state_dir / f"{container_name}{c.Tests.DOCKER_STATE_LOCK_SUFFIX}"

    @staticmethod
    def docker_lease_lock_file(state_dir: Path, container_name: str) -> Path:
        """Return the lock shared by the sessions that use one container."""
        return state_dir / f"{container_name}{c.Tests.DOCKER_LEASE_LOCK_SUFFIX}"

    @staticmethod
    def read_container_state(
        state_dir: Path,
        container_name: str,
    ) -> p.Result[m.Tests.ContainerState]:
        """Read the record of one container; no record means unprovisioned.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerState]``.
        """
        unprovisioned = FlextTestsDockerStateUtilitiesMixin._unprovisioned(
            container_name,
        )
        if unprovisioned.failure:
            return unprovisioned
        state_file = FlextTestsDockerStateUtilitiesMixin.docker_state_file(
            state_dir,
            container_name,
        )
        if not state_file.exists():
            return unprovisioned
        return (
            u.Cli
            .files_read_text(state_file)
            .flat_map(
                lambda text: u.try_(
                    lambda: m.Tests.ContainerState.model_validate_json(text),
                    catch=c.EXC_VALIDATION_VALUE,
                    op_name=f"Parse container state {state_file}",
                ),
            )
            .flat_map(
                lambda state: FlextTestsDockerStateUtilitiesMixin._own_record(
                    state_file,
                    container_name,
                    state,
                ),
            )
        )

    @staticmethod
    def _unprovisioned(container_name: str) -> p.Result[m.Tests.ContainerState]:
        """Validate the name before it becomes a path; return its empty record.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerState]``.
        """
        return r[m.Tests.ContainerState].from_validation(
            {"container_name": container_name},
            m.Tests.ContainerState,
        )

    @staticmethod
    def _own_record(
        state_file: Path,
        container_name: str,
        state: m.Tests.ContainerState,
    ) -> p.Result[m.Tests.ContainerState]:
        """Reject a record that names another container.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerState]``.
        """
        if state.container_name == container_name:
            return r[m.Tests.ContainerState].ok(state)
        return r[m.Tests.ContainerState].fail(
            c.Tests.ERR_DOCKER_STATE_NAME_MISMATCH.format(
                path=state_file,
                recorded=state.container_name,
                expected=container_name,
            ),
        )

    @staticmethod
    def update_container_state(
        state_dir: Path,
        container_name: str,
        change: Callable[[m.Tests.ContainerState], m.Tests.ContainerState],
        *,
        timeout_seconds: float = c.Tests.DOCKER_STATE_LOCK_TIMEOUT_SECONDS,
    ) -> p.Result[m.Tests.ContainerState]:
        """Rewrite one record atomically under its state lock and return it.

        The state lock is awaited at most ``timeout_seconds``; a longer holder
        fails the rewrite with ``LOCK_TIMEOUT`` and leaves the record intact.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerState]``.
        """
        named = FlextTestsDockerStateUtilitiesMixin._unprovisioned(container_name)
        if named.failure:
            return named
        state_file = FlextTestsDockerStateUtilitiesMixin.docker_state_file(
            state_dir,
            container_name,
        )
        lock = FlextTestsTestContextUtilitiesMixin.FileLock(
            FlextTestsDockerStateUtilitiesMixin.docker_state_lock_file(
                state_dir,
                container_name,
            ),
            timeout_seconds=timeout_seconds,
        )
        try:
            with lock:
                return (
                    FlextTestsDockerStateUtilitiesMixin
                    .read_container_state(state_dir, container_name)
                    .map(change)
                    .flat_map(
                        lambda changed: FlextTestsDockerStateUtilitiesMixin._own_record(
                            state_file,
                            container_name,
                            changed,
                        ),
                    )
                    .flat_map(
                        lambda owned: FlextTestsDockerStateUtilitiesMixin._publish(
                            state_file,
                            owned,
                        ),
                    )
                )
        except TimeoutError as exc:
            return r[m.Tests.ContainerState].fail(
                str(exc),
                error_code=c.Tests.DockerErrorCode.LOCK_TIMEOUT,
                exception=exc,
            )

    @staticmethod
    def _publish(
        state_file: Path,
        state: m.Tests.ContainerState,
    ) -> p.Result[m.Tests.ContainerState]:
        """Atomically replace the record file with ``state``.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerState]``.
        """
        return u.Cli.atomic_write_text_file(state_file, state.model_dump_json()).map(
            lambda _: state,
        )

    @staticmethod
    def list_container_states(
        state_dir: Path,
    ) -> p.Result[t.SequenceOf[m.Tests.ContainerState]]:
        """Read every record of the host, ordered by container name.

        Returns:
            The resulting ``p.Result[t.SequenceOf[m.Tests.ContainerState]]``.
        """
        states: list[m.Tests.ContainerState] = []
        record_files = (
            sorted(state_dir.glob(f"*{c.Tests.DOCKER_STATE_FILE_SUFFIX}"))
            if state_dir.is_dir()
            else []
        )
        for record_file in record_files:
            read = FlextTestsDockerStateUtilitiesMixin.read_container_state(
                state_dir,
                record_file.name.removesuffix(c.Tests.DOCKER_STATE_FILE_SUFFIX),
            )
            if read.failure:
                return r[t.SequenceOf[m.Tests.ContainerState]].from_failure(read)
            states.append(read.value)
        return r[t.SequenceOf[m.Tests.ContainerState]].ok(tuple(states))

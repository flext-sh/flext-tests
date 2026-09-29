"""The health-aware Docker lifecycle against a real Docker daemon.

Every test binds its own compose project (a random token), keeps the host
records under ``tmp_path`` and removes its project on teardown. The ``docker``
marker keeps these tests out of ``make test`` and CI; ``make test-full`` runs
them on a Docker host.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import multiprocessing
import secrets
import time
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from flext_tests import FlextTestsDocker, m, r, tm
from tests import c, t, u

if TYPE_CHECKING:
    from collections.abc import Generator
    from multiprocessing.queues import Queue

    from tests import p

pytestmark = [pytest.mark.docker, pytest.mark.integration, pytest.mark.slow]


class TestsFlextTestsDockerLifecycle:
    """Create once, reuse while sealed and healthy, recreate when stale."""

    CREATION_VARIABLE = "FLEXT_TESTS_LIFECYCLE_VALUE"

    @staticmethod
    def _compose_file() -> Path:
        return (
            Path(__file__).resolve().parents[1]
            / "fixtures"
            / "docker"
            / "lifecycle.compose.yml"
        )

    @staticmethod
    def _docker(
        project: str,
        state_dir: Path,
        *,
        service: str = "probe",
        inputs: t.VariadicTuple[Path] = (),
        startup_timeout: int = 20,
    ) -> FlextTestsDocker:
        compose_file = TestsFlextTestsDockerLifecycle._compose_file()
        return FlextTestsDocker.compose(
            compose_file,
            target=m.Tests.ContainerConfig(
                container_name=f"{project}-{service}-1",
                service=service,
                project_name=project,
                port=80 if service == "probe" else None,
                fingerprint_inputs=inputs,
                startup_timeout=startup_timeout,
                lock_timeout_seconds=float(startup_timeout),
            ),
            repository_root=compose_file.parent,
            state_dir=state_dir,
        )

    @staticmethod
    def _marker(marker_file: Path) -> p.Tests.ContainerInitializer:
        """Initializer appending the created container id to a file."""

        def append(info: m.Tests.ContainerInfo) -> p.Result[bool]:
            with marker_file.open("a", encoding="utf-8") as handle:
                _ = handle.write(f"{info.container_id}\n")
            return r[bool].ok(True)

        return append

    @staticmethod
    def _await_health(
        docker: FlextTestsDocker, name: str, health: c.Tests.ContainerHealth
    ) -> m.Tests.ContainerInfo:
        """Poll Docker until the container reports ``health`` (bounded)."""
        deadline = time.monotonic() + 15
        while True:
            info = tm.ok(docker.fetch_container_info(name))
            if info.health == health or time.monotonic() >= deadline:
                tm.that(info.health, eq=health)
                return info
            time.sleep(c.Tests.DOCKER_HEALTH_POLL_SECONDS)

    @pytest.fixture
    def project(self, tmp_path: Path) -> Generator[str]:
        """A fresh compose project whose containers and volumes are removed."""
        name = f"flext-tests-lc-{secrets.token_hex(4)}"
        yield name
        tm.ok(self._docker(name, tmp_path / "teardown").down())

    def test_reuse_keeps_the_sealed_container(
        self, project: str, tmp_path: Path
    ) -> None:
        """A second ensure reuses the container the first one created."""
        state_dir = tmp_path / "state"
        docker = self._docker(project, state_dir)
        created = tmp_path / "created.txt"
        first = tm.ok(docker.execute(initializer=self._marker(created)))
        second = tm.ok(docker.execute(initializer=self._marker(created)))
        tm.that(second.container_id, eq=first.container_id)
        tm.that(created.read_text(encoding="utf-8").splitlines(), len=1)
        record = tm.ok(u.Tests.read_container_state(state_dir, first.name))
        tm.that(record.sealed, eq=True)
        tm.that(record.container_id, eq=first.container_id)
        tm.that(record.fingerprint, eq=tm.ok(docker.fingerprint()))
        tm.that(tm.ok(docker.verify()).container_id, eq=first.container_id)
        tm.that(tm.ok(u.Tests.resolve_host_port(first, 80)), gt=0)

    def test_unhealthy_container_is_recreated(
        self, project: str, tmp_path: Path
    ) -> None:
        """A failing healthcheck makes verify fail and ensure recreate."""
        docker = self._docker(project, tmp_path / "state")
        first = tm.ok(docker.execute())
        client = tm.not_none(docker.client)
        _ = client.containers.get(first.name).exec_run(["touch", "/unhealthy"])
        _ = self._await_health(docker, first.name, c.Tests.ContainerHealth.UNHEALTHY)
        tm.fail(docker.verify(), code=c.Tests.DockerErrorCode.UNHEALTHY)
        second = tm.ok(docker.execute())
        tm.that(second.container_id, ne=first.container_id)
        tm.that(second.health, eq=c.Tests.ContainerHealth.HEALTHY)

    def test_changed_fingerprint_input_recreates(
        self, project: str, tmp_path: Path
    ) -> None:
        """Changing a declared input invalidates the seal."""
        declared = tmp_path / "declared-input.txt"
        _ = declared.write_text("first\n", encoding="utf-8")
        docker = self._docker(project, tmp_path / "state", inputs=(declared,))
        first = tm.ok(docker.execute())
        _ = declared.write_text("second\n", encoding="utf-8")
        tm.fail(docker.verify(), code=c.Tests.DockerErrorCode.FINGERPRINT_MISMATCH)
        second = tm.ok(docker.execute())
        tm.that(second.container_id, ne=first.container_id)
        tm.ok(docker.verify())

    def test_creation_environment_reads_back_as_secret(
        self, project: str, tmp_path: Path
    ) -> None:
        """Creation values reach the container and never stay on disk."""
        state_dir = tmp_path / "state"
        docker = self._docker(project, state_dir)
        value = secrets.token_hex(8)
        info = tm.ok(
            docker.execute(
                creation_environment={self.CREATION_VARIABLE: t.SecretStr(value)}
            )
        )
        environment = tm.ok(
            docker.fetch_container_environment(info.name, [self.CREATION_VARIABLE])
        )
        tm.that(environment[self.CREATION_VARIABLE].get_secret_value(), eq=value)
        tm.that(list(state_dir.glob(f"*{c.Tests.DOCKER_ENV_FILE_SUFFIX}")), empty=True)
        tm.ok(docker.verify(required_environment=[self.CREATION_VARIABLE]))
        tm.fail(
            docker.verify(required_environment=["FLEXT_TESTS_ABSENT_KEY"]),
            code=c.Tests.DockerErrorCode.ENVIRONMENT_MISSING,
        )

    def test_verify_never_mutates(self, project: str, tmp_path: Path) -> None:
        """Verification reports state; it neither creates nor recreates."""
        state_dir = tmp_path / "state"
        docker = self._docker(project, state_dir)
        name = f"{project}-probe-1"
        tm.fail(docker.verify(), code=c.Tests.DockerErrorCode.NOT_PROVISIONED)
        tm.fail(
            docker.fetch_container_info(name),
            code=c.Tests.DockerErrorCode.NOT_PROVISIONED,
        )
        created = tm.ok(docker.execute())
        tm.ok(docker.mark_container_dirty(name))
        record = u.Tests.docker_state_file(state_dir, name)
        recorded = record.read_bytes()
        tm.fail(docker.verify(), code=c.Tests.DockerErrorCode.DIRTY)
        tm.that(record.read_bytes(), eq=recorded)
        tm.that(
            tm.ok(docker.fetch_container_info(name)).container_id,
            eq=created.container_id,
        )

    @staticmethod
    def _ensure_in_child(
        project: str, state_dir: str, marker_file: str, results: Queue[str]
    ) -> None:
        """Process body of the concurrency test: one ensure, report its id."""
        docker = TestsFlextTestsDockerLifecycle._docker(project, Path(state_dir))
        ensured = docker.execute(
            initializer=TestsFlextTestsDockerLifecycle._marker(Path(marker_file))
        )
        results.put(
            ensured.value.container_id
            if ensured.success
            else f"failure: {ensured.error}"
        )

    def test_concurrent_ensures_create_once(self, project: str, tmp_path: Path) -> None:
        """Two processes ensuring the same container create it exactly once."""
        state_dir = tmp_path / "state"
        created = tmp_path / "created.txt"
        context = multiprocessing.get_context("spawn")
        results: Queue[str] = context.Queue()
        workers = [
            context.Process(
                target=self._ensure_in_child,
                args=(project, str(state_dir), str(created), results),
            )
            for _ in range(2)
        ]
        for worker in workers:
            worker.start()
        reported = [results.get(timeout=25) for _ in workers]
        for worker in workers:
            worker.join(timeout=5)
            tm.that(worker.exitcode, eq=0)
        tm.that(reported[0], eq=reported[1])
        tm.that(reported[0], lacks="failure")
        tm.that(created.read_text(encoding="utf-8").splitlines(), eq=[reported[0]])

    def test_never_healthy_service_fails_within_startup_timeout(
        self, project: str, tmp_path: Path
    ) -> None:
        """A service that never turns healthy fails the ensure, unsealed."""
        state_dir = tmp_path / "state"
        docker = self._docker(
            project, state_dir, service="never-healthy", startup_timeout=5
        )
        started = time.monotonic()
        tm.fail(docker.execute())
        tm.that(time.monotonic() - started, lt=20)
        record = tm.ok(
            u.Tests.read_container_state(state_dir, f"{project}-never-healthy-1")
        )
        tm.that(record.sealed, eq=False)

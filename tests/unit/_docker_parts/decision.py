"""Health-aware lifecycle decision-table tests (T2)."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from flext_tests import FlextTestsDocker, m, tm
from tests import c


def _info(status: c.Tests.ContainerStatus, health: str = "") -> m.Tests.ContainerInfo:
    """Build container info for one decision-table row."""
    return m.Tests.ContainerInfo(
        name="decision-target",
        status=status,
        ports={},
        image="img",
        container_id="id-1",
        health=health,
    )


def _state(
    *, sealed: bool = True, dirty: bool = False, fingerprint: str = "fp-current"
) -> m.Tests.ContainerState:
    """Build container state for one decision-table row."""
    return m.Tests.ContainerState(
        container_name="decision-target",
        container_id="id-1",
        fingerprint=fingerprint,
        sealed=sealed,
        dirty=dirty,
    )


class TestsFlextTestsDockerDecisionMixin:
    """docker_action decision table through the public facade."""

    def test_absent_state_creates(self) -> None:
        """No persisted state means the container must be created."""
        action = FlextTestsDocker.docker_action(
            None, _info(c.Tests.ContainerStatus.RUNNING), "fp"
        )
        tm.that(action, eq="CREATE")

    def test_absent_info_creates(self) -> None:
        """No inspectable container means CREATE even with state on disk."""
        action = FlextTestsDocker.docker_action(_state(), None, "fp-current")
        tm.that(action, eq="CREATE")

    def test_exited_starts(self) -> None:
        """An exited container is started, not recreated."""
        action = FlextTestsDocker.docker_action(
            _state(), _info(c.Tests.ContainerStatus.EXITED), "fp-current"
        )
        tm.that(action, eq="START")

    def test_running_unhealthy_recreates(self) -> None:
        """A running but unhealthy container is recreated."""
        action = FlextTestsDocker.docker_action(
            _state(), _info(c.Tests.ContainerStatus.RUNNING, "unhealthy"), "fp-current"
        )
        tm.that(action, eq="RECREATE")

    def test_dirty_state_recreates_even_when_healthy(self) -> None:
        """The dirty marker forces recreation regardless of health."""
        action = FlextTestsDocker.docker_action(
            _state(dirty=True),
            _info(c.Tests.ContainerStatus.RUNNING, "healthy"),
            "fp-current",
        )
        tm.that(action, eq="RECREATE")

    def test_unsealed_state_recreates(self) -> None:
        """A never-sealed container is recreated before first reuse."""
        action = FlextTestsDocker.docker_action(
            _state(sealed=False),
            _info(c.Tests.ContainerStatus.RUNNING, "healthy"),
            "fp-current",
        )
        tm.that(action, eq="RECREATE")

    def test_fingerprint_drift_recreates(self) -> None:
        """A changed tracked input (fingerprint drift) recreates."""
        action = FlextTestsDocker.docker_action(
            _state(fingerprint="fp-old"),
            _info(c.Tests.ContainerStatus.RUNNING, "healthy"),
            "fp-new",
        )
        tm.that(action, eq="RECREATE")

    def test_healthy_sealed_matching_reuses(self) -> None:
        """Healthy + sealed + matching fingerprint keeps the container id."""
        action = FlextTestsDocker.docker_action(
            _state(), _info(c.Tests.ContainerStatus.RUNNING, "healthy"), "fp-current"
        )
        tm.that(action, eq="REUSE")

    def test_running_without_healthcheck_reuses_when_sealed(self) -> None:
        """No declared healthcheck: running + sealed + matching reuses."""
        action = FlextTestsDocker.docker_action(
            _state(), _info(c.Tests.ContainerStatus.RUNNING, ""), "fp-current"
        )
        tm.that(action, eq="REUSE")

    def test_fingerprint_tracks_compose_bytes(self, tmp_path: Path) -> None:
        """The fingerprint changes when the tracked compose bytes change."""
        compose_a = tmp_path / f"a-{uuid4().hex[:8]}.yml"
        compose_b = tmp_path / f"b-{uuid4().hex[:8]}.yml"
        compose_a.write_text("services: {x: {image: t1}}", encoding="utf-8")
        compose_b.write_text("services: {x: {image: t2}}", encoding="utf-8")
        manager = FlextTestsDocker(state_root=tmp_path / "docker-state")
        target_a = m.Tests.ContainerConfig(compose_file=compose_a)
        target_b = m.Tests.ContainerConfig(compose_file=compose_b)
        tm.that(
            manager.fingerprint(target_a) == manager.fingerprint(target_b), eq=False
        )

    def test_fingerprint_extra_inputs_change_the_hash(self, tmp_path: Path) -> None:
        """Declared fingerprint_inputs participate in the hash."""
        compose = tmp_path / f"c-{uuid4().hex[:8]}.yml"
        compose.write_text("services: {}", encoding="utf-8")
        extra = tmp_path / "cluster-config.yaml"
        extra.write_text("schema: v1", encoding="utf-8")
        manager = FlextTestsDocker(state_root=tmp_path / "docker-state")
        base = m.Tests.ContainerConfig(compose_file=compose)
        with_extra = m.Tests.ContainerConfig(
            compose_file=compose, fingerprint_inputs=[str(extra)]
        )
        tm.that(manager.fingerprint(base) == manager.fingerprint(with_extra), eq=False)

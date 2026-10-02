"""Private docker host-state test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker, m, tm
from tests import c, u


class TestsFlextTestsDockerStateMixin:
    """Host-scoped container state through the public facade and utilities."""

    def test_client_cached(self) -> None:
        """The Docker client is resolved once and reused."""
        manager = FlextTestsDocker()
        client1 = manager.client
        client2 = manager.client
        tm.that(client1 is client2, eq=True)

    def test_dirty_state_is_shared_by_every_facade_of_the_host(
        self,
        tmp_path: Path,
    ) -> None:
        """Facades over one state directory see one record per container."""
        state_dir = tmp_path / "host-state"
        writer = FlextTestsDocker(state_dir=state_dir)
        _ = u.Tests.assert_success(writer.mark_container_dirty("container1"))
        reader = FlextTestsDocker(state_dir=state_dir)
        tm.that(reader.container_dirty("container1"), eq=True)
        tm.that(reader.dirty_containers, eq=("container1",))

    def test_mark_container_dirty(self, docker_manager: FlextTestsDocker) -> None:
        """Test marking container as dirty."""
        result = docker_manager.mark_container_dirty("test_container")
        _ = u.Tests.assert_success(result)
        tm.that(docker_manager.container_dirty("test_container"), eq=True)

    def test_mark_container_clean(self, docker_manager: FlextTestsDocker) -> None:
        """Test marking container as clean."""
        _ = docker_manager.mark_container_dirty("test_container")
        result = docker_manager.mark_container_clean("test_container")
        _ = u.Tests.assert_success(result)
        tm.that(docker_manager.container_dirty("test_container"), eq=False)

    def test_container_dirty(self, docker_manager: FlextTestsDocker) -> None:
        """Test checking if container is dirty."""
        _ = docker_manager.mark_container_dirty("dirty_container")
        tm.that(docker_manager.container_dirty("dirty_container"), eq=True)
        tm.that(docker_manager.container_dirty("clean_container"), eq=False)

    def test_dirty_containers(self, docker_manager: FlextTestsDocker) -> None:
        """Dirty names are listed in name order; clean records are omitted."""
        _ = docker_manager.mark_container_dirty("container2")
        _ = docker_manager.mark_container_dirty("container1")
        _ = docker_manager.mark_container_clean("container3")
        tm.that(docker_manager.dirty_containers, eq=("container1", "container2"))

    def test_unrecorded_container_is_unprovisioned(self, tmp_path: Path) -> None:
        """A name without a record reads as clean, unsealed, with no identity."""
        state = tm.ok(u.Tests.read_container_state(tmp_path, "never-seen"))
        tm.that(state.container_name, eq="never-seen")
        tm.that(state.container_id, empty=True)
        tm.that(state.fingerprint, empty=True)
        tm.that(state.dirty, eq=False)
        tm.that(state.sealed, eq=False)

    def test_state_record_round_trips_every_field(self, tmp_path: Path) -> None:
        """A rewritten record reads back exactly as published."""
        published = tm.ok(
            u.Tests.update_container_state(
                tmp_path,
                "round-trip",
                lambda state: state.model_copy(
                    update={
                        "container_id": "0123abcd",
                        "fingerprint": "f00d",
                        "dirty": True,
                        "sealed": True,
                    },
                ),
            ),
        )
        tm.that(
            tm.ok(u.Tests.read_container_state(tmp_path, "round-trip")),
            eq=published,
        )
        tm.that(tm.ok(u.Tests.list_container_states(tmp_path)), eq=(published,))

    def test_corrupt_record_fails_loud(self, docker_manager: FlextTestsDocker) -> None:
        """An unparsable record fails every reader and is never overwritten."""
        record = u.Tests.docker_state_file(docker_manager.state_dir, "corrupt")
        record.parent.mkdir(parents=True)
        _ = record.write_text("{not json", encoding="utf-8")
        failure = u.Tests.read_container_state(docker_manager.state_dir, "corrupt")
        tm.fail(failure, has=str(record))
        tm.fail(docker_manager.mark_container_dirty("corrupt"), has=str(record))
        with pytest.raises(RuntimeError):
            docker_manager.container_dirty("corrupt")
        with pytest.raises(RuntimeError):
            _ = docker_manager.dirty_containers
        tm.that(record.read_text(encoding="utf-8"), eq="{not json")

    def test_record_naming_another_container_fails(self, tmp_path: Path) -> None:
        """A record whose content names another container is rejected."""
        record = u.Tests.docker_state_file(tmp_path, "expected-name")
        _ = record.write_text(
            m.Tests.ContainerState(container_name="other-name").model_dump_json(),
            encoding="utf-8",
        )
        tm.fail(
            u.Tests.read_container_state(tmp_path, "expected-name"),
            has="other-name",
        )

    def test_invalid_container_name_is_rejected(self, tmp_path: Path) -> None:
        """A name outside Docker's grammar never becomes a record path."""
        state_dir = tmp_path / "state"
        tm.fail(u.Tests.read_container_state(state_dir, "../escape"))
        tm.fail(
            u.Tests.update_container_state(state_dir, "../escape", lambda state: state),
        )
        tm.that(list(tmp_path.iterdir()), eq=[])

    def test_state_lock_timeout_is_typed(self, tmp_path: Path) -> None:
        """A rewrite that cannot take the state lock fails LOCK_TIMEOUT intact."""
        holder = u.Tests.FileLock(u.Tests.docker_state_lock_file(tmp_path, "held"))
        with holder:
            result = u.Tests.update_container_state(
                tmp_path,
                "held",
                lambda state: state.model_copy(update={"dirty": True}),
                timeout_seconds=0.2,
            )
        tm.fail(result, code=c.Tests.DockerErrorCode.LOCK_TIMEOUT)
        tm.that(u.Tests.docker_state_file(tmp_path, "held").exists(), eq=False)

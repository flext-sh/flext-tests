"""Behavioral unit tests for the flext_tests Docker control facade (FlextTestsDocker).

The Docker surface is composed from the canonical ``_docker_parts`` mixins
(single source of truth for each behavioral slice); this module contributes only
the CI-lifecycle guards that have no shared owner.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker, tm
from tests import c

from ._docker_parts.builders import DockerBuildersMixin
from ._docker_parts.operations import DockerOperationsMixin
from ._docker_parts.state import DockerStateMixin
from ._docker_parts.targets import DockerTargetsMixin


@pytest.fixture
def docker_manager(tmp_path: Path) -> FlextTestsDocker:
    """Create a FlextTestsDocker instance with a known-clean container baseline."""
    fixtures_dir = Path(__file__).parent.parent.parent / "fixtures"
    manager = FlextTestsDocker(
        repository_root=fixtures_dir, worker_id=f"test-{tmp_path.name}"
    )
    _ = manager.mark_container_clean("container1")
    _ = manager.mark_container_clean("container2")
    _ = manager.mark_container_clean("test_container")
    _ = manager.mark_container_clean("dirty_container")
    return manager


class TestsFlextTestsDocker(
    DockerStateMixin, DockerBuildersMixin, DockerOperationsMixin, DockerTargetsMixin
):
    """Behavioral contract of the Docker control facade (FlextTestsDocker)."""

    # ------------------------------------------------------------------ #
    # CI=Y disables Docker lifecycle (exact Make token, not CI=true)     #
    # ------------------------------------------------------------------ #

    def test_ci_disables_docker_only_for_exact_make_token(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """ci_disables_docker() is true only for CI=Y, not GitHub CI=true."""
        monkeypatch.delenv(c.Tests.ENV_CI, raising=False)
        tm.that(FlextTestsDocker.ci_disables_docker(), eq=False)
        monkeypatch.setenv(c.Tests.ENV_CI, "true")
        tm.that(FlextTestsDocker.ci_disables_docker(), eq=False)
        monkeypatch.setenv(c.Tests.ENV_CI, c.Tests.CI_MAKE_VALUE)
        tm.that(FlextTestsDocker.ci_disables_docker(), eq=True)

    def test_compose_up_skips_under_ci_y(
        self, docker_manager: FlextTestsDocker, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """compose_up() pytest.skips under exact CI=Y before touching Docker."""
        monkeypatch.setenv(c.Tests.ENV_CI, c.Tests.CI_MAKE_VALUE)
        with pytest.raises(pytest.skip.Exception) as skipped:
            _ = docker_manager.compose_up("missing-compose.yml")
        tm.that(str(skipped.value), has=c.Tests.DOCKER_CI_SKIP_REASON)

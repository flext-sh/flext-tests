"""Behavioral unit tests for the flext_tests Docker control facade (FlextTestsDocker).

The Docker surface is composed from the canonical ``_docker_parts`` mixins
(single source of truth for each behavioral slice); this module contributes only
the CI-lifecycle guards that have no shared owner.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker, tm
from tests import c

from ._docker_parts.builders import TestsFlextTestsDockerBuilders
from ._docker_parts.operations import TestsFlextTestsDockerOperations
from ._docker_parts.state import TestsFlextTestsDockerState
from ._docker_parts.targets import TestsFlextTestsDockerTargets


class TestsFlextTestsDocker(
    TestsFlextTestsDockerState,
    TestsFlextTestsDockerBuilders,
    TestsFlextTestsDockerOperations,
    TestsFlextTestsDockerTargets,
):
    """Behavioral contract of the Docker control facade (FlextTestsDocker)."""

    class Tests:
        """flext-tests docker test namespace."""

    # ------------------------------------------------------------------ #
    # CI=Y disables Docker lifecycle (exact Make token, not CI=true)     #
    # ------------------------------------------------------------------ #

    @staticmethod
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

    # ------------------------------------------------------------------ #
    # CI=Y disables Docker lifecycle (exact Make token, not CI=true)     #
    # ------------------------------------------------------------------ #

    def test_ci_disables_docker_only_for_exact_make_token(self) -> None:
        """ci_disables_docker() is true only for CI=Y, not GitHub CI=true."""
        saved = os.environ.get(c.Tests.ENV_CI)
        try:
            os.environ.pop(c.Tests.ENV_CI, None)
            tm.that(FlextTestsDocker.ci_disables_docker(), eq=False)
            os.environ[c.Tests.ENV_CI] = "true"
            tm.that(FlextTestsDocker.ci_disables_docker(), eq=False)
            os.environ[c.Tests.ENV_CI] = c.Tests.CI_MAKE_VALUE
            tm.that(FlextTestsDocker.ci_disables_docker(), eq=True)
        finally:
            if saved is None:
                os.environ.pop(c.Tests.ENV_CI, None)
            else:
                os.environ[c.Tests.ENV_CI] = saved

    def test_compose_up_skips_under_ci_y(
        self, docker_manager: FlextTestsDocker
    ) -> None:
        """compose_up() pytest.skips under exact CI=Y before touching Docker."""
        saved = os.environ.get(c.Tests.ENV_CI)
        try:
            os.environ[c.Tests.ENV_CI] = c.Tests.CI_MAKE_VALUE
            tm.that(FlextTestsDocker.ci_disables_docker(), eq=True)
            with pytest.raises(pytest.skip.Exception) as skipped:
                docker_manager.skip_if_ci_disables_docker()
            tm.that(str(skipped.value), has=c.Tests.DOCKER_CI_SKIP_REASON)
        finally:
            if saved is None:
                os.environ.pop(c.Tests.ENV_CI, None)
            else:
                os.environ[c.Tests.ENV_CI] = saved

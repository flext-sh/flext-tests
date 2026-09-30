"""Behavioral unit tests for the flext_tests Docker control facade (FlextTestsDocker).

The Docker surface is composed from the canonical ``_docker_parts`` mixins
(single source of truth for each behavioral slice); this module contributes only
the CI-lifecycle guards that have no shared owner.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os

from flext_tests import FlextTestsDocker, tm
from tests import c, u

from ._docker_parts import builders, decision, operations, state, targets


class TestsFlextTestsDocker(
    state.TestsFlextTestsDockerStateMixin,
    builders.TestsFlextTestsDockerBuildersMixin,
    operations.TestsFlextTestsDockerOperationsMixin,
    decision.TestsFlextTestsDockerDecisionMixin,
    targets.TestsFlextTestsDockerTargetsMixin,
):
    """Behavioral contract of the Docker control facade (FlextTestsDocker)."""

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

    def test_compose_up_returns_typed_disabled_under_ci_y(
        self, docker_manager: FlextTestsDocker
    ) -> None:
        """compose_up() is a typed NOT EXECUTED failure under exact CI=Y."""
        saved = os.environ.get(c.Tests.ENV_CI)
        try:
            os.environ[c.Tests.ENV_CI] = c.Tests.CI_MAKE_VALUE
            tm.that(FlextTestsDocker.ci_disables_docker(), eq=True)
            result = docker_manager.compose_up("docker/docker-compose.nothing.yml")
            _ = u.Tests.assert_failure(result)
            tm.that(result.error or "", has="CI=Y")
        finally:
            if saved is None:
                os.environ.pop(c.Tests.ENV_CI, None)
            else:
                os.environ[c.Tests.ENV_CI] = saved

"""Behavioral unit tests for the flext_tests Docker control facade (FlextTestsDocker).

The Docker surface is composed from the canonical ``_docker_parts`` mixins,
one behavioral slice each: host state, builders, operations, target
validation, the Make CI token gate and the lifecycle rules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._docker_parts import builders, ci, lifecycle, operations, state, targets


class TestsFlextTestsDocker(
    state.TestsFlextTestsDockerStateMixin,
    builders.TestsFlextTestsDockerBuildersMixin,
    operations.TestsFlextTestsDockerOperationsMixin,
    targets.TestsFlextTestsDockerTargetsMixin,
    ci.TestsFlextTestsDockerCiMixin,
    lifecycle.TestsFlextTestsDockerLifecycleMixin,
):
    """Behavioral contract of the Docker control facade (FlextTestsDocker)."""

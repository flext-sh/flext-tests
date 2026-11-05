"""Scenario data: a docker-marked test that reads its isolated .env.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from flext_tests import c, tm, u


@pytest.mark.docker
def test_isolated_environment(docker_test_environment: Path) -> None:
    """The harness hands this test an isolated .env outside its own folder."""
    tm.that(docker_test_environment.name, eq=".env")
    tm.fail((Path(__file__).parent / ".env").exists())
    declared = docker_test_environment.read_text(encoding="utf-8").strip()
    name, value = declared.split(c.Tests.DOCKER_ENV_SEPARATOR, 1)
    tm.that(os.environ[name], eq=value)

"""Scenario fixture-tree materialization shared by every consumer suite.

Tests never embed source code or long text as string literals (ADR-028 point 9):
the content lives as files under ``tests/fixtures/<scenario>`` and a test asks
for a private copy through ``fixture_tree``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from importlib import import_module
from pathlib import Path

import pytest


class FlextTestsFixtureTreesFixtures:
    """Native plugin owner binding the requesting test module and ``tmp_path``."""

    @staticmethod
    @pytest.fixture
    def fixture_tree(
        request: pytest.FixtureRequest,
        tmp_path: Path,
    ) -> Callable[[str], Path]:
        """Materialize ``tests/fixtures/<scenario>`` into this test's ``tmp_path``.

        Returns:
            A callable taking the scenario name and returning ``tmp_path``.

        """
        materialize: Callable[..., Path] = import_module(
            "flext_tests"
        ).u.Tests.materialize
        return partial(materialize, request.path, destination=tmp_path)


__all__: list[str] = ["FlextTestsFixtureTreesFixtures"]

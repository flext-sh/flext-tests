"""Scenario fixture-tree materialization shared by every consumer suite.

Tests never embed source code or long text as string literals (ADR-028 point 9):
the content lives as files under the project's scenario root and a test asks
for a private copy through ``fixture_tree``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from functools import partial
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from flext_tests import p


class FlextTestsFixtureTreesFixtures:
    """Native plugin owner of scenario fixture trees and their ini key."""

    @staticmethod
    def pytest_addoption(parser: pytest.Parser) -> None:
        """Declare the scenario-root key flext-infra projects into every project."""
        parser.addini(
            import_module("flext_tests").c.Tests.FIXTURE_TREES_INI,
            default="",
            help="Scenario fixture-tree root (projected from flext-infra).",
        )

    @staticmethod
    def pytest_ignore_collect(
        collection_path: Path, config: pytest.Config
    ) -> bool | None:
        """Keep every scenario tree out of live test collection.

        Returns:
            ``True`` for a scenario directory, ``None`` to defer otherwise.

        """
        tests = import_module("flext_tests")
        scenario = tests.u.Tests.is_fixture_tree(
            collection_path,
            config.rootpath,
            config.getini(tests.c.Tests.FIXTURE_TREES_INI),
        )
        return True if scenario else None

    @pytest.fixture
    @staticmethod
    def fixture_tree(
        request: pytest.FixtureRequest,
        tmp_path: Path,
    ) -> p.Tests.FixtureTree:
        """Materialize one scenario tree, into ``tmp_path`` unless told otherwise.

        Returns:
            The materializer bound to this run's scenario root.

        """
        tests = import_module("flext_tests")
        root = tests.u.Tests.fixture_trees_root(
            request.config.rootpath,
            request.config.getini(tests.c.Tests.FIXTURE_TREES_INI),
        )
        return partial(tests.u.Tests.materialize, root, destination=tmp_path)


__all__: list[str] = ["FlextTestsFixtureTreesFixtures"]

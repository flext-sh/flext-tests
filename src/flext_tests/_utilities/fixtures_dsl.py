"""Fixture DSL mixin for project-specific test classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar

from flext_tests import c


class FlextTestsUtilitiesFixturesDSL:
    """DSL mixin that exposes flat fixture-loading verbs on a project Tests class.

    Usage — in your project's tests/utilities.py::

        class Tests(FlextTestsUtilitiesFixturesDSL):
            _FIXTURES_ROOT = c.Project.Tests.FIXTURES_DIR
            _FILE_EXTENSION = ".ldif"  # optional, default is ".ldif"

    Then test code calls::

        content = u.Project.Tests.load("oid", "schema")
        fixture = u.Project.Tests.path("oid", "schema")  # existing file path
        present = u.Project.Tests.exists("oid", "schema")
        servers = u.Project.Tests.servers()  # ("oid", "oud", …)
        kinds = u.Project.Tests.kinds("oid")  # ("acl", "entries", …)
    """

    _FIXTURES_ROOT: ClassVar[Path | None] = None
    _FILE_EXTENSION: ClassVar[str] = ".ldif"

    @classmethod
    def _root(cls) -> Path:
        if cls._FIXTURES_ROOT is None:
            msg = f"{cls.__name__} must set _FIXTURES_ROOT: ClassVar[Path]"
            raise TypeError(msg)
        return cls._FIXTURES_ROOT

    @classmethod
    def _resolve_path(cls, group: str, kind: str) -> Path:
        """Compute the candidate fixture path without checking existence.

        Returns:
            The resulting ``Path``.

        """
        root = cls._root()
        return root / group / f"{group}_{kind}_fixtures{cls._FILE_EXTENSION}"

    @classmethod
    def path(cls, group: str, kind: str) -> Path:
        """Resolve the fixture file path for one server group and kind.

        Args:
            group: The server group directory name.
            kind: The fixture kind within the group.

        Returns:
            The resulting ``Path``.

        Raises:
            FileNotFoundError: If the resolved fixture file does not exist.

        """
        fp = cls._resolve_path(group, kind)
        if not fp.exists():
            msg = f"Fixture not found: {fp}"
            raise FileNotFoundError(msg)
        return fp

    @classmethod
    def load(cls, group: str, kind: str) -> str:
        """Load one fixture file's text for a server group and kind.

        Args:
            group: The server group directory name.
            kind: The fixture kind within the group.

        Returns:
            The resulting ``str``.

        """
        return cls.path(group, kind).read_text(encoding="utf-8")

    @classmethod
    def exists(cls, group: str, kind: str) -> bool:
        """Return whether the fixture file for a server group and kind exists.

        Args:
            group: The server group directory name.
            kind: The fixture kind within the group.

        Returns:
            The resulting ``bool``.

        """
        return cls._resolve_path(group, kind).exists()

    @classmethod
    def servers(cls) -> Sequence[str]:
        """List the server group directories under the fixtures root.

        Returns:
            The resulting ``Sequence[str]``.

        """
        root = cls._root()
        if not root.exists():
            return ()
        return tuple(sorted(d.name for d in root.iterdir() if d.is_dir()))

    @staticmethod
    def fixture_trees_root(rootpath: Path, trees_root: str) -> Path:
        """Resolve the scenario fixture-tree root of one pytest run.

        The root is the ``c.Tests.FIXTURE_TREES_INI`` ini value, projected by
        flext-infra into every project, under the run's ``rootpath``.

        Args:
            rootpath: The pytest run's root directory.
            trees_root: The configured ini value.

        Returns:
            The absolute scenario fixture-tree root.

        Raises:
            ValueError: If the project declares no scenario root.

        """
        if not trees_root:
            msg = f"pytest ini {c.Tests.FIXTURE_TREES_INI} is not configured"
            raise ValueError(msg)
        return rootpath / trees_root

    @staticmethod
    def is_fixture_tree(path: Path, rootpath: Path, trees_root: str) -> bool:
        """Return whether ``path`` is one scenario directory of the run.

        Scenario trees hold consumer sources (``test_*.py`` included) that are
        data for ``fixture_tree``, never live tests. A project that declares no
        scenario root has none to exclude.

        Returns:
            Whether ``path`` is a direct child directory of the scenario root.

        """
        return (
            bool(trees_root) and path.parent == rootpath / trees_root and path.is_dir()
        )

    @staticmethod
    def materialize(examples_root: Path, scenario: str, destination: Path) -> Path:
        """Copy one scenario fixture tree into a test-owned directory.

        The tree lives at ``<examples_root>/<scenario>``; its contents land
        directly under ``destination``. This replaces source code or long text
        embedded as string literals in tests (ADR-028 point 9).

        Args:
            examples_root: The run's scenario root (``fixture_trees_root``).
            scenario: The scenario directory name under the fixtures root.
            destination: The test-owned directory receiving the tree.

        Returns:
            The ``destination`` path holding the materialized tree.

        Raises:
            FileNotFoundError: If the scenario directory does not exist.
            FileExistsError: If a scenario file already exists in ``destination``.

        """
        source = examples_root / scenario
        if not source.is_dir():
            msg = f"Fixture tree not found: {source}"
            raise FileNotFoundError(msg)
        for entry in source.rglob("*"):
            target = destination / entry.relative_to(source)
            if entry.is_file() and target.exists():
                msg = f"Fixture tree target already exists: {target}"
                raise FileExistsError(msg)
        shutil.copytree(source, destination, dirs_exist_ok=True)
        return destination

    @classmethod
    def kinds(cls, group: str) -> Sequence[str]:
        """List the fixture kinds available for one server group.

        Args:
            group: The server group directory name.

        Returns:
            The resulting ``Sequence[str]``.

        """
        root = cls._root()
        server_dir = root / group
        if not server_dir.exists():
            return ()
        prefix = f"{group}_"
        suffix = f"_fixtures{cls._FILE_EXTENSION}"
        return tuple(
            sorted(
                name[len(prefix) : -len(suffix)]
                for name in sorted(e.name for e in server_dir.iterdir())
                if name.startswith(prefix) and name.endswith(suffix)
            ),
        )


__all__: list[str] = ["FlextTestsUtilitiesFixturesDSL"]

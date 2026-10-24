"""Fixture DSL mixin for project-specific test classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from flext_tests import c

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsFixturesDSLMixin:
    """DSL mixin that exposes flat fixture-loading verbs on a project Tests class.

    Usage — in your project's tests/utilities.py::

        class Tests(FlextTestsFixturesDSLMixin):
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
    def servers(cls) -> t.StrSequence:
        """List the server group directories under the fixtures root.

        Returns:
            The resulting ``t.StrSequence``.

        """
        root = cls._root()
        if not root.exists():
            return ()
        return tuple(sorted(d.name for d in root.iterdir() if d.is_dir()))

    @staticmethod
    def materialize(checkout_root: Path, scenario: str, destination: Path) -> Path:
        """Copy one scenario fixture tree into a test-owned directory.

        The tree lives at ``<checkout>/tests/fixtures/<scenario>`` (parts owned by
        ``c.Tests.FIXTURE_TREES_PARTS``); its contents land directly under
        ``destination``. This replaces source code or long text embedded as
        string literals in tests (ADR-028 point 9).

        Args:
            checkout_root: The project checkout root (pytest ``rootpath``).
            scenario: The scenario directory name under the fixtures root.
            destination: The test-owned directory receiving the tree.

        Returns:
            The ``destination`` path holding the materialized tree.

        Raises:
            FileNotFoundError: If the scenario directory does not exist.
            FileExistsError: If a scenario file already exists in ``destination``.

        """
        source = checkout_root.joinpath(*c.Tests.FIXTURE_TREES_PARTS, scenario)
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
    def kinds(cls, group: str) -> t.StrSequence:
        """List the fixture kinds available for one server group.

        Args:
            group: The server group directory name.

        Returns:
            The resulting ``t.StrSequence``.

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


__all__: list[str] = ["FlextTestsFixturesDSLMixin"]

"""Behavioral unit tests for the pytest enforcement dispatcher.

Asserts the observable public contract exposed through ``u.Tests``:
workspace discovery, CSV parsing and catalog rule filtering, plus the CLI
options the installed ``flext_tests_enforcement`` pytest11 plugin registers.
Lifecycle hooks run end to end through ``pytester`` in
``test_enforcement_plugin.py``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import c, m, tm, u


class TestsFlextTestsEnforcementDispatcher:
    """Observable behavior of the enforcement dispatcher facade."""

    class Tests:
        """flext-tests enforcement dispatcher test namespace."""

    # ------------------------------------------------------------------ #
    # Fixtures                                                           #
    # ------------------------------------------------------------------ #

    @pytest.fixture
    def workspace(self, tmp_path: Path) -> Path:
        """Create a directory carrying every FLEXT workspace marker."""
        root = tmp_path / "ws"
        root.mkdir()
        for marker in c.Tests.ENFORCEMENT_WORKSPACE_MARKERS:
            (root / marker).mkdir(parents=True, exist_ok=True)
        return root

    @staticmethod
    def _cfg(
        *, include: frozenset[str] = frozenset(), exclude: frozenset[str] = frozenset()
    ) -> m.Tests.EnforcementDispatcherConfig:
        return m.Tests.EnforcementDispatcherConfig(
            active=True, strict=False, include=include, exclude=exclude
        )

    # ------------------------------------------------------------------ #
    # discover_repository_root                                            #
    # ------------------------------------------------------------------ #

    def test_discovers_root_from_nested_descendant(self, workspace: Path) -> None:
        nested = workspace / "flext-core" / "src" / "pkg"
        nested.mkdir(parents=True)

        tm.that(u.Tests.discover_repository_root(nested), eq=workspace)

    def test_returns_workspace_itself_when_start_is_root(self, workspace: Path) -> None:
        tm.that(u.Tests.discover_repository_root(workspace), eq=workspace)

    def test_returns_none_when_no_marker_present(self, tmp_path: Path) -> None:
        stray = tmp_path / "unrelated" / "deep"
        stray.mkdir(parents=True)

        tm.that(u.Tests.discover_repository_root(stray), none=True)

    def test_returns_none_when_a_single_marker_is_missing(self, tmp_path: Path) -> None:
        partial = tmp_path / "partial"
        partial.mkdir()
        # All markers but the last one -> not a workspace.
        for marker in list(c.Tests.ENFORCEMENT_WORKSPACE_MARKERS)[:-1]:
            (partial / marker).mkdir(parents=True, exist_ok=True)

        tm.that(u.Tests.discover_repository_root(partial), none=True)

    def test_sub_project_root_resolves_to_workspace_not_itself(
        self, workspace: Path
    ) -> None:
        # Auto-activation contract: a sub-project path discovers the workspace
        # above it, and that workspace is distinguishable from the sub-project
        # (so running pytest inside a sub-project stays a no-op).
        sub = workspace / "flext-core"
        discovered = u.Tests.discover_repository_root(sub)

        tm.that(discovered, eq=workspace)
        tm.that(discovered, ne=sub)

    # ------------------------------------------------------------------ #
    # split_csv                                                          #
    # ------------------------------------------------------------------ #

    @pytest.mark.parametrize("raw", ["", None])
    def test_split_csv_empty_input_yields_empty_set(self, raw: str | None) -> None:
        tm.that(u.Tests.split_csv(raw), eq=frozenset())

    def test_split_csv_strips_whitespace_and_drops_blank_fields(self) -> None:
        got = u.Tests.split_csv("ENFORCE-001, ENFORCE-002 ,,ENFORCE-003")

        tm.that(got, eq=frozenset({"ENFORCE-001", "ENFORCE-002", "ENFORCE-003"}))

    def test_split_csv_deduplicates_repeated_ids(self) -> None:
        tm.that(u.Tests.split_csv("A, A ,A"), eq=frozenset({"A"}))

    # ------------------------------------------------------------------ #
    # active_rules                                                       #
    # ------------------------------------------------------------------ #

    def test_active_rules_returns_only_enabled_rules(self) -> None:
        active = u.Tests.active_rules(self._cfg())

        tm.that(len(active) > 0, eq=True)
        tm.that(all(r.enabled for r in active), eq=True)

    def test_active_rules_excludes_disabled_skill_pointer_rules(self) -> None:
        # ENFORCE-034..038 ship disabled by default.
        ids = {r.id for r in u.Tests.active_rules(self._cfg())}

        tm.that(ids.isdisjoint({"ENFORCE-034", "ENFORCE-035", "ENFORCE-038"}), eq=True)

    def test_include_narrows_to_the_listed_ids(self) -> None:
        active = u.Tests.active_rules(self._cfg(include=frozenset({"ENFORCE-001"})))

        tm.that({r.id for r in active}, eq={"ENFORCE-001"})

    def test_include_of_unknown_id_yields_no_rules(self) -> None:
        active = u.Tests.active_rules(
            self._cfg(include=frozenset({"ENFORCE-DOES-NOT-EXIST"}))
        )

        tm.that(active, eq=())

    def test_exclude_removes_the_listed_id(self) -> None:
        ids = {
            r.id
            for r in u.Tests.active_rules(
                self._cfg(exclude=frozenset({"ENFORCE-001"}))
            )
        }

        tm.that(ids, lacks="ENFORCE-001")

    def test_exclude_takes_precedence_over_include(self) -> None:
        active = u.Tests.active_rules(
            self._cfg(
                include=frozenset({"ENFORCE-001"}), exclude=frozenset({"ENFORCE-001"})
            )
        )

        tm.that(active, eq=())

    def test_active_rules_is_idempotent(self) -> None:
        first = u.Tests.active_rules(self._cfg())
        second = u.Tests.active_rules(self._cfg())

        tm.that([r.id for r in first], eq=[r.id for r in second])

    # ------------------------------------------------------------------ #
    # pytest_addoption                                                   #
    # ------------------------------------------------------------------ #

    def test_plugin_registers_flext_enforce_cli_options(
        self, pytester: pytest.Pytester
    ) -> None:
        """The installed pytest11 plugin publishes the enforcement options."""
        result = pytester.runpytest("--help")
        result.stdout.fnmatch_lines([
            "*--flext-enforce *",
            "*--no-flext-enforce*",
            "*--flext-enforce-strict*",
            "*--flext-enforce-rules=*",
            "*--flext-enforce-exclude-rules=*",
            "*--flext-enforce-workspace-root=*",
        ])

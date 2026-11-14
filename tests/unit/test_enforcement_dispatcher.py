"""Behavioral unit tests for the pytest enforcement dispatcher.

Asserts catalog rule filtering through ``u.Tests``, the session activation
contract (workspace discovery, forced and disabled modes, rule-list parsing)
observed through the installed ``flext_tests_enforcement`` pytest11 plugin in a
subprocess sandbox, and the CLI options that plugin registers. Lifecycle hooks
run end to end through ``pytester`` in ``test_enforcement_plugin.py``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path

from tests import c, m, p, t, tm, u


class TestsFlextTestsEnforcementDispatcher:
    """Observable behavior of the enforcement dispatcher facade."""

    class Tests:
        """flext-tests enforcement dispatcher test namespace."""

    # ------------------------------------------------------------------ #
    # Fixtures                                                           #
    # ------------------------------------------------------------------ #

    @u.Tests.fixture
    @staticmethod
    def workspace(tmp_path: Path) -> Path:
        """Create a directory carrying every FLEXT workspace marker.

        Returns:
            The resulting ``Path``.

        """
        root = tmp_path / "ws"
        root.mkdir()
        for marker in c.Tests.ENFORCEMENT_WORKSPACE_MARKERS:
            (root / marker).mkdir(parents=True, exist_ok=True)
        return root

    project_root = Path(__file__).resolve().parents[2]

    @staticmethod
    def _cfg(
        *,
        include: frozenset[str] = frozenset(),
        exclude: frozenset[str] = frozenset(),
    ) -> p.Tests.EnforcementDispatcherConfig:
        return m.Tests.EnforcementDispatcherConfig(
            strict=False,
            include=include,
            exclude=exclude,
            repository_root=TestsFlextTestsEnforcementDispatcher.project_root,
            catalog_root=TestsFlextTestsEnforcementDispatcher.project_root,
        )

    # ------------------------------------------------------------------ #
    # Session activation (installed plugin, subprocess sandbox)          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _sandbox_project(workspace: Path) -> Path:
        """Create a real sub-project repository with one passing test.

        flext-infra plans one repository: a Git checkout whose
        ``pyproject.toml`` declares ``[project]``, whose package is its own
        (it never shadows an installed FLEXT package) and whose runtime
        environment is provisioned — here, this session's environment.

        Returns:
            The resulting ``Path``.

        """
        project = workspace / "flext-probe"
        package = project / "src" / "flext_probe"
        package.mkdir(parents=True, exist_ok=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
        (project / "pyproject.toml").write_text(
            '[project]\nname = "flext-probe"\nversion = "0"\n', encoding="utf-8"
        )
        u.Cli.run_checked([*c.Cli.GIT_INIT_COMMAND, str(project)]).unwrap()
        (project / ".venv").symlink_to(Path(sys.prefix), target_is_directory=True)
        (project / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        (project / "test_probe.py").write_text(
            "def test_probe() -> None:\n    assert True\n",
            encoding="utf-8",
        )
        return project

    @classmethod
    def _runtime_rule_id(cls) -> str:
        """Return the first declarative engine rule of the live catalog."""
        return next(
            rule.id
            for rule in u.Tests.active_rules(cls._cfg())
            if rule.source.kind == "flext_infra_rule"
        )

    @classmethod
    def _collect(
        cls,
        pytester: t.Tests.Pytester,
        project: Path,
        *args: str,
        rules: str = "",
    ) -> t.Tests.RunResult:
        """Collect ``project`` as its own rootdir with the enforcement options.

        Returns:
            The resulting ``pytest.RunResult``.

        """
        return u.Tests.pytest_subprocess(
            pytester,
            "--collect-only",
            "-q",
            f"--rootdir={project}",
            f"--flext-enforce-rules={rules or cls._runtime_rule_id()}",
            *args,
            str(project),
        )

    @c.Tests.MARK.slow
    def test_forced_run_discovers_the_workspace_above_a_sub_project(
        self,
        pytester: t.Tests.Pytester,
        workspace: Path,
    ) -> None:
        """Test forced run discovers the workspace above a sub project."""
        result = self._collect(
            pytester,
            self._sandbox_project(workspace),
            "--flext-enforce",
        )

        result.stdout.fnmatch_lines(["*flext-enforce*", "catalog active: 1 rules*"])

    @c.Tests.MARK.slow
    def test_forced_sub_project_plans_its_own_catalog(
        self,
        pytester: t.Tests.Pytester,
        workspace: Path,
    ) -> None:
        """A sub-project under a workspace plans the catalog of its own repository.

        The sandbox workspace holds a sibling file no repository can name as a
        module; planning the workspace root would fail on it, planning the
        collected sub-project does not.
        """
        (workspace / "flext-tests" / "unnamed-dir").mkdir(parents=True)
        (workspace / "flext-tests" / "unnamed-dir" / "probe.py").write_text(
            "VALUE = 1\n", encoding="utf-8"
        )
        result = self._collect(
            pytester,
            self._sandbox_project(workspace),
            "--flext-enforce",
        )

        result.stdout.no_fnmatch_line("*INTERNALERROR*")
        result.stdout.fnmatch_lines(["*flext-enforce*", "catalog active: 1 rules*"])

    @c.Tests.MARK.slow
    def test_sub_project_rootdir_stays_inactive_without_force(
        self,
        pytester: t.Tests.Pytester,
        workspace: Path,
    ) -> None:
        """Test sub project rootdir stays inactive without force."""
        result = self._collect(pytester, self._sandbox_project(workspace))

        result.stdout.no_fnmatch_line("*flext-enforce*")

    @c.Tests.MARK.slow
    def test_forced_run_without_every_marker_stays_inactive(
        self,
        pytester: t.Tests.Pytester,
        tmp_path: Path,
    ) -> None:
        """Test forced run without every marker stays inactive."""
        partial = tmp_path / "partial"
        for marker in list(c.Tests.ENFORCEMENT_WORKSPACE_MARKERS)[:-1]:
            (partial / marker).mkdir(parents=True, exist_ok=True)

        result = self._collect(
            pytester,
            self._sandbox_project(partial),
            "--flext-enforce",
        )

        result.stdout.no_fnmatch_line("*flext-enforce*")

    @c.Tests.MARK.slow
    def test_no_flext_enforce_overrides_an_explicit_workspace_root(
        self,
        pytester: t.Tests.Pytester,
        workspace: Path,
    ) -> None:
        """Test no flext enforce overrides an explicit workspace root."""
        result = self._collect(
            pytester,
            self._sandbox_project(workspace),
            f"--flext-enforce-workspace-root={workspace}",
            "--no-flext-enforce",
        )

        result.stdout.no_fnmatch_line("*flext-enforce*")

    @c.Tests.MARK.slow
    def test_rule_list_strips_blank_and_padded_fields(
        self,
        pytester: t.Tests.Pytester,
        workspace: Path,
    ) -> None:
        """Test rule list strips blank and padded fields."""
        rule = self._runtime_rule_id()
        result = self._collect(
            pytester,
            self._sandbox_project(workspace),
            f"--flext-enforce-workspace-root={workspace}",
            rules=f" {rule} ,, {rule} ,",
        )

        result.stdout.fnmatch_lines(["catalog active: 1 rules*"])

    # ------------------------------------------------------------------ #
    # active_rules                                                       #
    # ------------------------------------------------------------------ #

    def test_active_rules_without_filters_is_the_whole_catalog(self) -> None:
        # No rule is suspended: an unfiltered session runs every catalog rule.
        """Test active rules without filters is the whole catalog."""
        active = u.Tests.active_rules(self._cfg())
        catalog = u.Tests.build_canonical_catalog(self.project_root)

        tm.that(
            [r.id for r in active],
            eq=[r.id for r in catalog.rules],
        )

    def test_include_narrows_to_the_listed_ids(self) -> None:
        """Test include narrows to the listed ids."""
        rule_id = self._runtime_rule_id()
        active = u.Tests.active_rules(self._cfg(include=frozenset({rule_id})))

        tm.that({r.id for r in active}, eq={rule_id})

    def test_include_of_unknown_id_yields_no_rules(self) -> None:
        """Test include of unknown id yields no rules."""
        active = u.Tests.active_rules(
            self._cfg(include=frozenset({"ENFORCE-DOES-NOT-EXIST"})),
        )

        tm.that(active, eq=())

    def test_exclude_removes_the_listed_id(self) -> None:
        """Test exclude removes the listed id."""
        rule_id = self._runtime_rule_id()
        ids = {
            r.id for r in u.Tests.active_rules(self._cfg(exclude=frozenset({rule_id})))
        }

        tm.that(ids, lacks=rule_id)

    def test_exclude_takes_precedence_over_include(self) -> None:
        """Test exclude takes precedence over include."""
        rule_id = self._runtime_rule_id()
        active = u.Tests.active_rules(
            self._cfg(include=frozenset({rule_id}), exclude=frozenset({rule_id})),
        )

        tm.that(active, eq=())

    def test_active_rules_is_idempotent(self) -> None:
        """Test active rules is idempotent."""
        first = u.Tests.active_rules(self._cfg())
        second = u.Tests.active_rules(self._cfg())

        tm.that([r.id for r in first], eq=[r.id for r in second])

    # ------------------------------------------------------------------ #
    # pytest_addoption                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    @c.Tests.MARK.slow
    def test_plugin_registers_flext_enforce_cli_options(
        pytester: t.Tests.Pytester,
    ) -> None:
        """The installed pytest11 plugin publishes the enforcement options.

        A subprocess sandbox isolates the run from this session's process-global
        warning filters, so ``--help`` reflects a cold entry-point load.
        """
        pytester.makeini("[pytest]\n")
        result = u.Tests.pytest_subprocess(pytester, "--help")
        result.stdout.fnmatch_lines([
            "*--flext-enforce *",
            "*--no-flext-enforce*",
            "*--flext-enforce-strict*",
            "*--flext-enforce-rules=*",
            "*--flext-enforce-exclude-rules=*",
            "*--flext-enforce-workspace-root=*",
        ])

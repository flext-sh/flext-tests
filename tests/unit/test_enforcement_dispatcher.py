"""Behavioral unit tests for the pytest enforcement dispatcher.

Asserts catalog rule filtering through ``u.Tests``, the session activation
contract (workspace discovery, forced and disabled modes, rule-list parsing)
observed through the installed ``flext_tests_enforcement`` pytest11 plugin in a
subprocess sandbox, and the CLI options that plugin registers. Lifecycle hooks
run end to end through ``pytester`` in ``test_enforcement_plugin.py``.
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
            strict=False, include=include, exclude=exclude
        )

    # ------------------------------------------------------------------ #
    # Session activation (installed plugin, subprocess sandbox)          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _sandbox_project(workspace: Path) -> Path:
        """Create a sub-project with one passing test under ``workspace``."""
        project = workspace / "flext-core"
        project.mkdir(parents=True, exist_ok=True)
        (project / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        (project / "test_probe.py").write_text(
            "def test_probe() -> None:\n    assert True\n", encoding="utf-8"
        )
        return project

    @classmethod
    def _runtime_rule_id(cls) -> str:
        """Return the first enabled runtime-warning rule of the live catalog."""
        return next(
            rule.id
            for rule in u.Tests.active_rules(cls._cfg())
            if rule.source.kind == "runtime_warning"
        )

    @classmethod
    def _collect(
        cls, pytester: pytest.Pytester, project: Path, *args: str, rules: str = ""
    ) -> pytest.RunResult:
        """Collect ``project`` as its own rootdir with the enforcement options."""
        return pytester.runpytest_subprocess(
            "--collect-only",
            "-q",
            f"--rootdir={project}",
            f"--flext-enforce-rules={rules or cls._runtime_rule_id()}",
            *args,
            str(project),
        )

    @pytest.mark.slow
    def test_forced_run_discovers_the_workspace_above_a_sub_project(
        self, pytester: pytest.Pytester, workspace: Path
    ) -> None:
        result = self._collect(
            pytester, self._sandbox_project(workspace), "--flext-enforce"
        )

        result.stdout.fnmatch_lines(["*flext-enforce*", "catalog active: 1 rules*"])

    @pytest.mark.slow
    def test_sub_project_rootdir_stays_inactive_without_force(
        self, pytester: pytest.Pytester, workspace: Path
    ) -> None:
        result = self._collect(pytester, self._sandbox_project(workspace))

        result.stdout.no_fnmatch_line("*flext-enforce*")

    @pytest.mark.slow
    def test_forced_run_without_every_marker_stays_inactive(
        self, pytester: pytest.Pytester, tmp_path: Path
    ) -> None:
        partial = tmp_path / "partial"
        for marker in list(c.Tests.ENFORCEMENT_WORKSPACE_MARKERS)[:-1]:
            (partial / marker).mkdir(parents=True, exist_ok=True)

        result = self._collect(
            pytester, self._sandbox_project(partial), "--flext-enforce"
        )

        result.stdout.no_fnmatch_line("*flext-enforce*")

    @pytest.mark.slow
    def test_no_flext_enforce_overrides_an_explicit_workspace_root(
        self, pytester: pytest.Pytester, workspace: Path
    ) -> None:
        result = self._collect(
            pytester,
            self._sandbox_project(workspace),
            f"--flext-enforce-workspace-root={workspace}",
            "--no-flext-enforce",
        )

        result.stdout.no_fnmatch_line("*flext-enforce*")

    @pytest.mark.slow
    def test_rule_list_strips_blank_and_padded_fields(
        self, pytester: pytest.Pytester, workspace: Path
    ) -> None:
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
        active = u.Tests.active_rules(self._cfg())

        tm.that(
            [r.id for r in active],
            eq=[r.id for r in u.build_canonical_catalog().rules],
        )

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
            for r in u.Tests.active_rules(self._cfg(exclude=frozenset({"ENFORCE-001"})))
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
        """The installed pytest11 plugin publishes the enforcement options.

        A subprocess sandbox isolates the run from this session's process-global
        warning filters, so ``--help`` reflects a cold entry-point load.
        """
        pytester.makeini("[pytest]\n")
        result = pytester.runpytest_subprocess("--help")
        result.stdout.fnmatch_lines([
            "*--flext-enforce *",
            "*--no-flext-enforce*",
            "*--flext-enforce-strict*",
            "*--flext-enforce-rules=*",
            "*--flext-enforce-exclude-rules=*",
            "*--flext-enforce-workspace-root=*",
        ])

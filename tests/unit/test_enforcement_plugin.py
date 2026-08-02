"""Behavioral coverage for the enforcement dispatcher public contract.

Two behavioral surfaces are exercised through the module's public API only:

* Pure exported functions (``split_csv``, ``discover_workspace_root``,
  ``active_rules``) are called directly and asserted on their return values and
  invariants.
* The end-to-end pytest11 pipeline (entry-point load -> ``pytest_configure``
  filterwarnings -> ``pytest_warning_recorded`` -> ``pytest_terminal_summary``)
  is driven inside a ``pytester`` in-process sandbox and asserted on observable
  outcomes plus the terminal summary the plugin promises to print.
"""

from __future__ import annotations

import os
from importlib.metadata import entry_points
from typing import TYPE_CHECKING

import pytest

from flext_tests import (
    SessionConfig,
    active_rules,
    discover_workspace_root,
    load_infra_report,
    m,
    split_csv,
    tm,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsEnforcementPlugin:
    """Public contract of the enforcement dispatcher facade."""

    @staticmethod
    def _run_pytest(pytester: pytest.Pytester, *args: str) -> pytest.RunResult:
        """Run only the real plugins owned by this behavioral sandbox."""
        variable = "PYTEST_DISABLE_PLUGIN_AUTOLOAD"
        previous = os.environ.get(variable)
        os.environ[variable] = "1"
        try:
            return pytester.runpytest_inprocess(
                "-p", "pytest_timeout", "-p", "flext_tests._fixtures.enforcement", *args
            )
        finally:
            if previous is None:
                os.environ.pop(variable, None)
            else:
                os.environ[variable] = previous

    def test_flext_pytest11_entrypoints_have_one_package_owner(self) -> None:
        """Only the two flext-tests plugins participate in pytest autoload."""
        names = {
            entry.name
            for entry in entry_points(group="pytest11")
            if entry.name.startswith("flext_")
        }
        tm.that(names, eq={"flext_tests", "flext_tests_enforcement"})

    # ---- split_csv: pure CSV parsing contract --------------------------------

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            (None, frozenset()),
            ("", frozenset()),
            ("   ", frozenset()),
            ("ENFORCE-022", frozenset({"ENFORCE-022"})),
            ("a,b,c", frozenset({"a", "b", "c"})),
            ("  a , b ,c ", frozenset({"a", "b", "c"})),
            ("a,,b,", frozenset({"a", "b"})),
            ("a,a,a", frozenset({"a"})),
        ],
    )
    def test_split_csv_parses_and_normalizes_tokens(
        self, raw: str | None, expected: frozenset[str]
    ) -> None:
        """split_csv trims whitespace, drops empties, and dedups into a set."""
        tm.that(split_csv(raw), eq=expected)

    def test_split_csv_is_idempotent_under_rejoin(self) -> None:
        """Re-splitting the sorted tokens yields the same set (stable contract)."""
        first = split_csv("gamma, alpha , beta,alpha")
        rejoined = split_csv(",".join(sorted(first)))
        tm.that(first, eq=rejoined)

    # ---- discover_workspace_root: filesystem marker walk ---------------------

    @staticmethod
    def _stamp_workspace_markers(root: Path) -> None:
        """Write the marker set that identifies a FLEXT workspace root."""
        (root / "AGENTS.md").write_text("# sandbox workspace stub")
        (root / "flext-core").mkdir()
        (root / "flext-tests").mkdir()

    def test_discover_workspace_root_returns_marked_root(self, tmp_path: Path) -> None:
        """A directory carrying every marker is reported as the workspace root."""
        self._stamp_workspace_markers(tmp_path)
        tm.that(discover_workspace_root(tmp_path), eq=tmp_path)

    def test_discover_workspace_root_walks_upward_from_nested_start(
        self, tmp_path: Path
    ) -> None:
        """Discovery climbs parents until the marked root is found."""
        self._stamp_workspace_markers(tmp_path)
        nested = tmp_path / "pkg" / "sub"
        nested.mkdir(parents=True)
        tm.that(discover_workspace_root(nested), eq=tmp_path)

    def test_discover_workspace_root_returns_none_without_markers(
        self, tmp_path: Path
    ) -> None:
        """A tree missing any marker yields None rather than a false root."""
        (tmp_path / "AGENTS.md").write_text("stub")
        # flext-core / flext-tests markers deliberately absent.
        tm.that(discover_workspace_root(tmp_path), none=True)

    # ---- active_rules: catalog filtering contract ----------------------------

    @staticmethod
    def _config(
        *, include: frozenset[str] = frozenset(), exclude: frozenset[str] = frozenset()
    ) -> m.Tests.EnforcementDispatcherConfig:
        """Build a resolved dispatcher config for catalog filtering."""
        return m.Tests.EnforcementDispatcherConfig(
            active=True, strict=False, include=include, exclude=exclude
        )

    def test_active_rules_returns_only_enabled_rules(self) -> None:
        """The unfiltered result contains exclusively enabled catalog rules."""
        rules = active_rules(self._config())
        tm.that(rules, empty=False)
        tm.that(all(rule.enabled for rule in rules), eq=True)

    def test_active_rules_include_restricts_to_allow_list(self) -> None:
        """An include allow-list narrows the result to the requested id only."""
        baseline = active_rules(self._config())
        chosen = baseline[0].id
        restricted = active_rules(self._config(include=frozenset({chosen})))
        tm.that({rule.id for rule in restricted}, eq={chosen})

    def test_active_rules_exclude_removes_blocked_rule(self) -> None:
        """An exclude block-list drops exactly the named id from the result."""
        baseline = active_rules(self._config())
        blocked = baseline[0].id
        remaining = active_rules(self._config(exclude=frozenset({blocked})))
        tm.that({rule.id for rule in remaining}, lacks=blocked)
        tm.that(len(remaining), eq=len(baseline) - 1)

    def test_active_rules_include_unknown_id_yields_empty(self) -> None:
        """An allow-list of unknown ids selects no rules (no silent fallback)."""
        tm.that(active_rules(self._config(include=frozenset({"ENFORCE-000"}))), eq=())

    # ---- end-to-end pytest11 pipeline via pytester ---------------------------

    @staticmethod
    def _write_violation_module(pytester: pytest.Pytester) -> None:
        """Write a sandbox test that emits one runtime enforcement warning."""
        pytester.makepyfile(
            test_violation=(
                "import warnings\n"
                "\n"
                "from flext_core import e\n"
                "\n"
                "\n"
                "def test_emits_runtime_enforcement_warning() -> None:\n"
                "    warnings.warn(\n"
                '        "synthetic MRO violation",\n'
                "        e.MroViolation,\n"
                "        stacklevel=2,\n"
                "    )\n"
            )
        )

    @classmethod
    def _make_workspace_sandbox(cls, pytester: pytest.Pytester) -> None:
        """Shape the sandbox as a FLEXT workspace root so auto-activation fires."""
        pytester.makeini("[pytest]\naddopts = --timeout=2.5\n")
        (pytester.path / "AGENTS.md").write_text("# sandbox workspace stub")
        (pytester.path / "flext-core").mkdir()
        (pytester.path / "flext-tests").mkdir()
        cls._write_violation_module(pytester)

    def test_dispatcher_records_warning_and_prints_summary(
        self, pytester: pytest.Pytester
    ) -> None:
        """Non-strict run captures the warning and reports it in the summary."""
        self._make_workspace_sandbox(pytester)
        result = self._run_pytest(pytester, "--flext-enforce-rules=ENFORCE-022")
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.fnmatch_lines([
            "*flext-enforce*",
            "catalog active: 1 rules across 1 source kinds",
            "  runtime_warning: 1",
            "runtime warnings captured: 1",
        ])

    def test_strict_mode_promotes_warning_to_failure(
        self, pytester: pytest.Pytester
    ) -> None:
        """--flext-enforce-strict promotes the configured warning to a failure."""
        self._make_workspace_sandbox(pytester)
        result = self._run_pytest(
            pytester, "--flext-enforce-rules=ENFORCE-022", "--flext-enforce-strict"
        )
        result.assert_outcomes(failed=1)
        result.stdout.fnmatch_lines([
            "*FlextMroViolation: synthetic MRO violation*",
            "runtime warnings captured: 0",
        ])

    def test_dispatcher_inactive_outside_workspace(
        self, pytester: pytest.Pytester
    ) -> None:
        """Without workspace markers the dispatcher stays silent and passive."""
        pytester.makeini("[pytest]\naddopts = --timeout=2.5\n")
        self._write_violation_module(pytester)
        result = self._run_pytest(pytester)
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.no_fnmatch_line("*flext-enforce*")
        result.stdout.no_fnmatch_line("runtime warnings captured:*")

    def test_nested_session_restores_outer_config(
        self, pytester: pytest.Pytester
    ) -> None:
        """A nested pytest lifecycle restores the caller's warning config."""
        outer_config = SessionConfig.value
        tm.that(outer_config, none=False)
        pytester.makeini("[pytest]\naddopts = --timeout=2.5\n")
        pytester.makepyfile("def test_nested_probe() -> None:\n    pass\n")
        self._run_pytest(pytester).assert_outcomes(passed=1)
        tm.that(SessionConfig.value is outer_config, eq=True)

    def test_infra_report_boundary_returns_real_report(self, tmp_path: Path) -> None:
        """Return the real infra report through the public Result boundary."""
        project = tmp_path / "flext-contract-probe"
        package = project / "src" / "flext_contract_probe"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
        (project / "pyproject.toml").write_text(
            '[project]\nname = "flext-contract-probe"\nversion = "0.1.0"\n',
            encoding="utf-8",
        )
        report = load_infra_report(project, project_names=(project.name,)).unwrap()
        tm.that(report.workspace, eq=str(project.resolve()))

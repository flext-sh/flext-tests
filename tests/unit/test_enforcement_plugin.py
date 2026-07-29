"""Behavioral coverage for the enforcement dispatcher public contract.

Two behavioral surfaces are exercised through the module's public API only:

* Pure exported functions (``split_csv``, ``discover_workspace_root``,
  ``active_rules``) are called directly and asserted on their return values and
  invariants.
* The end-to-end pytest11 pipeline (entry-point load -> ``pytest_configure``
  filterwarnings -> ``pytest_warning_recorded`` -> ``pytest_terminal_summary``)
  uses one default-autoload subprocess plus fast isolated in-process sandboxes.
  A separate subprocess consumes the installed public infra-report boundary.
"""

from __future__ import annotations

from importlib.metadata import entry_points
from typing import TYPE_CHECKING

import pytest

from flext_tests import (
    SessionConfig,
    active_rules,
    discover_workspace_root,
    split_csv,
    tm,
    u,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsEnforcementPlugin:
    """Public contract of the enforcement dispatcher facade."""

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

    def test_discover_workspace_root_returns_marked_root(self, tmp_path: Path) -> None:
        """A directory carrying every marker is reported as the workspace root."""
        u.Tests.pytester_stamp_workspace_markers(tmp_path)
        tm.that(discover_workspace_root(tmp_path), eq=tmp_path)

    def test_discover_workspace_root_walks_upward_from_nested_start(
        self, tmp_path: Path
    ) -> None:
        """Discovery climbs parents until the marked root is found."""
        u.Tests.pytester_stamp_workspace_markers(tmp_path)
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

    def test_active_rules_returns_only_enabled_rules(self) -> None:
        """The unfiltered result contains exclusively enabled catalog rules."""
        rules = active_rules(u.Tests.enforcement_dispatcher_config())
        tm.that(rules, empty=False)
        tm.that(all(rule.enabled for rule in rules), eq=True)

    def test_active_rules_include_restricts_to_allow_list(self) -> None:
        """An include allow-list narrows the result to the requested id only."""
        baseline = active_rules(u.Tests.enforcement_dispatcher_config())
        chosen = baseline[0].id
        restricted = active_rules(
            u.Tests.enforcement_dispatcher_config(include=frozenset({chosen}))
        )
        tm.that({rule.id for rule in restricted}, eq={chosen})

    def test_active_rules_exclude_removes_blocked_rule(self) -> None:
        """An exclude block-list drops exactly the named id from the result."""
        baseline = active_rules(u.Tests.enforcement_dispatcher_config())
        blocked = baseline[0].id
        remaining = active_rules(
            u.Tests.enforcement_dispatcher_config(exclude=frozenset({blocked}))
        )
        tm.that({rule.id for rule in remaining}, lacks=blocked)
        tm.that(len(remaining), eq=len(baseline) - 1)

    def test_active_rules_include_unknown_id_yields_empty(self) -> None:
        """An allow-list of unknown ids selects no rules (no silent fallback)."""
        tm.that(
            active_rules(
                u.Tests.enforcement_dispatcher_config(
                    include=frozenset({"ENFORCE-000"})
                )
            ),
            eq=(),
        )

    # ---- end-to-end pytest11 pipeline via pytester ---------------------------

    def test_dispatcher_records_warning_and_prints_summary(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Non-strict run captures the warning and reports it in the summary."""
        u.Tests.pytester_make_enforcement_workspace(pytester)
        result = u.Tests.pytester_run_installed_subprocess(
            pytester, monkeypatch, "--flext-enforce-rules=ENFORCE-022"
        )
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.fnmatch_lines([
            "*flext-enforce*",
            "catalog active: 1 rules across 1 source kinds",
            "  runtime_warning: 1",
            "runtime warnings captured: 1",
        ])

    def test_strict_mode_promotes_warning_to_failure(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """--flext-enforce-strict promotes the configured warning to a failure."""
        u.Tests.pytester_make_enforcement_workspace(pytester)
        result = u.Tests.pytester_run_enforcement(
            pytester,
            monkeypatch,
            "--flext-enforce-rules=ENFORCE-022",
            "--flext-enforce-strict",
        )
        result.assert_outcomes(failed=1)
        result.stdout.fnmatch_lines([
            "*FlextMroViolation: synthetic MRO violation*",
            "runtime warnings captured: 0",
        ])

    def test_dispatcher_inactive_outside_workspace(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Without workspace markers the dispatcher stays silent and passive."""
        pytester.makeini("[pytest]\naddopts = --timeout=2.5\n")
        u.Tests.pytester_make_enforcement_violation(pytester)
        result = u.Tests.pytester_run_enforcement(pytester, monkeypatch)
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.no_fnmatch_line("*flext-enforce*")
        result.stdout.no_fnmatch_line("runtime warnings captured:*")

    def test_nested_session_restores_outer_config(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A nested pytest lifecycle restores the caller's warning config."""
        outer_config = SessionConfig.value
        tm.that(outer_config, none=False)
        pytester.makeini("[pytest]\naddopts = --timeout=2.5\n")
        pytester.makepyfile("def test_nested_probe() -> None:\n    pass\n")
        u.Tests.pytester_run_enforcement(pytester, monkeypatch).assert_outcomes(
            passed=1
        )
        tm.that(SessionConfig.value is outer_config, eq=True)

    def test_infra_report_boundary_runs_in_subprocess(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exercise the installed public infra-report boundary in a subprocess."""
        pytester.makeini("[pytest]\naddopts = --timeout=2.5\n")
        pytester.makepyfile(
            test_public_boundary=(
                "from pathlib import Path\n"
                "\n"
                "from flext_tests import load_infra_report\n"
                "\n"
                "\n"
                "class TestsPublicInfraReportBoundary:\n"
                "    def test_public_boundary_wraps_direct_report(\n"
                "        self,\n"
                "        tmp_path: Path,\n"
                "    ) -> None:\n"
                "        project = tmp_path / 'flext-contract-probe'\n"
                "        package = project / 'src' / 'flext_contract_probe'\n"
                "        package.mkdir(parents=True)\n"
                "        (package / '__init__.py').write_text('', encoding='utf-8')\n"
                "        (project / 'pyproject.toml').write_text(\n"
                "            '[project]\\n'\n"
                "            'name = \\\"flext-contract-probe\\\"\\n'\n"
                "            'version = \\\"0.1.0\\\"\\n',\n"
                "            encoding='utf-8',\n"
                "        )\n"
                "        report = load_infra_report(\n"
                "            project,\n"
                "            project_names=(project.name,),\n"
                "        ).unwrap()\n"
                "        assert report.workspace == str(project.resolve())\n"
            )
        )
        u.Tests.pytester_run_installed_subprocess(
            pytester, monkeypatch
        ).assert_outcomes(passed=1)

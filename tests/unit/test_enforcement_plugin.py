"""Behavioral coverage for the enforcement dispatcher public contract.

Two behavioral surfaces are exercised through the module's public API only:

* Pure exported functions (``split_csv``, ``discover_workspace_root``,
  ``active_rules``) are called directly and asserted on their return values and
  invariants.
* The end-to-end pytest11 pipeline (entry-point load -> ``pytest_configure``
  filterwarnings -> ``pytest_warning_recorded`` -> ``pytest_terminal_summary``)
  is driven inside a ``pytester`` subprocess sandbox and asserted on observable
  outcomes plus the terminal summary the plugin promises to print. Subprocess
  runs keep the real workspace untouched and prove entry-point loading without
  any manual ``-p`` wiring.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import m
from flext_tests._fixtures.enforcement import (
    active_rules,
    discover_workspace_root,
    split_csv,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsEnforcementPlugin:
    """Public contract of the enforcement dispatcher facade."""

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
        self,
        raw: str | None,
        expected: frozenset[str],
    ) -> None:
        """split_csv trims whitespace, drops empties, and dedups into a set."""
        assert split_csv(raw) == expected

    def test_split_csv_is_idempotent_under_rejoin(self) -> None:
        """Re-splitting the sorted tokens yields the same set (stable contract)."""
        first = split_csv("gamma, alpha , beta,alpha")
        rejoined = split_csv(",".join(sorted(first)))
        assert first == rejoined == frozenset({"alpha", "beta", "gamma"})

    # ---- discover_workspace_root: filesystem marker walk ---------------------

    @staticmethod
    def _stamp_workspace_markers(root: Path) -> None:
        """Write the marker set that identifies a FLEXT workspace root."""
        (root / "AGENTS.md").write_text("# sandbox workspace stub")
        (root / "flext-core").mkdir()
        (root / "flext-tests").mkdir()

    def test_discover_workspace_root_returns_marked_root(
        self,
        tmp_path: Path,
    ) -> None:
        """A directory carrying every marker is reported as the workspace root."""
        self._stamp_workspace_markers(tmp_path)
        assert discover_workspace_root(tmp_path) == tmp_path

    def test_discover_workspace_root_walks_upward_from_nested_start(
        self,
        tmp_path: Path,
    ) -> None:
        """Discovery climbs parents until the marked root is found."""
        self._stamp_workspace_markers(tmp_path)
        nested = tmp_path / "pkg" / "sub"
        nested.mkdir(parents=True)
        assert discover_workspace_root(nested) == tmp_path

    def test_discover_workspace_root_returns_none_without_markers(
        self,
        tmp_path: Path,
    ) -> None:
        """A tree missing any marker yields None rather than a false root."""
        (tmp_path / "AGENTS.md").write_text("stub")
        # flext-core / flext-tests markers deliberately absent.
        assert discover_workspace_root(tmp_path) is None

    # ---- active_rules: catalog filtering contract ----------------------------

    @staticmethod
    def _config(
        *,
        include: frozenset[str] = frozenset(),
        exclude: frozenset[str] = frozenset(),
    ) -> m.Tests.EnforcementDispatcherConfig:
        """Build a resolved dispatcher config for catalog filtering."""
        return m.Tests.EnforcementDispatcherConfig(
            active=True,
            strict=False,
            include=include,
            exclude=exclude,
        )

    def test_active_rules_returns_only_enabled_rules(self) -> None:
        """The unfiltered result contains exclusively enabled catalog rules."""
        rules = active_rules(self._config())
        assert rules
        assert all(rule.enabled for rule in rules)

    def test_active_rules_include_restricts_to_allow_list(self) -> None:
        """An include allow-list narrows the result to the requested id only."""
        baseline = active_rules(self._config())
        chosen = baseline[0].id
        restricted = active_rules(self._config(include=frozenset({chosen})))
        assert {rule.id for rule in restricted} == {chosen}

    def test_active_rules_exclude_removes_blocked_rule(self) -> None:
        """An exclude block-list drops exactly the named id from the result."""
        baseline = active_rules(self._config())
        blocked = baseline[0].id
        remaining = active_rules(self._config(exclude=frozenset({blocked})))
        assert blocked not in {rule.id for rule in remaining}
        assert len(remaining) == len(baseline) - 1

    def test_active_rules_include_unknown_id_yields_empty(self) -> None:
        """An allow-list of unknown ids selects no rules (no silent fallback)."""
        assert active_rules(self._config(include=frozenset({"ENFORCE-000"}))) == ()

    # ---- end-to-end pytest11 pipeline via pytester subprocess ----------------

    @staticmethod
    def _write_violation_module(pytester: pytest.Pytester) -> None:
        """Write a sandbox test that emits one runtime enforcement warning."""
        pytester.makepyfile(
            test_violation=(
                "import warnings\n"
                "\n"
                "from flext_core import FlextMroViolation\n"
                "\n"
                "\n"
                "def test_emits_runtime_enforcement_warning() -> None:\n"
                "    warnings.warn(\n"
                '        "synthetic MRO violation",\n'
                "        FlextMroViolation,\n"
                "        stacklevel=2,\n"
                "    )\n"
            ),
        )

    @classmethod
    def _make_workspace_sandbox(cls, pytester: pytest.Pytester) -> None:
        """Shape the sandbox as a FLEXT workspace root so auto-activation fires."""
        pytester.makeini("[pytest]\n")
        (pytester.path / "AGENTS.md").write_text("# sandbox workspace stub")
        (pytester.path / "flext-core").mkdir()
        (pytester.path / "flext-tests").mkdir()
        cls._write_violation_module(pytester)

    def test_dispatcher_records_warning_and_prints_summary(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Non-strict run captures the warning and reports it in the summary."""
        self._make_workspace_sandbox(pytester)
        result = pytester.runpytest_subprocess("--flext-enforce-rules=ENFORCE-022")
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.fnmatch_lines(
            [
                "*flext-enforce*",
                "catalog active: 1 rules across 1 source kinds",
                "  runtime_warning: 1",
                "runtime warnings captured: 1",
            ],
        )

    def test_strict_mode_promotes_warning_to_failure(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """--flext-enforce-strict promotes the configured warning to a failure."""
        self._make_workspace_sandbox(pytester)
        result = pytester.runpytest_subprocess(
            "--flext-enforce-rules=ENFORCE-022",
            "--flext-enforce-strict",
        )
        result.assert_outcomes(failed=1)
        result.stdout.fnmatch_lines(
            [
                "*FlextMroViolation: synthetic MRO violation*",
                "runtime warnings captured: 0",
            ],
        )

    def test_dispatcher_inactive_outside_workspace(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Without workspace markers the dispatcher stays silent and passive."""
        pytester.makeini("[pytest]\n")
        self._write_violation_module(pytester)
        result = pytester.runpytest_subprocess()
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.no_fnmatch_line("*flext-enforce*")
        result.stdout.no_fnmatch_line("runtime warnings captured:*")

    def test_external_pytest11_plugins_are_loaded_in_subprocess(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Auto-registered pytest11 contributions from flext-core/infra load."""
        pytester.makeini("[pytest]\n")
        pytester.makepyfile(
            test_plugins=(
                "from flext_tests._fixtures._enforcement_parts.registry import builders\n"
                "\n"
                "\n"
                "def test_flext_core_plugin_is_registered() -> None:\n"
                "    assert 'flext_core_runtime_warning' in builders()\n"
                "\n"
                "\n"
                "def test_flext_infra_plugin_is_registered() -> None:\n"
                "    assert 'flext_infra_detector' in builders()\n"
            ),
        )
        result = pytester.runpytest_subprocess()
        result.assert_outcomes(passed=2)

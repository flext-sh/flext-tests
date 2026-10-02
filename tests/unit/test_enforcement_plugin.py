"""Behavioral coverage for the enforcement dispatcher public contract.

The end-to-end pytest11 pipeline (entry-point load -> ``pytest_configure``
filterwarnings -> ``pytest_warning_recorded`` -> ``pytest_terminal_summary``)
is driven inside a ``pytester`` subprocess sandbox and asserted on observable
outcomes plus the terminal summary the plugin promises to print. Subprocess
runs keep the real workspace untouched and prove entry-point loading without
any manual ``-p`` wiring.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import entry_points

import pytest

from flext_tests import tm


class TestsFlextTestsEnforcementPlugin:
    """Public contract of the enforcement dispatcher facade."""

    # Subprocess cases are reserved for contracts whose behavior is entry-point
    # discovery itself; ordinary dispatcher behavior stays in-process or loads
    # only its explicit owner plugins.

    def test_flext_pytest11_entrypoints_have_one_package_owner(self) -> None:
        """The flext-tests distribution publishes exactly its two pytest plugins."""
        names = {
            entry.name
            for entry in entry_points(group="pytest11")
            if entry.dist is not None and entry.dist.name == "flext-tests"
        }
        tm.that(names, eq={"flext_tests", "flext_tests_enforcement"})

    def test_flext_pytest11_entrypoint_load_defers_fixture_imports(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Cold entry-point discovery does not pre-import measured product code."""
        probe = (
            "from importlib.metadata import entry_points\n"
            "import sys\n"
            "entries = {entry.name: entry for entry in entry_points(group='pytest11')}\n"
            "entries['flext_tests'].load()\n"
            "entries['flext_tests_enforcement'].load()\n"
            "eager = sorted(\n"
            "    name for name in sys.modules\n"
            "    if name.startswith('flext_tests._fixtures')\n"
            ")\n"
            "if eager:\n"
            "    raise RuntimeError(f'eager fixture imports: {eager}')\n"
        )
        completed = pytester.runpython_c(probe)
        tm.that(completed.ret, eq=0)
        tm.that(completed.errlines, eq=[])

    @pytest.mark.slow
    def test_inactive_session_collects_without_the_model_facade(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """An ungoverned session configures and collects without ``m`` loaded."""
        pytester.makeini("[pytest]\n")
        pytester.makeconftest(
            "import sys\n"
            "\n"
            "\n"
            "def pytest_collection_finish(session):\n"
            "    if 'flext_tests.models' in sys.modules:\n"
            "        raise RuntimeError('flext_tests.models loaded at collection')\n",
        )
        pytester.makepyfile(test_probe="def test_probe() -> None:\n    assert True\n")
        result = pytester.runpytest_subprocess("--collect-only", "-q")
        tm.that(result.ret, eq=pytest.ExitCode.OK)
        result.stdout.fnmatch_lines(["*test_probe*"])

    # ---- end-to-end pytest11 pipeline via pytester subprocess ----------------

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

    @pytest.mark.slow
    def test_dispatcher_records_warning_and_prints_summary(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Non-strict run captures the warning and reports it in the summary."""
        self._make_workspace_sandbox(pytester)
        result = pytester.runpytest_subprocess("--flext-enforce-rules=ENFORCE-022")
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.fnmatch_lines([
            "*flext-enforce*",
            "catalog active: 1 rules across 1 source kinds",
            "  runtime_warning: 1",
            "runtime warnings captured: 1",
        ])

    @pytest.mark.slow
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
        result.stdout.fnmatch_lines([
            "*FlextMroViolation: synthetic MRO violation*",
            "runtime warnings captured: 0",
        ])

    @pytest.mark.slow
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

    @pytest.mark.slow
    def test_infra_rule_engine_boundary_runs_in_subprocess(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Engine findings come through the public Result boundary; a rule the
        engine does not declare is a failure, never an empty scan.
        """
        pytester.makeini("[pytest]\n")
        pytester.makepyfile(
            test_public_boundary=(
                "from pathlib import Path\n"
                "\n"
                "from flext_tests import u\n"
                "\n"
                "\n"
                "class TestsPublicInfraRuleBoundary:\n"
                "    def test_engine_boundary(self, tmp_path: Path) -> None:\n"
                "        project = tmp_path / 'flext-contract-probe'\n"
                "        package = project / 'src' / 'flext_contract_probe'\n"
                "        package.mkdir(parents=True)\n"
                "        (package / '__init__.py').write_text(\n"
                '            \'"""Probe."""\\n\\nfrom __future__ import annotations\\n\',\n'
                "            encoding='utf-8',\n"
                "        )\n"
                "        (project / 'pyproject.toml').write_text(\n"
                "            '[project]\\n'\n"
                "            'name = \\\"flext-contract-probe\\\"\\n'\n"
                "            'version = \\\"0.1.0\\\"\\n',\n"
                "            encoding='utf-8',\n"
                "        )\n"
                "        missing = u.Tests.infra_rule_findings(\n"
                "            project, required_rule_ids=frozenset({'no-such-rule'})\n"
                "        )\n"
                "        assert missing.failure\n"
                "        assert 'no-such-rule' in str(missing.error)\n"
                "        scanned = u.Tests.infra_rule_findings(\n"
                "            project, required_rule_ids=frozenset()\n"
                "        )\n"
                "        assert scanned.success\n"
            ),
        )
        result = pytester.runpytest_subprocess()
        result.assert_outcomes(passed=1)

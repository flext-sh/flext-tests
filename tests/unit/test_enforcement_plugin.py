"""Behavioral coverage for the enforcement dispatcher public contract.

The end-to-end pytest11 pipeline (entry-point load -> ``pytest_configure``
filterwarnings -> ``pytest_warning_recorded`` -> ``pytest_terminal_summary``)
is driven inside a ``pytester`` subprocess sandbox and asserted on observable
outcomes plus the terminal summary the plugin promises to print. Subprocess
runs keep the real workspace untouched and prove entry-point loading without
any manual ``-p`` wiring.
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
        """Only the two flext-tests plugins participate in pytest autoload."""
        names = {
            entry.name
            for entry in entry_points(group="pytest11")
            if entry.name.startswith("flext_")
        }
        tm.that(names, eq={"flext_tests", "flext_tests_enforcement"})

    def test_flext_pytest11_entrypoint_load_defers_fixture_imports(
        self, pytester: pytest.Pytester
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
            )
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
        self, pytester: pytest.Pytester
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
        self, pytester: pytest.Pytester
    ) -> None:
        """--flext-enforce-strict promotes the configured warning to a failure."""
        self._make_workspace_sandbox(pytester)
        result = pytester.runpytest_subprocess(
            "--flext-enforce-rules=ENFORCE-022", "--flext-enforce-strict"
        )
        result.assert_outcomes(failed=1)
        result.stdout.fnmatch_lines([
            "*FlextMroViolation: synthetic MRO violation*",
            "runtime warnings captured: 0",
        ])

    @pytest.mark.slow
    def test_dispatcher_inactive_outside_workspace(
        self, pytester: pytest.Pytester
    ) -> None:
        """Without workspace markers the dispatcher stays silent and passive."""
        pytester.makeini("[pytest]\n")
        self._write_violation_module(pytester)
        result = pytester.runpytest_subprocess()
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.no_fnmatch_line("*flext-enforce*")
        result.stdout.no_fnmatch_line("runtime warnings captured:*")

    @pytest.mark.slow
    def test_infra_report_boundary_runs_in_subprocess(
        self, pytester: pytest.Pytester
    ) -> None:
        """Return the real infra report through the public Result boundary."""
        # NOTE (multi-agent, mro-wkii.17.21): exercise only the installed public
        # boundary; private plugin registration is an implementation detail.
        pytester.makeini("[pytest]\n")
        pytester.makepyfile(
            test_public_boundary=(
                "from pathlib import Path\n"
                "\n"
                "from flext_tests import u\n"
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
                "        report = u.Tests.load_infra_report(\n"
                "            project,\n"
                "            project_names=(project.name,),\n"
                "        ).unwrap()\n"
                "        assert report.workspace == str(project.resolve())\n"
            )
        )
        result = pytester.runpytest_subprocess()
        result.assert_outcomes(passed=1)

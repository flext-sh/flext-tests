"""End-to-end pytester coverage for the enforcement dispatcher warning pipeline.

Each test drives a complete pytest run inside a pytester sandbox: the
``flext_tests_enforcement`` pytest11 entry point loads, ``pytest_configure``
registers filterwarnings for runtime-warning rules, ``pytest_warning_recorded``
counts emitted ``FlextMroViolation`` warnings, and ``pytest_terminal_summary``
prints the evidence asserted here. Subprocess runs keep the real workspace
untouched and prove entry-point loading without any manual ``-p`` wiring.
"""

from __future__ import annotations

import pytest


class TestsFlextTestsEnforcementPlugin:
    """Prove entry point -> config -> warning hook -> terminal summary."""

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
                '    warnings.warn(\n'
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

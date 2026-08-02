"""Behavioral contracts for the canonical pytest timeout policy."""

from __future__ import annotations

import os
from typing import ClassVar

import pytest

from flext_tests import tm


class TestsFlextTestsEnforcementTimeoutPolicy:
    """Exercise timeout enforcement through the installed pytest11 plugin."""

    policy_seconds: ClassVar[float] = 2.5

    @classmethod
    def _make_policy_ini(
        cls,
        pytester: pytest.Pytester,
        *,
        duplicate_addopts: bool = False,
        func_only: bool = False,
        include_addopts: bool = True,
        timeout_ini: float | None = None,
    ) -> None:
        """Configure an alternate valid ceiling without freezing production values."""
        lines = ["[pytest]"]
        if include_addopts:
            addopts = f"--timeout={cls.policy_seconds}"
            if duplicate_addopts:
                addopts = f"{addopts} --timeout {cls.policy_seconds}"
            lines.append(f"addopts = {addopts}")
        if timeout_ini is not None:
            lines.append(f"timeout = {timeout_ini}")
        lines.append(f"timeout_func_only = {'true' if func_only else 'false'}")
        pytester.makeini("\n".join(lines))

    @staticmethod
    def _make_test(pytester: pytest.Pytester, *, marker: str | None = None) -> None:
        """Write one trivial item, optionally decorated with a timeout marker."""
        decorator = f"@pytest.mark.timeout({marker})\n" if marker else ""
        pytester.makepyfile(
            f"import pytest\n\n{decorator}def test_policy_probe() -> None:\n    pass\n"
        )

    @staticmethod
    def _usage_error(result: pytest.RunResult) -> None:
        """Assert that a nested pytest run failed closed at the policy boundary."""
        tm.that(result.ret, ne=pytest.ExitCode.OK)
        tm.that("\n".join(result.stderr.lines), has="FLEXT timeout policy:")

    @staticmethod
    def _run_pytest(pytester: pytest.Pytester, *args: str) -> pytest.RunResult:
        """Run the owned plugins without unrelated entry-point side effects."""
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

    @pytest.mark.parametrize("ratio", [None, 1.0, 0.5])
    def test_accepts_no_cli_override_exact_or_below_policy(
        self, pytester: pytest.Pytester, ratio: float | None
    ) -> None:
        """No override and non-weakening CLI values preserve the configured ceiling."""
        self._make_policy_ini(pytester)
        self._make_test(pytester)
        args = () if ratio is None else (f"--timeout={self.policy_seconds * ratio}",)
        result = self._run_pytest(pytester, *args)
        result.assert_outcomes(passed=1)

    @pytest.mark.parametrize("ratio", [0.0, 2.0])
    def test_rejects_cli_timeout_that_disables_or_exceeds_policy(
        self, pytester: pytest.Pytester, ratio: float
    ) -> None:
        """CLI cannot disable the timer or increase its configured ceiling."""
        self._make_policy_ini(pytester)
        self._make_test(pytester)
        result = self._run_pytest(pytester, f"--timeout={self.policy_seconds * ratio}")
        self._usage_error(result)

    @pytest.mark.parametrize("ratio", [1.0, 0.5])
    def test_accepts_marker_at_or_below_policy(
        self, pytester: pytest.Pytester, ratio: float
    ) -> None:
        """A marker may only retain or tighten the configured item ceiling."""
        self._make_policy_ini(pytester)
        self._make_test(pytester, marker=str(self.policy_seconds * ratio))
        result = self._run_pytest(pytester)
        result.assert_outcomes(passed=1)

    @pytest.mark.parametrize("ratio", [1.0, 0.5])
    def test_accepts_timeout_ini_at_or_below_addopts_cap(
        self, pytester: pytest.Pytester, ratio: float
    ) -> None:
        """Optional timeout ini may retain or tighten the addopts-owned cap."""
        self._make_policy_ini(pytester, timeout_ini=self.policy_seconds * ratio)
        self._make_test(pytester)
        self._run_pytest(pytester).assert_outcomes(passed=1)

    @pytest.mark.parametrize(
        "marker",
        [
            "0",
            f"{policy_seconds * 2}",
            "1.0, timeout=1.0",
            "1.0, 'signal', method='thread'",
            "1.0, 'signal', False",
            "1.0, func_only=True",
            "1.0, unsupported=True",
        ],
    )
    def test_rejects_weakening_or_conflicting_timeout_marker(
        self, pytester: pytest.Pytester, marker: str
    ) -> None:
        """Marker zero, excess, duplicate values, and func-only are forbidden."""
        self._make_policy_ini(pytester)
        self._make_test(pytester, marker=marker)
        result = self._run_pytest(pytester)
        self._usage_error(result)

    def test_rejects_duplicate_addopts_timeout(self, pytester: pytest.Pytester) -> None:
        """Configured addopts must contain one and only one canonical timeout."""
        self._make_policy_ini(pytester, duplicate_addopts=True)
        self._make_test(pytester)
        self._usage_error(self._run_pytest(pytester))

    def test_rejects_missing_addopts_timeout(self, pytester: pytest.Pytester) -> None:
        """Timeout ini cannot replace the missing canonical addopts owner."""
        self._make_policy_ini(
            pytester, include_addopts=False, timeout_ini=self.policy_seconds
        )
        self._make_test(pytester)
        self._usage_error(self._run_pytest(pytester))

    def test_rejects_timeout_ini_above_addopts_cap(
        self, pytester: pytest.Pytester
    ) -> None:
        """Timeout ini cannot exceed the canonical addopts-owned cap."""
        self._make_policy_ini(pytester, timeout_ini=self.policy_seconds * 2)
        self._make_test(pytester)
        self._usage_error(self._run_pytest(pytester))

    def test_rejects_configured_func_only(self, pytester: pytest.Pytester) -> None:
        """Configuration cannot exclude fixture setup and teardown from the timer."""
        self._make_policy_ini(pytester, func_only=True)
        self._make_test(pytester)
        self._usage_error(self._run_pytest(pytester))

    @pytest.mark.parametrize(
        "override", [("-o", "timeout=5.0"), ("--override-ini=timeout=5.0",)]
    )
    def test_rejects_override_ini_forms(
        self, pytester: pytest.Pytester, override: tuple[str, ...]
    ) -> None:
        """Both pytest override-ini spellings are rejected fail-closed."""
        self._make_policy_ini(pytester)
        self._make_test(pytester)
        self._usage_error(self._run_pytest(pytester, *override))

    @pytest.mark.parametrize("variable", ["PYTEST_TIMEOUT", "PYTEST_ADDOPTS"])
    def test_rejects_environment_timeout_above_policy(
        self, pytester: pytest.Pytester, variable: str
    ) -> None:
        """Environment-controlled timeout precedence cannot weaken the ceiling."""
        self._make_policy_ini(pytester)
        self._make_test(pytester)
        previous = os.environ.get(variable)
        value = str(self.policy_seconds * 2)
        os.environ[variable] = (
            value if variable == "PYTEST_TIMEOUT" else f"--timeout={value}"
        )
        try:
            result = self._run_pytest(pytester)
        finally:
            if previous is None:
                os.environ.pop(variable, None)
            else:
                os.environ[variable] = previous
        self._usage_error(result)

    def test_rejects_timeout_marker_added_by_late_collection_plugin(
        self, pytester: pytest.Pytester
    ) -> None:
        """Trylast validation sees markers added by other collection plugins."""
        self._make_policy_ini(pytester)
        self._make_test(pytester)
        pytester.makeconftest(
            "import pytest\n"
            "\n"
            "\n"
            "@pytest.hookimpl(tryfirst=True)\n"
            "def pytest_collection_modifyitems(items):\n"
            "    for item in items:\n"
            "        item.add_marker(pytest.mark.timeout(0))\n"
        )
        self._usage_error(self._run_pytest(pytester))

"""Canonical pytester helpers for public pytest11 plugin contracts."""

from __future__ import annotations

import pytest

from flext_tests import tm


class FlextTestsPytesterUtilitiesMixin:
    """Compose reusable pytester operations under ``u.Tests``."""

    @staticmethod
    def pytester_run_installed_subprocess(
        pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, *args: str
    ) -> pytest.RunResult:
        """Run a subprocess with default pytest11 entry-point autoload enabled."""
        with monkeypatch.context() as environment:
            environment.delenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", raising=False)
            return pytester.runpytest_subprocess(*args)

    @staticmethod
    def pytester_run_enforcement(
        pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, *args: str
    ) -> pytest.RunResult:
        """Run only pytest-timeout and the installed enforcement entry point."""
        with monkeypatch.context() as environment:
            environment.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
            return pytester.runpytest_inprocess(
                "-p", "pytest_timeout", "-p", "flext_tests_enforcement", *args
            )

    @staticmethod
    def pytester_make_timeout_ini(
        pytester: pytest.Pytester,
        *,
        policy_seconds: float,
        duplicate_addopts: bool = False,
        func_only: bool = False,
        include_addopts: bool = True,
        timeout_ini: float | None = None,
    ) -> None:
        """Configure a sandbox timeout ceiling without production-value coupling."""
        lines = ["[pytest]"]
        if include_addopts:
            addopts = f"--timeout={policy_seconds}"
            if duplicate_addopts:
                addopts = f"{addopts} --timeout {policy_seconds}"
            lines.append(f"addopts = {addopts}")
        if timeout_ini is not None:
            lines.append(f"timeout = {timeout_ini}")
        lines.append(f"timeout_func_only = {'true' if func_only else 'false'}")
        pytester.makeini("\n".join(lines))

    @staticmethod
    def pytester_make_timeout_test(
        pytester: pytest.Pytester, *, marker: str | None = None
    ) -> None:
        """Write one trivial sandbox item with an optional timeout marker."""
        decorator = f"@pytest.mark.timeout({marker})\n" if marker else ""
        pytester.makepyfile(
            f"import pytest\n\n{decorator}def test_policy_probe() -> None:\n    pass\n"
        )

    @staticmethod
    def pytester_assert_usage_error(result: pytest.RunResult) -> None:
        """Assert that a nested pytest run failed at the timeout-policy boundary."""
        tm.that(result.ret, ne=pytest.ExitCode.OK)
        tm.that("\n".join(result.stderr.lines), has="FLEXT timeout policy:")


__all__: list[str] = ["FlextTestsPytesterUtilitiesMixin"]

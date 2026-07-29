"""Canonical pytester helpers for public pytest11 plugin contracts."""

from __future__ import annotations

from importlib.metadata import entry_points
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from flext_tests import c, m, tm

if TYPE_CHECKING:
    from flext_tests import p


class FlextTestsPytesterUtilitiesMixin:
    """Compose reusable pytester operations under ``u.Tests``."""

    @staticmethod
    def pytester_enforcement_plugin_name() -> str:
        """Resolve the enforcement route from installed pytest11 metadata."""
        from flext_tests import active_rules

        package_root = active_rules.__module__.partition(".")[0]
        matches = tuple(
            entry.name
            for entry in entry_points(group="pytest11")
            if entry.module.partition(".")[0] == package_root
            and getattr(entry.load(), "active_rules", None) is active_rules
        )
        if len(matches) != 1:
            message = (
                "installed pytest11 metadata must expose exactly one FLEXT "
                "enforcement plugin"
            )
            raise RuntimeError(message)
        return matches[0]

    @staticmethod
    def pytester_stamp_workspace_markers(root: Path) -> None:
        """Write the marker set that identifies a FLEXT workspace root."""
        for marker in c.Tests.ENFORCEMENT_WORKSPACE_MARKERS:
            (root / marker).mkdir()

    @staticmethod
    def enforcement_dispatcher_config(
        *, include: frozenset[str] = frozenset(), exclude: frozenset[str] = frozenset()
    ) -> p.Tests.EnforcementDispatcherConfig:
        """Build a resolved enforcement dispatcher config."""
        return m.Tests.EnforcementDispatcherConfig(
            active=True, strict=False, include=include, exclude=exclude
        )

    @staticmethod
    def pytester_make_enforcement_violation(pytester: pytest.Pytester) -> None:
        """Write a sandbox item that emits one runtime enforcement warning."""
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
    def pytester_make_enforcement_workspace(
        cls, pytester: pytest.Pytester, *, policy_seconds: float
    ) -> None:
        """Shape a sandbox workspace with an explicit generated timeout policy."""
        cls.pytester_make_timeout_ini(
            pytester, policy_seconds=policy_seconds, func_only=False
        )
        cls.pytester_stamp_workspace_markers(pytester.path)
        cls.pytester_make_enforcement_violation(pytester)

    @staticmethod
    def pytester_run_installed_subprocess(
        pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, *args: str
    ) -> pytest.RunResult:
        """Run a subprocess with default pytest11 entry-point autoload enabled."""
        with monkeypatch.context() as environment:
            environment.delenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", raising=False)
            return pytester.runpytest_subprocess(*args)

    @classmethod
    def pytester_run_enforcement(
        cls, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, *args: str
    ) -> pytest.RunResult:
        """Run only pytest-timeout and the installed enforcement entry point."""
        with monkeypatch.context() as environment:
            environment.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
            return pytester.runpytest_inprocess(
                "-p",
                "pytest_timeout",
                "-p",
                cls.pytester_enforcement_plugin_name(),
                *args,
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
            addopts = f"{c.Tests.PYTEST_TIMEOUT_OPTION}={policy_seconds}"
            if duplicate_addopts:
                addopts = f"{addopts} {c.Tests.PYTEST_TIMEOUT_OPTION} {policy_seconds}"
            lines.append(f"{c.Tests.PYTEST_ADDOPTS_INI} = {addopts}")
        if timeout_ini is not None:
            lines.append(f"{c.Tests.PYTEST_TIMEOUT_INI} = {timeout_ini}")
        lines.append(
            f"{c.Tests.PYTEST_TIMEOUT_FUNC_ONLY_INI} = "
            f"{'true' if func_only else 'false'}"
        )
        pytester.makeini("\n".join(lines))

    @staticmethod
    def pytester_make_timeout_test(
        pytester: pytest.Pytester, *, marker: str | None = None
    ) -> None:
        """Write one trivial sandbox item with an optional timeout marker."""
        decorator = (
            f"@pytest.mark.{c.Tests.PYTEST_TIMEOUT_MARKER}({marker})\n"
            if marker
            else ""
        )
        pytester.makepyfile(
            f"import pytest\n\n{decorator}def test_policy_probe() -> None:\n    pass\n"
        )

    @staticmethod
    def pytester_assert_usage_error(result: pytest.RunResult) -> None:
        """Assert that a nested pytest run failed at the timeout-policy boundary."""
        tm.that(result.ret, ne=pytest.ExitCode.OK)
        tm.that("\n".join(result.stderr.lines), has="FLEXT timeout policy:")


__all__: list[str] = ["FlextTestsPytesterUtilitiesMixin"]

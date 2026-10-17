"""Behavioral contracts for config-owned slow pytest item budgets.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os

import pytest

from flext_infra import config

from tests import tm


class TestsFlextTestsSlowTimeoutPolicy:
    """Exercise the installed enforcement adapter through nested pytest runs."""

    slow_timeout_seconds = 0.75

    @staticmethod
    def _make_ini(
        pytester: pytest.Pytester,
        *,
        slow_timeout: str | None,
    ) -> None:
        """Write one isolated policy using arbitrary non-production budgets."""
        lines = ["[pytest]", "markers = slow: explicitly slow contract"]
        if slow_timeout is not None:
            lines.append(f"flext_slow_timeout_seconds = {slow_timeout}")
        pytester.makeini("\n".join(lines))

    @staticmethod
    def _run_pytest(
        pytester: pytest.Pytester,
        *,
        include_timeout_plugin: bool = True,
        unbounded: bool = False,
    ) -> pytest.RunResult:
        """Run only the two owner plugins in a subprocess-isolated session.

        Returns:
            The resulting ``pytest.RunResult``.

        """
        variable = "PYTEST_DISABLE_PLUGIN_AUTOLOAD"
        previous = os.environ.get(variable)
        os.environ[variable] = "1"
        enforcement = config.Infra.tooling.tools.pytest.enforcement_plugin
        plugins = (
            ("-p", "pytest_timeout", "-p", enforcement)
            if include_timeout_plugin
            else ("-p", enforcement)
        )
        try:
            return pytester.runpytest_subprocess(
                *plugins,
                *(("--timeout=0",) if unbounded else ()),
            )
        finally:
            if previous is None:
                os.environ.pop(variable, None)
            else:
                os.environ[variable] = previous

    @pytest.mark.slow
    def test_configured_budget_applies_only_to_explicit_slow_items(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Only slow items receive a timer; regular items have no item budget."""
        self._make_ini(pytester, slow_timeout=str(self.slow_timeout_seconds))
        pytester.makepyfile(
            "import pytest\n"
            "\n"
            "from tests import tm\n"
            "\n"
            "\n"
            "@pytest.mark.slow\n"
            "def test_slow_budget(request: pytest.FixtureRequest) -> None:\n"
            "    marker = request.node.get_closest_marker('timeout')\n"
            "    tm.that(marker is not None, eq=True)\n"
            "    if marker is not None:\n"
            f"        tm.that(marker.args, eq=({self.slow_timeout_seconds},))\n"
            "\n"
            "\n"
            "def test_regular_budget(request: pytest.FixtureRequest) -> None:\n"
            "    tm.that(request.node.get_closest_marker('timeout'), none=True)\n",
        )

        self._run_pytest(pytester).assert_outcomes(passed=2)

    @pytest.mark.slow
    def test_unbounded_run_disables_regular_and_slow_item_timers(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """The full-run override disables timers without weakening policy."""
        self._make_ini(pytester, slow_timeout=str(self.slow_timeout_seconds))
        pytester.makepyfile(
            "import pytest\n"
            "from tests import tm\n"
            "\n"
            "def test_regular_unbounded(request: pytest.FixtureRequest) -> None:\n"
            "    tm.that(request.config.getoption('timeout'), eq=0)\n"
            "    tm.that(request.node.get_closest_marker('timeout'), none=True)\n"
            "\n"
            "@pytest.mark.slow\n"
            "def test_slow_unbounded(request: pytest.FixtureRequest) -> None:\n"
            "    tm.that(request.config.getoption('timeout'), eq=0)\n"
            "    tm.that(request.node.get_closest_marker('timeout'), none=True)\n",
        )

        self._run_pytest(pytester, unbounded=True).assert_outcomes(passed=2)

    @pytest.mark.slow
    def test_absent_slow_budget_requires_no_timeout_plugin(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """An unconfigured project needs no timer for slow or regular items."""
        self._make_ini(pytester, slow_timeout=None)
        pytester.makepyfile(
            "import pytest\n"
            "\n"
            "from tests import tm\n"
            "\n"
            "\n"
            "@pytest.mark.slow\n"
            "def test_slow_without_budget(request: pytest.FixtureRequest) -> None:\n"
            "    tm.that(request.node.get_closest_marker('timeout'), none=True)\n"
            "\n"
            "\n"
            "def test_regular_without_budget(request: pytest.FixtureRequest) -> None:\n"
            "    tm.that(request.node.get_closest_marker('timeout'), none=True)\n",
        )

        self._run_pytest(pytester, include_timeout_plugin=False).assert_outcomes(
            passed=2
        )

    @pytest.mark.slow
    @pytest.mark.parametrize("invalid_timeout", ["0", "nan", "not-a-number"])
    @pytest.mark.parametrize("unbounded", [False, True])
    def test_invalid_slow_budget_fails_closed(
        self,
        pytester: pytest.Pytester,
        invalid_timeout: str,
        *,
        unbounded: bool,
    ) -> None:
        """Non-positive, non-finite, and malformed policy values are rejected."""
        self._make_ini(pytester, slow_timeout=invalid_timeout)
        pytester.makepyfile("def test_policy_probe() -> None:\n    pass\n")

        result = self._run_pytest(pytester, unbounded=unbounded)

        tm.that(result.ret, ne=pytest.ExitCode.OK)
        result.stderr.fnmatch_lines([
            "*FLEXT slow timeout policy:*must be a positive finite number*",
        ])

    @pytest.mark.slow
    @pytest.mark.parametrize("unbounded", [False, True])
    def test_explicit_slow_timeout_marker_fails_closed(
        self,
        pytester: pytest.Pytester,
        *,
        unbounded: bool,
    ) -> None:
        """Slow test code cannot restate or weaken its config-owned budget."""
        self._make_ini(pytester, slow_timeout=str(self.slow_timeout_seconds))
        pytester.makepyfile(
            "import pytest\n"
            "\n"
            "\n"
            "@pytest.mark.slow\n"
            f"@pytest.mark.timeout({self.slow_timeout_seconds})\n"
            "def test_explicit_timeout() -> None:\n"
            "    pass\n",
        )

        result = self._run_pytest(pytester, unbounded=unbounded)

        tm.that(result.ret, ne=pytest.ExitCode.OK)
        result.stderr.fnmatch_lines([
            "*FLEXT slow timeout policy:*explicit pytest.mark.timeout is forbidden*",
        ])

    @pytest.mark.slow
    def test_configured_policy_requires_pytest_timeout(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Configured slow budgets fail if the timer owner is not loaded."""
        self._make_ini(pytester, slow_timeout=str(self.slow_timeout_seconds))
        pytester.makepyfile("def test_policy_probe() -> None:\n    pass\n")

        result = self._run_pytest(pytester, include_timeout_plugin=False)

        tm.that(result.ret, ne=pytest.ExitCode.OK)
        result.stderr.fnmatch_lines([
            "*FLEXT slow timeout policy requires the pytest-timeout plugin*",
        ])

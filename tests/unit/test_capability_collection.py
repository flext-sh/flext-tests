"""Capability-gated collection tests (T4, bead flext-ht1t9.6).

The inner runs are subprocesses with the fleet plugins disabled except the
pytest11 auto-loaded ones, matching a consumer suite's real environment.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

pytest_plugins = ["pytester"]

_COMMON_CONFTEST = (
    "import pytest\n"
    "from pathlib import Path\n"
    "from flext_tests import u\n"
    "\n"
    "@pytest.fixture\n"
    "def record_marker(request):\n"
    "    return [m.name for m in request.node.iter_markers()]\n"
)

_DOCKER_TEST = "test_docker.py"


def _write_docker_probe(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(**{
        _DOCKER_TEST: (
            "import pytest\n"
            "\n"
            "pytestmark = pytest.mark.docker\n"
            "\n"
            "def test_needs_docker():\n"
            "    assert True\n"
        ),
    })


class TestsFlextTestsCapabilityCollection:
    """Typed capability deselection replaces skip-based gating."""

    @staticmethod
    @pytest.mark.slow
    def test_ci_y_deselects_docker_tests_as_not_executed(
        pytester: pytest.Pytester,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Under exact CI=Y the docker test is DESELECTED, never skipped."""
        _write_docker_probe(pytester)
        pytester.makeconftest(_COMMON_CONFTEST)
        monkeypatch.setenv("CI", "Y")
        result = pytester.runpytest_subprocess(
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
        )
        result.assert_outcomes(passed=0, failed=0, skipped=0)
        out = result.stdout.str()
        assert "NOT EXECUTED" in out
        assert "test_needs_docker" in out

    @staticmethod
    @pytest.mark.slow
    def test_capable_host_executes_and_real_failure_is_red(
        pytester: pytest.Pytester,
    ) -> None:
        """On a Docker-capable host the test runs; a failure stays RED.

        The service layer adopts the rootless per-user endpoint when the SDK
        default socket is absent, so the pytester subprocess needs no env
        plant: the capability resolves the way the operator's docker runs.
        """
        pytester.makepyfile(**{
            _DOCKER_TEST: (
                "import pytest\n"
                "\n"
                "pytestmark = pytest.mark.docker\n"
                "\n"
                "def test_needs_docker():\n"
                "    assert False, 'service misbehaved'\n"
            ),
        })
        result = pytester.runpytest_subprocess(
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
        )
        result.assert_outcomes(failed=1)
        out = result.stdout.str()
        assert "service misbehaved" in out

    @staticmethod
    @pytest.mark.slow
    def test_unmarked_tests_are_never_touched(
        pytester: pytest.Pytester,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """CI=Y only deselects marker-carrying tests; plain tests execute."""
        pytester.makepyfile(test_plain="def test_plain():\n    assert True\n")
        pytester.makeconftest(_COMMON_CONFTEST)
        monkeypatch.setenv("CI", "Y")
        result = pytester.runpytest_subprocess(
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
        )
        result.assert_outcomes(passed=1)

    @staticmethod
    @pytest.mark.slow
    def test_no_skip_marker_is_ever_applied(
        pytester: pytest.Pytester,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """The deselection is collection-time: skipped count stays zero."""
        _write_docker_probe(pytester)
        pytester.makeconftest(_COMMON_CONFTEST)
        monkeypatch.setenv("CI", "Y")
        result = pytester.runpytest_subprocess(
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
            "-rs",
        )
        result.assert_outcomes(skipped=0)

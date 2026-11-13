"""Shared scratch-storage tests (T6, bead flext-ht1t9.8).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from tests import c, p, t, tm, u


class TestsFlextTestsScratchStorage:
    """Public contract of the shared scratch-storage plugin."""

    @staticmethod
    @c.Tests.MARK.slow
    def test_scratch_root_ini_override(
        pytester: t.Tests.Pytester,
        tmp_path: Path,
    ) -> None:
        """The flext_scratch_root ini redirects the shared storage root."""
        override = tmp_path / "custom-scratch"
        pytester.makepyfile(
            test_plain=(
                "def test_plain(scratch_root):\n"
                f"    assert str(scratch_root) == {str(override)!r}\n"
            ),
        )
        result = u.Tests.pytest_subprocess(
            pytester,
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
            "-o",
            f"{c.Tests.SCRATCH_ROOT_INI}={override}",
        )
        result.assert_outcomes(passed=1)
        tm.ok(override.exists())

    @staticmethod
    def test_scratch_root_utility_is_shared_and_honors_the_override(
        tmp_path: Path,
    ) -> None:
        """u.Tests.scratch_root is one root for every checkout; the ini overrides it."""
        override = tmp_path / "custom"
        tm.that(u.Tests.scratch_root(), eq=u.Tests.scratch_root())
        tm.that(u.Tests.scratch_root(override=str(override)), eq=override)

    @staticmethod
    def test_session_runtime_storage_is_the_controller_scratch_root(
        request: t.Tests.FixtureRequest,
        session_runtime: p.Tests.SessionRuntime,
    ) -> None:
        """Every worker's session runtime carries the controller's scratch root."""
        config = request.config
        expected = u.Tests.scratch_root(
            override=config.getini(c.Tests.SCRATCH_ROOT_INI) or None,
        )
        tm.that(session_runtime.storage, eq=expected)
        tm.that(
            session_runtime.directory.is_relative_to(session_runtime.storage),
            eq=False,
        )

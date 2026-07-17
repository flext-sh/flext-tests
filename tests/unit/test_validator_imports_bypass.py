"""Unit tests for the public import and bypass validator surfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import p, tm, tv
from tests import u


class TestsFlextTestsValidatorImportsBypass:
    """Verify import and bypass validator rules through the public facade."""

    @staticmethod
    def _write_source(tmp_path: Path, name: str, source: str) -> Path:
        file_path = tmp_path / name
        file_path.write_text(source, encoding="utf-8")
        return file_path

    def test_imports_flags_indented_imports_importerror_sys_path_and_internal_modules(
        self, tmp_path: Path
    ) -> None:
        file_path = self._write_source(
            tmp_path,
            "imports_scan.py",
            """from __future__ import annotations

from flext_core._utilities.project_metadata import read_project_constants


def load() -> None:
    import os
    try:
        from missing_package import api
    except ImportError:
        return None

    sys.path.append(os.getcwd())
""",
        )

        result: p.Tests.ScanResult = u.Tests.assert_success(tv.imports(file_path))
        rule_ids = {violation.rule_id for violation in result.violations}

        tm.that(result.passed, eq=False)
        tm.that("IMPORT-001" in rule_ids, eq=True)
        tm.that("IMPORT-003" in rule_ids, eq=True)
        tm.that("IMPORT-004" in rule_ids, eq=True)
        tm.that("IMPORT-006" in rule_ids, eq=True)

    def test_imports_allows_top_level_public_imports_only(self, tmp_path: Path) -> None:
        file_path = self._write_source(
            tmp_path,
            "imports_clean.py",
            """from __future__ import annotations

from flext_core import r
from flext_tests import m, p, t


def render() -> str:
    return "ready"
""",
        )

        result: p.Tests.ScanResult = u.Tests.assert_success(tv.imports(file_path))

        tm.that(result.passed, eq=True)
        tm.that(result.violations, empty=True)

    def test_bypass_flags_noqa_pragma_and_exception_swallowing(
        self, tmp_path: Path
    ) -> None:
        file_path = self._write_source(
            tmp_path,
            "bypass_scan.py",
            """from __future__ import annotations


def run(flag: bool) -> None:
    value = 1  # noqa
    if flag:  # pragma: no cover
        return None
    try:
        raise RuntimeError("boom")
    except:
        pass


def ignore_specific() -> None:
    try:
        raise ValueError("boom")
    except ValueError:
        ...
""",
        )

        result: p.Tests.ScanResult = u.Tests.assert_success(tv.bypass(file_path))
        rule_ids = [violation.rule_id for violation in result.violations]

        tm.that(result.passed, eq=False)
        tm.that(rule_ids.count("BYPASS-001") > 0, eq=True)
        tm.that(rule_ids.count("BYPASS-002") > 0, eq=True)
        tm.that(rule_ids.count("BYPASS-003") >= 2, eq=True)

    def test_bypass_ignores_suppression_text_inside_strings(
        self, tmp_path: Path
    ) -> None:
        file_path = self._write_source(
            tmp_path,
            "bypass_clean.py",
            """from __future__ import annotations


def render() -> str:
    return "# noqa and # pragma: no cover are documentation here"
""",
        )

        result: p.Tests.ScanResult = u.Tests.assert_success(tv.bypass(file_path))

        tm.that(result.passed, eq=True)
        tm.that(result.violations, empty=True)

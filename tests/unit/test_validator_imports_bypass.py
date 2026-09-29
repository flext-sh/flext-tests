"""Unit tests for the public import and bypass validator surfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import c, m, tm, tv
from tests import u

from ._validator_parts.helper import TestsFlextTestsValidatorTestFilesMixin

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsValidatorImportsBypass(TestsFlextTestsValidatorTestFilesMixin):
    """Verify import and bypass validator rules through the public facade."""

    @pytest.mark.parametrize("line_number", [-1, 0, 1, 2, 3])
    def test_violation_snippet_uses_one_based_source_lines(
        self, tmp_path: Path, line_number: int
    ) -> None:
        rule_name = next(
            name for name in dir(c.Tests) if name.startswith("VALIDATOR_RULE_")
        )
        rule_id = rule_name.removeprefix("VALIDATOR_RULE_").replace("_", "-")
        lines = ("  first source line  ", "  last source line  ")

        violation = u.Tests.create_violation(
            tmp_path / "source.py", line_number, rule_id, lines
        )

        expected_snippet = dict(enumerate(map(str.strip, lines), start=1)).get(
            line_number, ""
        )
        tm.that(violation.code_snippet, eq=expected_snippet)
        tm.that(violation.line_number, eq=line_number)

    @pytest.mark.parametrize(
        "rule_id",
        [
            name.removeprefix("VALIDATOR_RULE_").replace("_", "-")
            for name in dir(c.Tests)
            if name.startswith("VALIDATOR_RULE_") and name.endswith("_UNREADABLE")
        ],
    )
    def test_missing_scan_file_returns_a_file_level_violation(
        self, tmp_path: Path, rule_id: str
    ) -> None:
        severity, description = u.Tests.validator_rule(rule_id)
        missing_path = tmp_path / "absent.py"
        read = u.Cli.files_read_text(missing_path)

        content, violations = u.Tests.read_scan_file(missing_path, rule_id)

        tm.that(read.failure, eq=True)
        tm.that(content, none=True)
        tm.that(len(violations), eq=1)
        violation = violations[0]
        tm.that(violation.file_path, eq=missing_path)
        tm.that(violation.line_number, eq=0)
        tm.that(violation.rule_id, eq=rule_id)
        tm.that(violation.severity, eq=c.Tests.ValidatorSeverity(severity))
        tm.that(violation.description, eq=f"{description}: {read.error}")
        tm.that(violation.code_snippet, eq="")

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

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.imports(file_path))
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
from flext_tests import m, t


def render() -> str:
    return "ready"
""",
        )

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.imports(file_path))

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

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.bypass(file_path))
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

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.bypass(file_path))

        tm.that(result.passed, eq=True)
        tm.that(result.violations, empty=True)

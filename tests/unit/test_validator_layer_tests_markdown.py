"""Behavioral tests for the layer/tests/markdown validator surfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import c, m, tm, tv
from tests import u

if TYPE_CHECKING:
    from pathlib import Path

_HIGHER_LAYER_SOURCE = """from __future__ import annotations

from app.service import Service
import app.handlers as handlers
"""

_CLEAN_LAYER_SOURCE = """from __future__ import annotations

value: int = 1
"""

_MOCK_HEAVY_TEST_SOURCE = """from __future__ import annotations

from unittest.mock import Mock, patch


@patch("package.target")
def test_example(
    monkeypatch,
) -> None:
    monkeypatch.setattr(str, "upper", lambda self: self)
    Mock()
"""

_CLEAN_TEST_SOURCE = """from __future__ import annotations


def test_example() -> None:
    assert True
"""

_BAD_MARKDOWN = """# Example

```python
def broken(
```

```python
from typing import Optional

def render(value: object) -> Optional[str]:
    return None
```
"""

_CLEAN_MARKDOWN = """# Example

```python
from __future__ import annotations

value: int = 1
```
"""


class TestsFlextTestsValidatorLayerTestsMarkdown:
    """Verify the public contract of the layer/tests/markdown validators."""

    @staticmethod
    def _write(base_path: Path, name: str, source: str) -> Path:
        file_path = base_path / name
        file_path.write_text(source, encoding="utf-8")
        return file_path

    # ---- layer validator -------------------------------------------------

    def test_layer_flags_every_import_from_a_higher_layer(self, tmp_path: Path) -> None:
        file_path = self._write(tmp_path, "utilities.py", _HIGHER_LAYER_SOURCE)

        result: m.Tests.ScanResult = u.Tests.assert_success(
            tv.layer(
                file_path, layer_hierarchy={"utilities": 5, "service": 6, "handlers": 7}
            )
        )

        layer_violations = [v for v in result.violations if v.rule_id == "LAYER-001"]
        tm.that(result.passed, eq=False)
        tm.that(len(layer_violations) >= 2, eq=True)
        # Every reported violation must point at the scanned file with a real line.
        for violation in layer_violations:
            tm.that(str(violation.file_path), eq=str(file_path))
            tm.that(violation.line_number >= 1, eq=True)
            tm.that(len(violation.description) >= 1, eq=True)

    def test_layer_passes_when_no_higher_layer_imports_exist(
        self, tmp_path: Path
    ) -> None:
        file_path = self._write(tmp_path, "utilities.py", _CLEAN_LAYER_SOURCE)

        result: m.Tests.ScanResult = u.Tests.assert_success(
            tv.layer(file_path, layer_hierarchy={"utilities": 5})
        )

        tm.that(result.passed, eq=True)
        tm.that(len(result.violations), eq=0)
        tm.that(result.validator_name, eq="layer")

    # ---- tests validator -------------------------------------------------

    @pytest.mark.parametrize("expected_rule", ["TEST-001", "TEST-002", "TEST-003"])
    def test_tests_reports_each_forbidden_test_pattern(
        self, tmp_path: Path, expected_rule: str
    ) -> None:
        file_path = self._write(tmp_path, "test_example.py", _MOCK_HEAVY_TEST_SOURCE)

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.tests(file_path))
        rule_ids = {violation.rule_id for violation in result.violations}

        tm.that(result.passed, eq=False)
        tm.that(expected_rule in rule_ids, eq=True)

    def test_tests_violations_carry_severity_from_the_public_enum(
        self, tmp_path: Path
    ) -> None:
        file_path = self._write(tmp_path, "test_example.py", _MOCK_HEAVY_TEST_SOURCE)

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.tests(file_path))

        allowed = set(c.Tests.ValidatorSeverity)
        for violation in result.violations:
            tm.that(violation.severity in allowed, eq=True)

    def test_tests_passes_for_a_clean_test_module(self, tmp_path: Path) -> None:
        file_path = self._write(tmp_path, "test_clean.py", _CLEAN_TEST_SOURCE)

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.tests(file_path))

        tm.that(result.passed, eq=True)
        tm.that(len(result.violations), eq=0)
        tm.that(result.validator_name, eq="tests")

    # ---- markdown validator ---------------------------------------------

    @pytest.mark.parametrize("expected_rule", ["MD-001", "MD-002", "MD-003", "MD-004"])
    def test_markdown_reports_each_forbidden_code_block_pattern(
        self, tmp_path: Path, expected_rule: str
    ) -> None:
        self._write(tmp_path, "README.md", _BAD_MARKDOWN)

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.markdown(tmp_path))
        rule_ids = {violation.rule_id for violation in result.violations}

        tm.that(result.passed, eq=False)
        tm.that(expected_rule in rule_ids, eq=True)

    def test_markdown_passes_for_a_clean_code_block(self, tmp_path: Path) -> None:
        self._write(tmp_path, "README.md", _CLEAN_MARKDOWN)

        result: m.Tests.ScanResult = u.Tests.assert_success(tv.markdown(tmp_path))

        tm.that(result.passed, eq=True)
        tm.that(len(result.violations), eq=0)
        tm.that(result.validator_name, eq="markdown")

    # ---- cross-validator invariant --------------------------------------

    def test_passed_flag_is_consistent_with_violation_presence(
        self, tmp_path: Path
    ) -> None:
        dirty = self._write(tmp_path, "test_example.py", _MOCK_HEAVY_TEST_SOURCE)
        clean = self._write(tmp_path, "test_clean.py", _CLEAN_TEST_SOURCE)

        dirty_result: m.Tests.ScanResult = u.Tests.assert_success(tv.tests(dirty))
        clean_result: m.Tests.ScanResult = u.Tests.assert_success(tv.tests(clean))

        # Invariant: passed is True exactly when there are no violations.
        tm.that(dirty_result.passed, eq=len(dirty_result.violations) == 0)
        tm.that(clean_result.passed, eq=len(clean_result.violations) == 0)

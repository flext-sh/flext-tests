"""Unit tests for the remaining public validator surfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import tm, tv
from tests import u


class TestsFlextTestsValidatorLayerTestsMarkdown:
    """Verify the public layer/tests/markdown validator surfaces."""

    @staticmethod
    def _write_file(base_path: Path, name: str, source: str) -> Path:
        file_path = base_path / name
        file_path.write_text(source, encoding="utf-8")
        return file_path

    def test_layer_flags_imports_from_higher_layers(
        self,
        tmp_path: Path,
    ) -> None:
        file_path = self._write_file(
            tmp_path,
            "utilities.py",
            """from __future__ import annotations

from app.service import Service
import app.handlers as handlers
""",
        )

        result = u.Tests.assert_success(
            tv.layer(
                file_path,
                layer_hierarchy={
                    "utilities": 5,
                    "service": 6,
                    "handlers": 7,
                },
            ),
        )
        rule_ids = [violation.rule_id for violation in result.violations]

        tm.that(result.passed, eq=False)
        tm.that(rule_ids.count("LAYER-001") >= 2, eq=True)

    def test_tests_flags_monkeypatch_mock_and_patch_usage(
        self,
        tmp_path: Path,
    ) -> None:
        file_path = self._write_file(
            tmp_path,
            "test_example.py",
            """from __future__ import annotations

from unittest.mock import Mock, patch


@patch("package.target")
def test_example(
    monkeypatch,
) -> None:
    monkeypatch.setattr(str, "upper", lambda self: self)
    Mock()
""",
        )

        result = u.Tests.assert_success(tv.tests(file_path))
        rule_ids = {violation.rule_id for violation in result.violations}

        tm.that(result.passed, eq=False)
        tm.that("TEST-001" in rule_ids, eq=True)
        tm.that("TEST-002" in rule_ids, eq=True)
        tm.that("TEST-003" in rule_ids, eq=True)

    def test_markdown_flags_syntax_typing_future_and_object_rules(
        self,
        tmp_path: Path,
    ) -> None:
        self._write_file(
            tmp_path,
            "README.md",
            """# Example

```python
def broken(
```

```python
from typing import Optional

def render(value: object) -> Optional[str]:
    return None
```
""",
        )

        result = u.Tests.assert_success(tv.markdown(tmp_path))
        rule_ids = {violation.rule_id for violation in result.violations}

        tm.that(result.passed, eq=False)
        tm.that("MD-001" in rule_ids, eq=True)
        tm.that("MD-002" in rule_ids, eq=True)
        tm.that("MD-003" in rule_ids, eq=True)
        tm.that("MD-004" in rule_ids, eq=True)

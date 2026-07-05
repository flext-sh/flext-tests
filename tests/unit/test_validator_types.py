"""Behavioral tests for the public `tv.types` validator surface.

These tests exercise only the public contract of `tv.types`: the `r[T]`
outcome it returns and the public fields of `m.Tests.ScanResult` /
`m.Tests.Violation`. No private attribute, internal collaborator, or
scanner implementation detail is inspected.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import m, tm, tv
from tests.utilities import u

if TYPE_CHECKING:
    from pathlib import Path

_MODERN_TYPING_SOURCE = """from __future__ import annotations

from typing import TypeIs, final, override


type Scalar = str | int


class Base:
    def render(self) -> Scalar:
        return "base"


class Derived(Base):
    @override
    def render(self) -> Scalar:
        return 1


@final
class Leaf:
    pass


def scalar_value(value: Scalar | None) -> Scalar:
    if value is None:
        return "fallback"
    return value


def narrow_scalar(value: Scalar | None) -> TypeIs[Scalar]:
    return value is not None
"""

# The type-suppression comment is assembled from a fragment so this test module
# itself stays free of a real suppression comment while the written temp file
# still contains one.
_SUPPRESSION_MARKER = "# type:" + " ignore"

_TYPE_IGNORE_SOURCE = (
    f"from __future__ import annotations\n\nvalue = 1  {_SUPPRESSION_MARKER}\n"
)

_ANY_SOURCE = """from __future__ import annotations

from typing import Any


def render(value: Any) -> str:
    return str(value)
"""

_CAST_SOURCE = """from __future__ import annotations

from typing import cast


number = cast(int, '1')
"""

_LEGACY_FACTORY_SOURCE = """from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")
"""

_LEGACY_ANNOTATION_SOURCE = """from __future__ import annotations

from typing import Optional


def render(value: Optional[str]) -> str:
    return value or ''
"""

_OBJECT_SOURCE = "from __future__ import annotations\n\n\npayload: object = 'ready'\n"

_BOOL_IS_HELPER_SOURCE = """from __future__ import annotations


def is_ready(value: str) -> bool:
    return bool(value)
"""

# (filename, source, rule_id) — each source triggers exactly the named rule.
_OFFENDING_SOURCES: tuple[tuple[str, str, str], ...] = (
    ("type_ignore.py", _TYPE_IGNORE_SOURCE, "TYPE-001"),
    ("any_annotation.py", _ANY_SOURCE, "TYPE-002"),
    ("cast_usage.py", _CAST_SOURCE, "TYPE-003"),
    ("legacy_factory.py", _LEGACY_FACTORY_SOURCE, "TYPE-004"),
    ("legacy_annotation.py", _LEGACY_ANNOTATION_SOURCE, "TYPE-005"),
    ("object_annotation.py", _OBJECT_SOURCE, "TYPE-006"),
    ("bool_is_helper.py", _BOOL_IS_HELPER_SOURCE, "TYPE-007"),
)


class TestsFlextTestsValidatorTypes:
    """Verify strict typing rules through the public `tv.types` contract."""

    @staticmethod
    def _write_source(tmp_path: Path, name: str, source: str) -> Path:
        file_path = tmp_path / name
        file_path.write_text(source, encoding="utf-8")
        return file_path

    def test_types_passes_clean_modern_typing_with_metadata(
        self,
        tmp_path: Path,
    ) -> None:
        # Arrange
        file_path = self._write_source(
            tmp_path,
            "modern_typing.py",
            _MODERN_TYPING_SOURCE,
        )

        # Act
        result: m.Tests.ScanResult = u.Tests.assert_success(tv.types(file_path))

        # Assert — a compliant file passes with no violations and correct metadata.
        tm.that(result.passed, eq=True)
        tm.that(result.violations, empty=True)
        tm.that(result.validator_name, eq="types")
        tm.that(result.files_scanned, eq=1)

    @pytest.mark.parametrize(
        ("name", "source", "rule_id"),
        _OFFENDING_SOURCES,
        ids=[rule_id for _, _, rule_id in _OFFENDING_SOURCES],
    )
    def test_types_flags_offending_source_with_rule(
        self,
        tmp_path: Path,
        name: str,
        source: str,
        rule_id: str,
    ) -> None:
        # Arrange
        file_path = self._write_source(tmp_path, name, source)

        # Act
        result: m.Tests.ScanResult = u.Tests.assert_success(tv.types(file_path))
        rule_ids = {violation.rule_id for violation in result.violations}

        # Assert — the offending construct fails the scan and names its rule.
        tm.that(result.passed, eq=False)
        tm.that(rule_ids, contains=rule_id)

    def test_types_violation_exposes_public_location_and_snippet(
        self,
        tmp_path: Path,
    ) -> None:
        # Arrange
        file_path = self._write_source(
            tmp_path,
            "object_variable.py",
            "from __future__ import annotations\n\n\npayload: object = 'ready'\n",
        )

        # Act
        result: m.Tests.ScanResult = u.Tests.assert_success(tv.types(file_path))
        violation = next(
            item for item in result.violations if item.rule_id == "TYPE-006"
        )

        # Assert — the violation reports the real offending line via public fields.
        tm.that(violation.line_number, eq=4)
        tm.that(violation.code_snippet, eq="payload: object = 'ready'")
        tm.that(violation.severity, eq="CRITICAL")
        tm.that(violation.file_path, eq=file_path)
        tm.that(violation.description, empty=False)

    def test_types_approved_exception_suppresses_named_rule(
        self,
        tmp_path: Path,
    ) -> None:
        # Arrange — `service.py` matches a canonical approval path pattern.
        file_path = self._write_source(
            tmp_path,
            "service.py",
            "from __future__ import annotations\n\n\n"
            "def build(value: object) -> str:\n"
            "    return str(value)\n",
        )
        baseline: m.Tests.ScanResult = u.Tests.assert_success(tv.types(file_path))
        tm.that(
            {violation.rule_id for violation in baseline.violations},
            contains="TYPE-006",
        )

        # Act — approving TYPE-006 for service.py must clear that rule.
        approved: m.Tests.ScanResult = u.Tests.assert_success(
            tv.types(
                file_path,
                approved_exceptions={"TYPE-006": (r"service\.py$",)},
            ),
        )

        # Assert
        tm.that(approved.passed, eq=True)
        tm.that(approved.violations, empty=True)

    def test_types_is_idempotent_for_the_same_source(
        self,
        tmp_path: Path,
    ) -> None:
        # Arrange
        file_path = self._write_source(
            tmp_path,
            "repeat.py",
            "from __future__ import annotations\n\n\npayload: object = 'ready'\n",
        )

        # Act — two independent scans of the same file.
        first: m.Tests.ScanResult = u.Tests.assert_success(tv.types(file_path))
        second: m.Tests.ScanResult = u.Tests.assert_success(tv.types(file_path))

        # Assert — the observable outcome is stable across runs.
        tm.that(first.passed, eq=second.passed)
        tm.that(
            {violation.rule_id for violation in first.violations},
            eq={violation.rule_id for violation in second.violations},
        )

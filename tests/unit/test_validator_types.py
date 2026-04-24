"""Unit tests for the public `tv.types` validator surface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import tm, tv
from tests import u


class TestsFlextTestsValidatorTypes:
    """Verify strict typing validator rules through the public validator facade."""

    @staticmethod
    def _write_source(tmp_path: Path, name: str, source: str) -> Path:
        file_path = tmp_path / name
        file_path.write_text(source, encoding="utf-8")
        return file_path

    def test_types_flags_legacy_typing_factories_and_annotations(
        self,
        tmp_path: Path,
    ) -> None:
        file_path = self._write_source(
            tmp_path,
            "legacy_typing.py",
            """from __future__ import annotations

from typing import Generic, Optional, ParamSpec, TypeAlias, TypeGuard, TypeVar

T = TypeVar("T")
P = ParamSpec("P")
LegacyScalar: TypeAlias = str | int


class Box(Generic[T]):
    value: T


def narrow(value: Optional[str]) -> TypeGuard[str]:
    return isinstance(value, str)
""",
        )

        result = u.Tests.assert_success(tv.types(file_path))
        rule_ids = {violation.rule_id for violation in result.violations}

        tm.that(result.passed, eq=False)
        tm.that("TYPE-004" in rule_ids, eq=True)
        tm.that("TYPE-005" in rule_ids, eq=True)

    def test_types_flags_object_annotations_and_bool_is_helpers(
        self,
        tmp_path: Path,
    ) -> None:
        file_path = self._write_source(
            tmp_path,
            "object_annotations.py",
            """from __future__ import annotations


payload: object = "ready"


def render(value: object) -> str:
    return str(value)


def is_ready(value: str) -> bool:
    return bool(value)
""",
        )

        result = u.Tests.assert_success(tv.types(file_path))
        rule_ids = {violation.rule_id for violation in result.violations}

        tm.that(result.passed, eq=False)
        tm.that("TYPE-006" in rule_ids, eq=True)
        tm.that("TYPE-007" in rule_ids, eq=True)

    def test_types_allows_modern_python_313_typing_forms(
        self,
        tmp_path: Path,
    ) -> None:
        file_path = self._write_source(
            tmp_path,
            "modern_typing.py",
            """from __future__ import annotations

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
""",
        )

        result = u.Tests.assert_success(tv.types(file_path))

        tm.that(result.passed, eq=True)
        tm.that(result.violations, empty=True)

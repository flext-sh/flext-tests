"""Pytest collection item for enforcement violations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from flext_tests import t


class FlextTestsEnforcementItem(pytest.Item):
    """Pytest item representing one ``(rule_id, project)`` violation group."""

    def __init__(
        self,
        name: str,
        parent: pytest.Collector,
        *,
        rule_id: str,
        severity: str,
        description: str,
        project: str,
        violations: t.StrSequence,
    ) -> None:
        super().__init__(name, parent)
        self._rule_id = rule_id
        self._severity = severity
        self._description = description
        self._project = project
        self._violations = tuple(violations)

    @override
    def runtest(self) -> None:
        header = (
            f"{self._rule_id} ({self._severity}) in {self._project}: "
            f"{len(self._violations)} violation(s)"
        )
        from ._error import FlextTestsEnforcementViolationError

        raise FlextTestsEnforcementViolationError(
            "\n".join([header, *(f"  - {line}" for line in self._violations)]),
        )

    @override
    def repr_failure(
        self,
        excinfo: pytest.ExceptionInfo[BaseException],
        style: str | None = None,
    ) -> str:
        _ = style
        return str(excinfo.value)

    @override
    def reportinfo(self) -> tuple[Path | str, int | None, str]:
        return (
            f"flext-enforce::{self._rule_id}",
            None,
            f"{self._rule_id} [{self._project}] {self._description}",
        )


__all__: list[str] = ["FlextTestsEnforcementItem"]

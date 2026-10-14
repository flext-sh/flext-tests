"""Pytest collection item for enforcement violations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, override

import pytest

from flext_tests._fixtures._enforcement_parts._error import (
    FlextTestsEnforcementViolationError,
)

if TYPE_CHECKING:
    from pathlib import Path

    from flext_tests import m


class FlextTestsEnforcementItem(pytest.Item):
    """Pytest item representing one ``(rule_id, project)`` violation group."""

    @classmethod
    def create(
        cls,
        parent: pytest.Collector,
        name: str,
        *,
        violation: m.Tests.EnforcementViolation,
    ) -> Self:
        """Build one item through pytest's public node factory.

        ``from_parent`` forwards these exact arguments to the fully typed
        item constructor and derives the configuration and session from the
        parent, as pytest's node creation contract requires.

        Returns:
            The resulting ``Self``.

        """
        return cls.from_parent(parent=parent, name=name, violation=violation)

    def __init__(
        self,
        name: str,
        parent: pytest.Collector,
        *,
        violation: m.Tests.EnforcementViolation,
    ) -> None:
        # Item forwards name/parent to Node and initializes reporting.
        super().__init__(name, parent)
        self._rule_id = violation.rule_id
        self._severity = violation.severity
        self._description = violation.description
        self._project = violation.project
        self._violations = tuple(violation.violations)

    @override
    def runtest(self) -> None:
        header = (
            f"{self._rule_id} ({self._severity}) in {self._project}: "
            f"{len(self._violations)} violation(s)"
        )
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

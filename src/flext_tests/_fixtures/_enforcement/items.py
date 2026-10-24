"""Pytest collection item for enforcement violations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pytest

from flext_tests._fixtures._enforcement._error import (
    FlextTestsEnforcementViolationError,
)
from flext_tests._protocols.enforcement import FlextTestsEnforcementProtocolsMixin

if TYPE_CHECKING:
    from pathlib import Path

    from flext_tests import m


class FlextTestsEnforcementItem(
    FlextTestsEnforcementProtocolsMixin.TypedNode,
    pytest.Item,
):
    """Pytest item representing one ``(rule_id, project)`` violation group."""

    def __init__(
        self,
        name: str,
        parent: pytest.Collector,
        *,
        violation: m.Tests.EnforcementViolation,
    ) -> None:
        # pytest.Item.__init__ is unannotated upstream, so bind the fully
        # typed Node base and initialize the documented public Item
        # attributes this item's failure reporting consumes.
        super(pytest.Item, self).__init__(name, parent)
        self._report_sections: list[tuple[str, str, str]] = []
        self.user_properties = []
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

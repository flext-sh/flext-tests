"""Pytest collection item for enforcement violations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, cast, override

import pytest

from flext_tests._fixtures._enforcement_parts._error import (
    FlextTestsEnforcementViolationError,
)

if TYPE_CHECKING:
    from collections.abc import Callable
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
        """Build one item through a fully typed factory boundary.

        ``pytest.Node.from_parent`` carries a partially unknown ``**kw`` in
        the supported pytest stubs; this wrapper owns the single cast.

        Returns:
            The resulting ``Self``.

        """
        factory = cast("Callable[..., Self]", cls.from_parent)
        return factory(parent=parent, name=name, violation=violation)

    def __init__(
        self,
        name: str,
        parent: pytest.Collector,
        *,
        violation: m.Tests.EnforcementViolation,
    ) -> None:
        node_init = cast("Callable[..., None]", super().__init__)
        node_init(name, parent)
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

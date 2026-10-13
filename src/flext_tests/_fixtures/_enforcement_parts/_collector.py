"""Collector for enforcement items.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, override

import pytest

from flext_tests import p
from flext_tests._fixtures._enforcement_parts import FlextTestsEnforcementItem

if TYPE_CHECKING:
    from collections.abc import Iterable

    from flext_tests import t


class FlextTestsEnforcementCollector(pytest.Collector):
    """Synthetic collector owning session ``FlextTestsEnforcementItem`` items."""

    @classmethod
    def create(
        cls,
        parent: pytest.Session,
        name: str,
    ) -> Self:
        """Build one collector through a fully typed factory boundary.

        Pytest's unannotated ``**kw`` forwards these exact arguments to the
        collector constructor; the protocol records that public boundary.

        Returns:
            The resulting ``Self``.

        """
        factory: p.Tests.EnforcementCollectorFactory[Self] = cls.from_parent
        return factory(parent=parent, name=name)

    def __init__(
        self,
        name: str,
        parent: pytest.Session,
        *,
        items: t.SequenceOf[FlextTestsEnforcementItem] = (),
    ) -> None:
        super().__init__(name, parent)
        self._items: list[FlextTestsEnforcementItem] = list(items)

    def add(self, item: FlextTestsEnforcementItem) -> None:
        self._items.append(item)

    @override
    def collect(self) -> Iterable[pytest.Item]:
        return list(self._items)

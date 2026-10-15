"""Collector for enforcement items.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, override

import pytest

from flext_tests._fixtures._enforcement_parts import FlextTestsEnforcementItem
from flext_tests._protocols.enforcement import FlextTestsEnforcementCollectorNodeMixin

if TYPE_CHECKING:
    from collections.abc import Iterable

    from flext_tests import t


class FlextTestsEnforcementCollector(
    FlextTestsEnforcementCollectorNodeMixin,
    pytest.Collector,
):
    """Synthetic collector owning session ``FlextTestsEnforcementItem`` items."""

    @classmethod
    def create(
        cls,
        parent: pytest.Session,
        name: str,
    ) -> Self:
        """Build one collector through pytest's public node factory.

        ``from_parent`` forwards these exact arguments to the fully typed
        collector constructor and derives the configuration and session from
        the parent, as pytest's node creation contract requires.

        Returns:
            The resulting ``Self``.

        """
        return cls.from_parent(parent=parent, name=name)

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


__all__: list[str] = ["FlextTestsEnforcementCollector"]

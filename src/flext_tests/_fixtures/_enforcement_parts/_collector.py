"""Private collector for enforcement items."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pytest

from .items import FlextTestsEnforcementItem

if TYPE_CHECKING:
    from collections.abc import Iterable

    from flext_tests import t


class _EnforcementCollector(pytest.Collector):
    """Synthetic collector that owns every ``FlextTestsEnforcementItem`` for the session."""

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
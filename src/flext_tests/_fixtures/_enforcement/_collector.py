"""Collector for enforcement items.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pytest

from flext_tests._fixtures._enforcement import FlextTestsEnforcementItem
from flext_tests._protocols.enforcement import FlextTestsEnforcementProtocolsMixin

if TYPE_CHECKING:
    from collections.abc import Iterable

    from flext_tests import t


class FlextTestsEnforcementCollector(
    FlextTestsEnforcementProtocolsMixin.TypedNode,
    pytest.Collector,
):
    """Synthetic collector owning session ``FlextTestsEnforcementItem`` items."""

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

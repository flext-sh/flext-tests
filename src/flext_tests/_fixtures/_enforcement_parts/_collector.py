"""Collector for enforcement items.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterable

    from flext_tests import t
    from flext_tests._fixtures._enforcement_parts.items import FlextTestsEnforcementItem


class FlextTestsEnforcementCollector(pytest.Collector):
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

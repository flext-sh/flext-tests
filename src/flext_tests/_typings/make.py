"""Typing aliases for the generic Make command framework.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable

from flext_cli import m, t


class FlextTestsMakeTypesMixin:
    """Type aliases for registry-driven Make command metadata."""

    type MakeTomlValue = t.JsonValue
    type MakeTomlTable = t.JsonMapping
    type MutableMakeTomlTable = t.MutableJsonMapping
    type DispatchMain = Callable[[tuple[str, ...]], int]

    MAKE_TOML_TABLE_ADAPTER: m.TypeAdapter[MakeTomlTable] = m.TypeAdapter(MakeTomlTable)


__all__: list[str] = ["FlextTestsMakeTypesMixin"]

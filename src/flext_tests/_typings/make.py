"""Typing aliases for the generic Make command framework.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable

from flext_infra import m, t


class FlextTestsMakeTypesMixin:
    """Type aliases for registry-driven Make command metadata."""

    type DispatchMain = Callable[[tuple[str, ...]], int]
    type TomlValue = t.JsonValue
    type TomlMapping = t.JsonMapping
    type MutableTomlMapping = t.MutableJsonMapping

    TOML_MAPPING_ADAPTER: m.TypeAdapter[TomlMapping] = m.TypeAdapter(TomlMapping)


__all__: list[str] = ["FlextTestsMakeTypesMixin"]

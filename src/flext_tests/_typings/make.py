"""Typing aliases for the generic Make command framework.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable

from flext_infra import m, p, t


class FlextTestsTypesMake:
    """Type aliases for registry-driven Make command metadata."""

    type DispatchMain = Callable[[tuple[str, ...]], int]

    TOML_MAPPING_ADAPTER: p.TypeAdapter[t.JsonMapping] = m.TypeAdapter(t.JsonMapping)


__all__: list[str] = ["FlextTestsTypesMake"]

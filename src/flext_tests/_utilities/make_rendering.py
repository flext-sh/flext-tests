"""Rendering utilities for flext-tests Make command metadata."""

from __future__ import annotations

from flext_tests._utilities._make_parts.make_rendering_part_02 import (
    FlextTestsMakeRenderingUtilitiesMixin as FlextTestsMakeRenderingUtilitiesMixinPart02,
)


class FlextTestsMakeRenderingUtilitiesMixin(
    FlextTestsMakeRenderingUtilitiesMixinPart02,
):
    """Render registry-driven Make help and dry-run output."""


__all__: list[str] = ["FlextTestsMakeRenderingUtilitiesMixin"]

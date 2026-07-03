"""Markdown Python code block validation for FLEXT architecture."""

from __future__ import annotations

from flext_tests._validator._markdown_parts.markdown_part_02 import (
    FlextValidatorMarkdown as FlextValidatorMarkdownPart02,
)


class FlextValidatorMarkdown(FlextValidatorMarkdownPart02):
    """Markdown Python code block validator."""


__all__: list[str] = ["FlextValidatorMarkdown"]

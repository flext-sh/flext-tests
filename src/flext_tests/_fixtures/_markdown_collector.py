"""Pytest collector for markdown files."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pytest

from .markdown_validation import FlextTestsMarkdownCodeBlockItem

if TYPE_CHECKING:
    from pathlib import Path


class _MarkdownCodeBlockCollector(pytest.File):
    """Pytest collector for markdown files."""

    @override
    def collect(self) -> list[FlextTestsMarkdownCodeBlockItem]:
        """Collect markdown file as a test item."""
        return [
            FlextTestsMarkdownCodeBlockItem.from_parent(
                self, name=self.path.name, md_path=self.path
            )
        ]
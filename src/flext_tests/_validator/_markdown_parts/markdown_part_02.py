"""Markdown file discovery for FLEXT validator."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import t, u
from flext_tests._validator._markdown_parts.markdown_part_01 import (
    FlextValidatorMarkdown as FlextValidatorMarkdownPart01,
)

if TYPE_CHECKING:
    from collections.abc import MutableSequence
    from pathlib import Path


class FlextValidatorMarkdown(FlextValidatorMarkdownPart01):
    """Markdown Python code block validator."""

    @classmethod
    def collect_markdown_files(
        cls,
        project_root: Path,
    ) -> t.SequenceOf[Path]:
        """Collect all .md files that may contain Python code blocks."""
        md_files: MutableSequence[Path] = []
        for search_dir in (
            project_root,
            project_root / ".claude" / "skills",
            project_root / "docs",
        ):
            if search_dir.is_dir():
                md_files.extend(
                    u.Infra.iter_matching_files(search_dir, includes=["*.md"]),
                )
        return md_files


__all__: list[str] = ["FlextValidatorMarkdown"]

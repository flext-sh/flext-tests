"""Exception for markdown validation failures."""

from __future__ import annotations


class _MarkdownValidationError(Exception):
    """Raised when markdown code block validation fails."""
"""Shared test helper mixin for validator test classes.

Centralizes the ``_write_source`` helper that writes a source string to a
file inside ``tmp_path`` — used by multiple validator test suites so the
scaffolding lives in one owner (YAGNI/DRY).
"""

from __future__ import annotations

from pathlib import Path


class ValidatorTestFilesMixin:
    """Mixin providing shared file-writing helpers for validator tests."""

    @staticmethod
    def _write_source(
        tmp_path: Path, name: str, source: str
    ) -> Path:
        """Write ``source`` to ``tmp_path / name`` and return the path."""
        file_path = tmp_path / name
        file_path.write_text(source, encoding="utf-8")
        return file_path


__all__: list[str] = ["ValidatorTestFilesMixin"]

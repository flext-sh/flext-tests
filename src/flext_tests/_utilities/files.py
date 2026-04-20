"""Test-domain file helpers (format detection only).

Hash, CSV I/O, and text I/O delegate directly to ``u.Cli.*`` at call sites;
no wrappers live here.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path

from flext_tests import c, t


class FlextTestsFilesUtilitiesMixin:
    """Test-only format detection helpers; no I/O."""

    @staticmethod
    def detect_format(
        content: str
        | bytes
        | Mapping[str, t.Tests.TestobjectSerializable]
        | Sequence[t.StrSequence],
        name: str,
        fmt: str,
    ) -> str:
        """Detect format by content shape + name; honors explicit ``fmt``."""
        if fmt != c.Tests.Format.AUTO:
            return fmt
        if isinstance(content, bytes):
            return c.Tests.Format.BIN
        if isinstance(content, Mapping):
            ext = Path(name).suffix.lower()
            return (
                c.Tests.Format.YAML if ext in {".yaml", ".yml"} else c.Tests.Format.JSON
            )
        if isinstance(content, list):
            return c.Tests.Format.CSV
        return c.Tests.format_for_extension(Path(name).suffix)

    @staticmethod
    def detect_format_from_path(path: Path, fmt: str) -> str:
        """Detect format from path extension; honors explicit ``fmt``."""
        if fmt != c.Tests.Format.AUTO:
            return fmt
        return c.Tests.format_for_extension(path.suffix)

    @staticmethod
    def format_size(size: int) -> str:
        """Human-readable size via c.Tests.format_size."""
        return c.Tests.format_size(size)

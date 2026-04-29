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

from flext_tests import c, m, t


class FlextTestsFilesUtilitiesMixin:
    """Test-only format detection helpers; no I/O."""

    @staticmethod
    def detect_format(
        content: str
        | bytes
        | m.ConfigMap
        | m.Dict
        | Mapping[str, t.Tests.TestobjectSerializable]
        | Sequence[t.StrSequence],
        name: str,
        fmt: str,
    ) -> str:
        """Detect format by content shape + name; honors explicit ``fmt``."""
        if fmt != c.Tests.Format.AUTO:
            return fmt
        if isinstance(content, bytes):
            return str(c.Tests.Format.BIN)
        if isinstance(content, (m.ConfigMap, m.Dict, Mapping)):
            ext = Path(name).suffix.lower()
            mapping_format: str = (
                c.Tests.Format.YAML if ext in {".yaml", ".yml"} else c.Tests.Format.JSON
            )
            return mapping_format
        if isinstance(content, list):
            return str(c.Tests.Format.CSV)
        suffix_format: str = c.Tests.format_for_extension(Path(name).suffix)
        return suffix_format

    @staticmethod
    def detect_format_from_path(path: Path, fmt: str) -> str:
        """Detect format from path extension; honors explicit ``fmt``."""
        if fmt != c.Tests.Format.AUTO:
            return fmt
        path_format: str = c.Tests.format_for_extension(path.suffix)
        return path_format

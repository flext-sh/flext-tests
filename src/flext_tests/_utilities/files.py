"""Test-domain file helpers (format detection only).

Hash, CSV I/O, and text I/O delegate directly to ``u.Cli.*`` at call sites;
no wrappers live here.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from pathlib import Path

from flext_tests._typings.base import FlextTestsBaseTypesMixin
from flext_tests.constants import FlextTestsConstants as c
from flext_tests.models import FlextTestsModels as m
from flext_tests.typings import FlextTestsTypes as t


class FlextTestsFilesUtilitiesMixin:
    """Test-only format detection helpers; no I/O."""

    @staticmethod
    def detect_format(
        content: str
        | bytes
        | m.ConfigMap
        | m.Dict
        | t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | t.SequenceOf[t.StrSequence],
        name: str,
        fmt: str,
    ) -> str:
        """Detect format by content shape + name; honors explicit ``fmt``."""
        if fmt != c.Tests.FILE_FORMAT_AUTO:
            return fmt
        if isinstance(content, bytes):
            return str(c.Tests.FILE_FORMAT_BIN)
        if isinstance(content, (m.ConfigMap, m.Dict, Mapping)):
            ext = Path(name).suffix.lower()
            mapping_format: str = (
                c.Tests.FILE_FORMAT_YAML
                if ext in {".yaml", ".yml"}
                else c.Tests.FILE_FORMAT_JSON
            )
            return mapping_format
        if isinstance(content, list):
            return str(c.Tests.FILE_FORMAT_CSV)
        suffix_format: str = c.Tests.format_for_extension(Path(name).suffix)
        return suffix_format

    @staticmethod
    def detect_format_from_path(path: Path, fmt: str) -> str:
        """Detect format from path extension; honors explicit ``fmt``."""
        if fmt != c.Tests.FILE_FORMAT_AUTO:
            return fmt
        path_format: str = c.Tests.format_for_extension(path.suffix)
        return path_format

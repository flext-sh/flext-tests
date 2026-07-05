"""Test-domain file helpers (format detection only).

Format detection delegates to ``u.Cli`` canonical helpers; no I/O lives here.
"""

from __future__ import annotations

from pathlib import Path

from flext_cli import u as cli_u
from flext_tests.models import m
from flext_tests.typings import t


class FlextTestsFilesUtilitiesMixin:
    """Test-only format-detection facade; delegates to ``u.Cli`` canonical helpers."""

    @staticmethod
    def detect_format(
        content: str
        | bytes
        | m.ConfigMap
        | m.Dict
        | t.MappingKV[str, t.Tests.TestobjectSerializable]
        | t.SequenceOf[t.StrSequence],
        name: str,
        fmt: str,
    ) -> str:
        """Detect format by content shape + name; honors explicit ``fmt``."""
        detected_format: str = cli_u.Cli.files_detect_format_from_content(
            content,
            name,
            fmt,
        )
        return detected_format

    @staticmethod
    def detect_format_from_path(path: Path, fmt: str) -> str:
        """Detect format from path extension; honors explicit ``fmt``."""
        detected_format: str = cli_u.Cli.files_detect_format_from_path(path, fmt)
        return detected_format

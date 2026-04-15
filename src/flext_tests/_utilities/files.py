"""Extracted mixin for flext_tests."""

from __future__ import annotations

import csv
from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path

from flext_cli import FlextCliUtilities
from flext_tests import (
    c,
    t,
)


class FlextTestsFilesUtilitiesMixin:
    """File utilities for test file operations.

    Provides reusable helper functions for file operations that can be
    used by FlextTestsFiles and other test utilities.
    """

    @staticmethod
    def compute_hash(path: Path, chunk_size: int | None = None) -> str:
        """Compute SHA256 hash of file via u.Cli.sha256_file().

        Args:
            path: Path to file
            chunk_size: Unused, kept for API compatibility

        Returns:
            SHA256 hash as hex string

        """
        _ = chunk_size
        return FlextCliUtilities.Cli.sha256_file(path)

    @staticmethod
    def detect_format(
        content: str
        | bytes
        | Mapping[str, t.Tests.TestobjectSerializable]
        | Sequence[t.StrSequence],
        name: str,
        fmt: str,
    ) -> str:
        """Detect file format from content type or filename.

        Args:
            content: File content (type determines format)
            name: Filename (extension hints format)
            fmt: Explicit format override ("auto" for detection)

        Returns:
            r[TEntity]: Result containing created entity or error
            Detected format string

        """
        if fmt != c.Tests.Format.AUTO:
            return fmt
        if isinstance(content, bytes):
            return c.Tests.Format.BIN
        if isinstance(content, Mapping):
            ext = Path(name).suffix.lower()
            if ext in {".yaml", ".yml"}:
                return c.Tests.Format.YAML
            return c.Tests.Format.JSON
        if isinstance(content, list):
            return c.Tests.Format.CSV
        return c.Tests.format_for_extension(Path(name).suffix)

    @staticmethod
    def detect_format_from_path(path: Path, fmt: str) -> str:
        """Detect format from file path.

        Args:
            path: File path
            fmt: Explicit format override ("auto" for detection)

        Returns:
            r[TEntity]: Result containing created entity or error
            Detected format string

        """
        if fmt != c.Tests.Format.AUTO:
            return fmt
        return c.Tests.format_for_extension(path.suffix)

    @staticmethod
    def format_size(size: int) -> str:
        """Format size in human-readable format.

        Delegates to constants.Files.format_size for consistency.

        Args:
            size: Size in bytes

        Returns:
            r[TEntity]: Result containing created entity or error
            Human-readable size string like "1.2 KB"

        """
        return c.Tests.format_size(size)

    @staticmethod
    def read_csv(
        path: Path,
        delimiter: str | None = None,
        encoding: str | None = None,
        *,
        has_headers: bool = True,
    ) -> Sequence[t.StrSequence]:
        """Read CSV file.

        Args:
            path: File path
            delimiter: CSV delimiter (default: from constants)
            encoding: File encoding (default: from constants)
            has_headers: If True, skip first row (headers)

        Returns:
            r[TEntity]: Result containing created entity or error
            List of rows (each row is list of strings)

        """
        delim = delimiter or c.Tests.DEFAULT_CSV_DELIMITER
        enc = encoding or c.Tests.DEFAULT_ENCODING
        with path.open(newline="", encoding=enc) as f:
            reader = csv.reader(f, delimiter=delim)
            rows = list(reader)
            if has_headers and rows:
                return rows[1:]
            return rows

    @staticmethod
    def write_csv(
        path: Path,
        content: str
        | bytes
        | Mapping[str, t.Tests.TestobjectSerializable]
        | Sequence[t.StrSequence],
        headers: t.StrSequence | None,
        delimiter: str | None = None,
        encoding: str | None = None,
    ) -> None:
        """Write CSV file.

        Args:
            path: File path
            content: Content to write (list of rows)
            headers: Optional header row
            delimiter: CSV delimiter (default: from constants)
            encoding: File encoding (default: from constants)

        """
        delim = delimiter or c.Tests.DEFAULT_CSV_DELIMITER
        enc = encoding or c.Tests.DEFAULT_ENCODING
        with path.open("w", newline="", encoding=enc) as f:
            writer = csv.writer(f, delimiter=delim)
            if headers:
                writer.writerow(headers)
            if isinstance(content, list):
                for row in content:
                    writer.writerow(row)

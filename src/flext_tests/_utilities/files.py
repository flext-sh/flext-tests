"""Extracted mixin for flext_tests."""

from __future__ import annotations

import csv
import hashlib
from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path

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
        """Compute SHA256 hash of file.

        Args:
            path: Path to file
            chunk_size: Size of chunks to read (default: from constants)

        Returns:
            r[TEntity]: Result containing created entity or error
            SHA256 hash as hex string

        """
        size = chunk_size or c.Tests.Files.HASH_CHUNK_SIZE
        sha256 = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(size), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def detect_format(
        content: str
        | bytes
        | Mapping[str, t.Tests.Testobject]
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
        if fmt != c.Tests.Files.Format.AUTO:
            return fmt
        if isinstance(content, bytes):
            return c.Tests.Files.Format.BIN
        if isinstance(content, Mapping):
            ext = Path(name).suffix.lower()
            if ext in {".yaml", ".yml"}:
                return c.Tests.Files.Format.YAML
            return c.Tests.Files.Format.JSON
        if isinstance(content, list):
            return c.Tests.Files.Format.CSV
        return c.Tests.Files.get_format(Path(name).suffix)

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
        if fmt != c.Tests.Files.Format.AUTO:
            return fmt
        return c.Tests.Files.get_format(path.suffix)

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
        return c.Tests.Files.format_size(size)

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
        delim = delimiter or c.Tests.Files.DEFAULT_CSV_DELIMITER
        enc = encoding or c.Tests.Files.DEFAULT_ENCODING
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
        | Mapping[str, t.Tests.Testobject]
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
        delim = delimiter or c.Tests.Files.DEFAULT_CSV_DELIMITER
        enc = encoding or c.Tests.Files.DEFAULT_ENCODING
        with path.open("w", newline="", encoding=enc) as f:
            writer = csv.writer(f, delimiter=delim)
            if headers:
                writer.writerow(headers)
            if isinstance(content, list):
                for row in content:
                    writer.writerow(row)

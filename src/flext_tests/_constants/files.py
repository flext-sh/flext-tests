"""File management constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_cli import FlextCliConstants
from flext_tests import t


class FlextTestsFilesConstantsMixin:
    """File management constants mixin for test infrastructure."""

    @unique
    class Format(StrEnum):
        """File format enumeration."""

        AUTO = "auto"
        TEXT = "text"
        BIN = "bin"
        JSON = "json"
        YAML = "yaml"
        CSV = "csv"
        UNKNOWN = "unknown"

    @unique
    class CompareMode(StrEnum):
        """File comparison mode enumeration."""

        CONTENT = "content"
        SIZE = "size"
        HASH = "hash"
        LINES = "lines"

    @unique
    class Operation(StrEnum):
        """File operation type enumeration."""

        CREATE = "create"
        READ = "read"
        DELETE = "delete"

    @unique
    class ErrorMode(StrEnum):
        """Error handling mode enumeration."""

        STOP = "stop"
        SKIP = "skip"
        COLLECT = "collect"

    EXT_TO_FMT: Final[t.StrMapping] = {
        ".txt": "text",
        ".log": "text",
        ".md": "text",
        ".rst": "text",
        ".bin": "bin",
        ".dat": "bin",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".csv": "csv",
        ".tsv": "csv",
    }
    DEFAULT_FILENAME: Final[str] = "file"
    DEFAULT_ENCODING: Final[str] = FlextCliConstants.DEFAULT_ENCODING
    DEFAULT_BINARY_ENCODING: Final[str] = "binary"
    DEFAULT_JSON_INDENT: Final[int] = 2
    DEFAULT_CSV_DELIMITER: Final[str] = ","
    DEFAULT_EXTENSION: Final[str] = ".txt"
    PERMISSION_READONLY_FILE: Final[int] = 292
    PERMISSION_WRITABLE_FILE: Final[int] = 420
    PERMISSION_WRITABLE_DIR: Final[int] = 493
    HASH_CHUNK_SIZE: Final[int] = 8192
    SIZE_UNITS: Final[tuple[str, ...]] = ("B", "KB", "MB", "GB", "TB", "PB")
    SIZE_THRESHOLD: Final[int] = 1024
    ERROR_FILE_NOT_FOUND: Final[str] = "File not found: {path}"
    ERROR_INVALID_JSON: Final[str] = "Invalid JSON: {error}"
    ERROR_INVALID_YAML: Final[str] = "Invalid YAML: {error}"
    ERROR_ENCODING: Final[str] = "Encoding error: {error}"
    ERROR_READ: Final[str] = "Read error: {error}"
    ERROR_COMPARE: Final[str] = "Compare error: {error}"
    ERROR_INFO: Final[str] = "Info error: {error}"

    @classmethod
    def format_size(cls, size: int) -> str:
        """Format size in human-readable format.

        Args:
            size: Size in bytes.

        Returns:
            Human-readable size string like "1.2 KB".

        """
        for unit in cls.SIZE_UNITS:
            if size < cls.SIZE_THRESHOLD:
                return f"{size:.1f} {unit}" if unit != "B" else f"{size} {unit}"
            size //= cls.SIZE_THRESHOLD
        return f"{size:.1f} PB"

    @classmethod
    def get_format(cls, extension: str) -> str:
        """Get format from file extension.

        Args:
            extension: File extension (e.g., ".json").

        Returns:
            Format string or "text" as default.

        """
        return cls.EXT_TO_FMT.get(extension.lower(), "text")

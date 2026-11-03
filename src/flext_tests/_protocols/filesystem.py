# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tests/_protocols/filesystem
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_tests import c, t

if TYPE_CHECKING:
    from flext_cli import p

    from flext_tests._protocols import FlextTestsProtocolsBase


class FlextTestsProtocolsFilesystem:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class FileInfo(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def exists(self) -> bool:
            """True when the file exists."""
            ...

        @property
        def path(self) -> Path | None:
            """Absolute path to the file."""
            ...

        @property
        def size(self) -> int:
            """File size in bytes."""
            ...

        @property
        def size_human(self) -> str:
            """Human-readable size."""
            ...

        @property
        def lines(self) -> int:
            """Line count for text files."""
            ...

        @property
        def encoding(self) -> str:
            """Text encoding detected or assumed."""
            ...

        @property
        def is_empty(self) -> bool:
            """True when the file has zero bytes."""
            ...

        @property
        def first_line(self) -> str:
            """First line of the file."""
            ...

        @property
        def fmt(self) -> str:
            """Detected format label."""
            ...

        @property
        def valid(self) -> bool:
            """True when the file parses cleanly."""
            ...

        @property
        def created(self) -> dt.datetime | None:
            """File creation timestamp."""
            ...

        @property
        def modified(self) -> dt.datetime | None:
            """File last-modified timestamp."""
            ...

        @property
        def permissions(self) -> int:
            """Unix-style permission bits."""
            ...

        @property
        def is_readonly(self) -> bool:
            """True when the file is not writable."""
            ...

        @property
        def sha256(self) -> str | None:
            """Hex-encoded SHA-256 digest."""
            ...

        @property
        def content_meta(self) -> FlextTestsProtocolsFilesystem.ContentMeta | None:
            """Optional content metadata for parsed files."""
            ...

    @runtime_checkable
    class ContentMeta(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def key_count(self) -> int | None:
            """Number of keys for JSON/YAML dicts."""
            ...

        @property
        def item_count(self) -> int | None:
            """Number of items for JSON/YAML lists."""
            ...

        @property
        def row_count(self) -> int | None:
            """Number of rows for CSV files."""
            ...

        @property
        def column_count(self) -> int | None:
            """Number of columns for CSV files."""
            ...

        @property
        def model_valid(self) -> bool | None:
            """Whether content is valid for a specific model."""
            ...

        @property
        def model_name(self) -> str | None:
            """Model class name if validated."""
            ...

    @runtime_checkable
    class CreateParams(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def content(self) -> FlextTestsProtocolsBase.Payload:
            """Owned native file content to create."""
            ...

        @property
        def name(self) -> t.NonEmptyStr:
            """Filename for the created file."""
            ...

        @property
        def directory(self) -> Path | None:
            """Target directory."""
            ...

        @property
        def fmt(self) -> c.Tests.FileFormat:
            """File format override."""
            ...

        @property
        def enc(self) -> t.NonEmptyStr:
            """File encoding."""
            ...

        @property
        def indent(self) -> t.NonNegativeInt:
            """JSON/YAML indentation."""
            ...

        @property
        def delim(self) -> str:
            """CSV delimiter."""
            ...

        @property
        def headers(self) -> Sequence[str] | None:
            """CSV headers."""
            ...

        @property
        def readonly(self) -> bool:
            """Create file as read-only."""
            ...

        @property
        def extract_result(self) -> bool:
            """Auto-extract result value."""
            ...

    @runtime_checkable
    class ReadParams(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def path(self) -> Path:
            """Path to file to read."""
            ...

        @property
        def model_cls(self) -> FlextTestsProtocolsBase.ModelReader[p.Model] | None:
            """Optional Pydantic model class."""
            ...

        @property
        def fmt(self) -> c.Tests.FileFormat:
            """Format override."""
            ...

        @property
        def enc(self) -> t.NonEmptyStr:
            """File encoding."""
            ...

        @property
        def delim(self) -> str:
            """CSV delimiter."""
            ...

        @property
        def has_headers(self) -> bool:
            """CSV has headers."""
            ...

    @runtime_checkable
    class PathCoercingParams(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class CompareParams(PathCoercingParams, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def file1(self) -> Path:
            """First file to compare."""
            ...

        @property
        def file2(self) -> Path:
            """Second file to compare."""
            ...

        @property
        def mode(self) -> str:
            """Comparison mode."""
            ...

        @property
        def ignore_ws(self) -> bool:
            """Ignore whitespace in comparison."""
            ...

        @property
        def ignore_case(self) -> bool:
            """Case-insensitive comparison."""
            ...

        @property
        def pattern(self) -> str | None:
            """Pattern to check if both files contain."""
            ...

        @property
        def deep(self) -> bool:
            """Use deep comparison for nested structures."""
            ...

        @property
        def keys(self) -> Sequence[str] | None:
            """Only compare these keys."""
            ...

        @property
        def exclude_keys(self) -> Sequence[str] | None:
            """Exclude these keys from comparison."""
            ...

    @runtime_checkable
    class InfoParams(PathCoercingParams, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def path(self) -> Path:
            """Path to file."""
            ...

        @property
        def compute_hash(self) -> bool:
            """Compute SHA256 hash."""
            ...

        @property
        def detect_fmt(self) -> bool:
            """Auto-detect format."""
            ...

        @property
        def parse_content(self) -> bool:
            """Parse content and include metadata."""
            ...

        @property
        def validate_model(self) -> FlextTestsProtocolsBase.ModelReader[p.Model] | None:
            """Pydantic model to validate content against."""
            ...

    @runtime_checkable
    class AssertExistsParams(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def is_file(self) -> bool | None:
            """Assert path is file."""
            ...

        @property
        def is_dir(self) -> bool | None:
            """Assert path is directory."""
            ...

        @property
        def not_empty(self) -> bool | None:
            """Assert path content emptiness state."""
            ...

        @property
        def readable(self) -> bool | None:
            """Assert readable permission when True."""
            ...

        @property
        def writable(self) -> bool | None:
            """Assert writable permission when True."""
            ...

    @runtime_checkable
    class CreateKwargsParams(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def directory(self) -> Path | None:
            """Directory to create file in."""
            ...

        @property
        def fmt(self) -> c.Tests.FileFormat:
            """File format override."""
            ...

        @property
        def enc(self) -> t.NonEmptyStr:
            """File encoding."""
            ...

        @property
        def indent(self) -> t.NonNegativeInt:
            """JSON indentation level."""
            ...

        @property
        def delim(self) -> str:
            """CSV delimiter."""
            ...

        @property
        def headers(self) -> Sequence[str] | None:
            """CSV column headers."""
            ...

        @property
        def readonly(self) -> bool:
            """Create file as read-only."""
            ...


__all__: list[str] = [
    "FlextTestsProtocolsFilesystem",
]

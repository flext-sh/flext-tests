"""Filesystem models for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import datetime as dt
from collections.abc import Sequence
from pathlib import Path
from typing import Annotated

from flext_cli import m

from flext_tests import c, p, t
from flext_tests._models import FlextTestsModelsFlextBase


class FlextTestsModelsFilesystem:
    """Filesystem model group (info, content, and operation parameters)."""

    class FileInfo(m.Value):
        """Comprehensive file information model."""

        exists: Annotated[bool, m.Field(description="True when the file exists.")]
        path: Annotated[
            Path | None,
            m.Field(description="Absolute path to the file."),
        ] = None
        size: Annotated[int, m.Field(description="File size in bytes.")] = 0
        size_human: Annotated[str, m.Field(description="Human-readable size.")] = ""
        lines: Annotated[int, m.Field(description="Line count for text files.")] = 0
        encoding: Annotated[
            str,
            m.Field(description="Text encoding detected or assumed."),
        ] = c.Tests.DEFAULT_ENCODING
        is_empty: Annotated[
            bool,
            m.Field(description="True when the file has zero bytes."),
        ] = False
        first_line: Annotated[str, m.Field(description="First line of the file.")] = ""
        fmt: Annotated[str, m.Field(description="Detected format label.")] = "unknown"
        valid: Annotated[
            bool,
            m.Field(description="True when the file parses cleanly."),
        ] = True
        created: Annotated[
            dt.datetime | None,
            m.Field(description="File creation timestamp."),
        ] = None
        modified: Annotated[
            dt.datetime | None,
            m.Field(description="File last-modified timestamp."),
        ] = None
        permissions: Annotated[
            int,
            m.Field(description="Unix-style permission bits."),
        ] = 0
        is_readonly: Annotated[
            bool,
            m.Field(description="True when the file is not writable."),
        ] = False
        sha256: Annotated[
            str | None,
            m.Field(description="Hex-encoded SHA-256 digest."),
        ] = None
        content_meta: Annotated[
            FlextTestsModelsFilesystem.ContentMeta | None,
            m.Field(description="Optional content metadata for parsed files."),
        ] = None

    class ContentMeta(m.Value):
        """Content-specific metadata for parsed files."""

        key_count: Annotated[
            int | None,
            m.Field(description="Number of keys for JSON/YAML dicts."),
        ] = None
        item_count: Annotated[
            int | None,
            m.Field(description="Number of items for JSON/YAML lists."),
        ] = None
        row_count: Annotated[
            int | None,
            m.Field(description="Number of rows for CSV files."),
        ] = None
        column_count: Annotated[
            int | None,
            m.Field(description="Number of columns for CSV files."),
        ] = None
        model_valid: Annotated[
            bool | None,
            m.Field(description="Whether content is valid for a specific model."),
        ] = None
        model_name: Annotated[
            str | None,
            m.Field(description="Model class name if validated."),
        ] = None

    class CreateParams(m.Value):
        """Parameters for file creation operations."""

        content: Annotated[
            FlextTestsModelsFlextBase.Payload,
            m.Field(description="Owned native file content to create."),
        ]
        name: Annotated[
            t.NonEmptyStr,
            m.Field(description="Filename for the created file."),
        ] = c.Tests.DEFAULT_FILENAME
        directory: Annotated[Path | None, m.Field(description="Target directory.")] = (
            None
        )
        fmt: Annotated[
            c.Tests.FileFormat,
            m.BeforeValidator(
                lambda v: (
                    type(c.Tests.FILE_FORMAT_AUTO)(v) if isinstance(v, str) else v
                ),
            ),
            m.Field(
                default=c.Tests.FILE_FORMAT_AUTO,
                description="File format override.",
            ),
        ]
        enc: Annotated[t.NonEmptyStr, m.Field(description="File encoding.")] = (
            c.Tests.DEFAULT_ENCODING
        )
        indent: Annotated[
            t.NonNegativeInt,
            m.Field(description="JSON/YAML indentation."),
        ] = c.Tests.DEFAULT_JSON_INDENT
        delim: Annotated[str, m.Field(description="CSV delimiter.")] = (
            c.Tests.DEFAULT_CSV_DELIMITER
        )
        headers: Annotated[
            Sequence[str] | None,
            m.Field(description="CSV headers."),
        ] = None
        readonly: Annotated[bool, m.Field(description="Create file as read-only.")] = (
            False
        )
        extract_result: Annotated[
            bool,
            m.Field(description="Auto-extract result value."),
        ] = True

        @m.field_validator("name", mode="before")
        @classmethod
        def normalize_name(cls, value: p.AttributeProbe) -> str:
            """Normalize filename by stripping whitespace.

            Returns:
                The resulting ``str``.

            """
            if isinstance(value, str):
                return value.strip()
            return str(value)

    class ReadParams(m.Value):
        """Parameters for file read operations."""

        path: Annotated[Path, m.Field(description="Path to file to read.")]
        model_cls: Annotated[
            type[m.BaseModel] | None,
            m.Field(description="Optional Pydantic model class."),
        ] = None
        fmt: Annotated[
            c.Tests.FileFormat,
            m.BeforeValidator(
                lambda v: (
                    type(c.Tests.FILE_FORMAT_AUTO)(v) if isinstance(v, str) else v
                ),
            ),
            m.Field(default=c.Tests.FILE_FORMAT_AUTO, description="Format override."),
        ]
        enc: Annotated[t.NonEmptyStr, m.Field(description="File encoding.")] = (
            c.Tests.DEFAULT_ENCODING
        )
        delim: Annotated[
            str,
            m.Field(min_length=1, max_length=1, description="CSV delimiter."),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        has_headers: Annotated[bool, m.Field(description="CSV has headers.")] = True

        @m.field_validator("path", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Coerce a string path operand to ``Path`` before validation.

            Args:
                value: The declared path operand as ``Path`` or string.

            Returns:
                The resulting ``Path``.

            """
            return Path(value) if isinstance(value, str) else value

    class PathCoercingParams(m.Value):
        """Coerce declared path operands to ``Path`` before validation."""

        @m.field_validator(
            "file1",
            "file2",
            "path",
            mode="before",
            check_fields=False,
        )
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Coerce a string path operand to ``Path`` before validation.

            Args:
                value: The declared path operand as ``Path`` or string.

            Returns:
                The resulting ``Path``.

            """
            return Path(value)

    class CompareParams(PathCoercingParams):
        """Parameters for file comparison operations."""

        file1: Annotated[Path, m.Field(description="First file to compare.")]
        file2: Annotated[Path, m.Field(description="Second file to compare.")]
        mode: Annotated[str, m.Field(description="Comparison mode.")] = (
            c.Tests.CompareMode.CONTENT.value
        )
        ignore_ws: Annotated[
            bool,
            m.Field(description="Ignore whitespace in comparison."),
        ] = False
        ignore_case: Annotated[
            bool,
            m.Field(description="Case-insensitive comparison."),
        ] = False
        pattern: Annotated[
            str | None,
            m.Field(description="Pattern to check if both files contain."),
        ] = None
        deep: Annotated[
            bool,
            m.Field(description="Use deep comparison for nested structures."),
        ] = True
        keys: Annotated[
            Sequence[str] | None,
            m.Field(description="Only compare these keys."),
        ] = None
        exclude_keys: Annotated[
            Sequence[str] | None,
            m.Field(description="Exclude these keys from comparison."),
        ] = None

    class InfoParams(PathCoercingParams):
        """Parameters for file info operations."""

        path: Annotated[Path, m.Field(description="Path to file.")]
        compute_hash: Annotated[bool, m.Field(description="Compute SHA256 hash.")] = (
            False
        )
        detect_fmt: Annotated[bool, m.Field(description="Auto-detect format.")] = True
        parse_content: Annotated[
            bool,
            m.Field(description="Parse content and include metadata."),
        ] = False
        validate_model: Annotated[
            type[m.BaseModel] | None,
            m.Field(description="Pydantic model to validate content against."),
        ] = None

    class AssertExistsParams(m.Value):
        """Validation options for file/dir existence assertions."""

        is_file: Annotated[bool | None, m.Field(description="Assert path is file.")] = (
            None
        )
        is_dir: Annotated[
            bool | None,
            m.Field(description="Assert path is directory."),
        ] = None
        not_empty: Annotated[
            bool | None,
            m.Field(description="Assert path content emptiness state."),
        ] = None
        readable: Annotated[
            bool | None,
            m.Field(description="Assert readable permission when True."),
        ] = None
        writable: Annotated[
            bool | None,
            m.Field(description="Assert writable permission when True."),
        ] = None

    class CreateKwargsParams(m.Value):
        """Parameters for file create kwargs."""

        directory: Annotated[
            Path | None,
            m.Field(description="Directory to create file in."),
        ] = None
        fmt: Annotated[
            c.Tests.FileFormat,
            m.BeforeValidator(
                lambda v: (
                    type(c.Tests.FILE_FORMAT_AUTO)(v) if isinstance(v, str) else v
                ),
            ),
            m.Field(description="File format override."),
        ] = c.Tests.FILE_FORMAT_AUTO
        enc: Annotated[t.NonEmptyStr, m.Field(description="File encoding.")] = (
            c.Tests.DEFAULT_ENCODING
        )
        indent: Annotated[
            t.NonNegativeInt,
            m.Field(description="JSON indentation level."),
        ] = c.Tests.DEFAULT_JSON_INDENT
        delim: Annotated[
            str,
            m.Field(min_length=1, max_length=1, description="CSV delimiter."),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        headers: Annotated[
            Sequence[str] | None,
            m.Field(description="CSV column headers."),
        ] = None
        readonly: Annotated[bool, m.Field(description="Create file as read-only.")] = (
            False
        )


__all__: list[str] = ["FlextTestsModelsFilesystem"]

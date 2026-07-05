"""Filesystem information and creation models for flext-tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from flext_infra import m, u
from flext_tests.constants import c
from flext_tests.typings import t

if TYPE_CHECKING:
    import datetime

from pathlib import Path


class FlextTestsFilesystemModelsMixin:
    """Filesystem model group for flext-tests."""

    class FileInfo(m.Value):
        """Comprehensive file information model."""

        exists: Annotated[bool, u.Field(description="True when the file exists.")]
        path: Annotated[
            Path | None,
            u.Field(description="Absolute path to the file."),
        ] = None
        size: Annotated[int, u.Field(description="File size in bytes.")] = 0
        size_human: Annotated[
            str,
            u.Field(description="Human-readable size."),
        ] = ""
        lines: Annotated[int, u.Field(description="Line count for text files.")] = 0
        encoding: Annotated[
            str,
            u.Field(description="Text encoding detected or assumed."),
        ] = c.Tests.DEFAULT_ENCODING
        is_empty: Annotated[
            bool,
            u.Field(description="True when the file has zero bytes."),
        ] = False
        first_line: Annotated[
            str,
            u.Field(description="First line of the file."),
        ] = ""
        fmt: Annotated[str, u.Field(description="Detected format label.")] = "unknown"
        valid: Annotated[
            bool,
            u.Field(description="True when the file parses cleanly."),
        ] = True
        created: Annotated[
            datetime.datetime | None,
            u.Field(description="File creation timestamp."),
        ] = None
        modified: Annotated[
            datetime.datetime | None,
            u.Field(description="File last-modified timestamp."),
        ] = None
        permissions: Annotated[
            int,
            u.Field(description="Unix-style permission bits."),
        ] = 0
        is_readonly: Annotated[
            bool,
            u.Field(description="True when the file is not writable."),
        ] = False
        sha256: Annotated[
            str | None,
            u.Field(description="Hex-encoded SHA-256 digest."),
        ] = None
        content_meta: Annotated[
            FlextTestsFilesystemModelsMixin.ContentMeta | None,
            u.Field(description="Optional content metadata for parsed files."),
        ] = None

    class ContentMeta(m.Value):
        """Content-specific metadata for parsed files."""

        key_count: Annotated[
            int | None,
            u.Field(description="Number of keys for JSON/YAML dicts."),
        ] = None
        item_count: Annotated[
            int | None,
            u.Field(description="Number of items for JSON/YAML lists."),
        ] = None
        row_count: Annotated[
            int | None,
            u.Field(description="Number of rows for CSV files."),
        ] = None
        column_count: Annotated[
            int | None,
            u.Field(description="Number of columns for CSV files."),
        ] = None
        model_valid: Annotated[
            bool | None,
            u.Field(description="Whether content is valid for a specific model."),
        ] = None
        model_name: Annotated[
            str | None,
            u.Field(description="Model class name if validated."),
        ] = None

    class CreateParams(m.Value):
        """Parameters for file creation operations."""

        content: Annotated[
            t.Tests.FileContentPlain,
            u.Field(description="File content to create."),
        ]
        name: Annotated[
            t.NonEmptyStr,
            u.Field(description="Filename for the created file."),
        ] = c.Tests.DEFAULT_FILENAME
        directory: Annotated[
            Path | None,
            u.Field(description="Target directory."),
        ] = None
        fmt: Annotated[
            c.Tests.FileFormat,
            m.BeforeValidator(
                lambda v: (
                    type(c.Tests.FILE_FORMAT_AUTO)(v) if isinstance(v, str) else v
                ),
            ),
            u.Field(
                default=c.Tests.FILE_FORMAT_AUTO,
                description="File format override.",
            ),
        ]
        enc: Annotated[
            t.NonEmptyStr,
            u.Field(description="File encoding."),
        ] = c.Tests.DEFAULT_ENCODING
        indent: Annotated[
            t.NonNegativeInt,
            u.Field(description="JSON/YAML indentation."),
        ] = c.Tests.DEFAULT_JSON_INDENT
        delim: Annotated[
            str,
            u.Field(description="CSV delimiter."),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        headers: Annotated[
            t.StrSequence | None,
            u.Field(description="CSV headers."),
        ] = None
        readonly: Annotated[
            bool,
            u.Field(description="Create file as read-only."),
        ] = False
        extract_result: Annotated[
            bool,
            u.Field(description="Auto-extract result value."),
        ] = True

        @u.field_validator("name", mode="before")
        @classmethod
        def normalize_name(cls, value: t.Tests.TestobjectSerializable) -> str:
            """Normalize filename by stripping whitespace."""
            if isinstance(value, str):
                return value.strip()
            return str(value)


__all__: list[str] = ["FlextTestsFilesystemModelsMixin"]

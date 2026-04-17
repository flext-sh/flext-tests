"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
)

from flext_core import m, u
from flext_tests import c, t


class FlextTestsFilesystemModelsMixin:
    class FileInfo(m.Value):
        """Comprehensive file information model."""

        exists: bool
        path: Path | None = None
        size: int = 0
        size_human: str = ""
        lines: int = 0
        encoding: str = "utf-8"
        is_empty: bool = False
        first_line: str = ""
        fmt: str = "unknown"
        valid: bool = True
        created: datetime.datetime | None = None
        modified: datetime.datetime | None = None
        permissions: int = 0
        is_readonly: bool = False
        sha256: str | None = None
        content_meta: FlextTestsFilesystemModelsMixin.ContentMeta | None = None
        """Optional content metadata for parsed files."""

    class ContentMeta(m.Value):
        """Content-specific metadata for parsed files."""

        key_count: int | None = None
        """Number of keys for JSON/YAML dicts."""
        item_count: int | None = None
        """Number of items for JSON/YAML lists."""
        row_count: int | None = None
        """Number of rows for CSV files."""
        column_count: int | None = None
        """Number of columns for CSV files."""
        model_valid: bool | None = None
        """Whether content is valid for a specific model."""
        model_name: str | None = None
        """Model class name if validated."""

    class CreateParams(m.Value):
        """Parameters for file creation operations with Pydantic 2 advanced validation."""

        content: t.Tests.TestobjectSerializable
        """File content to create."""
        name: Annotated[
            t.NonEmptyStr,
            u.Field(
                description="Filename for the created file (non-empty).",
            ),
        ] = c.Tests.DEFAULT_FILENAME
        directory: Annotated[
            Path | None,
            u.Field(
                description="Target directory (uses base_dir or temp if None).",
            ),
        ] = None
        fmt: Annotated[
            c.Tests.Format,
            BeforeValidator(lambda v: c.Tests.Format(v) if isinstance(v, str) else v),
            u.Field(
                default=c.Tests.Format.AUTO,
                description="File format override.",
            ),
        ]
        enc: Annotated[
            t.NonEmptyStr,
            u.Field(
                description="File encoding.",
            ),
        ] = c.Tests.DEFAULT_ENCODING
        indent: Annotated[
            t.NonNegativeInt,
            u.Field(
                description="JSON/YAML indentation (non-negative).",
            ),
        ] = c.Tests.DEFAULT_JSON_INDENT
        delim: Annotated[
            str,
            u.Field(
                description="CSV delimiter (single character).",
            ),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        headers: Annotated[
            t.StrSequence | None,
            u.Field(
                description="CSV headers.",
            ),
        ] = None
        readonly: Annotated[
            bool,
            u.Field(
                description="Create file as read-only.",
            ),
        ] = False
        extract_result: Annotated[
            bool,
            u.Field(
                description="Auto-extract r value.",
            ),
        ] = True

        @u.field_validator("name", mode="before")
        @classmethod
        def normalize_name(cls, value: t.Tests.TestobjectSerializable) -> str:
            """Normalize filename by stripping whitespace."""
            if isinstance(value, str):
                return value.strip()
            return str(value)

    class ReadParams(m.Value):
        """Parameters for file read operations with Pydantic 2 advanced validation."""

        path: Annotated[
            Path,
            u.Field(
                description="Path to file to read (str or Path converted automatically).",
            ),
        ]
        model_cls: Annotated[
            type[BaseModel] | None,
            u.Field(
                description="Optional Pydantic model class to deserialize into.",
            ),
        ] = None
        fmt: Annotated[
            c.Tests.Format,
            BeforeValidator(lambda v: c.Tests.Format(v) if isinstance(v, str) else v),
            u.Field(
                default=c.Tests.Format.AUTO,
                description="Format override.",
            ),
        ]
        enc: Annotated[
            t.NonEmptyStr,
            u.Field(
                description="File encoding.",
            ),
        ] = c.Tests.DEFAULT_ENCODING
        delim: Annotated[
            str,
            u.Field(
                min_length=1,
                max_length=1,
                description="CSV delimiter (single character).",
            ),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        has_headers: Annotated[
            bool,
            u.Field(
                description="CSV has headers.",
            ),
        ] = True

        @u.field_validator("path", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path - Field constraints cannot handle type conversion."""
            return Path(value) if isinstance(value, str) else value

    class CompareParams(m.Value):
        """Parameters for file comparison operations with Pydantic 2 advanced validation."""

        file1: Annotated[
            Path,
            u.Field(
                description="First file to compare (str or Path converted automatically).",
            ),
        ]
        file2: Annotated[
            Path,
            u.Field(
                description="Second file to compare (str or Path converted automatically).",
            ),
        ]
        mode: Annotated[
            str,
            u.Field(
                description="Comparison mode.",
            ),
        ] = c.Tests.CompareMode.CONTENT.value
        ignore_ws: Annotated[
            bool,
            u.Field(
                description="Ignore whitespace in comparison.",
            ),
        ] = False
        ignore_case: Annotated[
            bool,
            u.Field(
                description="Case-insensitive comparison.",
            ),
        ] = False
        pattern: Annotated[
            str | None,
            u.Field(
                description="Pattern to check if both files contain.",
            ),
        ] = None
        deep: Annotated[
            bool,
            u.Field(
                description="Use deep comparison for nested structures (dict/JSON/YAML).",
            ),
        ] = True
        keys: Annotated[
            t.StrSequence | None,
            u.Field(
                description="Only compare these keys (for dict/JSON/YAML content).",
            ),
        ] = None
        exclude_keys: Annotated[
            t.StrSequence | None,
            u.Field(
                description="Exclude these keys from comparison (for dict/JSON/YAML content).",
            ),
        ] = None

        @u.field_validator("file1", "file2", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path - Field constraints cannot handle type conversion."""
            return Path(value)

    class InfoParams(m.Value):
        """Parameters for file info() operations with Pydantic 2 validation."""

        path: Annotated[
            Path,
            u.Field(
                description="Path to file (str or Path converted automatically).",
            ),
        ]
        compute_hash: Annotated[
            bool,
            u.Field(
                description="Compute SHA256 hash.",
            ),
        ] = False
        detect_fmt: Annotated[
            bool,
            u.Field(
                description="Auto-detect format.",
            ),
        ] = True
        parse_content: Annotated[
            bool,
            u.Field(
                description="Parse content and include metadata.",
            ),
        ] = False
        validate_model: Annotated[
            type[BaseModel] | None,
            u.Field(
                description="Pydantic model to validate content against.",
            ),
        ] = None

        @u.field_validator("path", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path - Field constraints cannot handle type conversion."""
            return Path(value)

    class CreateKwargsParams(m.Value):
        """Parameters for file create() kwargs with Pydantic 2 validation.

        Fields match FlextTestsFileManager.create() method signature exactly.
        """

        directory: Annotated[
            Path | None,
            u.Field(
                description="Directory to create file in.",
            ),
        ] = None
        fmt: Annotated[
            c.Tests.Format,
            BeforeValidator(lambda v: c.Tests.Format(v) if isinstance(v, str) else v),
            u.Field(
                default=c.Tests.Format.AUTO,
                description="File format override.",
            ),
        ]
        enc: Annotated[
            t.NonEmptyStr,
            u.Field(
                description="File encoding.",
            ),
        ] = c.Tests.DEFAULT_ENCODING
        indent: Annotated[
            t.NonNegativeInt,
            u.Field(
                description="JSON indentation level.",
            ),
        ] = c.Tests.DEFAULT_JSON_INDENT
        delim: Annotated[
            str,
            u.Field(
                min_length=1,
                max_length=1,
                description="CSV delimiter (single character).",
            ),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        headers: Annotated[
            t.StrSequence | None,
            u.Field(
                description="CSV column headers.",
            ),
        ] = None
        readonly: Annotated[
            bool,
            u.Field(
                description="Create file as read-only.",
            ),
        ] = False

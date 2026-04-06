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
    Field,
    field_validator,
)

from flext_core import FlextModels
from flext_tests import c, t


class FlextTestsFilesystemModelsMixin:
    class FileInfo(FlextModels.Value):
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
        is_valid: bool = True
        created: datetime.datetime | None = None
        modified: datetime.datetime | None = None
        permissions: int = 0
        is_readonly: bool = False
        sha256: str | None = None
        content_meta: FlextTestsFilesystemModelsMixin.ContentMeta | None = None
        """Optional content metadata for parsed files."""

    class ContentMeta(FlextModels.Value):
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

    class CreateParams(FlextModels.Value):
        """Parameters for file creation operations with Pydantic 2 advanced validation."""

        content: t.Tests.Testobject
        """File content to create."""
        name: Annotated[
            t.NonEmptyStr,
            Field(
                default=c.Tests.DEFAULT_FILENAME,
                description="Filename for the created file (non-empty).",
            ),
        ]
        directory: Annotated[
            Path | None,
            Field(
                default=None,
                description="Target directory (uses base_dir or temp if None).",
            ),
        ]
        fmt: Annotated[
            c.Tests.Format,
            BeforeValidator(lambda v: c.Tests.Format(v) if isinstance(v, str) else v),
            Field(
                default=c.Tests.Format.AUTO,
                description="File format override.",
            ),
        ]
        enc: Annotated[
            t.NonEmptyStr,
            Field(
                default=c.Tests.DEFAULT_ENCODING,
                description="File encoding.",
            ),
        ]
        indent: Annotated[
            t.NonNegativeInt,
            Field(
                default=c.Tests.DEFAULT_JSON_INDENT,
                description="JSON/YAML indentation (non-negative).",
            ),
        ]
        delim: Annotated[
            str,
            Field(
                default=c.Tests.DEFAULT_CSV_DELIMITER,
                description="CSV delimiter (single character).",
            ),
        ]
        headers: Annotated[
            t.StrSequence | None,
            Field(
                default=None,
                description="CSV headers.",
            ),
        ]
        readonly: Annotated[
            bool,
            Field(
                default=False,
                description="Create file as read-only.",
            ),
        ]
        extract_result: Annotated[
            bool,
            Field(
                default=True,
                description="Auto-extract r value.",
            ),
        ]

        @field_validator("name", mode="before")
        @classmethod
        def normalize_name(cls, value: t.Tests.Testobject) -> str:
            """Normalize filename by stripping whitespace."""
            if isinstance(value, str):
                return value.strip()
            return str(value)

    class ReadParams(FlextModels.Value):
        """Parameters for file read operations with Pydantic 2 advanced validation."""

        path: Annotated[
            Path,
            Field(
                description="Path to file to read (str or Path converted automatically).",
            ),
        ]
        model_cls: Annotated[
            type[BaseModel] | None,
            Field(
                default=None,
                description="Optional Pydantic model class to deserialize into.",
            ),
        ]
        fmt: Annotated[
            c.Tests.Format,
            BeforeValidator(lambda v: c.Tests.Format(v) if isinstance(v, str) else v),
            Field(
                default=c.Tests.Format.AUTO,
                description="Format override.",
            ),
        ]
        enc: Annotated[
            t.NonEmptyStr,
            Field(
                default=c.Tests.DEFAULT_ENCODING,
                description="File encoding.",
            ),
        ]
        delim: Annotated[
            str,
            Field(
                default=c.Tests.DEFAULT_CSV_DELIMITER,
                min_length=1,
                max_length=1,
                description="CSV delimiter (single character).",
            ),
        ]
        has_headers: Annotated[
            bool,
            Field(
                default=True,
                description="CSV has headers.",
            ),
        ]

        @field_validator("path", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path - Field constraints cannot handle type conversion."""
            return Path(value) if isinstance(value, str) else value

    class CompareParams(FlextModels.Value):
        """Parameters for file comparison operations with Pydantic 2 advanced validation."""

        file1: Annotated[
            Path,
            Field(
                description="First file to compare (str or Path converted automatically).",
            ),
        ]
        file2: Annotated[
            Path,
            Field(
                description="Second file to compare (str or Path converted automatically).",
            ),
        ]
        mode: Annotated[
            str,
            Field(
                default=c.Tests.CompareMode.CONTENT.value,
                description="Comparison mode.",
            ),
        ]
        ignore_ws: Annotated[
            bool,
            Field(
                default=False,
                description="Ignore whitespace in comparison.",
            ),
        ]
        ignore_case: Annotated[
            bool,
            Field(
                default=False,
                description="Case-insensitive comparison.",
            ),
        ]
        pattern: Annotated[
            str | None,
            Field(
                default=None,
                description="Pattern to check if both files contain.",
            ),
        ]
        deep: Annotated[
            bool,
            Field(
                default=True,
                description="Use deep comparison for nested structures (dict/JSON/YAML).",
            ),
        ]
        keys: Annotated[
            t.StrSequence | None,
            Field(
                default=None,
                description="Only compare these keys (for dict/JSON/YAML content).",
            ),
        ]
        exclude_keys: Annotated[
            t.StrSequence | None,
            Field(
                default=None,
                description="Exclude these keys from comparison (for dict/JSON/YAML content).",
            ),
        ]

        @field_validator("file1", "file2", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path - Field constraints cannot handle type conversion."""
            return Path(value)

    class InfoParams(FlextModels.Value):
        """Parameters for file info() operations with Pydantic 2 validation."""

        path: Annotated[
            Path,
            Field(
                description="Path to file (str or Path converted automatically).",
            ),
        ]
        compute_hash: Annotated[
            bool,
            Field(
                default=False,
                description="Compute SHA256 hash.",
            ),
        ]
        detect_fmt: Annotated[
            bool,
            Field(
                default=True,
                description="Auto-detect format.",
            ),
        ]
        parse_content: Annotated[
            bool,
            Field(
                default=False,
                description="Parse content and include metadata.",
            ),
        ]
        validate_model: Annotated[
            type[BaseModel] | None,
            Field(
                default=None,
                description="Pydantic model to validate content against.",
            ),
        ]

        @field_validator("path", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path - Field constraints cannot handle type conversion."""
            return Path(value)

    class CreateKwargsParams(FlextModels.Value):
        """Parameters for file create() kwargs with Pydantic 2 validation.

        Fields match FlextTestsFileManager.create() method signature exactly.
        """

        directory: Annotated[
            Path | None,
            Field(
                default=None,
                description="Directory to create file in.",
            ),
        ]
        fmt: Annotated[
            c.Tests.Format,
            BeforeValidator(lambda v: c.Tests.Format(v) if isinstance(v, str) else v),
            Field(
                default=c.Tests.Format.AUTO,
                description="File format override.",
            ),
        ]
        enc: Annotated[
            t.NonEmptyStr,
            Field(
                default=c.Tests.DEFAULT_ENCODING,
                description="File encoding.",
            ),
        ]
        indent: Annotated[
            t.NonNegativeInt,
            Field(
                default=c.Tests.DEFAULT_JSON_INDENT,
                description="JSON indentation level.",
            ),
        ]
        delim: Annotated[
            str,
            Field(
                default=c.Tests.DEFAULT_CSV_DELIMITER,
                min_length=1,
                max_length=1,
                description="CSV delimiter (single character).",
            ),
        ]
        headers: Annotated[
            t.StrSequence | None,
            Field(
                default=None,
                description="CSV column headers.",
            ),
        ]
        readonly: Annotated[
            bool,
            Field(
                default=False,
                description="Create file as read-only.",
            ),
        ]

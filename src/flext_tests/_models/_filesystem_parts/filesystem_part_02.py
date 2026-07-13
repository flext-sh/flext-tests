"""Filesystem operation parameter models for flext-tests."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from flext_infra import m, u
from flext_tests import c, t
from flext_tests._models._filesystem_parts.filesystem_part_01 import (
    FlextTestsFilesystemModelsMixin as FlextTestsFilesystemModelsMixinPart01,
)


class FlextTestsFilesystemModelsMixin(FlextTestsFilesystemModelsMixinPart01):
    """Filesystem operation parameter models for flext-tests."""

    class ReadParams(m.Value):
        """Parameters for file read operations."""

        path: Annotated[Path, u.Field(description="Path to file to read.")]
        model_cls: Annotated[
            type[m.BaseModel] | None,
            u.Field(description="Optional Pydantic model class."),
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
                description="Format override.",
            ),
        ]
        enc: Annotated[
            t.NonEmptyStr,
            u.Field(description="File encoding."),
        ] = c.Tests.DEFAULT_ENCODING
        delim: Annotated[
            str,
            u.Field(min_length=1, max_length=1, description="CSV delimiter."),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        has_headers: Annotated[
            bool,
            u.Field(description="CSV has headers."),
        ] = True

        @u.field_validator("path", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path."""
            return Path(value) if isinstance(value, str) else value

    class CompareParams(m.Value):
        """Parameters for file comparison operations."""

        file1: Annotated[Path, u.Field(description="First file to compare.")]
        file2: Annotated[Path, u.Field(description="Second file to compare.")]
        mode: Annotated[str, u.Field(description="Comparison mode.")] = (
            c.Tests.CompareMode.CONTENT.value
        )
        ignore_ws: Annotated[
            bool,
            u.Field(description="Ignore whitespace in comparison."),
        ] = False
        ignore_case: Annotated[
            bool,
            u.Field(description="Case-insensitive comparison."),
        ] = False
        pattern: Annotated[
            str | None,
            u.Field(description="Pattern to check if both files contain."),
        ] = None
        deep: Annotated[
            bool,
            u.Field(description="Use deep comparison for nested structures."),
        ] = True
        keys: Annotated[
            t.StrSequence | None,
            u.Field(description="Only compare these keys."),
        ] = None
        exclude_keys: Annotated[
            t.StrSequence | None,
            u.Field(description="Exclude these keys from comparison."),
        ] = None

        @u.field_validator("file1", "file2", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path."""
            return Path(value)

    class InfoParams(m.Value):
        """Parameters for file info operations."""

        path: Annotated[Path, u.Field(description="Path to file.")]
        compute_hash: Annotated[
            bool,
            u.Field(description="Compute SHA256 hash."),
        ] = False
        detect_fmt: Annotated[
            bool,
            u.Field(description="Auto-detect format."),
        ] = True
        parse_content: Annotated[
            bool,
            u.Field(description="Parse content and include metadata."),
        ] = False
        validate_model: Annotated[
            type[m.BaseModel] | None,
            u.Field(description="Pydantic model to validate content against."),
        ] = None

        @u.field_validator("path", mode="before")
        @classmethod
        def convert_path(cls, value: Path | str) -> Path:
            """Convert string to Path."""
            return Path(value)

    class AssertExistsParams(m.Value):
        """Validation options for file/dir existence assertions."""

        is_file: Annotated[
            bool | None,
            u.Field(description="Assert path is file."),
        ] = None
        is_dir: Annotated[
            bool | None,
            u.Field(description="Assert path is directory."),
        ] = None
        not_empty: Annotated[
            bool | None,
            u.Field(description="Assert path content emptiness state."),
        ] = None
        readable: Annotated[
            bool | None,
            u.Field(description="Assert readable permission when True."),
        ] = None
        writable: Annotated[
            bool | None,
            u.Field(description="Assert writable permission when True."),
        ] = None

    class CreateKwargsParams(m.Value):
        """Parameters for file create kwargs."""

        directory: Annotated[
            Path | None,
            u.Field(description="Directory to create file in."),
        ] = None
        fmt: Annotated[
            c.Tests.FileFormat,
            m.BeforeValidator(
                lambda v: (
                    type(c.Tests.FILE_FORMAT_AUTO)(v) if isinstance(v, str) else v
                ),
            ),
            u.Field(
                description="File format override.",
            ),
        ] = c.Tests.FILE_FORMAT_AUTO
        enc: Annotated[
            t.NonEmptyStr,
            u.Field(description="File encoding."),
        ] = c.Tests.DEFAULT_ENCODING
        indent: Annotated[
            t.NonNegativeInt,
            u.Field(description="JSON indentation level."),
        ] = c.Tests.DEFAULT_JSON_INDENT
        delim: Annotated[
            str,
            u.Field(min_length=1, max_length=1, description="CSV delimiter."),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        headers: Annotated[
            t.StrSequence | None,
            u.Field(description="CSV column headers."),
        ] = None
        readonly: Annotated[
            bool,
            u.Field(description="Create file as read-only."),
        ] = False


__all__: list[str] = ["FlextTestsFilesystemModelsMixin"]

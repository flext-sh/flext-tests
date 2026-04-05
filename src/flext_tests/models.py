"""Models for FLEXT tests.

Provides FlextTestsModels, extending FlextModels with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import datetime
import sys
from collections.abc import Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import Annotated, ClassVar, TypeAliasType, override

from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    TypeAdapter,
    computed_field,
    field_validator,
    model_validator,
)

from flext_core import FlextModels, r
from flext_tests import c, p, t


class FlextTestsModels(
    FlextModels,
):
    """Test models extending FlextModels with test-specific factory models."""

    class Tests:
        """Test-specific models namespace."""

        class ContainerInfo(FlextModels.Value):
            """Container information model."""

            name: str
            status: c.Tests.Docker.ContainerStatus
            ports: t.StrMapping
            image: str
            container_id: str = ""

            @override
            def model_post_init(self, __context: t.Container | None, /) -> None:
                """Validate container info after initialization."""
                super().model_post_init(__context)
                if not self.name:
                    msg = "Container name cannot be empty"
                    raise ValueError(msg)
                if not self.image:
                    msg = "Container image cannot be empty"
                    raise ValueError(msg)

        class ContainerConfig(FlextModels.Value):
            """Container configuration model."""

            compose_file: Path
            service: str
            port: int

            @override
            def model_post_init(self, __context: t.Container | None, /) -> None:
                """Validate container config after initialization."""
                super().model_post_init(__context)
                if not self.compose_file.exists():
                    msg = f"Compose file not found: {self.compose_file}"
                    raise ValueError(msg)
                if not self.service:
                    msg = "Service name cannot be empty"
                    raise ValueError(msg)
                if not (c.DEFAULT_RETRY_DELAY_SECONDS <= self.port <= c.MAX_PORT):
                    msg = f"Port {self.port} out of valid range"
                    raise ValueError(msg)

        class ContainerState(FlextModels.Value):
            """Container state tracking model."""

            container_name: str
            is_dirty: bool
            worker_id: str
            last_updated: str | None = None

        class User(FlextModels.Value):
            """Test user model - immutable value t.NormalizedValue."""

            id: str
            name: str
            email: str
            active: bool = True

        class Config(FlextModels.Value):
            """Test configuration model - immutable value t.NormalizedValue."""

            service_type: str = "api"
            environment: str = "test"
            debug: bool = True
            log_level: str = "DEBUG"
            timeout: int = 30
            max_retries: int = 3

        class Service(FlextModels.Value):
            """Test service model - immutable value t.NormalizedValue."""

            id: str
            type: str = "api"
            name: str = ""
            status: str = "active"

        class Entity(FlextModels.Entity):
            """Factory entity class for tests."""

            name: str = ""
            value: t.Tests.Testobject = None

        class Value(FlextModels.Value):
            """Factory value t.NormalizedValue class for tests."""

            data: str = ""
            count: int = 0

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
            content_meta: FlextTestsModels.Tests.ContentMeta | None = None
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
                    default=c.Tests.Files.DEFAULT_FILENAME,
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
                c.Tests.Files.Format,
                BeforeValidator(
                    lambda v: c.Tests.Files.Format(v) if isinstance(v, str) else v
                ),
                Field(
                    default=c.Tests.Files.Format.AUTO,
                    description="File format override.",
                ),
            ]
            enc: Annotated[
                t.NonEmptyStr,
                Field(
                    default=c.Tests.Files.DEFAULT_ENCODING,
                    description="File encoding.",
                ),
            ]
            indent: Annotated[
                t.NonNegativeInt,
                Field(
                    default=c.Tests.Files.DEFAULT_JSON_INDENT,
                    description="JSON/YAML indentation (non-negative).",
                ),
            ]
            delim: Annotated[
                str,
                Field(
                    default=c.Tests.Files.DEFAULT_CSV_DELIMITER,
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
                c.Tests.Files.Format,
                BeforeValidator(
                    lambda v: c.Tests.Files.Format(v) if isinstance(v, str) else v
                ),
                Field(
                    default=c.Tests.Files.Format.AUTO,
                    description="Format override.",
                ),
            ]
            enc: Annotated[
                t.NonEmptyStr,
                Field(
                    default=c.Tests.Files.DEFAULT_ENCODING,
                    description="File encoding.",
                ),
            ]
            delim: Annotated[
                str,
                Field(
                    default=c.Tests.Files.DEFAULT_CSV_DELIMITER,
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
                    default=c.Tests.Files.CompareMode.CONTENT.value,
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
                c.Tests.Files.Format,
                BeforeValidator(
                    lambda v: c.Tests.Files.Format(v) if isinstance(v, str) else v
                ),
                Field(
                    default=c.Tests.Files.Format.AUTO,
                    description="File format override.",
                ),
            ]
            enc: Annotated[
                t.NonEmptyStr,
                Field(
                    default=c.Tests.Files.DEFAULT_ENCODING,
                    description="File encoding.",
                ),
            ]
            indent: Annotated[
                t.NonNegativeInt,
                Field(
                    default=c.Tests.Files.DEFAULT_JSON_INDENT,
                    description="JSON indentation level.",
                ),
            ]
            delim: Annotated[
                str,
                Field(
                    default=c.Tests.Files.DEFAULT_CSV_DELIMITER,
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

        class BatchParams(FlextModels.Value):
            """Parameters for FlextTestsFiles.batch() method."""

            files: Annotated[
                t.Tests.Files.BatchFiles,
                Field(
                    description="Mapping or Sequence of files to process",
                ),
            ]
            directory: Annotated[
                Path | None,
                Field(
                    default=None,
                    description="Target directory for create operations",
                ),
            ]
            operation: Annotated[
                c.Tests.Files.Operation,
                BeforeValidator(
                    lambda v: c.Tests.Files.Operation(v) if isinstance(v, str) else v
                ),
                Field(
                    default=c.Tests.Files.Operation.CREATE,
                    description="Operation type: create, read, or delete",
                ),
            ]
            model: Annotated[
                type[BaseModel] | None,
                Field(
                    default=None,
                    description="Optional model class for read operations",
                ),
            ]
            on_error: Annotated[
                c.Tests.Files.ErrorMode,
                BeforeValidator(
                    lambda v: c.Tests.Files.ErrorMode(v) if isinstance(v, str) else v
                ),
                Field(
                    default=c.Tests.Files.ErrorMode.COLLECT,
                    description="Error handling mode: stop, skip, or collect",
                ),
            ]
            parallel: Annotated[
                bool,
                Field(
                    default=False,
                    description="Run operations in parallel",
                ),
            ]

        class BatchResult(FlextModels.Value):
            """Result of batch file operations."""

            succeeded: Annotated[
                int,
                Field(
                    ge=0,
                    description="Number of successful operations",
                ),
            ]
            failed: Annotated[
                t.NonNegativeInt,
                Field(description="Number of failed operations"),
            ]
            total: Annotated[
                t.NonNegativeInt,
                Field(description="Total number of operations"),
            ]
            results: Annotated[
                Mapping[str, r[Path | t.Tests.Testobject]],
                Field(
                    description="Mapping of file names to operation results",
                ),
            ] = Field(default_factory=dict)
            errors: Annotated[
                t.StrMapping,
                Field(
                    description="Mapping of file names to error messages",
                ),
            ] = Field(default_factory=dict)

            @computed_field
            def failure_count(self) -> int:
                """Alias for failed count."""
                return self.failed

            @computed_field
            def success_count(self) -> int:
                """Alias for succeeded count."""
                return self.succeeded

            @computed_field
            def success_rate(self) -> float:
                """Compute success rate as percentage."""
                if self.total == 0:
                    return 0.0
                return (self.succeeded / self.total) * 100.0

        class Violation(FlextModels.Value):
            """A detected architecture violation."""

            file_path: Path
            line_number: int
            rule_id: str
            severity: c.Tests.Validator.Severity
            description: str
            code_snippet: str = ""

            @field_validator("severity", mode="before")
            @classmethod
            def _coerce_severity(
                cls,
                value: c.Tests.Validator.Severity | str,
            ) -> c.Tests.Validator.Severity:
                if isinstance(value, c.Tests.Validator.Severity):
                    return value
                return c.Tests.Validator.Severity(str(value).upper())

            def format(self) -> str:
                """Format violation as string."""
                return c.Tests.Validator.Messages.VIOLATION_WITH_SNIPPET.format(
                    rule_id=self.rule_id,
                    description=self.description,
                    snippet=self.code_snippet or "(no snippet)",
                )

            def format_short(self) -> str:
                """Format violation as short string."""
                return c.Tests.Validator.Messages.VIOLATION.format(
                    rule_id=self.rule_id,
                    file=self.file_path.name,
                    line=self.line_number,
                )

        class ScanResult(FlextModels.Value):
            """Result of a validation scan."""

            validator_name: str
            files_scanned: int
            violations: Sequence[FlextTestsModels.Tests.Violation]
            passed: bool

            @classmethod
            def create(
                cls,
                validator_name: str,
                files_scanned: int,
                violations: Sequence[FlextTestsModels.Tests.Violation],
            ) -> FlextTestsModels.Tests.ScanResult:
                """Create a ScanResult from violations."""
                return cls(
                    validator_name=validator_name,
                    files_scanned=files_scanned,
                    violations=violations,
                    passed=not violations,
                )

        class OkParams(FlextModels.Value):
            """Matcher parameters for successful result assertions."""

            model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

            eq: Annotated[
                (
                    Mapping[str, t.Tests.Testobject]
                    | Sequence[t.Tests.Testobject]
                    | bytes
                    | str
                    | int
                    | float
                    | bool
                    | TypeAliasType
                    | None
                ),
                Field(
                    default=None,
                    description="Expected value (equality check)",
                    union_mode="left_to_right",
                ),
            ]
            ne: Annotated[
                (
                    Mapping[str, t.Tests.Testobject]
                    | Sequence[t.Tests.Testobject]
                    | bytes
                    | str
                    | int
                    | float
                    | bool
                    | TypeAliasType
                    | None
                ),
                Field(
                    default=None,
                    description="Value must not equal",
                    union_mode="left_to_right",
                ),
            ]
            is_: Annotated[
                type | tuple[type, ...] | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("is_", "is"),
                    description="Runtime type check",
                ),
            ]
            none: Annotated[bool | None, Field(default=None, description="None check")]
            empty: Annotated[
                bool | None,
                Field(default=None, description="Empty check"),
            ]
            gt: Annotated[
                float | int | None,
                Field(default=None, description="Greater than"),
            ]
            gte: Annotated[
                float | int | None,
                Field(default=None, description="Greater than or equal"),
            ]
            lt: Annotated[
                float | int | None,
                Field(default=None, description="Less than"),
            ]
            lte: Annotated[
                float | int | None,
                Field(default=None, description="Less than or equal"),
            ]
            has: Annotated[
                t.Tests.Matcher.ContainmentSpec | None,
                Field(default=None, description="Unified containment check"),
            ]
            lacks: Annotated[
                t.Tests.Matcher.ExclusionSpec | None,
                Field(default=None, description="Unified non-containment check"),
            ]
            starts: Annotated[
                str | None,
                Field(default=None, description="String starts with prefix"),
            ]
            ends: Annotated[
                str | None,
                Field(default=None, description="String ends with suffix"),
            ]
            match: Annotated[
                str | None,
                Field(default=None, description="Regex pattern"),
            ]
            len: Annotated[
                t.Tests.Matcher.LengthSpec | None,
                Field(default=None, description="Length spec"),
            ]
            deep: Annotated[
                t.Tests.Matcher.DeepSpec | None,
                Field(default=None, description="Deep structural matching"),
            ]
            path: Annotated[
                t.Tests.Matcher.PathSpec | None,
                Field(
                    default=None,
                    description="Extract nested value via dot notation",
                ),
            ]
            where: Annotated[
                t.Tests.Matcher.PredicateSpec | None,
                Field(default=None, description="Custom predicate function"),
            ]
            msg: Annotated[
                str | None,
                Field(default=None, description="Custom error message"),
            ]

        class FailParams(FlextModels.Value):
            """Matcher parameters for failure result assertions."""

            model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

            msg: Annotated[
                str | None,
                Field(default=None, description="Custom error message"),
            ]
            has: Annotated[
                t.Tests.Matcher.ExclusionSpec | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("has", "contains"),
                    description="Error contains substring(s)",
                ),
            ]
            lacks: Annotated[
                t.Tests.Matcher.ExclusionSpec | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("lacks", "excludes"),
                    description="Error does NOT contain substring(s)",
                ),
            ]
            starts: Annotated[
                str | None,
                Field(default=None, description="Error starts with prefix"),
            ]
            ends: Annotated[
                str | None,
                Field(default=None, description="Error ends with suffix"),
            ]
            match: Annotated[
                str | None,
                Field(default=None, description="Error matches regex"),
            ]
            code: Annotated[
                str | None,
                Field(default=None, description="Error code equals"),
            ]
            code_has: Annotated[
                t.Tests.Matcher.ErrorCodeSpec | None,
                Field(default=None, description="Error code contains substring(s)"),
            ]
            data: Annotated[
                t.Tests.Matcher.ErrorDataSpec | None,
                Field(default=None, description="Error data contains key-value pairs"),
            ]

        class ThatParams(FlextModels.Value):
            """Generic matcher parameters for value assertions."""

            model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

            msg: Annotated[
                str | None,
                Field(default=None, description="Custom error message"),
            ]
            eq: Annotated[
                t.Tests.Testobject | None,
                Field(default=None, description="Expected value (equality check)"),
            ]
            ne: Annotated[
                t.Tests.Testobject | None,
                Field(default=None, description="Value must not equal"),
            ]
            is_: Annotated[
                type | tuple[type, ...] | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("is_", "is"),
                    description="Runtime type check",
                ),
            ]
            not_: Annotated[
                type | tuple[type, ...] | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("not_", "not"),
                    description="Type check — value is NOT instance of type(s)",
                ),
            ]
            none: Annotated[bool | None, Field(default=None, description="None check")]
            empty: Annotated[
                bool | None,
                Field(default=None, description="Empty check"),
            ]
            gt: Annotated[
                float | int | None,
                Field(default=None, description="Greater than"),
            ]
            gte: Annotated[
                float | int | None,
                Field(default=None, description="Greater than or equal"),
            ]
            lt: Annotated[
                float | int | None,
                Field(default=None, description="Less than"),
            ]
            lte: Annotated[
                float | int | None,
                Field(default=None, description="Less than or equal"),
            ]
            len: Annotated[
                t.Tests.Matcher.LengthSpec | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("len", "length"),
                    description="Length spec",
                ),
            ]
            length_gt: Annotated[
                int | None,
                Field(default=None, description="Length greater than"),
            ]
            length_gte: Annotated[
                int | None,
                Field(default=None, description="Length greater than or equal"),
            ]
            length_lt: Annotated[
                int | None,
                Field(default=None, description="Length less than"),
            ]
            length_lte: Annotated[
                int | None,
                Field(default=None, description="Length less than or equal"),
            ]
            has: Annotated[
                t.Tests.Matcher.ContainmentSpec | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("has", "contains"),
                    description="Unified containment check",
                ),
            ]
            lacks: Annotated[
                t.Tests.Matcher.ExclusionSpec | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("lacks", "excludes"),
                    description="Unified non-containment check",
                ),
            ]
            starts: Annotated[
                str | None,
                Field(default=None, description="String starts with prefix"),
            ]
            ends: Annotated[
                str | None,
                Field(default=None, description="String ends with suffix"),
            ]
            match: Annotated[
                str | None,
                Field(default=None, description="Regex pattern"),
            ]
            first: Annotated[
                t.Tests.Testobject | None,
                Field(default=None, description="Sequence first item equals"),
            ]
            last: Annotated[
                t.Tests.Testobject | None,
                Field(default=None, description="Sequence last item equals"),
            ]
            all_: Annotated[
                t.Tests.Matcher.SequencePredicate | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("all_", "all"),
                    description="All items match type or predicate",
                ),
            ]
            any_: Annotated[
                t.Tests.Matcher.SequencePredicate | None,
                Field(
                    default=None,
                    validation_alias=AliasChoices("any_", "any"),
                    description="Each item matches type or predicate",
                ),
            ]
            sorted: Annotated[
                t.Tests.Matcher.SortKey | None,
                Field(default=None, description="Is sorted"),
            ]
            unique: Annotated[
                bool | None,
                Field(default=None, description="All items unique"),
            ]
            keys: Annotated[
                t.Tests.Matcher.KeySpec | None,
                Field(default=None, description="Mapping has all keys"),
            ]
            lacks_keys: Annotated[
                t.Tests.Matcher.KeySpec | None,
                Field(default=None, description="Mapping missing keys"),
            ]
            values: Annotated[
                Sequence[t.Tests.Testobject] | None,
                Field(default=None, description="Mapping has all values"),
            ]
            kv: Annotated[
                t.Tests.Matcher.KeyValueSpec | None,
                Field(default=None, description="Key-value pairs"),
            ]
            attrs: Annotated[
                t.Tests.Matcher.AttributeSpec | None,
                Field(default=None, description="Object has attribute(s)"),
            ]
            methods: Annotated[
                t.Tests.Matcher.AttributeSpec | None,
                Field(default=None, description="Object has method(s)"),
            ]
            attr_eq: Annotated[
                t.Tests.Matcher.AttributeValueSpec | None,
                Field(default=None, description="Attribute equals"),
            ]
            ok: Annotated[
                bool | None,
                Field(default=None, description="For r: assert success"),
            ]
            error: Annotated[
                str | t.StrSequence | None,
                Field(default=None, description="For r: error contains"),
            ]
            deep: Annotated[
                t.Tests.Matcher.DeepSpec | None,
                Field(default=None, description="Deep structural matching"),
            ]
            where: Annotated[
                t.Tests.Matcher.PredicateSpec | None,
                Field(default=None, description="Custom predicate function"),
            ]

            @model_validator(mode="after")
            def normalize_legacy_parameters(self) -> FlextTestsModels.Tests.ThatParams:
                updates: MutableMapping[str, t.Tests.Testobject] = {}
                if self.error is not None and self.has is None:
                    updates["has"] = self.error
                if self.len is None and any(
                    v is not None
                    for v in (
                        self.length_gt,
                        self.length_gte,
                        self.length_lt,
                        self.length_lte,
                    )
                ):
                    min_len = 0
                    max_len = sys.maxsize
                    if self.length_gt is not None:
                        min_len = self.length_gt + 1
                    if self.length_gte is not None:
                        min_len = max(min_len, self.length_gte)
                    if self.length_lt is not None:
                        max_len = self.length_lt - 1
                    if self.length_lte is not None:
                        max_len = min(max_len, self.length_lte)
                    updates["len"] = (min_len, max_len)
                if updates:
                    return self.model_copy(update=updates)
                return self

        class ScopeParams(FlextModels.Value):
            """Parameters for temporary test scope configuration."""

            model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

            config: Annotated[
                Mapping[str, t.Tests.Testobject] | None,
                Field(default=None, description="Initial configuration values"),
            ]
            container: Annotated[
                Mapping[str, t.Tests.Testobject] | None,
                Field(default=None, description="Initial container/service mappings"),
            ]
            context: Annotated[
                Mapping[str, t.Tests.Testobject] | None,
                Field(default=None, description="Initial context values"),
            ]
            cleanup: Annotated[
                t.Tests.Matcher.CleanupSpec | None,
                Field(default=None, description="Cleanup functions"),
            ]
            env: Annotated[
                t.Tests.Matcher.EnvironmentSpec | None,
                Field(default=None, description="Temporary environment variables"),
            ]
            cwd: Annotated[
                Path | str | None,
                Field(default=None, description="Temporary working directory"),
            ]

            @field_validator("cwd", mode="before")
            @classmethod
            def convert_cwd(cls, value: Path | str | None) -> Path | str | None:
                if isinstance(value, str):
                    return Path(value)
                return value

        class DeepMatchResult(FlextModels.Value):
            """Structured output for deep-match comparisons."""

            path: Annotated[
                str,
                Field(description="Path where match occurred or failed"),
            ]
            expected: Annotated[
                t.Tests.Matcher.ValueSpec,
                Field(description="Expected value or predicate"),
            ]
            actual: Annotated[
                t.Tests.Testobject | None,
                Field(default=None, description="Actual value found"),
            ]
            matched: Annotated[bool, Field(description="Whether match succeeded")]
            reason: Annotated[
                str,
                Field(default="", description="Reason for match failure"),
            ]

        class Validate:
            """Centralized TypeAdapters for test data validation.

            All TypeAdapters used across flext_tests modules are defined here.
            Access via m.Tests.Validate.* with flat aliases.
            """

            DICT_ADAPTER: ClassVar[
                TypeAdapter[Mapping[str, t.Tests.TestobjectSerializable]]
            ] = t.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER
            LIST_ADAPTER: ClassVar[
                TypeAdapter[Sequence[t.Tests.TestobjectSerializable]]
            ] = t.TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER

        class Chain[TResult](FlextModels.Value):
            """Container for chained result assertions."""

            result: Annotated[
                r[TResult] | p.Result[TResult],
                Field(description="r being chained"),
            ]

        class TestScope(FlextModels.ArbitraryTypesModel):
            """Scope container for test configuration and runtime state."""

            __test__ = False

            config: Annotated[
                Mapping[str, t.Tests.TestobjectSerializable],
                Field(description="Configuration dictionary"),
            ] = Field(default_factory=dict)
            container: Annotated[
                Mapping[str, t.Tests.TestobjectSerializable],
                Field(description="Container/service mappings"),
            ] = Field(default_factory=dict)
            context: Annotated[
                Mapping[str, t.Tests.TestobjectSerializable],
                Field(description="Context values"),
            ] = Field(default_factory=dict)


m = FlextTestsModels

__all__ = ["FlextTestsModels", "m"]

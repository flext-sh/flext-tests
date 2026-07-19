"""Filesystem, docker, and validator model protocols for flext_tests.

Protocol-of-model contracts (mirroring m.Tests.* models) consumed at runtime by
the file/docker/validator test service bases. Published under p.Tests.*.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from datetime import datetime
    from pathlib import Path

    from flext_infra import p
    from flext_tests import c, t


class FlextTestsFilesystemProtocolsMixin:
    """Filesystem, docker, and validator model protocols under p.Tests.*."""

    @runtime_checkable
    class ContentMeta(Protocol):
        """Metadata derived from parsed file content."""

        @property
        def key_count(self) -> int | None: ...

        @property
        def item_count(self) -> int | None: ...

        @property
        def row_count(self) -> int | None: ...

        @property
        def column_count(self) -> int | None: ...

        @property
        def model_valid(self) -> bool | None: ...

        @property
        def model_name(self) -> str | None: ...

    @runtime_checkable
    class CreateParams(Protocol):
        """Validated file-creation parameters."""

        @property
        def content(self) -> t.Tests.FileContentPlain: ...

        @property
        def name(self) -> t.NonEmptyStr: ...

        @property
        def directory(self) -> Path | None: ...

        @property
        def fmt(self) -> c.Tests.FileFormat: ...

        @property
        def enc(self) -> t.NonEmptyStr: ...

        @property
        def indent(self) -> t.NonNegativeInt: ...

        @property
        def delim(self) -> str: ...

        @property
        def headers(self) -> t.StrSequence | None: ...

        @property
        def readonly(self) -> bool: ...

        @property
        def extract_result(self) -> bool: ...

    @runtime_checkable
    class ReadParams(Protocol):
        """Validated file-reading parameters."""

        @property
        def path(self) -> Path: ...

        @property
        def model_cls(self) -> t.ModelClass[t.BaseModelType] | None: ...

        @property
        def fmt(self) -> c.Tests.FileFormat: ...

        @property
        def enc(self) -> t.NonEmptyStr: ...

        @property
        def delim(self) -> str: ...

        @property
        def has_headers(self) -> bool: ...

    @runtime_checkable
    class CompareParams(Protocol):
        """Validated file-comparison parameters."""

        @property
        def file1(self) -> Path: ...

        @property
        def file2(self) -> Path: ...

        @property
        def mode(self) -> str: ...

        @property
        def ignore_ws(self) -> bool: ...

        @property
        def ignore_case(self) -> bool: ...

        @property
        def pattern(self) -> str | None: ...

        @property
        def deep(self) -> bool: ...

        @property
        def keys(self) -> t.StrSequence | None: ...

        @property
        def exclude_keys(self) -> t.StrSequence | None: ...

    @runtime_checkable
    class InfoParams(Protocol):
        """Validated file-information parameters."""

        @property
        def path(self) -> Path: ...

        @property
        def compute_hash(self) -> bool: ...

        @property
        def detect_fmt(self) -> bool: ...

        @property
        def parse_content(self) -> bool: ...

        @property
        def validate_model(self) -> t.ModelClass[t.BaseModelType] | None: ...

    @runtime_checkable
    class AssertExistsParams(Protocol):
        """Filesystem existence assertion options."""

        @property
        def is_file(self) -> bool | None: ...

        @property
        def is_dir(self) -> bool | None: ...

        @property
        def not_empty(self) -> bool | None: ...

        @property
        def readable(self) -> bool | None: ...

        @property
        def writable(self) -> bool | None: ...

    @runtime_checkable
    class CreateKwargsParams(Protocol):
        """Optional keyword parameters for file creation."""

        @property
        def directory(self) -> Path | None: ...

        @property
        def fmt(self) -> c.Tests.FileFormat: ...

        @property
        def enc(self) -> t.NonEmptyStr: ...

        @property
        def indent(self) -> t.NonNegativeInt: ...

        @property
        def delim(self) -> str: ...

        @property
        def headers(self) -> t.StrSequence | None: ...

        @property
        def readonly(self) -> bool: ...

    @runtime_checkable
    class BatchParams(Protocol):
        """Validated batch file-operation parameters."""

        @property
        def files(
            self,
        ) -> (
            t.MappingKV[str, t.Tests.TestobjectSerializable]
            | t.SequenceOf[tuple[str, t.Tests.TestobjectSerializable]]
        ): ...

        @property
        def directory(self) -> Path | None: ...

        @property
        def operation(self) -> c.Tests.Operation: ...

        @property
        def model(self) -> t.ModelClass[t.BaseModelType] | None: ...

        @property
        def on_error(self) -> c.Tests.ErrorMode: ...

        @property
        def parallel(self) -> bool: ...

    @runtime_checkable
    class BatchResult(Protocol):
        """Summary of batch file operations."""

        @property
        def succeeded(self) -> int: ...

        @property
        def failed(self) -> t.NonNegativeInt: ...

        @property
        def total(self) -> t.NonNegativeInt: ...

        @property
        def results(
            self,
        ) -> t.MappingKV[str, p.ResultLike[t.Tests.TestResultValue]]: ...

        @property
        def errors(self) -> t.StrMapping: ...

        @property
        def failure_count(self) -> int: ...

        @property
        def success_count(self) -> int: ...

        @property
        def success_rate(self) -> float: ...

    # mro-qc84 (fix-forward): protocol-of-model for a single validator finding
    # (m.Tests.Violation). Consumed by ScanResult.violations.
    @runtime_checkable
    class Violation(Protocol):
        """Single validator violation record."""

        @property
        def file_path(self) -> Path: ...

        @property
        def line_number(self) -> int: ...

        @property
        def rule_id(self) -> str: ...

        @property
        def severity(self) -> str: ...

        @property
        def description(self) -> str: ...

        @property
        def code_snippet(self) -> str: ...

    # mro-qc84 (fix-forward): protocol-of-model for a validator scan outcome
    # (m.Tests.ScanResult). Consumed at runtime by s[p.Tests.ScanResult].
    @runtime_checkable
    class ScanResult(Protocol):
        """Aggregate validator scan result."""

        @property
        def validator_name(self) -> str: ...

        @property
        def files_scanned(self) -> int: ...

        @property
        def violations(
            self,
        ) -> t.SequenceOf[FlextTestsFilesystemProtocolsMixin.Violation]: ...

        @property
        def passed(self) -> bool: ...

    # mro-qc84 (fix-forward): protocol-of-model for a docker container snapshot
    # (m.Tests.ContainerInfo). Consumed at runtime by s[p.Tests.ContainerInfo].
    @runtime_checkable
    class ContainerInfo(Protocol):
        """Materialized docker container state."""

        @property
        def name(self) -> str: ...

        @property
        def status(self) -> str: ...

        @property
        def ports(self) -> t.StrMapping: ...

        @property
        def image(self) -> str: ...

        @property
        def container_id(self) -> str: ...

    # mro-qc84 (fix-forward): protocol-of-model for a probed file snapshot
    # (m.Tests.FileInfo). Consumed at runtime by the file test helper ClassVar.
    @runtime_checkable
    class FileInfo(Protocol):
        """Materialized filesystem probe result for one file."""

        @property
        def exists(self) -> bool: ...

        @property
        def path(self) -> Path | None: ...

        @property
        def size(self) -> int: ...

        @property
        def size_human(self) -> str: ...

        @property
        def lines(self) -> int: ...

        @property
        def encoding(self) -> str: ...

        @property
        def is_empty(self) -> bool: ...

        @property
        def first_line(self) -> str: ...

        @property
        def fmt(self) -> str: ...

        @property
        def valid(self) -> bool: ...

        @property
        def created(self) -> datetime | None: ...

        @property
        def modified(self) -> datetime | None: ...

        @property
        def permissions(self) -> int: ...

        @property
        def is_readonly(self) -> bool: ...

        @property
        def sha256(self) -> str | None: ...


__all__: list[str] = ["FlextTestsFilesystemProtocolsMixin"]

"""Filesystem, docker, and validator model protocols for flext_tests.

Protocol-of-model contracts (mirroring m.Tests.* models) consumed at runtime by
the file/docker/validator test service bases. Published under p.Tests.*.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Protocol, runtime_checkable

from flext_infra import p
from flext_tests import t


class FlextTestsFilesystemProtocolsMixin:
    """Filesystem, docker, and validator model protocols under p.Tests.*."""

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
        def violations(self) -> t.SequenceOf[p.Tests.Violation]: ...

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

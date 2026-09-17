"""File management constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Inherits all canonical file-format constants from ``FlextCliConstantsFiles``
(SSOT in ``flext-cli``) and adds only test-specific constants that have no
production counterpart.
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_cli.constants import FlextCliConstantsFiles
from flext_infra import c as infra_c


class FlextTestsConstantsFiles(FlextCliConstantsFiles):
    """File management constants mixin for test infrastructure.

    Inherits all shared file-format constants from ``FlextCliConstantsFiles``
    and adds test-only constants (comparison modes, permissions, error
    message templates).
    """

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

    # ── Test-specific file constants ────────────────────────────

    DEFAULT_ENCODING: Final[str] = infra_c.DEFAULT_ENCODING
    DEFAULT_BINARY_ENCODING: Final[str] = "binary"
    PERMISSION_READONLY_FILE: Final[int] = 292
    PERMISSION_WRITABLE_FILE: Final[int] = 420
    PERMISSION_WRITABLE_DIR: Final[int] = 493
    HASH_CHUNK_SIZE: Final[int] = 8192
    ERROR_FILE_NOT_FOUND: Final[str] = "File not found: {path}"
    ERROR_INVALID_JSON: Final[str] = "Invalid JSON: {error}"
    ERROR_INVALID_YAML: Final[str] = "Invalid YAML: {error}"
    ERROR_ENCODING: Final[str] = "Encoding error: {error}"
    ERROR_READ: Final[str] = "Read error: {error}"
    ERROR_COMPARE: Final[str] = "Compare error: {error}"
    ERROR_INFO: Final[str] = "Info error: {error}"


__all__: list[str] = ["FlextTestsConstantsFiles"]

"""File management constants for flext_tests.

Declares only test-specific constants that have no production counterpart;
shared file constants resolve through the FlextCliConstants MRO (SSOT in
``flext-cli``).

Copyright (c) 2025 FLEXT Team. All rights reserved.
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

from enum import StrEnum, unique
from typing import ClassVar

from flext_cli import c


class FlextTestsConstantsFiles:
    """File management constants mixin for test infrastructure.

    Adds test-only constants (comparison modes, permissions, error message
    templates); shared file-format constants come from the upstream MRO.
    """

    @unique
    class CompareMode(StrEnum):
        """File comparison mode enumeration."""

        CONTENT = "content"
        SIZE = "size"
        HASH = "hash"
        LINES = "lines"

    # ── Test-specific file constants ────────────────────────────

    DEFAULT_ENCODING: ClassVar[str] = c.DEFAULT_ENCODING
    DEFAULT_BINARY_ENCODING: ClassVar[str] = "binary"
    PERMISSION_READONLY_FILE: ClassVar[int] = 292
    PERMISSION_WRITABLE_FILE: ClassVar[int] = 420
    PERMISSION_WRITABLE_DIR: ClassVar[int] = 493
    HASH_CHUNK_SIZE: ClassVar[int] = 8192
    FIXTURE_TREES_INI: ClassVar[str] = "flext_fixture_trees_root"
    """Ini key the fixture-tree plugin registers for the scenario (ADR-028 point 9)."""
    ERROR_FILE_NOT_FOUND: ClassVar[str] = "File not found: {path}"
    ERROR_INVALID_JSON: ClassVar[str] = "Invalid JSON: {error}"
    ERROR_INVALID_YAML: ClassVar[str] = "Invalid YAML: {error}"
    ERROR_ENCODING: ClassVar[str] = "Encoding error: {error}"
    ERROR_READ: ClassVar[str] = "Read error: {error}"
    ERROR_COMPARE: ClassVar[str] = "Compare error: {error}"
    ERROR_INFO: ClassVar[str] = "Info error: {error}"


__all__: list[str] = ["FlextTestsConstantsFiles"]

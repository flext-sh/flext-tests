"""File comparison utilities for flext-tests — re-exported from _comparison_parts.

This module previously held a monolithic 217-line ``FlextTestsFilesComparisonMixin``
that duplicated the parsing helpers already present in
``_comparison_parts/comparison_part_01`` and also contained 5 methods that had
not yet been moved to a part file. Those 5 methods now live in
``comparison_part_02`` (which extends the part-01 mixin). The modular chain is
the canonical owner; this shim preserves the import path used by
``_files/__init__.py`` while eliminating 217 lines of duplicated code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from ._comparison_parts import FlextTestsFilesComparisonMixin

__all__: list[str] = ["FlextTestsFilesComparisonMixin"]

"""Type-usage validator for flext-tests — re-exported from _types_parts.

This module previously held a monolithic 297-line ``FlextValidatorTypes``
that duplicated the content of the modular ``_types_parts/`` split
(``types_part_01`` + ``types_part_02``). The modular chain is the canonical
owner; this shim preserves the import path used by ``_validator/__init__.py``
while eliminating the duplicated 297 lines.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from ._types_parts import FlextValidatorTypes

__all__: list[str] = ["FlextValidatorTypes"]

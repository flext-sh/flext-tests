"""Extracted facade class for files.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests._utilities._files import (
    FlextTestsUtilitiesFiles,
    FlextTestsUtilitiesFilesInfo,
)


class FlextTestsUtilitiesFiles(
    FlextTestsUtilitiesFiles,
    FlextTestsUtilitiesFilesInfo,
):
    """Facade for files."""


__all__: list[str] = ["FlextTestsUtilitiesFiles"]

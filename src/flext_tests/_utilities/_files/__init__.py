# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Files package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import defer_lazy_bases, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._files.assertions import (
        FlextTestsUtilitiesFilesAssertions,
    )
    from flext_tests._utilities._files.comparison import (
        FlextTestsUtilitiesFilesComparison,
    )
    from flext_tests._utilities._files.contexts import FlextTestsUtilitiesFilesContexts
    from flext_tests._utilities._files.creation import FlextTestsUtilitiesFilesCreation
    from flext_tests._utilities._files.info import FlextTestsUtilitiesFilesInfo
    from flext_tests._utilities._files.lifecycle import (
        FlextTestsUtilitiesFilesLifecycle,
    )
    from flext_tests._utilities._files.reading import FlextTestsUtilitiesFilesReading
    from flext_tests._utilities._files.size import FlextTestsUtilitiesFilesSize


__all__: tuple[str, ...] = (
    "FlextTestsUtilitiesFilesAssertions",
    "FlextTestsUtilitiesFilesComparison",
    "FlextTestsUtilitiesFilesContexts",
    "FlextTestsUtilitiesFilesCreation",
    "FlextTestsUtilitiesFilesInfo",
    "FlextTestsUtilitiesFilesLifecycle",
    "FlextTestsUtilitiesFilesReading",
    "FlextTestsUtilitiesFilesSize",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTestsUtilitiesFilesAssertions": ".assertions",
        "FlextTestsUtilitiesFilesComparison": ".comparison",
        "FlextTestsUtilitiesFilesContexts": ".contexts",
        "FlextTestsUtilitiesFilesCreation": ".creation",
        "FlextTestsUtilitiesFilesInfo": ".info",
        "FlextTestsUtilitiesFilesLifecycle": ".lifecycle",
        "FlextTestsUtilitiesFilesReading": ".reading",
        "FlextTestsUtilitiesFilesSize": ".size",
    },
    public_exports=__all__,
    deferred_members={
        "FlextTestsUtilitiesFilesAssertions": ("assert_exists",),
        "FlextTestsUtilitiesFilesContexts": (
            "files",
            "temporary_directory",
        ),
        "FlextTestsUtilitiesFilesCreation": (
            "matches_native_mapping",
            "to_payload_mapping",
            "_to_string_rows",
            "_coerce_file_content",
            "_extract_content",
            "_is_nested_rows",
            "_write_content_by_format",
            "_build_json_payload",
            "_build_csv_rows",
            "CreateOptions",
            "create",
        ),
        "FlextTestsUtilitiesFilesInfo": (
            "info",
            "_build_file_info",
            "_read_info_text",
            "_parse_content_metadata",
        ),
        "FlextTestsUtilitiesFilesLifecycle": (
            "_create_file_manager",
            "created_dirs",
            "created_files",
            "cleanup",
            "_resolve_directory",
        ),
        "FlextTestsUtilitiesFilesReading": (
            "ReadOptions",
            "_validate_model_content",
            "_read_fail",
            "read",
            "_read_content_by_format",
        ),
        "FlextTestsUtilitiesFilesSize": ("format_size",),
    },
)

defer_lazy_bases(
    __name__,
    {
        "FlextTestsUtilitiesFilesAssertions": (
            (".", "FlextTestsUtilitiesFilesContexts"),
        ),
        "FlextTestsUtilitiesFilesContexts": ((".", "FlextTestsUtilitiesFilesReading"),),
        "FlextTestsUtilitiesFilesCreation": (
            (".", "FlextTestsUtilitiesFilesLifecycle"),
        ),
        "FlextTestsUtilitiesFilesInfo": ((".", "FlextTestsUtilitiesFilesAssertions"),),
        "FlextTestsUtilitiesFilesReading": ((".", "FlextTestsUtilitiesFilesCreation"),),
    },
)

# AUTO-GENERATED FILE — Regenerate with: make gen
"""Files package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests._utilities._files._assertions import FlextTestsFilesAssertionsMixin
    from flext_tests._utilities._files._batch import FlextTestsFilesBatchMixin
    from flext_tests._utilities._files._comparison_parts.comparison_part_02 import (
        FlextTestsFilesComparisonMixin,
    )
    from flext_tests._utilities._files._contexts import FlextTestsFilesContextsMixin
    from flext_tests._utilities._files._creation_parts.creation_part_03 import (
        FlextTestsFilesCreationMixin,
    )
    from flext_tests._utilities._files._info import FlextTestsFilesInfoMixin
    from flext_tests._utilities._files._lifecycle import FlextTestsFilesLifecycleMixin
    from flext_tests._utilities._files._reading import FlextTestsFilesReadingMixin
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._comparison_parts",
        "._creation_parts",
    ),
    build_lazy_import_map(
        {
            "._assertions": ("FlextTestsFilesAssertionsMixin",),
            "._batch": ("FlextTestsFilesBatchMixin",),
            "._comparison_parts": ("_comparison_parts",),
            "._comparison_parts.comparison_part_02": (
                "FlextTestsFilesComparisonMixin",
            ),
            "._contexts": ("FlextTestsFilesContextsMixin",),
            "._creation_parts": ("_creation_parts",),
            "._creation_parts.creation_part_03": ("FlextTestsFilesCreationMixin",),
            "._info": ("FlextTestsFilesInfoMixin",),
            "._lifecycle": ("FlextTestsFilesLifecycleMixin",),
            "._reading": ("FlextTestsFilesReadingMixin",),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)

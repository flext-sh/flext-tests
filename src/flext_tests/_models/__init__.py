# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests._models._filesystem_parts.filesystem_part_02 import (
        FlextTestsFilesystemModelsMixin,
    )
    from flext_tests._models._matchers_parts.matchers_part_03 import (
        FlextTestsMatchersModelsMixin,
    )
    from flext_tests._models.base import FlextTestsBaseModelsMixin
    from flext_tests._models.batch import FlextTestsBatchModelsMixin
    from flext_tests._models.docker import FlextTestsDockerModelsMixin
    from flext_tests._models.domains import FlextTestsDomainModelsMixin
    from flext_tests._models.make import FlextTestsMakeModelsMixin
    from flext_tests._models.validator import FlextTestsValidatorModelsMixin
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._filesystem_parts",
        "._matchers_parts",
    ),
    build_lazy_import_map(
        {
            "._filesystem_parts": ("_filesystem_parts",),
            "._filesystem_parts.filesystem_part_02": (
                "FlextTestsFilesystemModelsMixin",
            ),
            "._matchers_parts": ("_matchers_parts",),
            "._matchers_parts.matchers_part_03": ("FlextTestsMatchersModelsMixin",),
            ".base": ("FlextTestsBaseModelsMixin",),
            ".batch": ("FlextTestsBatchModelsMixin",),
            ".docker": ("FlextTestsDockerModelsMixin",),
            ".domains": ("FlextTestsDomainModelsMixin",),
            ".make": ("FlextTestsMakeModelsMixin",),
            ".validator": ("FlextTestsValidatorModelsMixin",),
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

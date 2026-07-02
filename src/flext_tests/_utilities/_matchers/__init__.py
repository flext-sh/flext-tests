# AUTO-GENERATED FILE — Regenerate with: make gen
"""Matchers package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests._utilities._matchers._assertions import (
        FlextTestsMatchersAssertionsMixin as FlextTestsMatchersAssertionsMixin,
    )
    from flext_tests._utilities._matchers._containment import (
        FlextTestsMatchersContainmentMixin as FlextTestsMatchersContainmentMixin,
    )
    from flext_tests._utilities._matchers._result_parts.result_part_03 import (
        FlextTestsMatchersResultMixin as FlextTestsMatchersResultMixin,
    )
    from flext_tests._utilities._matchers._scope import (
        FlextTestsMatchersScopeMixin as FlextTestsMatchersScopeMixin,
    )
    from flext_tests._utilities._matchers._that_parts.that_part_06 import (
        FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixin,
    )
    from flext_tests._utilities._matchers._typeguards import (
        FlextTestsMatchersTypeGuardsMixin as FlextTestsMatchersTypeGuardsMixin,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._result_parts",
        "._that_parts",
    ),
    build_lazy_import_map(
        {
            "._assertions": ("FlextTestsMatchersAssertionsMixin",),
            "._containment": ("FlextTestsMatchersContainmentMixin",),
            "._result_parts": ("_result_parts",),
            "._result_parts.result_part_03": ("FlextTestsMatchersResultMixin",),
            "._scope": ("FlextTestsMatchersScopeMixin",),
            "._that_parts": ("_that_parts",),
            "._that_parts.that_part_06": ("FlextTestsMatchersThatMixin",),
            "._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
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

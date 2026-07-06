# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

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
    from flext_tests._utilities._make_parts.make_contract_part_02 import (
        FlextTestsMakeContractUtilitiesMixin,
    )
    from flext_tests._utilities._make_parts.make_parsing_part_02 import (
        FlextTestsMakeParsingUtilitiesMixin,
    )
    from flext_tests._utilities._make_parts.make_registry_part_03 import (
        FlextTestsMakeRegistryUtilitiesMixin,
    )
    from flext_tests._utilities._make_parts.make_rendering_part_02 import (
        FlextTestsMakeRenderingUtilitiesMixin,
    )
    from flext_tests._utilities._matchers._assertions import (
        FlextTestsMatchersAssertionsMixin,
    )
    from flext_tests._utilities._matchers._containment import (
        FlextTestsMatchersContainmentMixin,
    )
    from flext_tests._utilities._matchers._result_parts.result_part_03 import (
        FlextTestsMatchersResultMixin,
    )
    from flext_tests._utilities._matchers._scope import FlextTestsMatchersScopeMixin
    from flext_tests._utilities._matchers._that_parts.that_part_06 import (
        FlextTestsMatchersThatMixin,
    )
    from flext_tests._utilities._matchers._typeguards import (
        FlextTestsMatchersTypeGuardsMixin,
    )
    from flext_tests._utilities.container import (
        FlextTestsContainerHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.files import FlextTestsFilesUtilitiesMixin
    from flext_tests._utilities.fixtures_dsl import FlextTestsFixturesDSLMixin
    from flext_tests._utilities.generic import FlextTestsGenericHelpersUtilitiesMixin
    from flext_tests._utilities.handler import FlextTestsHandlerHelpersUtilitiesMixin
    from flext_tests._utilities.make import FlextTestsMakeUtilitiesMixin
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities
    from flext_tests._utilities.payload import FlextTestsPayloadUtilities
    from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin
    from flext_tests._utilities.settings import FlextTestsConfigHelpersUtilitiesMixin
    from flext_tests._utilities.testcontext import FlextTestsTestContextUtilitiesMixin
    from flext_tests._utilities.validator import FlextTestsValidatorUtilitiesMixin
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._files",
        "._make_parts",
        "._matchers",
    ),
    build_lazy_import_map(
        {
            "._files": ("_files",),
            "._files._assertions": ("FlextTestsFilesAssertionsMixin",),
            "._files._batch": ("FlextTestsFilesBatchMixin",),
            "._files._comparison_parts.comparison_part_02": (
                "FlextTestsFilesComparisonMixin",
            ),
            "._files._contexts": ("FlextTestsFilesContextsMixin",),
            "._files._creation_parts.creation_part_03": (
                "FlextTestsFilesCreationMixin",
            ),
            "._files._info": ("FlextTestsFilesInfoMixin",),
            "._files._lifecycle": ("FlextTestsFilesLifecycleMixin",),
            "._files._reading": ("FlextTestsFilesReadingMixin",),
            "._make_parts": ("_make_parts",),
            "._make_parts.make_contract_part_02": (
                "FlextTestsMakeContractUtilitiesMixin",
            ),
            "._make_parts.make_parsing_part_02": (
                "FlextTestsMakeParsingUtilitiesMixin",
            ),
            "._make_parts.make_registry_part_03": (
                "FlextTestsMakeRegistryUtilitiesMixin",
            ),
            "._make_parts.make_rendering_part_02": (
                "FlextTestsMakeRenderingUtilitiesMixin",
            ),
            "._matchers": ("_matchers",),
            "._matchers._assertions": ("FlextTestsMatchersAssertionsMixin",),
            "._matchers._containment": ("FlextTestsMatchersContainmentMixin",),
            "._matchers._result_parts.result_part_03": (
                "FlextTestsMatchersResultMixin",
            ),
            "._matchers._scope": ("FlextTestsMatchersScopeMixin",),
            "._matchers._that_parts.that_part_06": ("FlextTestsMatchersThatMixin",),
            "._matchers._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
            ".container": ("FlextTestsContainerHelpersUtilitiesMixin",),
            ".files": ("FlextTestsFilesUtilitiesMixin",),
            ".fixtures_dsl": ("FlextTestsFixturesDSLMixin",),
            ".generic": ("FlextTestsGenericHelpersUtilitiesMixin",),
            ".handler": ("FlextTestsHandlerHelpersUtilitiesMixin",),
            ".make": ("FlextTestsMakeUtilitiesMixin",),
            ".matchers": (
                "FlextTestsMatchersUtilities",
                "tm",
            ),
            ".payload": ("FlextTestsPayloadUtilities",),
            ".result": ("FlextTestsResultUtilitiesMixin",),
            ".settings": ("FlextTestsConfigHelpersUtilitiesMixin",),
            ".testcontext": ("FlextTestsTestContextUtilitiesMixin",),
            ".validator": ("FlextTestsValidatorUtilitiesMixin",),
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

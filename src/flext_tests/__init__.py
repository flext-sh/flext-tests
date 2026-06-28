# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_tests.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _t.TYPE_CHECKING:
    from flext_core import d as d, e as e, h as h, r as r, x as x
    from flext_tests._constants.data_cases import (
        FlextTestsConstantsDataCases as FlextTestsConstantsDataCases,
    )
    from flext_tests._constants.docker import (
        FlextTestsConstantsDocker as FlextTestsConstantsDocker,
    )
    from flext_tests._constants.files import (
        FlextTestsConstantsFiles as FlextTestsConstantsFiles,
    )
    from flext_tests._constants.make import (
        FlextTestsConstantsMake as FlextTestsConstantsMake,
    )
    from flext_tests._constants.matcher import (
        FlextTestsConstantsMatcher as FlextTestsConstantsMatcher,
    )
    from flext_tests._constants.validator import (
        FlextTestsConstantsValidator as FlextTestsConstantsValidator,
    )
    from flext_tests._fixtures.enforcement import (
        EnforcementCollector as EnforcementCollector,
        EnforcementItem as EnforcementItem,
        EnforcementViolationError as EnforcementViolationError,
    )
    from flext_tests._fixtures.markdown_validation import (
        MarkdownCodeBlockCollector as MarkdownCodeBlockCollector,
        MarkdownCodeBlockItem as MarkdownCodeBlockItem,
        MarkdownValidationError as MarkdownValidationError,
    )
    from flext_tests._fixtures.project_metadata import (
        project_metadata as project_metadata,
        project_namespace_config as project_namespace_config,
        project_tool_flext as project_tool_flext,
    )
    from flext_tests._fixtures.settings import (
        clean_container as clean_container,
        reset_settings as reset_settings,
        sample_data as sample_data,
        settings as settings,
        settings_factory as settings_factory,
        temp_dir as temp_dir,
        temp_file as temp_file,
        test_context as test_context,
        test_runtime as test_runtime,
    )
    from flext_tests._models.base import (
        FlextTestsBaseModelsMixin as FlextTestsBaseModelsMixin,
    )
    from flext_tests._models.batch import (
        FlextTestsBatchModelsMixin as FlextTestsBatchModelsMixin,
    )
    from flext_tests._models.docker import (
        FlextTestsDockerModelsMixin as FlextTestsDockerModelsMixin,
    )
    from flext_tests._models.domains import (
        FlextTestsDomainModelsMixin as FlextTestsDomainModelsMixin,
    )
    from flext_tests._models.filesystem import (
        FlextTestsFilesystemModelsMixin as FlextTestsFilesystemModelsMixin,
    )
    from flext_tests._models.make import (
        FlextTestsMakeModelsMixin as FlextTestsMakeModelsMixin,
    )
    from flext_tests._models.matchers import (
        FlextTestsMatchersModelsMixin as FlextTestsMatchersModelsMixin,
    )
    from flext_tests._models.validator import (
        FlextTestsValidatorModelsMixin as FlextTestsValidatorModelsMixin,
    )
    from flext_tests._protocols.valuefactory import (
        FlextTestsValueFactoryProtocolsMixin as FlextTestsValueFactoryProtocolsMixin,
    )
    from flext_tests._typings.base import (
        FlextTestsBaseTypesMixin as FlextTestsBaseTypesMixin,
    )
    from flext_tests._typings.files import (
        FlextTestsFilesTypesMixin as FlextTestsFilesTypesMixin,
    )
    from flext_tests._typings.guards import (
        FlextTestsGuardsTypesMixin as FlextTestsGuardsTypesMixin,
    )
    from flext_tests._typings.make import (
        FlextTestsMakeTypesMixin as FlextTestsMakeTypesMixin,
    )
    from flext_tests._typings.matchers import (
        FlextTestsMatchersTypesMixin as FlextTestsMatchersTypesMixin,
    )
    from flext_tests._utilities._files._assertions import (
        FlextTestsFilesAssertionsMixin as FlextTestsFilesAssertionsMixin,
    )
    from flext_tests._utilities._files._batch import (
        FlextTestsFilesBatchMixin as FlextTestsFilesBatchMixin,
    )
    from flext_tests._utilities._files._comparison import (
        FlextTestsFilesComparisonMixin as FlextTestsFilesComparisonMixin,
    )
    from flext_tests._utilities._files._contexts import (
        FlextTestsFilesContextsMixin as FlextTestsFilesContextsMixin,
    )
    from flext_tests._utilities._files._creation import (
        FlextTestsFilesCreationMixin as FlextTestsFilesCreationMixin,
    )
    from flext_tests._utilities._files._info import (
        FlextTestsFilesInfoMixin as FlextTestsFilesInfoMixin,
    )
    from flext_tests._utilities._files._lifecycle import (
        FlextTestsFilesLifecycleMixin as FlextTestsFilesLifecycleMixin,
    )
    from flext_tests._utilities._files._reading import (
        FlextTestsFilesReadingMixin as FlextTestsFilesReadingMixin,
    )
    from flext_tests._utilities._matchers._assertions import (
        FlextTestsMatchersAssertionsMixin as FlextTestsMatchersAssertionsMixin,
    )
    from flext_tests._utilities._matchers._containment import (
        FlextTestsMatchersContainmentMixin as FlextTestsMatchersContainmentMixin,
    )
    from flext_tests._utilities._matchers._result import (
        FlextTestsMatchersResultMixin as FlextTestsMatchersResultMixin,
    )
    from flext_tests._utilities._matchers._rules import (
        FlextTestsMatchersRulesMixin as FlextTestsMatchersRulesMixin,
    )
    from flext_tests._utilities._matchers._scope import (
        FlextTestsMatchersScopeMixin as FlextTestsMatchersScopeMixin,
    )
    from flext_tests._utilities._matchers._that import (
        FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixin,
    )
    from flext_tests._utilities._matchers._typeguards import (
        FlextTestsMatchersTypeGuardsMixin as FlextTestsMatchersTypeGuardsMixin,
    )
    from flext_tests._utilities.container import (
        FlextTestsContainerHelpersUtilitiesMixin as FlextTestsContainerHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.files import (
        FlextTestsFilesUtilitiesMixin as FlextTestsFilesUtilitiesMixin,
    )
    from flext_tests._utilities.fixtures_dsl import (
        FlextTestsFixturesDSLMixin as FlextTestsFixturesDSLMixin,
    )
    from flext_tests._utilities.generic import (
        FlextTestsGenericHelpersUtilitiesMixin as FlextTestsGenericHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.handler import (
        FlextTestsHandlerHelpersUtilitiesMixin as FlextTestsHandlerHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.make import (
        FlextTestsMakeUtilitiesMixin as FlextTestsMakeUtilitiesMixin,
    )
    from flext_tests._utilities.make_contract import (
        FlextTestsMakeContractUtilitiesMixin as FlextTestsMakeContractUtilitiesMixin,
    )
    from flext_tests._utilities.make_parsing import (
        FlextTestsMakeParsingUtilitiesMixin as FlextTestsMakeParsingUtilitiesMixin,
    )
    from flext_tests._utilities.make_registry import (
        FlextTestsMakeRegistryUtilitiesMixin as FlextTestsMakeRegistryUtilitiesMixin,
    )
    from flext_tests._utilities.make_rendering import (
        FlextTestsMakeRenderingUtilitiesMixin as FlextTestsMakeRenderingUtilitiesMixin,
    )
    from flext_tests._utilities.matchers import (
        FlextTestsMatchersUtilities as FlextTestsMatchersUtilities,
        tm as tm,
    )
    from flext_tests._utilities.payload import (
        FlextTestsPayloadUtilities as FlextTestsPayloadUtilities,
    )
    from flext_tests._utilities.result import (
        FlextTestsResultUtilitiesMixin as FlextTestsResultUtilitiesMixin,
    )
    from flext_tests._utilities.settings import (
        FlextTestsConfigHelpersUtilitiesMixin as FlextTestsConfigHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.testcontext import (
        FlextTestsTestContextUtilitiesMixin as FlextTestsTestContextUtilitiesMixin,
    )
    from flext_tests._utilities.validator import (
        FlextTestsValidatorUtilitiesMixin as FlextTestsValidatorUtilitiesMixin,
    )
    from flext_tests._validator.bypass import (
        FlextValidatorBypass as FlextValidatorBypass,
    )
    from flext_tests._validator.imports import (
        FlextValidatorImports as FlextValidatorImports,
    )
    from flext_tests._validator.layer import FlextValidatorLayer as FlextValidatorLayer
    from flext_tests._validator.markdown import (
        FlextValidatorMarkdown as FlextValidatorMarkdown,
    )
    from flext_tests._validator.models import (
        FlextTestsValidatorModels as FlextTestsValidatorModels,
    )
    from flext_tests._validator.settings import (
        FlextValidatorSettings as FlextValidatorSettings,
    )
    from flext_tests._validator.tests import FlextValidatorTests as FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes as FlextValidatorTypes
    from flext_tests.base import (
        FlextService as FlextService,
        FlextTestsCase as FlextTestsCase,
        FlextTestsServiceBase as FlextTestsServiceBase,
        s as s,
    )
    from flext_tests.constants import FlextTestsConstants as FlextTestsConstants, c as c
    from flext_tests.docker import FlextTestsDocker as FlextTestsDocker, tk as tk
    from flext_tests.domains import FlextTestsDomains as FlextTestsDomains, td as td
    from flext_tests.files import FlextTestsFiles as FlextTestsFiles, tf as tf
    from flext_tests.models import FlextTestsModels as FlextTestsModels, m as m
    from flext_tests.protocols import FlextTestsProtocols as FlextTestsProtocols, p as p
    from flext_tests.settings import FlextTestsSettings as FlextTestsSettings
    from flext_tests.typings import FlextTestsTypes as FlextTestsTypes, t as t
    from flext_tests.utilities import FlextTestsUtilities as FlextTestsUtilities, u as u
    from flext_tests.validator import (
        FlextTestsValidator as FlextTestsValidator,
        tv as tv,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._constants",
        "._models",
        "._protocols",
        "._typings",
        "._utilities",
        "._validator",
    ),
    build_lazy_import_map(
        {
            "._constants.data_cases": ("FlextTestsConstantsDataCases",),
            "._constants.docker": ("FlextTestsConstantsDocker",),
            "._constants.files": ("FlextTestsConstantsFiles",),
            "._constants.make": ("FlextTestsConstantsMake",),
            "._constants.matcher": ("FlextTestsConstantsMatcher",),
            "._constants.validator": ("FlextTestsConstantsValidator",),
            "._fixtures.enforcement": (
                "EnforcementCollector",
                "EnforcementItem",
                "EnforcementViolationError",
            ),
            "._fixtures.markdown_validation": (
                "MarkdownCodeBlockCollector",
                "MarkdownCodeBlockItem",
                "MarkdownValidationError",
            ),
            "._fixtures.project_metadata": (
                "project_metadata",
                "project_namespace_config",
                "project_tool_flext",
            ),
            "._fixtures.settings": (
                "clean_container",
                "reset_settings",
                "sample_data",
                "settings",
                "settings_factory",
                "temp_dir",
                "temp_file",
                "test_context",
                "test_runtime",
            ),
            "._models.base": ("FlextTestsBaseModelsMixin",),
            "._models.batch": ("FlextTestsBatchModelsMixin",),
            "._models.docker": ("FlextTestsDockerModelsMixin",),
            "._models.domains": ("FlextTestsDomainModelsMixin",),
            "._models.filesystem": ("FlextTestsFilesystemModelsMixin",),
            "._models.make": ("FlextTestsMakeModelsMixin",),
            "._models.matchers": ("FlextTestsMatchersModelsMixin",),
            "._models.validator": ("FlextTestsValidatorModelsMixin",),
            "._protocols.valuefactory": ("FlextTestsValueFactoryProtocolsMixin",),
            "._typings.base": ("FlextTestsBaseTypesMixin",),
            "._typings.files": ("FlextTestsFilesTypesMixin",),
            "._typings.guards": ("FlextTestsGuardsTypesMixin",),
            "._typings.make": ("FlextTestsMakeTypesMixin",),
            "._typings.matchers": ("FlextTestsMatchersTypesMixin",),
            "._utilities._files._assertions": ("FlextTestsFilesAssertionsMixin",),
            "._utilities._files._batch": ("FlextTestsFilesBatchMixin",),
            "._utilities._files._comparison": ("FlextTestsFilesComparisonMixin",),
            "._utilities._files._contexts": ("FlextTestsFilesContextsMixin",),
            "._utilities._files._creation": ("FlextTestsFilesCreationMixin",),
            "._utilities._files._info": ("FlextTestsFilesInfoMixin",),
            "._utilities._files._lifecycle": ("FlextTestsFilesLifecycleMixin",),
            "._utilities._files._reading": ("FlextTestsFilesReadingMixin",),
            "._utilities._matchers._assertions": ("FlextTestsMatchersAssertionsMixin",),
            "._utilities._matchers._containment": (
                "FlextTestsMatchersContainmentMixin",
            ),
            "._utilities._matchers._result": ("FlextTestsMatchersResultMixin",),
            "._utilities._matchers._rules": ("FlextTestsMatchersRulesMixin",),
            "._utilities._matchers._scope": ("FlextTestsMatchersScopeMixin",),
            "._utilities._matchers._that": ("FlextTestsMatchersThatMixin",),
            "._utilities._matchers._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
            "._utilities.container": ("FlextTestsContainerHelpersUtilitiesMixin",),
            "._utilities.files": ("FlextTestsFilesUtilitiesMixin",),
            "._utilities.fixtures_dsl": ("FlextTestsFixturesDSLMixin",),
            "._utilities.generic": ("FlextTestsGenericHelpersUtilitiesMixin",),
            "._utilities.handler": ("FlextTestsHandlerHelpersUtilitiesMixin",),
            "._utilities.make": ("FlextTestsMakeUtilitiesMixin",),
            "._utilities.make_contract": ("FlextTestsMakeContractUtilitiesMixin",),
            "._utilities.make_parsing": ("FlextTestsMakeParsingUtilitiesMixin",),
            "._utilities.make_registry": ("FlextTestsMakeRegistryUtilitiesMixin",),
            "._utilities.make_rendering": ("FlextTestsMakeRenderingUtilitiesMixin",),
            "._utilities.matchers": (
                "FlextTestsMatchersUtilities",
                "tm",
            ),
            "._utilities.payload": ("FlextTestsPayloadUtilities",),
            "._utilities.result": ("FlextTestsResultUtilitiesMixin",),
            "._utilities.settings": ("FlextTestsConfigHelpersUtilitiesMixin",),
            "._utilities.testcontext": ("FlextTestsTestContextUtilitiesMixin",),
            "._utilities.validator": ("FlextTestsValidatorUtilitiesMixin",),
            "._validator.bypass": ("FlextValidatorBypass",),
            "._validator.imports": ("FlextValidatorImports",),
            "._validator.layer": ("FlextValidatorLayer",),
            "._validator.markdown": ("FlextValidatorMarkdown",),
            "._validator.models": ("FlextTestsValidatorModels",),
            "._validator.settings": ("FlextValidatorSettings",),
            "._validator.tests": ("FlextValidatorTests",),
            "._validator.types": ("FlextValidatorTypes",),
            ".base": (
                "FlextService",
                "FlextTestsCase",
                "FlextTestsServiceBase",
                "s",
            ),
            ".constants": (
                "FlextTestsConstants",
                "c",
            ),
            ".docker": (
                "FlextTestsDocker",
                "tk",
            ),
            ".domains": (
                "FlextTestsDomains",
                "td",
            ),
            ".files": (
                "FlextTestsFiles",
                "tf",
            ),
            ".models": (
                "FlextTestsModels",
                "m",
            ),
            ".protocols": (
                "FlextTestsProtocols",
                "p",
            ),
            ".settings": ("FlextTestsSettings",),
            ".typings": (
                "FlextTestsTypes",
                "t",
            ),
            ".utilities": (
                "FlextTestsUtilities",
                "u",
            ),
            ".validator": (
                "FlextTestsValidator",
                "tv",
            ),
            "flext_core": (
                "d",
                "e",
                "h",
                "r",
                "x",
            ),
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
    [
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)

__all__: list[str] = [
    "EnforcementCollector",
    "EnforcementItem",
    "EnforcementViolationError",
    "FlextService",
    "FlextTestsCase",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsModels",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsSettings",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidator",
    "MarkdownCodeBlockCollector",
    "MarkdownCodeBlockItem",
    "MarkdownValidationError",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "clean_container",
    "d",
    "e",
    "h",
    "m",
    "p",
    "project_metadata",
    "project_namespace_config",
    "project_tool_flext",
    "r",
    "reset_settings",
    "s",
    "sample_data",
    "settings",
    "settings_factory",
    "t",
    "td",
    "temp_dir",
    "temp_file",
    "test_context",
    "test_runtime",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]

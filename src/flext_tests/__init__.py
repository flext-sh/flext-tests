# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_tests.__version__ import *

if _t.TYPE_CHECKING:
    from flext_cli import d, e, h, r, x
    from flext_tests._constants.docker import FlextTestsDockerConstantsMixin
    from flext_tests._constants.files import FlextTestsFilesConstantsMixin
    from flext_tests._constants.matcher import FlextTestsMatcherConstantsMixin
    from flext_tests._constants.validator import FlextTestsValidatorConstantsMixin
    from flext_tests._fixtures.enforcement import (
        EnforcementCollector,
        EnforcementItem,
        EnforcementViolationError,
    )
    from flext_tests._fixtures.markdown_validation import (
        MarkdownCodeBlockCollector,
        MarkdownCodeBlockItem,
        MarkdownValidationError,
    )
    from flext_tests._fixtures.project_metadata import (
        project_metadata,
        project_namespace_config,
        project_tool_flext,
    )
    from flext_tests._fixtures.settings import (
        reset_settings,
        settings,
        settings_factory,
    )
    from flext_tests._models.base import FlextTestsBaseModelsMixin
    from flext_tests._models.batch import FlextTestsBatchModelsMixin
    from flext_tests._models.docker import FlextTestsDockerModelsMixin
    from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
    from flext_tests._models.matchers import FlextTestsMatchersModelsMixin
    from flext_tests._models.validator import FlextTestsValidatorModelsMixin
    from flext_tests._protocols.valuefactory import FlextTestsValueFactoryProtocolsMixin
    from flext_tests._typings.base import FlextTestsBaseTypesMixin
    from flext_tests._typings.files import FlextTestsFilesTypesMixin
    from flext_tests._typings.guards import FlextTestsGuardsTypesMixin
    from flext_tests._typings.matchers import FlextTestsMatchersTypesMixin
    from flext_tests._utilities.badobjects import FlextTestsBadObjectsUtilitiesMixin
    from flext_tests._utilities.constants import (
        FlextTestsConstantsHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.container import (
        FlextTestsContainerHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.context import FlextTestsContextHelpersUtilitiesMixin
    from flext_tests._utilities.domain import FlextTestsDomainHelpersUtilitiesMixin
    from flext_tests._utilities.exception import (
        FlextTestsExceptionHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.files import FlextTestsFilesUtilitiesMixin
    from flext_tests._utilities.generic import FlextTestsGenericHelpersUtilitiesMixin
    from flext_tests._utilities.handler import FlextTestsHandlerHelpersUtilitiesMixin
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities, tm
    from flext_tests._utilities.parser import FlextTestsParserHelpersUtilitiesMixin
    from flext_tests._utilities.payload import FlextTestsPayloadUtilities
    from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin
    from flext_tests._utilities.settings import FlextTestsConfigHelpersUtilitiesMixin
    from flext_tests._utilities.testcase import FlextTestsTestCaseHelpersUtilitiesMixin
    from flext_tests._utilities.testcontext import FlextTestsTestContextUtilitiesMixin
    from flext_tests._utilities.validation import FlextTestsValidationUtilitiesMixin
    from flext_tests._utilities.validator import FlextTestsValidatorUtilitiesMixin
    from flext_tests._validator.bypass import FlextValidatorBypass
    from flext_tests._validator.imports import FlextValidatorImports
    from flext_tests._validator.layer import FlextValidatorLayer
    from flext_tests._validator.markdown import FlextValidatorMarkdown
    from flext_tests._validator.models import FlextTestsValidatorModels
    from flext_tests._validator.settings import FlextValidatorSettings
    from flext_tests._validator.tests import FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes
    from flext_tests.constants import FlextTestsConstants, c
    from flext_tests.docker import FlextTestsDocker, tk
    from flext_tests.domains import FlextTestsDomains, td
    from flext_tests.files import FlextTestsFiles, tf
    from flext_tests.models import FlextTestsModels, m
    from flext_tests.protocols import FlextTestsProtocols, p
    from flext_tests.service import FlextService, s
    from flext_tests.typings import FlextTestsTypes, t
    from flext_tests.utilities import FlextTestsUtilities, u
    from flext_tests.validator import FlextTestsValidator, tv
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
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            "._constants.docker": ("FlextTestsDockerConstantsMixin",),
            "._constants.files": ("FlextTestsFilesConstantsMixin",),
            "._constants.matcher": ("FlextTestsMatcherConstantsMixin",),
            "._constants.validator": ("FlextTestsValidatorConstantsMixin",),
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
                "reset_settings",
                "settings",
                "settings_factory",
            ),
            "._models.base": ("FlextTestsBaseModelsMixin",),
            "._models.batch": ("FlextTestsBatchModelsMixin",),
            "._models.docker": ("FlextTestsDockerModelsMixin",),
            "._models.filesystem": ("FlextTestsFilesystemModelsMixin",),
            "._models.matchers": ("FlextTestsMatchersModelsMixin",),
            "._models.validator": ("FlextTestsValidatorModelsMixin",),
            "._protocols.valuefactory": ("FlextTestsValueFactoryProtocolsMixin",),
            "._typings.base": ("FlextTestsBaseTypesMixin",),
            "._typings.files": ("FlextTestsFilesTypesMixin",),
            "._typings.guards": ("FlextTestsGuardsTypesMixin",),
            "._typings.matchers": ("FlextTestsMatchersTypesMixin",),
            "._utilities.badobjects": ("FlextTestsBadObjectsUtilitiesMixin",),
            "._utilities.constants": ("FlextTestsConstantsHelpersUtilitiesMixin",),
            "._utilities.container": ("FlextTestsContainerHelpersUtilitiesMixin",),
            "._utilities.context": ("FlextTestsContextHelpersUtilitiesMixin",),
            "._utilities.domain": ("FlextTestsDomainHelpersUtilitiesMixin",),
            "._utilities.exception": ("FlextTestsExceptionHelpersUtilitiesMixin",),
            "._utilities.files": ("FlextTestsFilesUtilitiesMixin",),
            "._utilities.generic": ("FlextTestsGenericHelpersUtilitiesMixin",),
            "._utilities.handler": ("FlextTestsHandlerHelpersUtilitiesMixin",),
            "._utilities.matchers": (
                "FlextTestsMatchersUtilities",
                "tm",
            ),
            "._utilities.parser": ("FlextTestsParserHelpersUtilitiesMixin",),
            "._utilities.payload": ("FlextTestsPayloadUtilities",),
            "._utilities.result": ("FlextTestsResultUtilitiesMixin",),
            "._utilities.settings": ("FlextTestsConfigHelpersUtilitiesMixin",),
            "._utilities.testcase": ("FlextTestsTestCaseHelpersUtilitiesMixin",),
            "._utilities.testcontext": ("FlextTestsTestContextUtilitiesMixin",),
            "._utilities.validation": ("FlextTestsValidationUtilitiesMixin",),
            "._utilities.validator": ("FlextTestsValidatorUtilitiesMixin",),
            "._validator.bypass": ("FlextValidatorBypass",),
            "._validator.imports": ("FlextValidatorImports",),
            "._validator.layer": ("FlextValidatorLayer",),
            "._validator.markdown": ("FlextValidatorMarkdown",),
            "._validator.models": ("FlextTestsValidatorModels",),
            "._validator.settings": ("FlextValidatorSettings",),
            "._validator.tests": ("FlextValidatorTests",),
            "._validator.types": ("FlextValidatorTypes",),
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
            ".service": (
                "FlextService",
                "s",
            ),
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
            "flext_cli": (
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "EnforcementCollector",
    "EnforcementItem",
    "EnforcementViolationError",
    "FlextService",
    "FlextTestsBadObjectsUtilitiesMixin",
    "FlextTestsBaseModelsMixin",
    "FlextTestsBaseTypesMixin",
    "FlextTestsBatchModelsMixin",
    "FlextTestsConfigHelpersUtilitiesMixin",
    "FlextTestsConstants",
    "FlextTestsConstantsHelpersUtilitiesMixin",
    "FlextTestsContainerHelpersUtilitiesMixin",
    "FlextTestsContextHelpersUtilitiesMixin",
    "FlextTestsDocker",
    "FlextTestsDockerConstantsMixin",
    "FlextTestsDockerModelsMixin",
    "FlextTestsDomainHelpersUtilitiesMixin",
    "FlextTestsDomains",
    "FlextTestsExceptionHelpersUtilitiesMixin",
    "FlextTestsFiles",
    "FlextTestsFilesConstantsMixin",
    "FlextTestsFilesTypesMixin",
    "FlextTestsFilesUtilitiesMixin",
    "FlextTestsFilesystemModelsMixin",
    "FlextTestsGenericHelpersUtilitiesMixin",
    "FlextTestsGuardsTypesMixin",
    "FlextTestsHandlerHelpersUtilitiesMixin",
    "FlextTestsMatcherConstantsMixin",
    "FlextTestsMatchersModelsMixin",
    "FlextTestsMatchersTypesMixin",
    "FlextTestsMatchersUtilities",
    "FlextTestsModels",
    "FlextTestsParserHelpersUtilitiesMixin",
    "FlextTestsPayloadUtilities",
    "FlextTestsProtocols",
    "FlextTestsResultUtilitiesMixin",
    "FlextTestsTestCaseHelpersUtilitiesMixin",
    "FlextTestsTestContextUtilitiesMixin",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidationUtilitiesMixin",
    "FlextTestsValidator",
    "FlextTestsValidatorConstantsMixin",
    "FlextTestsValidatorModels",
    "FlextTestsValidatorModelsMixin",
    "FlextTestsValidatorUtilitiesMixin",
    "FlextTestsValueFactoryProtocolsMixin",
    "FlextValidatorBypass",
    "FlextValidatorImports",
    "FlextValidatorLayer",
    "FlextValidatorMarkdown",
    "FlextValidatorSettings",
    "FlextValidatorTests",
    "FlextValidatorTypes",
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
    "settings",
    "settings_factory",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]

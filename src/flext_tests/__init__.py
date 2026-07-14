# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_tests.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_infra import d as d, e as e, h as h, r as r, x as x
    from flext_tests._config import (
        FlextTestsConfig as FlextTestsConfig,
        config as config,
    )
    from flext_tests._fixtures.enforcement import (
        EnforcementBuildContext as EnforcementBuildContext,
        EnforcementCollector as EnforcementCollector,
        EnforcementContribution as EnforcementContribution,
        EnforcementItem as EnforcementItem,
        EnforcementViolationError as EnforcementViolationError,
        active_rules as active_rules,
        builder_for as builder_for,
        builders as builders,
        clear as clear,
        discover_workspace_root as discover_workspace_root,
        get as get,
        load_infra_report as load_infra_report,
        register as register,
        split_csv as split_csv,
        warning_categories as warning_categories,
    )
    from flext_tests._settings import (
        FlextTestsSettings as FlextTestsSettings,
        settings as settings,
    )
    from flext_tests._typings.base import (
        FlextTestsBaseTypesMixin as FlextTestsBaseTypesMixin,
    )
    from flext_tests._typings.files import (
        FlextTestsFilesTypesMixin as FlextTestsFilesTypesMixin,
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
    from flext_tests._validator.settings import (
        FlextValidatorSettings as FlextValidatorSettings,
    )
    from flext_tests._validator.tests import FlextValidatorTests as FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes as FlextValidatorTypes
    from flext_tests.base import (
        FlextTestsCase as FlextTestsCase,
        FlextTestsServiceBase as FlextTestsServiceBase,
        s as s,
    )
    from flext_tests.constants import (
        FlextTestsConstants as FlextTestsConstants,
        FlextTestsConstants as c,
    )
    from flext_tests.docker import FlextTestsDocker as FlextTestsDocker, tk as tk
    from flext_tests.domains import FlextTestsDomains as FlextTestsDomains, td as td
    from flext_tests.files import FlextTestsFiles as FlextTestsFiles, tf as tf
    from flext_tests.models import (
        FlextTestsModels as FlextTestsModels,
        FlextTestsModels as m,
    )
    from flext_tests.protocols import (
        FlextTestsProtocols as FlextTestsProtocols,
        FlextTestsProtocols as p,
    )
    from flext_tests.tmatchers import (
        FlextTestsMatchersUtilities as FlextTestsMatchersUtilities,
        tm as tm,
    )
    from flext_tests.typings import (
        FlextTestsTypes as FlextTestsTypes,
        FlextTestsTypes as t,
    )
    from flext_tests.utilities import (
        FlextTestsUtilities as FlextTestsUtilities,
        FlextTestsUtilities as u,
    )
    from flext_tests.validator import (
        FlextTestsValidator as FlextTestsValidator,
        tv as tv,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextTestsConfig", "config"),
<<<<<<< HEAD
=======
    "._constants.data_cases": ("FlextTestsConstantsDataCases",),
    "._constants.docker": ("FlextTestsConstantsDocker",),
    "._constants.files": ("FlextTestsConstantsFiles",),
    "._constants.make": ("FlextTestsConstantsMake",),
    "._constants.matcher": ("FlextTestsConstantsMatcher",),
    "._constants.validator": ("FlextTestsConstantsValidator",),
    "._fixtures._enforcement_parts.build": ("build_items",),
    "._fixtures._enforcement_parts.config": ("SessionConfig", "resolve_config"),
    "._fixtures._enforcement_parts.discovery": (
        "collected_project_names",
        "collected_validator_targets",
        "load_infra_report",
    ),
    "._fixtures._enforcement_parts.validators": (
        "build_tests_validator_items",
        "dispatch_infra_detector",
    ),
>>>>>>> origin/0.12.0-dev
    "._fixtures.enforcement": (
        "EnforcementBuildContext",
        "EnforcementCollector",
        "EnforcementContribution",
        "EnforcementItem",
        "EnforcementViolationError",
        "active_rules",
        "builder_for",
        "builders",
        "clear",
        "discover_workspace_root",
        "get",
<<<<<<< HEAD
        "load_infra_report",
=======
>>>>>>> origin/0.12.0-dev
        "register",
        "split_csv",
        "warning_categories",
    ),
<<<<<<< HEAD
    "._settings": ("FlextTestsSettings", "settings"),
=======
    "._fixtures.markdown_validation": (
        "MarkdownCodeBlockCollector",
        "MarkdownCodeBlockItem",
        "MarkdownValidationError",
    ),
    "._fixtures.project_metadata": ("project_metadata", "project_tool_flext"),
    "._fixtures.settings": (
        "clean_container",
        "reset_settings",
        "sample_data",
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
    "._protocols.enforcement": ("FlextTestsEnforcementProtocolsMixin",),
    "._protocols.valuefactory": ("FlextTestsValueFactoryProtocolsMixin",),
    "._settings": ("FlextTestsSettings", "settings"),
    "._typings.base": ("FlextTestsBaseTypesMixin",),
    "._typings.files": ("FlextTestsFilesTypesMixin",),
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
    "._utilities._matchers._containment": ("FlextTestsMatchersContainmentMixin",),
    "._utilities._matchers._result": ("FlextTestsMatchersResultMixin",),
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
    "._utilities.payload": ("FlextTestsPayloadUtilities",),
    "._utilities.result": ("FlextTestsResultUtilitiesMixin",),
    "._utilities.settings": ("FlextTestsConfigHelpersUtilitiesMixin",),
    "._utilities.testcontext": ("FlextTestsTestContextUtilitiesMixin",),
    "._utilities.validator": ("FlextTestsValidatorUtilitiesMixin",),
    "._validator.bypass": ("FlextValidatorBypass",),
    "._validator.imports": ("FlextValidatorImports",),
    "._validator.layer": ("FlextValidatorLayer",),
    "._validator.markdown": ("FlextValidatorMarkdown",),
    "._validator.settings": ("FlextValidatorSettings",),
    "._validator.tests": ("FlextValidatorTests",),
    "._validator.types": ("FlextValidatorTypes",),
>>>>>>> origin/0.12.0-dev
    ".base": ("FlextTestsCase", "FlextTestsServiceBase", "s"),
    ".constants": ("FlextTestsConstants", "c"),
    ".docker": ("FlextTestsDocker", "tk"),
    ".domains": ("FlextTestsDomains", "td"),
    ".files": ("FlextTestsFiles", "tf"),
    ".models": ("FlextTestsModels", "m"),
    ".protocols": ("FlextTestsProtocols", "p"),
    ".tmatchers": ("FlextTestsMatchersUtilities", "tm"),
    ".typings": ("FlextTestsTypes", "t"),
    ".utilities": ("FlextTestsUtilities", "u"),
    ".validator": ("FlextTestsValidator", "tv"),
    "flext_infra": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

__all__: tuple[str, ...] = (
<<<<<<< HEAD
    "EnforcementBuildContext",
    "EnforcementCollector",
    "EnforcementContribution",
    "EnforcementItem",
    "EnforcementViolationError",
=======
>>>>>>> origin/0.12.0-dev
    "FlextTestsCase",
    "FlextTestsConfig",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsMatchersUtilities",
    "FlextTestsModels",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsSettings",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidator",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
<<<<<<< HEAD
    "active_rules",
    "builder_for",
    "builders",
    "c",
    "clear",
    "config",
    "d",
    "discover_workspace_root",
    "e",
    "get",
    "h",
    "load_infra_report",
    "m",
    "p",
    "r",
    "register",
    "s",
    "settings",
    "split_csv",
=======
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "settings",
>>>>>>> origin/0.12.0-dev
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
<<<<<<< HEAD
    "warning_categories",
=======
>>>>>>> origin/0.12.0-dev
    "x",
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)

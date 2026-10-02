# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities import _files, _matchers
    from flext_tests._utilities._files._assertions import FlextTestsFilesAssertionsMixin
    from flext_tests._utilities._files._batch import FlextTestsFilesBatchMixin
    from flext_tests._utilities._files._comparison import FlextTestsFilesComparisonMixin
    from flext_tests._utilities._files._contexts import FlextTestsFilesContextsMixin
    from flext_tests._utilities._files._creation import FlextTestsFilesCreationMixin
    from flext_tests._utilities._files._info import FlextTestsFilesInfoMixin
    from flext_tests._utilities._files._lifecycle import FlextTestsFilesLifecycleMixin
    from flext_tests._utilities._files._reading import FlextTestsFilesReadingMixin
    from flext_tests._utilities._matchers._assertions import (
        FlextTestsMatchersAssertionsMixin,
    )
    from flext_tests._utilities._matchers._containment import (
        FlextTestsMatchersContainmentMixin,
    )
    from flext_tests._utilities._matchers._immutability import (
        FlextTestsMatchersImmutabilityMixin,
    )
    from flext_tests._utilities._matchers._result import FlextTestsMatchersResultMixin
    from flext_tests._utilities._matchers._scope import FlextTestsMatchersScopeMixin
    from flext_tests._utilities._matchers._that import FlextTestsMatchersThatMixin
    from flext_tests._utilities._matchers._typeguards import (
        FlextTestsMatchersTypeGuardsMixin,
    )
    from flext_tests._utilities.base import FlextTestsUtilitiesBase
    from flext_tests._utilities.container import (
        FlextTestsContainerHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.docker_lifecycle import (
        FlextTestsDockerLifecycleUtilitiesMixin,
    )
    from flext_tests._utilities.docker_state import FlextTestsDockerStateUtilitiesMixin
    from flext_tests._utilities.enforcement import FlextTestsEnforcementUtilitiesMixin
    from flext_tests._utilities.files import FlextTestsFilesUtilitiesMixin
    from flext_tests._utilities.fixtures_dsl import FlextTestsFixturesDSLMixin
    from flext_tests._utilities.generic import FlextTestsGenericHelpersUtilitiesMixin
    from flext_tests._utilities.governance import FlextTestsModuleGovernanceMixin
    from flext_tests._utilities.handler import FlextTestsHandlerHelpersUtilitiesMixin
    from flext_tests._utilities.make import FlextTestsMakeUtilitiesMixin
    from flext_tests._utilities.make_contract import (
        FlextTestsMakeContractUtilitiesMixin,
    )
    from flext_tests._utilities.make_parsing import FlextTestsMakeParsingUtilitiesMixin
    from flext_tests._utilities.make_registry import (
        FlextTestsMakeRegistryUtilitiesMixin,
    )
    from flext_tests._utilities.make_rendering import (
        FlextTestsMakeRenderingUtilitiesMixin,
    )
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities
    from flext_tests._utilities.namespace import FlextTestsNamespaceUtilitiesMixin
    from flext_tests._utilities.payload import FlextTestsPayloadUtilities
    from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin
    from flext_tests._utilities.scratch_storage import (
        FlextTestsScratchStorageUtilitiesMixin,
    )
    from flext_tests._utilities.settings import FlextTestsConfigHelpersUtilitiesMixin
    from flext_tests._utilities.testcontext import FlextTestsTestContextUtilitiesMixin
    from flext_tests._utilities.workspace_cleanup import (
        FlextTestsWorkspaceCleanupUtilitiesMixin,
    )
    from flext_tests._utilities.workspace_cleanup_git import (
        FlextTestsWorkspaceCleanupGitUtilitiesMixin,
    )
    from flext_tests._utilities.workspace_cleanup_inspect import (
        FlextTestsWorkspaceCleanupInspectUtilitiesMixin,
    )
    from flext_tests._utilities.workspace_cleanup_paths import (
        FlextTestsWorkspaceCleanupPathsUtilitiesMixin,
    )
    from flext_tests._utilities.workspace_cleanup_plan import (
        FlextTestsWorkspaceCleanupPlanUtilitiesMixin,
    )


__all__: tuple[str, ...] = (
    "FlextTestsConfigHelpersUtilitiesMixin",
    "FlextTestsContainerHelpersUtilitiesMixin",
    "FlextTestsDockerLifecycleUtilitiesMixin",
    "FlextTestsDockerStateUtilitiesMixin",
    "FlextTestsEnforcementUtilitiesMixin",
    "FlextTestsFilesAssertionsMixin",
    "FlextTestsFilesBatchMixin",
    "FlextTestsFilesComparisonMixin",
    "FlextTestsFilesContextsMixin",
    "FlextTestsFilesCreationMixin",
    "FlextTestsFilesInfoMixin",
    "FlextTestsFilesLifecycleMixin",
    "FlextTestsFilesReadingMixin",
    "FlextTestsFilesUtilitiesMixin",
    "FlextTestsFixturesDSLMixin",
    "FlextTestsGenericHelpersUtilitiesMixin",
    "FlextTestsHandlerHelpersUtilitiesMixin",
    "FlextTestsMakeContractUtilitiesMixin",
    "FlextTestsMakeParsingUtilitiesMixin",
    "FlextTestsMakeRegistryUtilitiesMixin",
    "FlextTestsMakeRenderingUtilitiesMixin",
    "FlextTestsMakeUtilitiesMixin",
    "FlextTestsMatchersAssertionsMixin",
    "FlextTestsMatchersContainmentMixin",
    "FlextTestsMatchersImmutabilityMixin",
    "FlextTestsMatchersResultMixin",
    "FlextTestsMatchersScopeMixin",
    "FlextTestsMatchersThatMixin",
    "FlextTestsMatchersTypeGuardsMixin",
    "FlextTestsMatchersUtilities",
    "FlextTestsModuleGovernanceMixin",
    "FlextTestsNamespaceUtilitiesMixin",
    "FlextTestsPayloadUtilities",
    "FlextTestsResultUtilitiesMixin",
    "FlextTestsScratchStorageUtilitiesMixin",
    "FlextTestsTestContextUtilitiesMixin",
    "FlextTestsUtilitiesBase",
    "FlextTestsWorkspaceCleanupGitUtilitiesMixin",
    "FlextTestsWorkspaceCleanupInspectUtilitiesMixin",
    "FlextTestsWorkspaceCleanupPathsUtilitiesMixin",
    "FlextTestsWorkspaceCleanupPlanUtilitiesMixin",
    "FlextTestsWorkspaceCleanupUtilitiesMixin",
    "_files",
    "_matchers",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._files": ("_files",),
            "._files._assertions": ("FlextTestsFilesAssertionsMixin",),
            "._files._batch": ("FlextTestsFilesBatchMixin",),
            "._files._comparison": ("FlextTestsFilesComparisonMixin",),
            "._files._contexts": ("FlextTestsFilesContextsMixin",),
            "._files._creation": ("FlextTestsFilesCreationMixin",),
            "._files._info": ("FlextTestsFilesInfoMixin",),
            "._files._lifecycle": ("FlextTestsFilesLifecycleMixin",),
            "._files._reading": ("FlextTestsFilesReadingMixin",),
            "._matchers": ("_matchers",),
            "._matchers._assertions": ("FlextTestsMatchersAssertionsMixin",),
            "._matchers._containment": ("FlextTestsMatchersContainmentMixin",),
            "._matchers._immutability": ("FlextTestsMatchersImmutabilityMixin",),
            "._matchers._result": ("FlextTestsMatchersResultMixin",),
            "._matchers._scope": ("FlextTestsMatchersScopeMixin",),
            "._matchers._that": ("FlextTestsMatchersThatMixin",),
            "._matchers._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
            ".base": ("FlextTestsUtilitiesBase",),
            ".container": ("FlextTestsContainerHelpersUtilitiesMixin",),
            ".docker_lifecycle": ("FlextTestsDockerLifecycleUtilitiesMixin",),
            ".docker_state": ("FlextTestsDockerStateUtilitiesMixin",),
            ".enforcement": ("FlextTestsEnforcementUtilitiesMixin",),
            ".files": ("FlextTestsFilesUtilitiesMixin",),
            ".fixtures_dsl": ("FlextTestsFixturesDSLMixin",),
            ".generic": ("FlextTestsGenericHelpersUtilitiesMixin",),
            ".governance": ("FlextTestsModuleGovernanceMixin",),
            ".handler": ("FlextTestsHandlerHelpersUtilitiesMixin",),
            ".make": ("FlextTestsMakeUtilitiesMixin",),
            ".make_contract": ("FlextTestsMakeContractUtilitiesMixin",),
            ".make_parsing": ("FlextTestsMakeParsingUtilitiesMixin",),
            ".make_registry": ("FlextTestsMakeRegistryUtilitiesMixin",),
            ".make_rendering": ("FlextTestsMakeRenderingUtilitiesMixin",),
            ".matchers": ("FlextTestsMatchersUtilities",),
            ".namespace": ("FlextTestsNamespaceUtilitiesMixin",),
            ".payload": ("FlextTestsPayloadUtilities",),
            ".result": ("FlextTestsResultUtilitiesMixin",),
            ".scratch_storage": ("FlextTestsScratchStorageUtilitiesMixin",),
            ".settings": ("FlextTestsConfigHelpersUtilitiesMixin",),
            ".testcontext": ("FlextTestsTestContextUtilitiesMixin",),
            ".workspace_cleanup": ("FlextTestsWorkspaceCleanupUtilitiesMixin",),
            ".workspace_cleanup_git": ("FlextTestsWorkspaceCleanupGitUtilitiesMixin",),
            ".workspace_cleanup_inspect": (
                "FlextTestsWorkspaceCleanupInspectUtilitiesMixin",
            ),
            ".workspace_cleanup_paths": (
                "FlextTestsWorkspaceCleanupPathsUtilitiesMixin",
            ),
            ".workspace_cleanup_plan": (
                "FlextTestsWorkspaceCleanupPlanUtilitiesMixin",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)

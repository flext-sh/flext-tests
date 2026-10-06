# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

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
    from flext_tests._utilities.governance import FlextTestsFlextUtilitiesGovernance
    from flext_tests._utilities.handler import FlextTestsFlextUtilitiesHandler
    from flext_tests._utilities.make import FlextTestsMakeUtilitiesMixin
    from flext_tests._utilities.make_contract import (
        FlextTestsFlextUtilitiesMakeContract,
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
    from flext_tests._utilities.payload import (
        FlextTestsFlextUtilitiesPayload,
        FlextTestsPayloadUtilities,
    )
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
    "FlextTestsFlextUtilitiesGovernance",
    "FlextTestsFlextUtilitiesHandler",
    "FlextTestsFlextUtilitiesMakeContract",
    "FlextTestsFlextUtilitiesPayload",
    "FlextTestsGenericHelpersUtilitiesMixin",
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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsConfigHelpersUtilitiesMixin": ".settings",
        "FlextTestsContainerHelpersUtilitiesMixin": ".container",
        "FlextTestsDockerLifecycleUtilitiesMixin": ".docker_lifecycle",
        "FlextTestsDockerStateUtilitiesMixin": ".docker_state",
        "FlextTestsEnforcementUtilitiesMixin": ".enforcement",
        "FlextTestsFilesAssertionsMixin": "._files._assertions",
        "FlextTestsFilesBatchMixin": "._files._batch",
        "FlextTestsFilesComparisonMixin": "._files._comparison",
        "FlextTestsFilesContextsMixin": "._files._contexts",
        "FlextTestsFilesCreationMixin": "._files._creation",
        "FlextTestsFilesInfoMixin": "._files._info",
        "FlextTestsFilesLifecycleMixin": "._files._lifecycle",
        "FlextTestsFilesReadingMixin": "._files._reading",
        "FlextTestsFilesUtilitiesMixin": ".files",
        "FlextTestsFixturesDSLMixin": ".fixtures_dsl",
        "FlextTestsFlextUtilitiesGovernance": ".governance",
        "FlextTestsFlextUtilitiesHandler": ".handler",
        "FlextTestsFlextUtilitiesMakeContract": ".make_contract",
        "FlextTestsFlextUtilitiesPayload": ".payload",
        "FlextTestsGenericHelpersUtilitiesMixin": ".generic",
        "FlextTestsMakeContractUtilitiesMixin": ".make_contract",
        "FlextTestsMakeParsingUtilitiesMixin": ".make_parsing",
        "FlextTestsMakeRegistryUtilitiesMixin": ".make_registry",
        "FlextTestsMakeRenderingUtilitiesMixin": ".make_rendering",
        "FlextTestsMakeUtilitiesMixin": ".make",
        "FlextTestsMatchersAssertionsMixin": "._matchers._assertions",
        "FlextTestsMatchersContainmentMixin": "._matchers._containment",
        "FlextTestsMatchersImmutabilityMixin": "._matchers._immutability",
        "FlextTestsMatchersResultMixin": "._matchers._result",
        "FlextTestsMatchersScopeMixin": "._matchers._scope",
        "FlextTestsMatchersThatMixin": "._matchers._that",
        "FlextTestsMatchersTypeGuardsMixin": "._matchers._typeguards",
        "FlextTestsMatchersUtilities": ".matchers",
        "FlextTestsNamespaceUtilitiesMixin": ".namespace",
        "FlextTestsPayloadUtilities": ".payload",
        "FlextTestsResultUtilitiesMixin": ".result",
        "FlextTestsScratchStorageUtilitiesMixin": ".scratch_storage",
        "FlextTestsTestContextUtilitiesMixin": ".testcontext",
        "FlextTestsUtilitiesBase": ".base",
        "FlextTestsWorkspaceCleanupGitUtilitiesMixin": ".workspace_cleanup_git",
        "FlextTestsWorkspaceCleanupInspectUtilitiesMixin": ".workspace_cleanup_inspect",
        "FlextTestsWorkspaceCleanupPathsUtilitiesMixin": ".workspace_cleanup_paths",
        "FlextTestsWorkspaceCleanupPlanUtilitiesMixin": ".workspace_cleanup_plan",
        "FlextTestsWorkspaceCleanupUtilitiesMixin": ".workspace_cleanup",
        "_files": "._files",
        "_matchers": "._matchers",
    }),
    public_exports=__all__,
)

# AUTO-GENERATED FILE — Regenerate with: make gen
"""Internal package for utilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities.base import FlextTestsUtilitiesBase
    from flext_tests._utilities.container import (
        FlextTestsContainerHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.docker_client import (
        FlextTestsDockerClientUtilitiesMixin,
    )
    from flext_tests._utilities.docker_lifecycle import (
        FlextTestsDockerLifecycleUtilitiesMixin,
    )
    from flext_tests._utilities.docker_state import FlextTestsDockerStateUtilitiesMixin
    from flext_tests._utilities.enforcement import FlextTestsEnforcementUtilitiesMixin
    from flext_tests._utilities.environment import FlextTestsEnvironmentUtilitiesMixin
    from flext_tests._utilities.files import FlextTestsUtilitiesFiles
    from flext_tests._utilities.fixtures_dsl import FlextTestsFixturesDSLMixin
    from flext_tests._utilities.governance import FlextTestsFlextUtilitiesGovernance
    from flext_tests._utilities.handler import FlextTestsFlextUtilitiesHandler
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities
    from flext_tests._utilities.namespace import FlextTestsNamespaceUtilitiesMixin
    from flext_tests._utilities.payload import FlextTestsFlextUtilitiesPayload
    from flext_tests._utilities.pytest_surface import FlextTestsPytestUtilitiesMixin
    from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin
    from flext_tests._utilities.scratch_storage import (
        FlextTestsScratchStorageUtilitiesMixin,
    )
    from flext_tests._utilities.settings import FlextTestsConfigHelpersUtilitiesMixin
    from flext_tests._utilities.testcontext import FlextTestsTestContextUtilitiesMixin

__all__: tuple[str, ...] = (
    "FlextTestsConfigHelpersUtilitiesMixin",
    "FlextTestsContainerHelpersUtilitiesMixin",
    "FlextTestsDockerClientUtilitiesMixin",
    "FlextTestsDockerLifecycleUtilitiesMixin",
    "FlextTestsDockerStateUtilitiesMixin",
    "FlextTestsEnforcementUtilitiesMixin",
    "FlextTestsEnvironmentUtilitiesMixin",
    "FlextTestsFixturesDSLMixin",
    "FlextTestsFlextUtilitiesGovernance",
    "FlextTestsFlextUtilitiesHandler",
    "FlextTestsFlextUtilitiesPayload",
    "FlextTestsMatchersUtilities",
    "FlextTestsNamespaceUtilitiesMixin",
    "FlextTestsPytestUtilitiesMixin",
    "FlextTestsResultUtilitiesMixin",
    "FlextTestsScratchStorageUtilitiesMixin",
    "FlextTestsTestContextUtilitiesMixin",
    "FlextTestsUtilitiesBase",
    "FlextTestsUtilitiesFiles",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsConfigHelpersUtilitiesMixin": ".settings",
        "FlextTestsContainerHelpersUtilitiesMixin": ".container",
        "FlextTestsDockerClientUtilitiesMixin": ".docker_client",
        "FlextTestsDockerLifecycleUtilitiesMixin": ".docker_lifecycle",
        "FlextTestsDockerStateUtilitiesMixin": ".docker_state",
        "FlextTestsEnforcementUtilitiesMixin": ".enforcement",
        "FlextTestsEnvironmentUtilitiesMixin": ".environment",
        "FlextTestsFixturesDSLMixin": ".fixtures_dsl",
        "FlextTestsFlextUtilitiesGovernance": ".governance",
        "FlextTestsFlextUtilitiesHandler": ".handler",
        "FlextTestsFlextUtilitiesPayload": ".payload",
        "FlextTestsMatchersUtilities": ".matchers",
        "FlextTestsNamespaceUtilitiesMixin": ".namespace",
        "FlextTestsPytestUtilitiesMixin": ".pytest_surface",
        "FlextTestsResultUtilitiesMixin": ".result",
        "FlextTestsScratchStorageUtilitiesMixin": ".scratch_storage",
        "FlextTestsTestContextUtilitiesMixin": ".testcontext",
        "FlextTestsUtilitiesBase": ".base",
        "FlextTestsUtilitiesFiles": ".files",
    }),
    public_exports=__all__,
)

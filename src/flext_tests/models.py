"""Models for FLEXT tests.

Provides FlextTestsModels, extending m with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_tests._models.base import FlextTestsFlextModelsBase
from flext_tests._models.batch import FlextTestsBatchModelsMixin
from flext_tests._models.docker import FlextTestsDockerModelsMixin
from flext_tests._models.domains import FlextTestsDomainModelsMixin
from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
from flext_tests._models.make import FlextTestsMakeModelsMixin
from flext_tests._models.matchers import FlextTestsMatchersModelsMixin
from flext_tests._models.namespace import FlextTestsNamespaceModelsMixin
from flext_tests._models.validator import FlextTestsValidatorModelsMixin
from flext_tests._models.workspace_cleanup import FlextTestsWorkspaceCleanupModelsMixin

try:
    from flext_tests import t
except ImportError:  # mid-init: the tail completion tolerates and defers
    t = None  # type: ignore[assignment]


class FlextTestsModels(FlextCliModels):
    """Test models extending m with test-specific factory models."""

    class Tests(
        FlextTestsDockerModelsMixin,
        FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin,
        FlextTestsDomainModelsMixin,
        FlextTestsFilesystemModelsMixin,
        FlextTestsNamespaceModelsMixin,
        FlextTestsBatchModelsMixin,
        FlextTestsMakeModelsMixin,
        FlextTestsValidatorModelsMixin,
        FlextTestsMatchersModelsMixin,
        # NOTE (multi-agent): expose the approved typed cleanup contract
        # through m.Tests.
        FlextTestsWorkspaceCleanupModelsMixin,
    ):
        """Test-specific models namespace."""


m = FlextTestsModels

# NOTE (import discipline): the family's nested models annotate through
# ``t.Tests.*`` and cross-mixin names that are only fully bound once the
# facade composed; complete every nested model here, at the module bounds,
# against the merged namespace (the module globals — including the composed
# family — plus the base family's names).
_models_ns: dict[str, object] = {
    **globals(),
    **vars(FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin),
}
if t is not None:
    _models_ns.setdefault("t", t)
for _mixin_name in tuple(globals()):
    _mixin = globals().get(_mixin_name)
    if isinstance(_mixin, type) and _mixin_name.endswith("Mixin"):
        for _member in tuple(vars(_mixin).values()):
            if isinstance(_member, type) and hasattr(_member, "model_rebuild"):
                _member.model_rebuild(_types_namespace=_models_ns, force=True)

__all__: list[str] = ["FlextTestsModels", "m"]

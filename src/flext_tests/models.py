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


# NOTE (import discipline): base.py's deferred models annotate through ``t.Tests.*``
# whose import fails while the package is mid-init (base loads first from here).
# Now that every mixin composed and the package namespace is complete, bind ``t``
# into base's module namespace and complete its deferred models — the entries the
# consumer's first import order needs.
import flext_tests._models.base as _models_base
from flext_tests import t as _t_final

_models_base.t = _t_final
_models_ns = {
    **globals(),
    **vars(_models_base),
    "t": _t_final,
}
for _mixin_name in tuple(globals()):
    _mixin = globals().get(_mixin_name)
    if not isinstance(_mixin, type) or not _mixin_name.endswith("Mixin"):
        continue
    for _member in tuple(vars(_mixin).values()):
        if isinstance(_member, type) and hasattr(_member, "model_rebuild"):
            _member.model_rebuild(
                _types_namespace=_models_ns,
                raise_errors=False,
                force=True,
            )


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

__all__: list[str] = ["FlextTestsModels", "m"]

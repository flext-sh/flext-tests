# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._models.base import FlextTestsModelsFlextBase
    from flext_tests._models.docker import FlextTestsModelsDocker
    from flext_tests._models.filesystem import FlextTestsModelsFilesystem
    from flext_tests._models.matchers import FlextTestsModelsMatchers
    from flext_tests._models.namespace import FlextTestsModelsNamespace
    from flext_tests._models.spec import FlextTestsModelsSpec
    from flext_tests._models.validator import FlextTestsModelsValidator


__all__: tuple[str, ...] = (
    "FlextTestsModelsDocker",
    "FlextTestsModelsFilesystem",
    "FlextTestsModelsFlextBase",
    "FlextTestsModelsMatchers",
    "FlextTestsModelsNamespace",
    "FlextTestsModelsSpec",
    "FlextTestsModelsValidator",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsModelsDocker": ".docker",
        "FlextTestsModelsFilesystem": ".filesystem",
        "FlextTestsModelsFlextBase": ".base",
        "FlextTestsModelsMatchers": ".matchers",
        "FlextTestsModelsNamespace": ".namespace",
        "FlextTestsModelsSpec": ".spec",
        "FlextTestsModelsValidator": ".validator",
    }),
    public_exports=__all__,
)

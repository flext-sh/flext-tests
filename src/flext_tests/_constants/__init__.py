# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Constants package.

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
    from flext_tests._constants.base import FlextTestsConstantsBase
    from flext_tests._constants.data_cases import FlextTestsConstantsDataCases
    from flext_tests._constants.docker import FlextTestsConstantsDocker
    from flext_tests._constants.files import FlextTestsConstantsFiles
    from flext_tests._constants.matcher import FlextTestsConstantsMatcher
    from flext_tests._constants.namespace import FlextTestsConstantsNamespace
    from flext_tests._constants.pytest_surface import FlextTestsConstantsPytest
    from flext_tests._constants.validator import FlextTestsConstantsValidator


__all__: tuple[str, ...] = (
    "FlextTestsConstantsBase",
    "FlextTestsConstantsDataCases",
    "FlextTestsConstantsDocker",
    "FlextTestsConstantsFiles",
    "FlextTestsConstantsMatcher",
    "FlextTestsConstantsNamespace",
    "FlextTestsConstantsPytest",
    "FlextTestsConstantsValidator",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsConstantsBase": ".base",
        "FlextTestsConstantsDataCases": ".data_cases",
        "FlextTestsConstantsDocker": ".docker",
        "FlextTestsConstantsFiles": ".files",
        "FlextTestsConstantsMatcher": ".matcher",
        "FlextTestsConstantsNamespace": ".namespace",
        "FlextTestsConstantsPytest": ".pytest_surface",
        "FlextTestsConstantsValidator": ".validator",
    }),
    public_exports=__all__,
)

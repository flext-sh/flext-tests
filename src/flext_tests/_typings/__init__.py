# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import defer_lazy_bases, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._typings.base import FlextTestsTypesBase
    from flext_tests._typings.docker import FlextTestsTypesDocker
    from flext_tests._typings.files import FlextTestsTypesFiles
    from flext_tests._typings.matchers import FlextTestsTypesMatchers
    from flext_tests._typings.pytest_surface import FlextTestsTypesPytest


__all__: tuple[str, ...] = (
    "FlextTestsTypesBase",
    "FlextTestsTypesDocker",
    "FlextTestsTypesFiles",
    "FlextTestsTypesMatchers",
    "FlextTestsTypesPytest",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTestsTypesBase": ".base",
        "FlextTestsTypesDocker": ".docker",
        "FlextTestsTypesFiles": ".files",
        "FlextTestsTypesMatchers": ".matchers",
        "FlextTestsTypesPytest": ".pytest_surface",
    },
    public_exports=__all__,
    deferred_members={
        "FlextTestsTypesBase": (
            "PayloadKind",
            "PayloadAtom",
            "PayloadItems",
            "PayloadEntries",
            "TestobjectAtom",
            "TestobjectCollection",
            "TestobjectNode",
            "TestobjectSerializable",
            "TestobjectHashable",
            "NormalizationInput",
            "TestResultValue",
            "Testobject",
        ),
        "FlextTestsTypesDocker": (
            "DockerSdkClient",
            "DockerContainer",
            "ComposeClient",
        ),
        "FlextTestsTypesFiles": (
            "ReadContent",
            "FileContentStructured",
            "FileContentPlain",
            "ParsedPair",
        ),
        "FlextTestsTypesMatchers": (
            "LengthSpec",
            "ComparableScalar",
            "ItemSelector",
            "PathSpec",
            "ExclusionSpec",
            "KeySpec",
            "AttributeSpec",
            "ErrorCodeSpec",
            "CleanupSpec",
            "EnvironmentSpec",
        ),
        "FlextTestsTypesPytest": (),
    },
)

defer_lazy_bases(
    __name__,
    {
        "FlextTestsTypesPytest": (("flext_infra", "FlextInfraTypes.Infra.Pytest"),),
    },
)

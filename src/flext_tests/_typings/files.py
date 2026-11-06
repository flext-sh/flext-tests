"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_core import p

from flext_tests._typings.base import FlextTestsTypesBase


class FlextTestsTypesFiles:
    type ReadContent = str | bytes | p.ConfigMap | Sequence[Sequence[str]]
    type FileContentStructured = (
        Mapping[str, FlextTestsTypesBase.TestobjectSerializable] | p.BaseModel
    )
    type FileContentPlain = ReadContent | FileContentStructured

    type ParsedPair = tuple[
        Mapping[str, FlextTestsTypesBase.TestobjectSerializable],
        Mapping[str, FlextTestsTypesBase.TestobjectSerializable],
    ]


__all__: list[str] = ["FlextTestsTypesFiles"]

"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import m, t

from flext_tests._typings.base import FlextTestsTypesBase


class FlextTestsTypesFiles:
    type ReadContent = str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence]
    type FileContentStructured = (
        t.MappingKV[str, FlextTestsTypesBase.TestobjectSerializable] | m.BaseModel
    )
    type FileContentPlain = ReadContent | FileContentStructured


__all__: list[str] = ["FlextTestsTypesFiles"]

"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import m
from flext_tests import t


class FlextTestsFilesTypesMixin:
    type BatchFiles = (
        t.MappingKV[str, t.Tests.TestobjectSerializable]
        | t.SequenceOf[t.Tests.TestobjectSerializable]
    )
    type ReadContent = str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence]
    type FileContentStructured = (
        t.MappingKV[str, t.Tests.TestobjectSerializable] | m.BaseModel
    )
    type FileContentPlain = ReadContent | FileContentStructured

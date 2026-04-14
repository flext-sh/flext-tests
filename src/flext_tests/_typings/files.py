"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from pydantic import BaseModel

from flext_core import FlextTypes, r
from flext_tests import FlextTestsBaseTypesMixin


class FlextTestsFilesTypesMixin:
    type BatchFiles = (
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type ReadContent = (
        str | bytes | FlextTypes.ConfigMap | Sequence[FlextTypes.StrSequence]
    )
    type FileContentPlain = ReadContent | BaseModel
    type FileInput = (
        FileContentPlain
        | r[str]
        | r[bytes]
        | r[FlextTypes.ConfigMap]
        | r[Sequence[FlextTypes.StrSequence]]
        | r[BaseModel]
    )

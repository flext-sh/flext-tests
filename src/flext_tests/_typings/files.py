"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)

from flext_core import FlextTypes, m, r

from flext_tests import FlextTestsBaseTypesMixin


class FlextTestsFilesTypesMixin:
    type BatchFiles = (
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type ReadContent = str | bytes | m.ConfigMap | Sequence[FlextTypes.StrSequence]
    type FileContentPlain = (
        ReadContent
        | Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | m.BaseModel
    )
    type FileInput = FileContentPlain | r[FileContentPlain]

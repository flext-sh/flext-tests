"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from pydantic import BaseModel

from flext_core import FlextResult, FlextTypes
from flext_tests._typings.base import FlextTestsBaseTypesMixin


class FlextTestsFilesTypesMixin:
    type BatchFiles = (
        Mapping[str, FlextTestsBaseTypesMixin.Testobject]
        | Sequence[FlextTestsBaseTypesMixin.Testobject]
    )
    type FileContentPlain = (
        str
        | bytes
        | FlextTypes.ConfigMap
        | Sequence[FlextTypes.StrSequence]
        | BaseModel
    )
    type FileInput = (
        FileContentPlain
        | FlextResult[str]
        | FlextResult[bytes]
        | FlextResult[FlextTypes.ConfigMap]
        | FlextResult[Sequence[FlextTypes.StrSequence]]
        | FlextResult[BaseModel]
    )

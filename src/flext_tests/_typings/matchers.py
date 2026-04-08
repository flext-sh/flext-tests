"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import TypeAliasType

from flext_core import FlextTypes
from flext_tests import FlextTestsBaseTypesMixin


class FlextTestsMatchersTypesMixin:
    type MatcherKwargValue = (
        FlextTestsBaseTypesMixin.Testobject
        | type
        | tuple[type, ...]
        | TypeAliasType
        | set[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Callable[..., FlextTestsBaseTypesMixin.Testobject]
        | Mapping[
            str,
            Callable[..., FlextTestsBaseTypesMixin.Testobject]
            | FlextTestsBaseTypesMixin.TestobjectSerializable,
        ]
        | Mapping[
            int,
            Callable[..., FlextTestsBaseTypesMixin.Testobject]
            | FlextTestsBaseTypesMixin.TestobjectSerializable,
        ]
    )
    type LengthSpec = int | tuple[int, int]
    type DeepSpec = Mapping[
        str,
        Callable[[FlextTestsBaseTypesMixin.Testobject], bool]
        | FlextTestsBaseTypesMixin.TestobjectSerializable,
    ]
    type PathSpec = str | FlextTypes.StrSequence
    type PredicateSpec = Callable[[FlextTestsBaseTypesMixin.Testobject], bool]
    type ValueSpec = (
        Callable[[FlextTestsBaseTypesMixin.Testobject], bool]
        | FlextTestsBaseTypesMixin.Testobject
    )
    type AssertionSpec = (
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Callable[[FlextTestsBaseTypesMixin.Testobject], bool]
        | type
        | tuple[type, ...]
    )
    type ContainmentSpec = (
        FlextTestsBaseTypesMixin.Testobject
        | Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type ExclusionSpec = str | FlextTypes.StrSequence
    type SequencePredicate = (
        type | Callable[[FlextTestsBaseTypesMixin.Testobject], bool]
    )
    type SortKey = (
        bool
        | Callable[
            [FlextTestsBaseTypesMixin.Testobject], FlextTestsBaseTypesMixin.Testobject
        ]
    )
    type KeySpec = FlextTypes.StrSequence | set[str]
    type KeyValueSpec = (
        tuple[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type AttributeSpec = str | FlextTypes.StrSequence
    type AttributeValueSpec = (
        tuple[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type ErrorCodeSpec = str | FlextTypes.StrSequence
    type ErrorDataSpec = FlextTypes.ConfigMap
    type CleanupSpec = Sequence[Callable[[], None]]
    type EnvironmentSpec = FlextTypes.StrMapping

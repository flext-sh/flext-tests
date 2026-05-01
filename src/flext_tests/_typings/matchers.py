"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Callable,
)
from typing import TypeAliasType

from flext_core import m
from flext_tests import t


class FlextTestsMatchersTypesMixin:
    type MatcherEqTarget = (
        t.MappingKV[str, t.Tests.TestobjectSerializable]
        | t.SequenceOf[t.Tests.TestobjectSerializable]
        | bytes
        | str
        | int
        | float
        | bool
        | TypeAliasType
    )
    """Expected-value target for ``Ok``/``Fail`` matcher ``eq`` / ``ne`` fields.

    The ``| None`` nullability is attached by the field defaulting to
    ``None`` rather than by the alias itself — Pydantic rejects
    ``union_mode`` on nullable schemas, so the alias stays non-nullable.
    """

    type MatchRuleLeaf = t.Tests.Testobject | type | tuple[type, ...] | TypeAliasType
    type MatchRuleKwargs = t.MappingKV[
        str,
        Callable[..., t.Tests.Testobject] | t.Tests.TestobjectSerializable,
    ]
    type MatchRuleValue = MatchRuleLeaf | MatchRuleKwargs
    type MatcherKwargValue = (
        MatchRuleLeaf
        | set[t.Tests.TestobjectSerializable]
        | Callable[..., t.Tests.Testobject]
        | MatchRuleKwargs
        | t.MappingKV[int, MatchRuleValue]
        | t.MappingKV[str, MatchRuleValue]
        | t.MappingKV[FlextTestsMatchersTypesMixin.ItemSelector, MatchRuleValue]
    )
    type LengthSpec = int | tuple[int, int]
    type ComparableScalar = float | int | str
    """Comparable scalar arms for matcher ``gt``/``gte``/``lt``/``lte`` fields.

    Centralized to satisfy AGENTS.md § Model governance rule against
    inline 3+-arm unions in Pydantic field annotations.
    """
    type MatchRuleSpec = (
        t.Tests.Testobject
        | type
        | tuple[type, ...]
        | t.MappingKV[str, FlextTestsMatchersTypesMixin.MatcherKwargValue]
    )
    type DeepSpec = t.MappingKV[
        str,
        Callable[[t.Tests.Testobject], bool] | t.Tests.TestobjectSerializable,
    ]
    type PathMatchSpec = t.MappingKV[str, FlextTestsMatchersTypesMixin.MatchRuleSpec]
    type ItemSelector = int | str
    type ItemMatchSpec = (
        t.SequenceOf[FlextTestsMatchersTypesMixin.MatchRuleSpec]
        | t.MappingKV[
            FlextTestsMatchersTypesMixin.ItemSelector,
            FlextTestsMatchersTypesMixin.MatchRuleSpec,
        ]
    )
    type AttributeMatchSpec = t.MappingKV[
        str,
        FlextTestsMatchersTypesMixin.MatchRuleSpec,
    ]
    type PathSpec = str | t.StrSequence
    type PredicateSpec = Callable[[t.Tests.Testobject], bool]
    type ContainmentSpec = (
        t.Tests.Testobject | t.SequenceOf[t.Tests.TestobjectSerializable]
    )
    type ExclusionSpec = str | t.StrSequence
    type SequencePredicate = type | Callable[[t.Tests.Testobject], bool]
    type SortKey = bool | Callable[[t.Tests.Testobject], t.Tests.Testobject]
    type KeySpec = t.StrSequence | set[str]
    type KeyValueSpec = (
        tuple[str, t.Tests.TestobjectSerializable]
        | t.MappingKV[str, t.Tests.TestobjectSerializable]
    )
    type AttributeSpec = str | t.StrSequence
    type AttributeValueSpec = (
        tuple[str, t.Tests.TestobjectSerializable]
        | t.MappingKV[str, t.Tests.TestobjectSerializable]
    )
    type ErrorCodeSpec = str | t.StrSequence
    type ErrorDataSpec = m.ConfigMap
    type CleanupSpec = t.SequenceOf[Callable[[], None]]
    type EnvironmentSpec = t.StrMapping

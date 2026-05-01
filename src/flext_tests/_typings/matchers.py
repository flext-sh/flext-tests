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
from flext_tests._typings.base import FlextTestsBaseTypesMixin


class FlextTestsMatchersTypesMixin:
    type MatcherEqTarget = (
        t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | t.SequenceOf[FlextTestsBaseTypesMixin.TestobjectSerializable]
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

    type MatchRuleLeaf = (
        FlextTestsBaseTypesMixin.Testobject | type | tuple[type, ...] | TypeAliasType
    )
    type MatchRuleKwargs = t.MappingKV[
        str,
        Callable[..., FlextTestsBaseTypesMixin.Testobject]
        | FlextTestsBaseTypesMixin.TestobjectSerializable,
    ]
    type MatchRuleValue = MatchRuleLeaf | MatchRuleKwargs
    type MatcherKwargValue = (
        MatchRuleLeaf
        | set[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Callable[..., FlextTestsBaseTypesMixin.Testobject]
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
        FlextTestsBaseTypesMixin.Testobject
        | type
        | tuple[type, ...]
        | t.MappingKV[str, FlextTestsMatchersTypesMixin.MatcherKwargValue]
    )
    type DeepSpec = t.MappingKV[
        str,
        Callable[[FlextTestsBaseTypesMixin.Testobject], bool]
        | FlextTestsBaseTypesMixin.TestobjectSerializable,
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
    type PredicateSpec = Callable[[FlextTestsBaseTypesMixin.Testobject], bool]
    type ContainmentSpec = (
        FlextTestsBaseTypesMixin.Testobject
        | t.SequenceOf[FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type ExclusionSpec = str | t.StrSequence
    type SequencePredicate = (
        type | Callable[[FlextTestsBaseTypesMixin.Testobject], bool]
    )
    type SortKey = (
        bool
        | Callable[
            [FlextTestsBaseTypesMixin.Testobject], FlextTestsBaseTypesMixin.Testobject
        ]
    )
    type KeySpec = t.StrSequence | set[str]
    type KeyValueSpec = (
        tuple[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type AttributeSpec = str | t.StrSequence
    type AttributeValueSpec = (
        tuple[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type ErrorCodeSpec = str | t.StrSequence
    type ErrorDataSpec = m.ConfigMap
    type CleanupSpec = t.SequenceOf[Callable[[], None]]
    type EnvironmentSpec = t.StrMapping

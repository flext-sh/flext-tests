"""Shared payload conversion helpers for flext_tests.

Low-level module with no dependency on flext_tests.utilities,
importable by both utilities.py and matchers.py without cycles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import KeysView, Mapping, ValuesView
from datetime import datetime, tzinfo
from enum import Enum
from importlib.machinery import ModuleSpec
from pathlib import Path
from re import Match
from types import (
    BuiltinFunctionType,
    CodeType,
    FunctionType,
    GenericAlias,
    ModuleType,
    UnionType,
)
from typing import TypeAliasType

from flext_infra import u

from flext_tests import m, p, t


class FlextTestsPayloadUtilities:
    """Namespace class for shared payload conversion helpers in flext_tests."""

    @staticmethod
    def _stable_sort_key(value: p.Tests.Payload) -> t.StrPair:
        """Return a total deterministic key for heterogeneous payload values."""
        native = FlextTestsPayloadUtilities.to_match_value(value)
        return type(native).__name__, str(native)

    @staticmethod
    def to_payload(value: p.AttributeProbe) -> m.Tests.Payload:
        """Own supported native values without serializing their model leaves."""
        to_p = FlextTestsPayloadUtilities.to_payload
        match value:
            case m.Tests.Payload():
                return value
            case m.RootModel():
                return to_p(value.root)
            case Enum():
                return to_p(value.value)
            case None:
                return m.Tests.Payload(kind="atom", atom=None)
            case (
                str()
                | int()
                | float()
                | bool()
                | bytes()
                | datetime()
                | tzinfo()
                | Path()
                | type()
                | BaseException()
                | p.Model()
            ):
                return m.Tests.Payload(kind="atom", atom=value)
            case value if hasattr(value, "__metadata__") and hasattr(
                value, "__origin__"
            ):
                # typing.Annotated[...] constructs are type-level atoms under
                # the same textual convention as the alias arm below.
                return m.Tests.Payload(kind="atom", atom=str(value))
            case Match():
                # A regex match compares by its matched text — the pattern
                # contract (semver, id shape) is what an expectation asserts.
                return m.Tests.Payload(kind="atom", atom=value.group(0))
            case (
                GenericAlias()
                | UnionType()
                | TypeAliasType()
                | FunctionType()
                | BuiltinFunctionType()
                | CodeType()
                | ModuleType()
                | ModuleSpec()
            ):
                # Typing constructs and runtime machinery (functions, modules,
                # code specs) are type-level atoms: the established textual
                # convention (mirrors the type() leaf above) keeps
                # alias-bearing expectations comparable as strings.
                return m.Tests.Payload(kind="atom", atom=str(value))
            case value if isinstance(value, (KeysView, ValuesView)):
                return to_p(list(value))
            case Mapping():
                entries: t.MutableMappingKV[str, m.Tests.Payload] = {}
                for key, item in value.items():
                    normalized_key = str(key)
                    if normalized_key in entries:
                        msg = (
                            f"Native payload mapping key collision: {normalized_key!r}"
                        )
                        raise ValueError(msg)
                    entries[normalized_key] = to_p(item)
                return m.Tests.Payload(kind="mapping", entries=entries)
            case list() | tuple() | set() | frozenset():
                children = tuple(to_p(item) for item in value)
                if isinstance(value, (set, frozenset)):
                    children = tuple(
                        sorted(
                            children, key=FlextTestsPayloadUtilities._stable_sort_key
                        )
                    )
                kind: t.Tests.PayloadKind
                if isinstance(value, list):
                    kind = "list"
                elif isinstance(value, tuple):
                    kind = "tuple"
                elif isinstance(value, set):
                    kind = "set"
                else:
                    kind = "frozenset"
                return m.Tests.Payload(kind=kind, items=children)
            case _:
                msg = f"Unsupported native payload leaf: {type(value).__name__}"
                raise TypeError(msg)

    @staticmethod
    def to_match_value(value: p.Tests.Payload) -> t.Tests.NativeMatchValue:
        """Project a native tree into the established list/mapping match semantics."""
        project = FlextTestsPayloadUtilities.to_match_value
        if value.kind == "atom":
            return value.atom
        if value.kind == "mapping":
            # Match values intentionally carry non-JSON sentinels (exceptions,
            # models, paths); NativeMatchValue stays JsonValue-only because
            # pyrefly cannot resolve a class-scoped self-referential alias.
            return {key: project(item) for key, item in value.entries.items()}  # pyrefly: ignore[bad-return]
        return [project(item) for item in value.items]  # pyrefly: ignore[bad-return]

    @staticmethod
    def to_normalized_value(value: p.Tests.Payload) -> t.JsonValue:
        """Project an owned tree at an explicit textual/metadata boundary."""
        to_n = FlextTestsPayloadUtilities.to_normalized_value
        if value.kind == "mapping":
            return u.normalize_to_metadata({
                key: to_n(item) for key, item in value.entries.items()
            })
        if value.kind != "atom":
            return u.normalize_to_metadata([to_n(item) for item in value.items])
        atom = value.atom
        if isinstance(atom, bytes):
            return atom.decode()
        if isinstance(atom, m.BaseModel | type | tzinfo):
            return str(atom)
        if atom is None or isinstance(atom, bool | datetime | Path | str | int | float):
            return u.normalize_to_metadata(atom)
        msg = f"Unsupported textual payload leaf: {type(atom).__name__}"
        raise TypeError(msg)

    @staticmethod
    def to_config_map(
        value: (
            m.BaseModel
            | t.MappingKV[str, t.Tests.TestobjectSerializable]
            | t.MappingKV[str, t.JsonPayload]
            | t.JsonMapping
        ),
    ) -> m.ConfigMap:
        """Convert a model or payload mapping to the canonical ConfigMap shape."""
        source = (
            value.model_dump(mode="python") if isinstance(value, m.BaseModel) else value
        )
        return m.ConfigMap.model_validate({
            key: (
                payload.atom
                if isinstance(
                    (payload := FlextTestsPayloadUtilities.to_payload(item)).atom,
                    m.BaseModel,
                )
                else FlextTestsPayloadUtilities.to_normalized_value(payload)
            )
            for key, item in source.items()
        })

    @staticmethod
    def path_node(
        subject: p.Tests.Payload, path: str, *, path_sep: str = "."
    ) -> p.Tests.Payload | None:
        """Walk an owned payload by path; ``None`` marks an absent path."""
        node = subject
        for segment in path.split(path_sep):
            if node.kind == "mapping":
                if segment not in node.entries:
                    return None
                node = node.entries[segment]
            elif node.kind != "atom":
                if not segment.lstrip("-").isdigit() or not (
                    -len(node.items) <= int(segment) < len(node.items)
                ):
                    return None
                node = node.items[int(segment)]
            elif hasattr(node.atom, segment):
                node = FlextTestsPayloadUtilities.to_payload(
                    getattr(node.atom, segment)
                )
            else:
                return None
        return node

    @staticmethod
    def deep_match(
        subject: p.Tests.Payload, spec: t.Tests.DeepSpec, *, path_sep: str = "."
    ) -> m.Tests.DeepMatchResult:
        """Match an owned payload tree against a path -> expectation spec.

        Literal expectations compare native projections; predicates receive the
        native value found at the path.
        """
        project = FlextTestsPayloadUtilities.to_match_value
        for path, expected in spec.items():
            node = FlextTestsPayloadUtilities.path_node(
                subject, path, path_sep=path_sep
            )
            if node is None:
                return m.Tests.DeepMatchResult(
                    path=path,
                    expected=expected,
                    actual=None,
                    matched=False,
                    reason=f"Path not found: {path}",
                )
            if isinstance(expected, m.Tests.Payload):
                if project(node) != project(expected):
                    return m.Tests.DeepMatchResult(
                        path=path,
                        expected=expected,
                        actual=node,
                        matched=False,
                        reason="Value mismatch",
                    )
            elif not expected(project(node)):
                return m.Tests.DeepMatchResult(
                    path=path,
                    expected="<predicate>",
                    actual=node,
                    matched=False,
                    reason="Predicate failed",
                )
        return m.Tests.DeepMatchResult(
            path="", expected=subject, actual=subject, matched=True, reason=""
        )

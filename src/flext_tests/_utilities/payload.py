"""Shared payload conversion helpers for flext_tests.

Low-level module with no dependency on flext_tests.utilities,
importable by both utilities.py and matchers.py without cycles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, tzinfo
from enum import Enum
from pathlib import Path

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
    def to_payload[ValueT](value: ValueT) -> m.Tests.Payload:
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
                | m.BaseModel()
            ):
                return m.Tests.Payload(kind="atom", atom=value)
            case BaseException():
                return m.Tests.Payload(kind="atom", atom=repr(value))
            case Mapping():
                entries: dict[str, m.Tests.Payload] = {}
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
    def to_match_value(
        value: p.Tests.Payload,
    ) -> (
        t.Tests.PayloadAtom
        | p.Model
        | p.Tests.NativeSequence
        | p.Tests.NativeMapping
        | None
    ):
        """Project a native tree into the established list/mapping match semantics."""
        project = FlextTestsPayloadUtilities.to_match_value
        if value.kind == "atom":
            return value.atom
        if value.kind == "mapping":
            return {key: project(item) for key, item in value.entries.items()}
        return [project(item) for item in value.items]

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
    def deep_match(
        obj: m.BaseModel | t.MappingKV[str, t.Tests.TestobjectSerializable],
        spec: t.Tests.DeepSpec,
        *,
        path_sep: str = ".",
    ) -> m.Tests.DeepMatchResult:
        """Match t.JsonValue against deep specification.

        Uses u.extract() for path extraction.
        Supports unlimited nesting depth via dot notation paths.

        Args:
            obj: Object to match against (dict or Pydantic model)
            spec: DeepSpec mapping of path -> expected value or predicate
            path_sep: Path separator (default: ".")

        Returns:
            DeepMatchResult with match status and details

        """
        source_obj = FlextTestsPayloadUtilities.to_config_map(obj)
        to_payload = FlextTestsPayloadUtilities.to_payload
        object_payload = to_payload(obj)
        for path, expected in spec.items():
            result = u.extract(source_obj, path, separator=path_sep)
            if result.failure:
                return m.Tests.DeepMatchResult(
                    path=path,
                    expected=expected,
                    actual=None,
                    matched=False,
                    reason=f"Path not found: {path}",
                )
            actual = result.value
            actual_payload = to_payload(actual)
            if callable(expected):
                if not expected(actual_payload):
                    return m.Tests.DeepMatchResult(
                        path=path,
                        expected="<predicate>",
                        actual=actual_payload,
                        matched=False,
                        reason="Predicate failed",
                    )
            elif actual != expected:
                return m.Tests.DeepMatchResult(
                    path=path,
                    expected=expected,
                    actual=actual_payload,
                    matched=False,
                    reason="Value mismatch",
                )
        return m.Tests.DeepMatchResult(
            path="",
            expected=object_payload,
            actual=object_payload,
            matched=True,
            reason="",
        )

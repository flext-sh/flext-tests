"""Shared payload conversion helpers for flext_tests.

Low-level module with no dependency on flext_tests.utilities,
importable by both utilities.py and matchers.py without cycles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import ClassVar

from flext_core import u
from flext_tests._typings.base import FlextTestsBaseTypesMixin
from flext_tests._typings.matchers import FlextTestsMatchersTypesMixin
from flext_tests.constants import FlextTestsConstants as c
from flext_tests.models import FlextTestsModels as m
from flext_tests.protocols import FlextTestsProtocols as p
from flext_tests.typings import FlextTestsTypes as t


class FlextTestsPayloadUtilities:
    """Namespace class for shared payload conversion helpers in flext_tests."""

    _SCALAR_PAYLOAD: ClassVar[tuple[type, ...]] = (
        str,
        int,
        float,
        bool,
        bytes,
        datetime,
        Path,
        m.BaseModel,
    )

    @staticmethod
    def to_payload(
        value: p.AttributeProbe,
    ) -> FlextTestsBaseTypesMixin.TestobjectSerializable:
        """Recursively flatten any runtime value to ``TestobjectSerializable``."""
        to_p = FlextTestsPayloadUtilities.to_payload
        match value:
            case m.RootModel():
                result = to_p(value.root)
            case Enum():
                result = to_p(value.value)
            case None:
                result = None
            case (
                str()
                | int()
                | float()
                | bool()
                | bytes()
                | datetime()
                | Path()
                | m.BaseModel()
            ):
                result = value
            case Mapping():
                normalized_map = {str(k): to_p(v) for k, v in value.items()}
                try:
                    validated_map = FlextTestsBaseTypesMixin.TESTOBJECT_MAPPING_ADAPTER.validate_python(
                        normalized_map,
                    )
                except c.ValidationError:
                    result = normalized_map
                else:
                    result = {k: to_p(v) for k, v in validated_map.items()}
            case list() | tuple() | set():
                normalized_seq = [to_p(item) for item in value]
                try:
                    validated_seq = FlextTestsBaseTypesMixin.TESTOBJECT_SEQUENCE_ADAPTER.validate_python(
                        normalized_seq,
                    )
                except c.ValidationError:
                    result = normalized_seq
                else:
                    result = [to_p(item) for item in validated_seq]
            case _:
                result = str(value)
        return result

    @staticmethod
    def to_normalized_value(
        value: FlextTestsBaseTypesMixin.TestobjectSerializable,
    ) -> t.JsonValue:
        """Flatten to pure Container via canonical runtime helper."""
        to_n = FlextTestsPayloadUtilities.to_normalized_value
        match value:
            case m.RootModel():
                result = to_n(value.root)
            case m.BaseModel():
                result = str(value)
            case bytes():
                result = value.decode(errors="ignore")
            case datetime():
                result = value.isoformat()
            case Path():
                result = str(value)
            case Mapping():
                result = {key: to_n(item) for key, item in value.items()}
            case list() | tuple() | frozenset():
                result = [to_n(item) for item in value]
            case None:
                result = ""
            case str() | int() | float() | bool():
                result = value
            case _:
                result = str(value)
        return result

    @staticmethod
    def to_config_map(
        value: m.BaseModel
        | t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable],
    ) -> m.ConfigMap:
        """Convert a model or payload mapping to the canonical ConfigMap shape."""
        source = (
            value.model_dump(mode="python") if isinstance(value, m.BaseModel) else value
        )
        config_map: dict[str, t.JsonPayload] = {}
        for key, item in source.items():
            payload = FlextTestsPayloadUtilities.to_payload(item)
            if isinstance(payload, m.BaseModel):
                config_map[key] = payload
                continue
            normalized_value = FlextTestsPayloadUtilities.to_normalized_value(payload)
            config_map[key] = "" if normalized_value is None else normalized_value
        return m.ConfigMap.model_validate(config_map)

    @staticmethod
    def deep_match(
        obj: m.BaseModel
        | t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable],
        spec: FlextTestsMatchersTypesMixin.DeepSpec,
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
        payload_types = (
            str,
            int,
            float,
            bool,
            bytes,
            datetime,
            Path,
            m.BaseModel,
            Mapping,
            Sequence,
        )
        to_payload = FlextTestsPayloadUtilities.to_payload
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
            actual_payload = to_payload(
                actual if isinstance(actual, payload_types) else str(actual)
            )
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
            expected=to_payload(obj),
            actual=to_payload(obj),
            matched=True,
            reason="",
        )

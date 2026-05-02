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
    Sized,
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
        if isinstance(value, m.RootModel):
            return to_p(value.root)
        if isinstance(value, Enum):
            return to_p(value.value)
        if value is None or isinstance(
            value, FlextTestsPayloadUtilities._SCALAR_PAYLOAD
        ):
            return value
        if isinstance(value, Mapping):
            normalized_map = {str(k): to_p(v) for k, v in value.items()}
            try:
                validated_map = (
                    FlextTestsBaseTypesMixin.TESTOBJECT_MAPPING_ADAPTER.validate_python(
                        normalized_map,
                    )
                )
            except c.ValidationError:
                return normalized_map
            return {k: to_p(v) for k, v in validated_map.items()}
        if isinstance(value, (list, tuple, set)):
            normalized_seq = [to_p(item) for item in value]
            try:
                validated_seq = FlextTestsBaseTypesMixin.TESTOBJECT_SEQUENCE_ADAPTER.validate_python(
                    normalized_seq,
                )
            except c.ValidationError:
                return normalized_seq
            return [to_p(item) for item in validated_seq]
        return str(value)

    @staticmethod
    def to_normalized_value(
        value: FlextTestsBaseTypesMixin.TestobjectSerializable,
    ) -> t.JsonValue:
        """Flatten to pure Container via canonical runtime helper."""
        to_n = FlextTestsPayloadUtilities.to_normalized_value
        if isinstance(value, m.RootModel):
            return to_n(value.root)
        if isinstance(value, m.BaseModel):
            return str(value)
        if isinstance(value, bytes):
            return value.decode(errors="ignore")
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, Mapping):
            return {key: to_n(item) for key, item in value.items()}
        if isinstance(value, (list, tuple, frozenset)):
            return [to_n(item) for item in value]
        if value is None:
            return ""
        return value if isinstance(value, (str, int, float, bool)) else str(value)

    @staticmethod
    def to_config_map_value(
        value: FlextTestsBaseTypesMixin.TestobjectSerializable,
    ) -> t.JsonPayload:
        """Preserve BaseModel, else delegate to canonical Container flattening."""
        if isinstance(value, m.BaseModel):
            return value
        normalized_value = FlextTestsPayloadUtilities.to_normalized_value(value)
        return "" if normalized_value is None else normalized_value

    @staticmethod
    def length_validate(
        value: FlextTestsBaseTypesMixin.TestobjectSerializable,
        spec: int | tuple[int, int],
    ) -> bool:
        """Validate length against spec.

        Uses u.chk() for validation.
        Supports exact length (int) or range (tuple[int, int]).

        Args:
            value: Value to check length of (must have __len__)
            spec: LengthSpec - exact int or (min, max) tuple

        Returns:
            True if length matches spec, False otherwise

        """
        try:
            if not isinstance(value, Sized):
                return False
            actual_len = len(value)
        except TypeError:
            return False
        if isinstance(spec, int):
            return u.chk(actual_len, m.GuardCheckSpec(eq=spec))
        min_len, max_len = spec
        return u.chk(
            actual_len,
            m.GuardCheckSpec(gte=min_len, lte=max_len),
        )

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
        source_obj: m.ConfigMap
        if isinstance(obj, m.BaseModel):
            dumped = obj.model_dump(mode="python")
            source_obj = m.ConfigMap.model_validate({
                key: FlextTestsPayloadUtilities.to_config_map_value(
                    FlextTestsPayloadUtilities.to_payload(value),
                )
                for key, value in dumped.items()
            })
        else:
            source_obj = m.ConfigMap.model_validate({
                key: FlextTestsPayloadUtilities.to_config_map_value(value)
                for key, value in obj.items()
            })
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

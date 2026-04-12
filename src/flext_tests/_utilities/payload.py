"""Shared payload conversion helpers for flext_tests.

Low-level module with no dependency on flext_tests.utilities,
importable by both utilities.py and matchers.py without cycles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableMapping,
    Sequence,
    Sized,
)
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, RootModel, ValidationError

from flext_core import u
from flext_tests import m, t


class FlextTestsPayloadUtilities:
    """Namespace class for shared payload conversion helpers in flext_tests."""

    @staticmethod
    def to_payload(
        value: t.Tests.TestobjectSerializable
        | RootModel[t.Tests.TestobjectSerializable]
        | set[t.Tests.TestobjectSerializable]
        | type
        | None,
    ) -> t.Tests.TestobjectSerializable:
        """Convert a value to testobject.

        Args:
            value: value to convert

        Returns:
            t.RecursiveContainer suitable for test assertions

        """
        if isinstance(value, RootModel):
            empty_map: MutableMapping[str, t.Tests.TestobjectSerializable] = {}
            return empty_map
        if value is None or isinstance(
            value,
            (str, int, float, bool, bytes, datetime, Path, BaseModel),
        ):
            payload_value: t.Tests.TestobjectSerializable = value
            return payload_value
        if isinstance(value, Mapping):
            try:
                mapping_value = t.Tests.TESTOBJECT_MAPPING_ADAPTER.validate_python(
                    value,
                )
            except ValidationError:
                empty_map2: MutableMapping[str, t.Tests.TestobjectSerializable] = {}
                return empty_map2
            payload_map: MutableMapping[str, t.Tests.TestobjectSerializable] = {}
            for key_raw, item_obj in mapping_value.items():
                payload_map[str(key_raw)] = FlextTestsPayloadUtilities.to_payload(
                    item_obj,
                )
            return payload_map
        if isinstance(value, (list, tuple, set)):
            try:
                iterable_items: Sequence[t.Tests.TestobjectSerializable] = (
                    t.Tests.TESTOBJECT_SEQUENCE_ADAPTER.validate_python(
                        value,
                    )
                )
            except ValidationError:
                empty_seq: Sequence[t.Tests.TestobjectSerializable] = []
                return empty_seq
            payload_items: Sequence[t.Tests.TestobjectSerializable] = [
                FlextTestsPayloadUtilities.to_payload(item_obj)
                for item_obj in iterable_items
            ]
            return payload_items
        return str(value)

    @staticmethod
    def to_normalized_value(
        value: t.Tests.TestobjectSerializable,
    ) -> t.RecursiveContainer:
        """Convert _Testobject to pure NormalizedValue (no BaseModel in output)."""
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, datetime):
            return value
        if isinstance(value, Path):
            return value
        if isinstance(value, bytes):
            return value.decode(errors="ignore")
        if isinstance(value, BaseModel):
            return str(value)
        if isinstance(value, (dict, Mapping)):
            validated_map: Mapping[str, t.Tests.TestobjectSerializable] = (
                t.Tests.TESTOBJECT_MAPPING_ADAPTER.validate_python(value)
            )
            result_map: t.MutableRecursiveContainerMapping = {}
            for k, v in validated_map.items():
                key: str = str(k)
                val: t.Tests.TestobjectSerializable = v
                result_map[key] = FlextTestsPayloadUtilities.to_normalized_value(val)
            return result_map
        if isinstance(value, (list, tuple)):
            validated_seq: Sequence[t.Tests.TestobjectSerializable] = (
                t.Tests.TESTOBJECT_SEQUENCE_ADAPTER.validate_python(value)
            )
            result_seq: Sequence[t.RecursiveContainer] = [
                FlextTestsPayloadUtilities.to_normalized_value(item)
                for item in validated_seq
            ]
            return result_seq
        return str(value)

    @staticmethod
    def to_config_map_value(value: t.Tests.TestobjectSerializable) -> t.ValueOrModel:
        """Convert value to NormalizedValue or BaseModel for AccessibleData compatibility."""
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, BaseModel):
            return value
        if isinstance(value, bytes):
            return value.decode(errors="ignore")
        if isinstance(value, datetime):
            return value
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, (dict, Mapping)):
            validated_map: Mapping[str, t.Tests.TestobjectSerializable] = (
                t.Tests.TESTOBJECT_MAPPING_ADAPTER.validate_python(value)
            )
            cfg_map: t.MutableRecursiveContainerMapping = {}
            for k, v in validated_map.items():
                key: str = str(k)
                val: t.Tests.TestobjectSerializable = v
                cfg_map[key] = FlextTestsPayloadUtilities.to_normalized_value(val)
            return cfg_map
        if isinstance(value, (list, tuple)):
            validated_seq: Sequence[t.Tests.TestobjectSerializable] = (
                t.Tests.TESTOBJECT_SEQUENCE_ADAPTER.validate_python(value)
            )
            cfg_seq: Sequence[t.RecursiveContainer] = [
                FlextTestsPayloadUtilities.to_normalized_value(item)
                for item in validated_seq
            ]
            return cfg_seq
        return str(value)

    @staticmethod
    def length_validate(
        value: t.Tests.TestobjectSerializable,
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
        obj: BaseModel | Mapping[str, t.Tests.TestobjectSerializable],
        spec: t.Tests.DeepSpec,
        *,
        path_sep: str = ".",
    ) -> m.Tests.DeepMatchResult:
        """Match t.RecursiveContainer against deep specification.

        Uses u.extract() for path extraction.
        Supports unlimited nesting depth via dot notation paths.

        Args:
            obj: Object to match against (dict or Pydantic model)
            spec: DeepSpec mapping of path -> expected value or predicate
            path_sep: Path separator (default: ".")

        Returns:
            DeepMatchResult with match status and details

        """
        source_obj: Mapping[str, t.ValueOrModel]
        if isinstance(obj, BaseModel):
            dumped = obj.model_dump(mode="python")
            source_obj = {
                str(key): FlextTestsPayloadUtilities.to_config_map_value(
                    FlextTestsPayloadUtilities.to_payload(value),
                )
                for key, value in dumped.items()
            }
        else:
            source_obj = {
                str(key): FlextTestsPayloadUtilities.to_config_map_value(value)
                for key, value in obj.items()
            }
        for path, expected in spec.items():
            result = u.extract(
                source_obj,
                path,
                separator=path_sep,
            )
            if result.failure:
                return m.Tests.DeepMatchResult(
                    path=path,
                    expected=expected,
                    actual=None,
                    matched=False,
                    reason=f"Path not found: {path}",
                )
            actual = result.value
            if callable(expected):
                actual_payload = (
                    FlextTestsPayloadUtilities.to_payload(actual)
                    if isinstance(
                        actual,
                        (
                            str,
                            int,
                            float,
                            bool,
                            bytes,
                            datetime,
                            Path,
                            BaseModel,
                            Mapping,
                            Sequence,
                        ),
                    )
                    else FlextTestsPayloadUtilities.to_payload(str(actual))
                )
                if not expected(actual_payload):
                    return m.Tests.DeepMatchResult(
                        path=path,
                        expected="<predicate>",
                        actual=actual_payload,
                        matched=False,
                        reason="Predicate failed",
                    )
            elif actual != expected:
                actual_payload = (
                    FlextTestsPayloadUtilities.to_payload(actual)
                    if isinstance(
                        actual,
                        (
                            str,
                            int,
                            float,
                            bool,
                            bytes,
                            datetime,
                            Path,
                            BaseModel,
                            Mapping,
                            Sequence,
                        ),
                    )
                    else FlextTestsPayloadUtilities.to_payload(str(actual))
                )
                return m.Tests.DeepMatchResult(
                    path=path,
                    expected=expected,
                    actual=actual_payload,
                    matched=False,
                    reason="Value mismatch",
                )
        return m.Tests.DeepMatchResult(
            path="",
            expected=FlextTestsPayloadUtilities.to_payload(obj),
            actual=FlextTestsPayloadUtilities.to_payload(obj),
            matched=True,
            reason="",
        )

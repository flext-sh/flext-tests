"""Shared payload conversion helpers for flext_tests.

Low-level module with no dependency on flext_tests.utilities,
importable by both utilities.py and matchers.py without cycles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence, Sized
from datetime import datetime
from pathlib import Path

from flext_core import FlextUtilities, m as core_m
from pydantic import BaseModel, ConfigDict, RootModel, TypeAdapter, ValidationError

from flext_tests.models import FlextTestsModels as m
from flext_tests.typings import FlextTestsTypes as t

_ARBTYPES = ConfigDict(arbitrary_types_allowed=True)
_PAYLOAD_MAPPING_ADAPTER = TypeAdapter(dict[str, t.Tests.Testobject], config=_ARBTYPES)
_PAYLOAD_SEQUENCE_ADAPTER = TypeAdapter(
    list[t.Tests.Testobject],
    config=_ARBTYPES,
)


def to_payload(
    value: t.Tests.Testobject
    | RootModel[t.Tests.Testobject]
    | set[t.Tests.Testobject]
    | type
    | None,
) -> t.Tests.Testobject:
    """Convert a value to testobject.

    Args:
        value: value to convert

    Returns:
        t.NormalizedValue suitable for test assertions

    """
    if isinstance(value, RootModel):
        return {}
    if value is None or isinstance(
        value,
        (str, int, float, bool, bytes, datetime, Path, BaseModel),
    ):
        payload_value: t.Tests.Testobject = value
        return payload_value
    if isinstance(value, Mapping):
        try:
            mapping_value = _PAYLOAD_MAPPING_ADAPTER.validate_python(value)
        except ValidationError:
            return {}
        payload_map: dict[str, t.Tests.Testobject] = {}
        for key_raw, item_obj in mapping_value.items():
            payload_map[str(key_raw)] = to_payload(item_obj)
        return payload_map
    if isinstance(value, (list, tuple, set)):
        try:
            iterable_items: list[t.Tests.Testobject] = (
                _PAYLOAD_SEQUENCE_ADAPTER.validate_python(value)
            )
        except ValidationError:
            return []
        payload_items: list[t.Tests.Testobject] = [
            to_payload(item_obj) for item_obj in iterable_items
        ]
        return payload_items
    return str(value)


def to_normalized_value(value: t.Tests.Testobject) -> t.NormalizedValue:
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
    if isinstance(value, Mapping):
        return {str(k): to_normalized_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_normalized_value(item) for item in value]
    return str(value)


def to_config_map_value(value: t.Tests.Testobject) -> t.NormalizedValue | BaseModel:
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
    if isinstance(value, Mapping):
        return {str(k): to_normalized_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_normalized_value(item) for item in value]
    return str(value)


def length_validate(
    value: t.Tests.Testobject,
    spec: int | tuple[int, int],
) -> bool:
    """Validate length against spec.

    Uses FlextUtilities.chk() for validation.
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
        return FlextUtilities.chk(actual_len, core_m.GuardCheckSpec(eq=spec))
    min_len, max_len = spec
    return FlextUtilities.chk(
        actual_len,
        core_m.GuardCheckSpec(gte=min_len, lte=max_len),
    )


def deep_match(
    obj: BaseModel | Mapping[str, t.Tests.Testobject],
    spec: Mapping[
        str,
        t.Tests.Testobject | Callable[[t.Tests.Testobject], bool],
    ],
    *,
    path_sep: str = ".",
) -> m.Tests.DeepMatchResult:
    """Match t.NormalizedValue against deep specification.

    Uses FlextUtilities.extract() for path extraction.
    Supports unlimited nesting depth via dot notation paths.

    Args:
        obj: Object to match against (dict or Pydantic model)
        spec: DeepSpec mapping of path -> expected value or predicate
        path_sep: Path separator (default: ".")

    Returns:
        DeepMatchResult with match status and details

    """
    source_obj: dict[str, t.NormalizedValue | BaseModel]
    if isinstance(obj, BaseModel):
        dumped = obj.model_dump(mode="python")
        source_obj = {
            str(key): to_config_map_value(to_payload(value))
            for key, value in dumped.items()
        }
    else:
        source_obj = {
            str(key): to_config_map_value(value) for key, value in obj.items()
        }
    for path, expected in spec.items():
        result = FlextUtilities.extract(
            source_obj,
            path,
            separator=path_sep,
        )
        if result.is_failure:
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
                to_payload(actual)
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
                else to_payload(str(actual))
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
                to_payload(actual)
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
                else to_payload(str(actual))
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
        expected=to_payload(obj),
        actual=to_payload(obj),
        matched=True,
        reason="",
    )

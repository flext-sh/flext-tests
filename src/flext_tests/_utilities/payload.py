"""Shared payload conversion helpers for flext_tests.

Low-level module with no dependency on flext_tests.utilities,
importable by both utilities.py and matchers.py without cycles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, KeysView, Mapping, ValuesView
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
    MappingProxyType,
    ModuleType,
    UnionType,
)
from typing import TYPE_CHECKING, Final, TypeAliasType

import flext_tests
from flext_core import m, u
from flext_tests import p, t
from flext_tests._models.base import FlextTestsFlextModelsBase

if TYPE_CHECKING:
    from flext_tests._models.matchers import FlextTestsMatchersModelsMixin


class FlextTestsFlextUtilitiesPayload:
    """Canonical namespace owner."""

    _PAYLOAD_SEQUENCE_KINDS: Final[t.MappingKV[type, t.Tests.PayloadKind]] = (
        MappingProxyType({
            list: "list",
            tuple: "tuple",
            set: "set",
            frozenset: "frozenset",
        })
    )

    @staticmethod
    def _stable_sort_key(value: p.Tests.Payload) -> t.StrPair:
        """Return a total deterministic key for heterogeneous payload values."""
        native = FlextTestsPayloadUtilities.to_match_value(
            value,
        )
        return type(native).__name__, str(native)

    @staticmethod
    def _payload_model_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own matcher model leaves (payload, root model, enum) recursively.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.
        """
        if isinstance(
            value,
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
        ):
            return value
        if isinstance(value, m.RootModel):
            return FlextTestsPayloadUtilities.to_payload(
                value.root,
            )
        if isinstance(value, Enum):
            return FlextTestsPayloadUtilities.to_payload(
                value.value,
            )
        return None

    @staticmethod
    def _payload_none_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own ``None`` as the canonical empty atom.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.
        """
        if value is None:
            return FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload(
                kind="atom",
                atom=None,
            )
        return None

    @staticmethod
    def _payload_scalar_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own supported native scalars and model leaves as atoms.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.
        """
        if isinstance(
            value,
            (
                str,
                int,
                float,
                bool,
                bytes,
                datetime,
                tzinfo,
                Path,
                type,
                BaseException,
                p.Model,
            ),
        ):
            return FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload(
                kind="atom",
                atom=value,
            )
        return None

    @staticmethod
    def _payload_annotated_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own ``typing.Annotated`` constructs as their textual atom.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.
        """
        if hasattr(value, "__metadata__") and hasattr(value, "__origin__"):
            # typing.Annotated[...] constructs are type-level atoms under
            # the same textual convention as the alias arm below.
            return FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload(
                kind="atom",
                atom=str(value),
            )
        return None

    @staticmethod
    def _payload_match_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own a regex match through its matched text.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.
        """
        if isinstance(value, Match):
            # A regex match compares by its matched text — the pattern
            # contract (semver, id shape) is what an expectation asserts.
            return FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload(
                kind="atom",
                atom=value.group(0),
            )
        return None

    @staticmethod
    def _payload_runtime_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own typing constructs and runtime machinery as textual atoms.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.
        """
        if isinstance(
            value,
            (
                GenericAlias,
                UnionType,
                TypeAliasType,
                FunctionType,
                BuiltinFunctionType,
                CodeType,
                ModuleType,
                ModuleSpec,
            ),
        ):
            # Typing constructs and runtime machinery (functions, modules,
            # code specs) are type-level atoms: the established textual
            # convention (mirrors the type() leaf above) keeps
            # alias-bearing expectations comparable as strings.
            return FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload(
                kind="atom",
                atom=str(value),
            )
        return None

    @staticmethod
    def _payload_view_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own dict and set views through their native iteration order.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.
        """
        if isinstance(value, (KeysView, ValuesView)):
            return FlextTestsPayloadUtilities.to_payload(
                list(value),
            )
        return None

    @staticmethod
    def _payload_mapping_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own a native mapping with stringified, collision-checked keys.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.

        Raises:
            ValueError: If Native payload mapping key collision.
        """
        if not isinstance(value, Mapping):
            return None
        entries: t.MutableMappingKV[
            str,
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
        ] = {}
        for key, item in value.items():
            normalized_key = str(key)
            if normalized_key in entries:
                msg = f"Native payload mapping key collision: {normalized_key!r}"
                raise ValueError(msg)
            entries[normalized_key] = FlextTestsPayloadUtilities.to_payload(
                item,
            )
        return FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload(
            kind="mapping",
            entries=entries,
        )

    @staticmethod
    def _payload_sequence_leaf(
        value: p.AttributeProbe,
    ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None:
        """Own a native sequence or set with deterministic set ordering.

        Returns:
            The resulting
                ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None``.
        """
        if not isinstance(value, (list, tuple, set, frozenset)):
            return None
        children = tuple(FlextTestsPayloadUtilities.to_payload(item) for item in value)
        if isinstance(value, (set, frozenset)):
            children = tuple(
                sorted(
                    children,
                    key=FlextTestsFlextUtilitiesPayload._stable_sort_key,
                ),
            )
        for (
            sequence_type,
            kind,
        ) in FlextTestsFlextUtilitiesPayload._PAYLOAD_SEQUENCE_KINDS:
            if isinstance(value, sequence_type):
                return FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload(
                    kind=kind,
                    items=children,
                )
        return None

    _PAYLOAD_LEAF_HANDLERS: Final[
        tuple[
            Callable[
                [p.AttributeProbe],
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            ],
            ...,
        ]
    ] = (
        _payload_model_leaf,
        _payload_none_leaf,
        _payload_scalar_leaf,
        _payload_annotated_leaf,
        _payload_match_leaf,
        _payload_runtime_leaf,
        _payload_view_leaf,
        _payload_mapping_leaf,
        _payload_sequence_leaf,
    )

    class FlextTestsPayloadUtilities:
        """Namespace class for shared payload conversion helpers in flext_tests."""

        @staticmethod
        def to_payload(
            value: p.AttributeProbe,
        ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload:
            """Own supported native values without serializing their model leaves.

            Returns:
                The resulting
                    ``FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload``.

            Raises:
                TypeError: If Unsupported native payload leaf.
            """
            for handler in FlextTestsFlextUtilitiesPayload._PAYLOAD_LEAF_HANDLERS:
                payload = handler(value)
                if payload is not None:
                    return payload
            msg = f"Unsupported native payload leaf: {type(value).__name__}"
            raise TypeError(msg)

        @staticmethod
        def to_match_value(value: p.Tests.Payload) -> t.Tests.NativeMatchValue:
            """Project a native tree into the established list/mapping match semantics.

            Returns:
                The resulting ``t.Tests.NativeMatchValue``.
            """
            project = FlextTestsPayloadUtilities.to_match_value
            if value.kind == "atom":
                return value.atom
            if value.kind == "mapping":
                # Match values intentionally carry non-JSON sentinels (exceptions,
                # models, paths); NativeMatchValue stays JsonValue-only because
                # pyrefly cannot resolve a class-scoped self-referential alias.
                pairs = value.entries.items()
                return {key: project(item) for key, item in pairs}
            items = value.items
            return [project(item) for item in items]  # pyrefly: ignore[bad-return]

        @staticmethod
        def to_normalized_value(value: p.Tests.Payload) -> t.JsonValue:
            """Project an owned tree at an explicit textual/metadata boundary.

            Returns:
                The resulting ``t.JsonValue``.

            Raises:
                TypeError: If Unsupported textual payload leaf.
            """
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
            if atom is None or isinstance(
                atom,
                bool | datetime | Path | str | int | float,
            ):
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
            """Convert a model or payload mapping to the canonical ConfigMap shape.

            Returns:
                The resulting ``m.ConfigMap``.
            """
            source = (
                value.model_dump(mode="python")
                if isinstance(value, m.BaseModel)
                else value
            )
            return m.ConfigMap.model_validate({
                key: (
                    payload.atom
                    if isinstance(
                        (
                            payload := FlextTestsPayloadUtilities.to_payload(
                                item,
                            )
                        ).atom,
                        m.BaseModel,
                    )
                    else FlextTestsPayloadUtilities.to_normalized_value(
                        payload,
                    )
                )
                for key, item in source.items()
            })

        @staticmethod
        def path_node(
            subject: p.Tests.Payload,
            path: str,
            *,
            path_sep: str = ".",
        ) -> p.Tests.Payload | None:
            """Walk an owned payload by path; ``None`` marks an absent path.

            Returns:
                The resulting ``p.Tests.Payload | None``.
            """
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
                        getattr(node.atom, segment),
                    )
                else:
                    return None
            return node

        @staticmethod
        def extract_path_value(subject: p.Tests.Payload, path: str) -> p.Tests.Payload:
            """Read nested payload nodes without serializing model leaves.

            Returns:
                The resulting ``p.Tests.Payload``.

            Raises:
                AssertionError: If Path not found.
            """
            node = FlextTestsPayloadUtilities.path_node(
                subject,
                path,
            )
            if node is None:
                msg = f"Path not found: {path}"
                raise AssertionError(msg)
            return node

        @staticmethod
        def deep_match(
            subject: p.Tests.Payload,
            spec: t.Tests.DeepSpec,
            *,
            path_sep: str = ".",
        ) -> FlextTestsMatchersModelsMixin.DeepMatchResult:
            """Match an owned payload tree against a path -> expectation spec.

            Literal expectations compare native projections; predicates receive the
            native value found at the path.

            Returns:
                The resulting ``m.Tests.DeepMatchResult``.
            """
            # ``DeepMatchResult`` is owned by ``flext_tests._models.matchers``, whose
            # module top-level imports this module: resolving the model through the
            # lazy ``flext_tests.m`` attribute here (never an import statement)
            # keeps both import orders cycle-free.
            result_model = flext_tests.m.Tests.DeepMatchResult
            project = FlextTestsPayloadUtilities.to_match_value
            for path, expected in spec.items():
                node = FlextTestsPayloadUtilities.path_node(
                    subject,
                    path,
                    path_sep=path_sep,
                )
                if node is None:
                    return result_model(
                        path=path,
                        expected=expected,
                        actual=None,
                        matched=False,
                        reason=f"Path not found: {path}",
                    )
                if isinstance(
                    expected,
                    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
                ):
                    if project(node) != project(expected):
                        return result_model(
                            path=path,
                            expected=expected,
                            actual=node,
                            matched=False,
                            reason="Value mismatch",
                        )
                elif not expected(project(node)):
                    return result_model(
                        path=path,
                        expected="<predicate>",
                        actual=node,
                        matched=False,
                        reason="Predicate failed",
                    )
            return result_model(
                path="",
                expected=subject,
                actual=subject,
                matched=True,
                reason="",
            )


FlextTestsPayloadUtilities = FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities

__all__: list[str] = [
    "FlextTestsFlextUtilitiesPayload",
    "FlextTestsPayloadUtilities",
]

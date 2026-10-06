"""File-comparison parsing helpers for FlextTestsFiles.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import r
from flext_tests import c, m, t, u
from flext_tests._utilities._files._creation import FlextTestsFilesCreationMixin
from flext_tests._utilities.payload import FlextTestsFlextUtilitiesPayload

if TYPE_CHECKING:
    from flext_tests.protocols import p


class FlextTestsFilesComparisonMixin:
    """Compare two files by content, lines, size, hash, or deep structure."""

    type ParsedPair = tuple[
        t.MappingKV[str, t.Tests.TestobjectSerializable],
        t.MappingKV[str, t.Tests.TestobjectSerializable],
    ]

    @staticmethod
    def _read_both(params: m.Tests.CompareParams) -> t.StrPair:
        enc = c.Tests.DEFAULT_ENCODING
        return (
            params.file1.read_text(encoding=enc),
            params.file2.read_text(encoding=enc),
        )

    @staticmethod
    def _parse_both(
        content1: str,
        content2: str,
        fmt: str,
    ) -> p.Result[FlextTestsFilesComparisonMixin.ParsedPair]:
        """Parse both contents as mappings in the given format.

        Returns:
            The resulting ``p.Result[FlextTestsFilesComparisonMixin.ParsedPair]``.
        """
        parse = (
            u.Cli.json_parse
            if fmt == c.Tests.FILE_FORMAT_JSON
            else u.Cli.yaml_parse
            if fmt == c.Tests.FILE_FORMAT_YAML
            else None
        )
        if parse is None:
            return r[FlextTestsFilesComparisonMixin.ParsedPair].fail(
                f"unsupported comparison format: {fmt}",
            )
        # Each parser reports its own failure; that failure is the result.
        r1 = parse(content1)
        if r1.failure:
            return r[FlextTestsFilesComparisonMixin.ParsedPair].from_failure(r1)
        r2 = parse(content2)
        if r2.failure:
            return r[FlextTestsFilesComparisonMixin.ParsedPair].from_failure(r2)
        d1, d2 = r1.value, r2.value
        if FlextTestsFilesCreationMixin.matches_native_mapping(
            d1,
        ) and FlextTestsFilesCreationMixin.matches_native_mapping(d2):
            return r[FlextTestsFilesComparisonMixin.ParsedPair].ok((
                FlextTestsFilesCreationMixin.to_payload_mapping(d1),
                FlextTestsFilesCreationMixin.to_payload_mapping(d2),
            ))
        return r[FlextTestsFilesComparisonMixin.ParsedPair].fail(
            "comparison contents are not both mappings",
        )

    @staticmethod
    def _apply_key_filtering(
        dict1: t.MappingKV[str, t.Tests.TestobjectSerializable],
        dict2: t.MappingKV[str, t.Tests.TestobjectSerializable],
        keys: t.StrSequence | None,
        exclude_keys: t.StrSequence | None,
    ) -> tuple[
        t.MappingKV[str, t.Tests.TestobjectSerializable],
        t.MappingKV[str, t.Tests.TestobjectSerializable],
    ]:
        """Apply key filtering to both dicts if specified.

        Returns:
            The resulting ``tuple[t.MappingKV[str, t.Tests.TestobjectSerializable],
                t.MappingKV[str, t.Tests.TestobjectSerializable]]``.
        """
        if keys is None and exclude_keys is None:
            return (dict1, dict2)
        filter_keys_set = set(keys) if keys is not None else None
        exclude_keys_set = set(exclude_keys) if exclude_keys is not None else None
        result1 = u.transform(
            FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_config_map(
                dict1
            ),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        result2 = u.transform(
            FlextTestsFlextUtilitiesPayload.FlextTestsPayloadUtilities.to_config_map(
                dict2
            ),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        if result1.success and result2.success:
            filtered1 = FlextTestsFilesCreationMixin.to_payload_mapping(result1.value)
            filtered2 = FlextTestsFilesCreationMixin.to_payload_mapping(result2.value)
            return (filtered1, filtered2)
        return (dict1, dict2)


__all__: list[str] = ["FlextTestsFilesComparisonMixin"]

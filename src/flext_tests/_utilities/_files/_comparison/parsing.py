"""File-comparison parsing helpers for FlextTestsFiles.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Annotated

from flext_core import r

from flext_tests import c, m, t, u
from flext_tests._utilities import FlextTestsUtilitiesPayload
from flext_tests._utilities._files import FlextTestsUtilitiesFilesCreation

if TYPE_CHECKING:
    from flext_core import p


class FlextTestsUtilitiesFilesComparisonParsing:
    """Compare two files by content, lines, size, hash, or deep structure."""

    class CompareOptions(m.Value):
        """Grouped comparison knobs for ``compare``."""

        mode: Annotated[
            c.Tests.CompareMode,
            m.Field(description="Comparison mode."),
        ] = c.Tests.CompareMode.CONTENT
        ignore_ws: Annotated[
            bool,
            m.Field(description="Ignore whitespace in comparison."),
        ] = False
        ignore_case: Annotated[
            bool,
            m.Field(description="Case-insensitive comparison."),
        ] = False
        pattern: Annotated[
            str | None,
            m.Field(description="Pattern to check if both files contain."),
        ] = None
        deep: Annotated[
            bool,
            m.Field(description="Use deep comparison for nested structures."),
        ] = True
        keys: Annotated[
            Sequence[str] | None,
            m.Field(description="Only compare these keys."),
        ] = None
        exclude_keys: Annotated[
            Sequence[str] | None,
            m.Field(description="Exclude these keys from comparison."),
        ] = None

    @staticmethod
    def _read_both(params: m.Tests.CompareParams) -> tuple[str, str]:
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
    ) -> p.Result[t.Tests.ParsedPair]:
        """Parse both contents as mappings in the given format.

        Returns:
            The resulting ``p.Result[t.Tests.ParsedPair]``.

        """
        parse = (
            u.Cli.json_parse
            if fmt == c.Tests.FILE_FORMAT_JSON
            else u.Cli.yaml_parse
            if fmt == c.Tests.FILE_FORMAT_YAML
            else None
        )
        if parse is None:
            return r[t.Tests.ParsedPair].fail(
                f"unsupported comparison format: {fmt}",
            )
        # Each parser reports its own failure; that failure is the result.
        r1 = parse(content1)
        if r1.failure:
            return r[t.Tests.ParsedPair].from_failure(r1)
        r2 = parse(content2)
        if r2.failure:
            return r[t.Tests.ParsedPair].from_failure(r2)
        d1, d2 = r1.value, r2.value
        if FlextTestsUtilitiesFilesCreation.matches_native_mapping(
            d1,
        ) and FlextTestsUtilitiesFilesCreation.matches_native_mapping(d2):
            return r[t.Tests.ParsedPair].ok((
                FlextTestsUtilitiesFilesCreation.to_payload_mapping(d1),
                FlextTestsUtilitiesFilesCreation.to_payload_mapping(d2),
            ))
        return r[t.Tests.ParsedPair].fail(
            "comparison contents are not both mappings",
        )

    @staticmethod
    def _apply_key_filtering(
        dict1: Mapping[str, t.Tests.TestobjectSerializable],
        dict2: Mapping[str, t.Tests.TestobjectSerializable],
        keys: Sequence[str] | None,
        exclude_keys: Sequence[str] | None,
    ) -> tuple[
        Mapping[str, t.Tests.TestobjectSerializable],
        Mapping[str, t.Tests.TestobjectSerializable],
    ]:
        """Apply key filtering to both dicts if specified.

        Returns:
            The resulting ``tuple[Mapping[str, t.Tests.TestobjectSerializable],
                Mapping[str, t.Tests.TestobjectSerializable]]``.

        """
        if keys is None and exclude_keys is None:
            return (dict1, dict2)
        filter_keys_set = set(keys) if keys is not None else None
        exclude_keys_set = set(exclude_keys) if exclude_keys is not None else None
        result1 = u.transform(
            FlextTestsUtilitiesPayload.to_config_map(
                dict1,
            ),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        result2 = u.transform(
            FlextTestsUtilitiesPayload.to_config_map(
                dict2,
            ),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        if result1.success and result2.success:
            filtered1 = FlextTestsUtilitiesFilesCreation.to_payload_mapping(
                result1.value
            )
            filtered2 = FlextTestsUtilitiesFilesCreation.to_payload_mapping(
                result2.value
            )
            return (filtered1, filtered2)
        return (dict1, dict2)


__all__: list[str] = ["FlextTestsUtilitiesFilesComparisonParsing"]

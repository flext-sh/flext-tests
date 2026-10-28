"""Facade for FlextTestsUtilitiesFilesComparison.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Mapping
from pathlib import Path

from flext_core import r

from flext_tests import c, m, p, t, u
from flext_tests._utilities import FlextTestsUtilitiesPayload
from flext_tests._utilities._files._comparison import (
    FlextTestsUtilitiesFilesComparisonParsing,
)


class FlextTestsUtilitiesFilesComparison(
    FlextTestsUtilitiesFilesComparisonParsing,
):
    """Compose the comparison domain through its native MRO.

    Extends the parsing helpers from ``parsing`` with the
    dispatch, mode comparison, and deep-compare methods.
    """

    def compare(
        self,
        file1: Path,
        file2: Path,
        *,
        options: FlextTestsUtilitiesFilesComparison.CompareOptions | None = None,
    ) -> p.Result[bool]:
        """Compare two files under the configured comparison options.

        Args:
            file1: The first file to compare.
            file2: The second file to compare.
            options: Optional comparison options; defaults apply when omitted.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        compare_options = (
            options
            if options is not None
            else FlextTestsUtilitiesFilesComparison.CompareOptions()
        )
        try:
            params = m.Tests.CompareParams.model_validate({
                "file1": file1,
                "file2": file2,
                "mode": compare_options.mode,
                "ignore_ws": compare_options.ignore_ws,
                "ignore_case": compare_options.ignore_case,
                "pattern": compare_options.pattern,
                c.MergeStrategy.DEEP: compare_options.deep,
                "keys": compare_options.keys,
                "exclude_keys": compare_options.exclude_keys,
            })
        except c.EXC_BASIC_TYPE as exc:
            return r[bool].fail(
                f"Invalid parameters for file comparison: {exc}",
                exception=exc,
            )
        if not params.file1.exists():
            return r[bool].fail(c.Tests.ERROR_FILE_NOT_FOUND.format(path=params.file1))
        if not params.file2.exists():
            return r[bool].fail(c.Tests.ERROR_FILE_NOT_FOUND.format(path=params.file2))
        try:
            result = self._compare_existing(params)
        except OSError as e:
            result = r[bool].fail(c.Tests.ERROR_COMPARE.format(error=e))
        return result

    def _compare_existing(self, params: m.Tests.CompareParams) -> p.Result[bool]:
        """Compare two existing files using the requested comparison mode.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        if params.pattern is not None:
            text1 = params.file1.read_text(encoding=c.Tests.DEFAULT_ENCODING)
            text2 = params.file2.read_text(encoding=c.Tests.DEFAULT_ENCODING)
            return r[bool].ok(params.pattern in text1 and params.pattern in text2)
        match params.mode:
            case "size":
                return r[bool].ok(
                    params.file1.stat().st_size == params.file2.stat().st_size,
                )
            case "hash":
                hash1 = u.Cli.sha256_file(params.file1)
                hash2 = u.Cli.sha256_file(params.file2)
                return r[bool].ok(hash1 == hash2)
            case "lines":
                return self._compare_lines(params)
            case _:
                return self._compare_content(params)

    def _compare_content(self, params: m.Tests.CompareParams) -> p.Result[bool]:
        """Compare file content with optional deep/structured comparison.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        c1, c2 = self._read_both(params)
        # Structured comparison is selected by the files' declared format,
        # never by trial: both JSON or both YAML compare as mappings and a
        # parse error is the result; any other pair compares as text.
        fmt = u.Cli.files_detect_format_from_path(params.file1)
        if (
            params.deep
            and fmt == u.Cli.files_detect_format_from_path(params.file2)
            and fmt in {c.Tests.FILE_FORMAT_JSON, c.Tests.FILE_FORMAT_YAML}
        ):
            structured = self._parse_both(c1, c2, fmt)
            if structured.failure:
                return r[bool].from_failure(structured)
            dict1, dict2 = structured.value
            return self._deep_compare_mappings(dict1, dict2, params)
        if params.ignore_ws:
            c1, c2 = "".join(c1.split()), "".join(c2.split())
        if params.ignore_case:
            c1, c2 = c1.lower(), c2.lower()
        return r[bool].ok(c1 == c2)

    @staticmethod
    def _deep_compare_mappings(
        dict1: Mapping[str, t.Tests.TestobjectSerializable],
        dict2: Mapping[str, t.Tests.TestobjectSerializable],
        params: m.Tests.CompareParams,
    ) -> p.Result[bool]:
        """Deeply compare already-parsed structured mappings.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        filter_keys_set = set(params.keys) if params.keys is not None else None
        exclude_keys_set = (
            set(params.exclude_keys) if params.exclude_keys is not None else None
        )
        left_result = u.transform(
            FlextTestsUtilitiesPayload.FlextTestsUtilitiesPayload.to_config_map(
                dict1,
            ),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        right_result = u.transform(
            FlextTestsUtilitiesPayload.FlextTestsUtilitiesPayload.to_config_map(
                dict2,
            ),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        if left_result.failure or right_result.failure:
            return r[bool].ok(value=False)
        return r[bool].ok(u.deep_eq(left_result.value, right_result.value))

    def _compare_lines(self, params: m.Tests.CompareParams) -> p.Result[bool]:
        """Compare files line by line with optional normalization.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        c1, c2 = self._read_both(params)
        lines1, lines2 = c1.splitlines(), c2.splitlines()
        if params.ignore_ws:
            lines1 = [line.strip() for line in lines1]
            lines2 = [line.strip() for line in lines2]
        if params.ignore_case:
            lines1 = [line.lower() for line in lines1]
            lines2 = [line.lower() for line in lines2]
        return r[bool].ok(lines1 == lines2)


__all__: list[str] = ["FlextTestsUtilitiesFilesComparison"]

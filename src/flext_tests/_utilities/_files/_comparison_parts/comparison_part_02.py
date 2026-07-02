"""File-comparison public helpers for FlextTestsFiles."""

from __future__ import annotations

from pathlib import Path

from flext_tests import c, m, p, r, t, u
from flext_tests._utilities._files._comparison_parts.comparison_part_01 import (
    FlextTestsFilesComparisonMixin as FlextTestsFilesComparisonMixinPart01,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsFilesComparisonMixin(FlextTestsFilesComparisonMixinPart01):
    """Compare two files by content, lines, size, hash, or deep structure."""

    def compare(
        self,
        file1: Path,
        file2: Path,
        *,
        mode: c.Tests.CompareMode = c.Tests.CompareMode.CONTENT,
        ignore_ws: bool = False,
        ignore_case: bool = False,
        pattern: str | None = None,
        deep: bool = True,
        keys: t.StrSequence | None = None,
        exclude_keys: t.StrSequence | None = None,
    ) -> p.Result[bool]:
        """Compare two files."""
        try:
            params = m.Tests.CompareParams.model_validate({
                "file1": file1,
                "file2": file2,
                "mode": mode,
                "ignore_ws": ignore_ws,
                "ignore_case": ignore_case,
                "pattern": pattern,
                "deep": deep,
                "keys": keys,
                "exclude_keys": exclude_keys,
            })
        except c.EXC_BASIC_TYPE as exc:
            return r[bool].fail(f"Invalid parameters for file comparison: {exc}")
        if not params.file1.exists():
            return r[bool].fail(
                c.Tests.ERROR_FILE_NOT_FOUND.format(path=params.file1),
            )
        if not params.file2.exists():
            return r[bool].fail(
                c.Tests.ERROR_FILE_NOT_FOUND.format(path=params.file2),
            )
        try:
            result = self._compare_existing(params)
        except OSError as e:
            result = r[bool].fail(c.Tests.ERROR_COMPARE.format(error=e))
        return result

    def _compare_existing(self, params: m.Tests.CompareParams) -> p.Result[bool]:
        """Compare two existing files using the requested comparison mode."""
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
        """Compare file content with optional deep/structured comparison."""
        c1, c2 = self._read_both(params)
        if params.deep:
            deep = self._try_deep_compare(c1, c2, params.keys, params.exclude_keys)
            if deep is not None:
                return deep
        if params.ignore_ws:
            c1, c2 = "".join(c1.split()), "".join(c2.split())
        if params.ignore_case:
            c1, c2 = c1.lower(), c2.lower()
        return r[bool].ok(c1 == c2)

    def _compare_lines(self, params: m.Tests.CompareParams) -> p.Result[bool]:
        """Compare files line by line with optional normalization."""
        c1, c2 = self._read_both(params)
        lines1, lines2 = c1.splitlines(), c2.splitlines()
        if params.ignore_ws:
            lines1 = [line.strip() for line in lines1]
            lines2 = [line.strip() for line in lines2]
        if params.ignore_case:
            lines1 = [line.lower() for line in lines1]
            lines2 = [line.lower() for line in lines2]
        return r[bool].ok(lines1 == lines2)

    def _try_deep_compare(
        self,
        content1_raw: str,
        content2_raw: str,
        keys: t.StrSequence | None,
        exclude_keys: t.StrSequence | None,
    ) -> p.Result[bool] | None:
        """Try to parse and deeply compare content as JSON or YAML."""
        parsed = self._try_parse_both(content1_raw, content2_raw, "json")
        if parsed is None:
            parsed = self._try_parse_both(content1_raw, content2_raw, "yaml")
        if parsed is None:
            return None
        dict1, dict2 = parsed
        filter_keys_set = set(keys) if keys is not None else None
        exclude_keys_set = set(exclude_keys) if exclude_keys is not None else None
        left_result = u.transform(
            FlextTestsPayloadUtilities.to_config_map(dict1),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        right_result = u.transform(
            FlextTestsPayloadUtilities.to_config_map(dict2),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        if left_result.failure or right_result.failure:
            return r[bool].ok(False)
        return r[bool].ok(u.deep_eq(left_result.value, right_result.value))


__all__: list[str] = ["FlextTestsFilesComparisonMixin"]

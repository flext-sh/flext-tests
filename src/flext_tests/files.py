"""File management utilities for FLEXT ecosystem tests.

Provides comprehensive file operations for testing across the FLEXT ecosystem
with a simplified API using generalist methods with powerful optional parameters.

Supports:
- r: Automatically extracts value before serialization
- Pydantic models: Serializes to JSON/YAML via model_dump()
- Lists, dicts, Mappings: Proper JSON/YAML serialization
- Generic type loading: Load files directly into Pydantic models

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import csv
import os
import re
import shutil
import tempfile
from collections.abc import (
    Generator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from types import TracebackType
from typing import ClassVar, Self, TypeIs, overload, override

from flext_tests import FlextTestsPayloadUtilities, c, m, p, r, t, u
from flext_tests.base import s


class FlextTestsFiles(s):
    """Manages test files for FLEXT ecosystem testing."""

    FileInfo: ClassVar[type[m.Tests.FileInfo]] = m.Tests.FileInfo

    @staticmethod
    def _validate_model_content[TModelRead: m.BaseModel](
        model_cls: type[TModelRead],
        content: t.Tests.ReadContent,
    ) -> p.Result[TModelRead]:
        try:
            model_instance: TModelRead = model_cls.model_validate(content)
            return r[TModelRead].ok(model_instance)
        except (TypeError, ValueError, AttributeError) as ex:
            return r[TModelRead].fail(f"Failed to validate model: {ex}")

    @staticmethod
    def _read_fail[TModelRead: m.BaseModel](
        error: str,
        model_cls: type[TModelRead] | None,
    ) -> p.Result[t.Tests.ReadContent] | p.Result[TModelRead]:
        """Dispatch a single read-failure message to the correct result type."""
        if model_cls is not None:
            return r[TModelRead].fail(error)
        return r[t.Tests.ReadContent].fail(error)

    _base_dir: Path | None = None
    _created_files: MutableSequence[Path] | None = None
    _created_dirs: MutableSequence[Path] | None = None

    def __init__(
        self,
        base_dir: Path | None = None,
        **data: t.Tests.TestobjectSerializable,
    ) -> None:
        """Initialize file manager with optional base directory.

        Args:
            base_dir: Optional base directory for file operations.
                     If not provided, temporary directories are used.
            **data: Additional data passed to parent service.

        """
        self._base_dir = base_dir
        self._created_files = list[Path]()
        self._created_dirs = list[Path]()

    def __enter__(self) -> Self:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit with cleanup."""
        self.cleanup()

    @property
    def base_dir(self) -> Path | None:
        """Get base directory."""
        return self._base_dir

    @property
    def created_dirs(self) -> Sequence[Path]:
        """Get list of created directories."""
        return self._created_dirs or []

    @property
    def created_files(self) -> Sequence[Path]:
        """Get list of created files."""
        return self._created_files or []

    def cleanup(self) -> None:
        """Cleanup all tracked files and directories created by this manager."""
        if self._created_files is not None:
            for file_path in reversed(self._created_files):
                if not file_path.exists():
                    continue
                try:
                    file_path.chmod(c.Tests.PERMISSION_WRITABLE_FILE)
                    file_path.unlink(missing_ok=True)
                except OSError:
                    pass
            self._created_files.clear()
        if self._created_dirs is not None:
            for dir_path in reversed(self._created_dirs):
                if not dir_path.exists():
                    continue
                try:
                    dir_path.chmod(c.Tests.PERMISSION_WRITABLE_DIR)
                    shutil.rmtree(dir_path)
                except OSError:
                    pass
            self._created_dirs.clear()

    @classmethod
    @contextmanager
    def files(
        cls,
        content: Mapping[
            str,
            t.Tests.FileContentPlain,
        ],
        *,
        directory: Path | None = None,
        ext: str | None = None,
        extract_result: bool = True,
        **kwargs: t.Tests.TestobjectSerializable,
    ) -> Generator[Mapping[str, Path]]:
        """Create temporary files with auto-cleanup.

        Supports Pydantic models, dicts, lists, and raw content.

        Args:
            content: Dict mapping names to content (str, bytes, dict, list, m.BaseModel)
            directory: Base directory (temp if None)
            ext: Default extension if not in name
            extract_result: Auto-extract r values (default: True)
            **kwargs: Passed to create()

        Yields:
            Dict mapping names to paths.

        """
        manager = cls()
        if directory is not None:
            manager._base_dir = directory
        with manager:
            paths: MutableMapping[str, Path] = {}
            default_ext = ext or c.Tests.DEFAULT_EXTENSION
            for name, data_raw in content.items():
                data: t.Tests.FileContentPlain = data_raw
                filename = name if "." in name else f"{name}{default_ext}"
                if "." not in name and isinstance(
                    data,
                    (Mapping, m.BaseModel, m.ConfigMap, m.Dict),
                ):
                    filename = f"{name}.json"
                else:
                    is_nested_sequence = "." not in name and manager._is_nested_rows(
                        data,
                    )
                    if is_nested_sequence:
                        filename = f"{name}.csv"
                try:
                    validated_kwargs = m.Tests.CreateKwargsParams.model_validate(kwargs)
                except (TypeError, ValueError, c.ValidationError):
                    validated_kwargs = m.Tests.CreateKwargsParams(
                        directory=None,
                        fmt=c.Tests.Format.AUTO,
                        enc=c.Tests.DEFAULT_ENCODING,
                        indent=2,
                        delim=",",
                        headers=None,
                        readonly=False,
                    )
                path = manager.create(
                    manager._coerce_file_content(data),
                    filename,
                    directory=validated_kwargs.directory,
                    fmt=manager._normalize_create_format(validated_kwargs.fmt),
                    enc=validated_kwargs.enc,
                    indent=validated_kwargs.indent,
                    delim=validated_kwargs.delim,
                    headers=validated_kwargs.headers,
                    readonly=validated_kwargs.readonly,
                    extract_result=extract_result,
                )
                paths[name] = path
            yield paths

    @staticmethod
    def _is_file_result[TFileContent: t.Tests.FileContentPlain](
        value: TFileContent | p.ResultLike[TFileContent],
    ) -> TypeIs[p.ResultLike[TFileContent]]:
        """Narrow file input to a result-like wrapper with the same payload type."""
        return isinstance(value, p.ResultLike)

    @staticmethod
    def _is_mapping(
        value: t.Tests.FileContentPlain | t.Tests.TestobjectSerializable | None,
    ) -> TypeIs[Mapping[str, t.Tests.TestobjectSerializable]]:
        return isinstance(value, Mapping)

    @staticmethod
    def _to_config_map(
        value: Mapping[str, t.Tests.TestobjectSerializable],
    ) -> m.ConfigMap:
        return m.ConfigMap(
            root={
                key: FlextTestsPayloadUtilities.to_config_map_value(
                    FlextTestsPayloadUtilities.to_payload(item),
                )
                for key, item in value.items()
            },
        )

    @staticmethod
    def _to_payload_mapping(
        value: Mapping[str, t.Tests.TestobjectSerializable],
    ) -> Mapping[str, t.Tests.TestobjectSerializable]:
        return {
            key: FlextTestsPayloadUtilities.to_payload(item)
            for key, item in value.items()
        }

    @staticmethod
    def _to_string_rows(
        value: Sequence[t.Tests.TestobjectSerializable],
    ) -> Sequence[t.StrSequence]:
        return [
            [str(cell) for cell in row]
            for row in value
            if isinstance(row, (list, tuple))
        ]

    @staticmethod
    def assert_exists(
        path: Path,
        msg: str | None = None,
        options: m.Tests.AssertExistsParams | None = None,
        **kwargs: t.JsonValue,
    ) -> Path:
        """Generalized file existence assertion - ALL file validations in ONE method.

        Consolidates: assert_exists(), assert_file(), assert_dir(), assert_not_empty()
        into single method with optional parameters.

        Args:
            path: File or directory path to check
            msg: Custom error message
            is_file: Assert is file (True) or not file (False)
            is_dir: Assert is directory (True) or not directory (False)
            not_empty: Assert file/dir is not empty (True) or empty (False)
            readable: Assert is readable (True)
            writable: Assert is writable (True)

        Returns:
            Path if all validations pass

        """
        payload: t.MutableJsonMapping = (
            options.model_dump(mode="python") if options is not None else {}
        )
        payload.update(kwargs)
        params = m.Tests.AssertExistsParams.model_validate(payload)
        if not path.exists():
            error_msg = msg or c.Tests.ERROR_FILE_NOT_FOUND.format(path=path)
            raise AssertionError(error_msg)
        is_file_path = path.is_file()
        is_dir_path = path.is_dir()
        is_empty_file = is_file_path and path.stat().st_size == 0
        is_empty_dir = is_dir_path and (not any(path.iterdir()))

        checks: MutableSequence[tuple[bool, str]] = []
        if params.is_file is not None:
            checks.extend([
                (params.is_file and (not is_file_path), f"Path {path} is not a file"),
                (
                    (not params.is_file) and is_file_path,
                    f"Path {path} should not be a file",
                ),
            ])
        if params.is_dir is not None:
            checks.extend([
                (
                    params.is_dir and (not is_dir_path),
                    f"Path {path} is not a directory",
                ),
                (
                    (not params.is_dir) and is_dir_path,
                    f"Path {path} should not be a directory",
                ),
            ])
        if params.not_empty is not None:
            checks.extend([
                (params.not_empty and is_empty_file, f"File {path} is empty"),
                (params.not_empty and is_empty_dir, f"Directory {path} is empty"),
                (
                    (not params.not_empty) and is_file_path and (not is_empty_file),
                    f"File {path} is not empty",
                ),
                (
                    (not params.not_empty) and is_dir_path and (not is_empty_dir),
                    f"Directory {path} is not empty",
                ),
            ])
        if params.readable:
            checks.append(
                (
                    is_file_path and (not os.access(path, os.R_OK)),
                    f"File {path} is not readable",
                ),
            )
        if params.writable:
            checks.extend([
                (
                    is_file_path and (not os.access(path, os.W_OK)),
                    f"File {path} is not writable",
                ),
                (
                    is_dir_path and (not os.access(path, os.W_OK)),
                    f"Directory {path} is not writable",
                ),
            ])

        for failed, check_msg in checks:
            if failed:
                raise AssertionError(msg or check_msg)
        return path

    @staticmethod
    def create_in[TFileContent: t.Tests.FileContentPlain](
        content: TFileContent | p.ResultLike[TFileContent],
        name: str,
        directory: Path,
        *,
        fmt: c.Tests.Format = c.Tests.Format.AUTO,
        enc: str = c.Tests.DEFAULT_ENCODING,
        indent: int = c.Tests.DEFAULT_JSON_INDENT,
        delim: str = c.Tests.DEFAULT_CSV_DELIMITER,
        headers: t.StrSequence | None = None,
        readonly: bool = False,
        extract_result: bool = True,
    ) -> Path:
        """Create file directly in directory - static convenience method.

        Supports r, Pydantic models, lists, dicts, and raw content.

        Args:
            content: File content (str, bytes, dict, list, m.BaseModel, or r[T])
            name: Filename
            directory: Target directory
            fmt: Format override ("auto", "text", "bin", "json", "yaml", "csv")
            enc: Encoding (default: utf-8)
            indent: JSON/YAML indent (default: 2)
            delim: CSV delimiter (default: ",")
            headers: CSV headers (default: None)
            readonly: Create as read-only (default: False)
            extract_result: Auto-extract r value (default: True)

        Returns:
            Path to created file.

        """
        manager = FlextTestsFiles(base_dir=directory)
        return manager.create(
            content,
            name,
            directory=None,
            fmt=fmt,
            enc=enc,
            indent=indent,
            delim=delim,
            headers=headers,
            readonly=readonly,
            extract_result=extract_result,
        )

    def batch_files[TModel: m.BaseModel](
        self,
        items: t.Tests.BatchFiles,
        *,
        directory: Path | None = None,
        operation: c.Tests.Operation = c.Tests.Operation.CREATE,
        model: type[TModel] | None = None,
        on_error: c.Tests.ErrorMode = c.Tests.ErrorMode.COLLECT,
        parallel: bool = False,
    ) -> p.Result[m.Tests.BatchResult]:
        """Batch file operations.

        Uses u.batch_files() for batch processing with error handling.

        Args:
            items: Mapping[str, t.FileContent] or Sequence[tuple[str, t.FileContent]]
            directory: Target directory for create operations
            operation: "create", "read", or "delete"
            model: Optional model class for read operations
            on_error: Error handling mode ("stop", "skip", "collect")
            parallel: Run operations in parallel (not implemented yet)

        Returns:
            r[m.Tests.BatchResult] with results and errors

        """
        try:
            params = m.Tests.BatchParams.model_validate({
                "files": items,
                "directory": directory,
                "operation": operation,
                "model": model,
                "on_error": on_error,
                "parallel": parallel,
            })
        except (TypeError, ValueError, AttributeError) as exc:
            return r[m.Tests.BatchResult].fail(
                f"Invalid parameters for batch operation: {exc}",
            )
        files_dict: MutableMapping[str, t.Tests.TestobjectSerializable]
        if isinstance(params.files, Mapping):
            files_dict = dict(params.files.items())
        elif not isinstance(params.files, str):
            files_dict = {}
            for item in params.files:
                if len(item) == 2:
                    try:
                        _ = m.Tests.CreateParams.model_validate({
                            "content": item[1],
                            "name": c.Tests.DEFAULT_FILENAME,
                        })
                    except (TypeError, ValueError, AttributeError):
                        continue
                    name = item[0]
                    files_dict[name] = item[1]
        else:
            return r[m.Tests.BatchResult].fail(
                f"Invalid BatchFiles type: {type(params.files)}",
            )
        error_mode_str = "collect" if params.on_error == "collect" else "fail"

        def process_one(
            name_and_content: tuple[str, t.Tests.TestobjectSerializable],
        ) -> p.Result[Path]:
            """Process single file operation."""
            name, content = name_and_content
            path = Path(content) if isinstance(content, (Path, str)) else Path(name)
            match params.operation:
                case "create":
                    try:
                        payload = (
                            {
                                k: FlextTestsPayloadUtilities.to_payload(v)
                                for k, v in content.items()
                            }
                            if isinstance(content, Mapping)
                            else content
                        )
                        return r[Path].ok(
                            self.create(
                                self._coerce_file_content(payload),
                                name,
                                params.directory,
                            )
                        )
                    except (OSError, TypeError, ValueError, AttributeError) as e:
                        return r[Path].fail(f"Failed to create {name}: {e}")
                case "read":
                    read_result = self.read(path, model_cls=None)
                    return (
                        r[Path].ok(path)
                        if read_result.success
                        else r[Path].fail(read_result.error or f"Failed to read {name}")
                    )
                case "delete":
                    try:
                        path.unlink(missing_ok=True)
                        return r[Path].ok(path)
                    except OSError as e:
                        return r[Path].fail(f"Failed to delete {name}: {e}")
                case _:
                    return r[Path].fail(f"Unknown operation: {params.operation}")

        items_list = list(files_dict.items())
        results_dict: MutableMapping[str, r[Path | t.Tests.TestobjectSerializable]] = {}
        failed_dict: t.MutableStrMapping = {}
        rtype = r[Path | t.Tests.TestobjectSerializable]
        for name, _ in items_list:
            op_result = process_one((name, files_dict[name]))
            if op_result.success:
                results_dict[name] = rtype.ok(op_result.value)
                continue
            err_msg = op_result.error or "Unknown error"
            results_dict[name] = rtype.fail(err_msg)
            failed_dict[name] = err_msg
            if error_mode_str == "fail":
                return r[m.Tests.BatchResult].fail(err_msg)

        summary = m.Tests.BatchResult.model_validate({
            "succeeded": len(items_list) - len(failed_dict),
            "failed": len(failed_dict),
            "total": len(items_list),
            "results": dict(results_dict),
            "errors": dict(failed_dict),
        })
        return r[m.Tests.BatchResult].ok(summary)

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
        """Compare two files.

        Args:
            file1: First file
            file2: Second file
            mode: "content" | "size" | "hash" | "lines"
            ignore_ws: Ignore whitespace
            ignore_case: Case-insensitive
            pattern: Check if both contain pattern
            keys: Only compare these keys (for dict/JSON content)
            exclude_keys: Exclude these keys from comparison (for dict/JSON content)
            deep: Use deep comparison for nested structures (default: True)

        Returns:
            r[bool] - True if match.

        """
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
        except (TypeError, ValueError, AttributeError) as exc:
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
        except OSError as e:
            return r[bool].fail(c.Tests.ERROR_COMPARE.format(error=e))

    def create[TFileContent: t.Tests.FileContentPlain](
        self,
        content: TFileContent | p.ResultLike[TFileContent],
        name: str = c.Tests.DEFAULT_FILENAME,
        directory: Path | None = None,
        *,
        fmt: c.Tests.Format = c.Tests.Format.AUTO,
        enc: str = c.Tests.DEFAULT_ENCODING,
        indent: int = c.Tests.DEFAULT_JSON_INDENT,
        delim: str = c.Tests.DEFAULT_CSV_DELIMITER,
        headers: t.StrSequence | None = None,
        readonly: bool = False,
        extract_result: bool = True,
    ) -> Path:
        r"""Create file with auto-detection or explicit format.

        Supports r, Pydantic models, lists, dicts, and raw content.

        Args:
            content: Content - type determines default format:
                - str: text file
                - bytes: binary file
                - dict/Mapping: JSON file
                - Sequence[t.StrSequence]: CSV file
                - m.BaseModel: JSON file (via model_dump())
                - r[T]: Extracts value if success (if extract_result=True)
            name: Filename (extension hints format)
            directory: Directory (uses base_dir or temp if None)
            fmt: Format override ("auto", "text", "bin", "json", "yaml", "csv")
            enc: Encoding (default: utf-8)
            indent: JSON/YAML indent (default: 2)
            delim: CSV delimiter (default: ",")
            headers: CSV headers (default: None)
            readonly: Create as read-only (default: False)
            extract_result: Auto-extract r value (default: True)

        Returns:
            Path to created file.

        Raises:
            ValueError: If r is failure and extract_result=True

        """
        content_to_validate = self._extract_content(content, extract_result)
        try:
            params = m.Tests.CreateParams.model_validate({
                "content": content_to_validate,
                "name": name,
                "directory": directory,
                "fmt": fmt,
                "enc": enc,
                "indent": indent,
                "delim": delim,
                "headers": headers,
                "readonly": readonly,
                "extract_result": extract_result,
            })
        except (TypeError, ValueError, AttributeError) as exc:
            raise ValueError(f"Invalid parameters for file creation: {exc}") from None
        target_dir = self._resolve_directory(params.directory)
        name_str = params.name
        file_path: Path = target_dir / name_str
        actual_content: (
            str
            | bytes
            | m.ConfigMap
            | Sequence[t.StrSequence]
            | m.BaseModel
            | Mapping[str, t.Tests.TestobjectSerializable]
        ) = self._coerce_file_content(params.content)
        if isinstance(actual_content, m.ConfigMap):
            actual_content = {
                key: FlextTestsPayloadUtilities.to_payload(value)
                for key, value in actual_content.root.items()
            }
        if isinstance(actual_content, m.BaseModel):
            actual_content = t.Tests.TESTOBJECT_MAPPING_ADAPTER.validate_python(
                FlextTestsPayloadUtilities.to_payload(
                    actual_content.model_dump(mode="json"),
                ),
            )
        actual_fmt = u.Tests.detect_format(
            actual_content
            if isinstance(actual_content, (str, bytes, Mapping, list))
            else str(actual_content),
            params.name,
            params.fmt,
        )
        self._write_content_by_format(
            file_path=file_path,
            actual_content=actual_content,
            actual_fmt=actual_fmt,
            params=params,
        )
        if params.readonly:
            file_path.chmod(c.Tests.PERMISSION_READONLY_FILE)
        if self._created_files is None:
            self._created_files = list[Path]()
        self._created_files.append(file_path)
        return file_path

    def _write_content_by_format(
        self,
        *,
        file_path: Path,
        actual_content: (
            str
            | bytes
            | m.ConfigMap
            | Sequence[t.StrSequence]
            | m.BaseModel
            | Mapping[str, t.Tests.TestobjectSerializable]
        ),
        actual_fmt: str,
        params: m.Tests.CreateParams,
    ) -> None:
        """Write normalized content using the selected output format."""
        match actual_fmt:
            case c.Tests.Format.BIN:
                _ = file_path.write_bytes(
                    actual_content
                    if isinstance(actual_content, bytes)
                    else str(actual_content).encode(params.enc),
                )
            case c.Tests.Format.JSON | c.Tests.Format.YAML:
                json_payload = self._build_json_payload(actual_content)
                if actual_fmt == c.Tests.Format.JSON:
                    u.Cli.json_write(
                        file_path,
                        json_payload,
                        m.Cli.JsonWriteOptions(indent=params.indent),
                    )
                else:
                    u.Cli.yaml_dump(file_path, json_payload, indent=params.indent)
            case c.Tests.Format.CSV:
                u.Cli.files_write_csv(
                    file_path,
                    self._build_csv_rows(
                        actual_content=actual_content,
                        headers=params.headers,
                    ),
                )
            case _:
                _ = file_path.write_text(str(actual_content), encoding=params.enc)

    @staticmethod
    def _build_json_payload(
        actual_content: (
            str
            | bytes
            | m.ConfigMap
            | Sequence[t.StrSequence]
            | m.BaseModel
            | Mapping[str, t.Tests.TestobjectSerializable]
        ),
    ) -> t.JsonValue:
        """Build normalized JSON payload from arbitrary file content."""
        mapping_content: Mapping[str, t.Tests.TestobjectSerializable] | None = (
            actual_content.root
            if isinstance(actual_content, (m.ConfigMap, m.Dict))
            else actual_content
            if isinstance(actual_content, Mapping)
            else None
        )
        fallback_value = FlextTestsPayloadUtilities.to_payload(actual_content)
        raw_payload = (
            {
                k: FlextTestsPayloadUtilities.to_normalized_value(v)
                for k, v in mapping_content.items()
            }
            if mapping_content is not None
            else {"value": fallback_value}
            if actual_content
            else dict[str, t.JsonValue]()
        )
        return t.json_value_adapter().validate_python(raw_payload)

    @staticmethod
    def _build_csv_rows(
        *,
        actual_content: (
            str
            | bytes
            | m.ConfigMap
            | Sequence[t.StrSequence]
            | m.BaseModel
            | Mapping[str, t.Tests.TestobjectSerializable]
        ),
        headers: t.StrSequence | None,
    ) -> list[t.StrSequence]:
        """Build CSV rows from normalized content and optional headers."""
        csv_rows: list[t.StrSequence] = []
        if headers:
            csv_rows.append(list(headers))
        if isinstance(actual_content, Sequence) and not isinstance(
            actual_content,
            (str, bytes),
        ):
            csv_rows.extend(
                list(row)
                for row in actual_content
                if isinstance(row, Sequence) and not isinstance(row, (str, bytes))
            )
        else:
            csv_rows.append([str(actual_content)])
        return csv_rows

    @override
    def execute(self) -> p.Result[t.JsonValue]:
        """Execute service - returns success for file manager.

        FlextTestsFiles is a utility service that doesn't have a specific
        execution result. Returns success by default.
        """
        return r[t.JsonValue].ok("")

    def info(
        self,
        path: Path,
        *,
        compute_hash: bool = False,
        detect_fmt: bool = True,
        parse_content: bool = False,
        validate_model: type[m.BaseModel] | None = None,
    ) -> p.Result[m.Tests.FileInfo]:
        """Get comprehensive file information.

        Args:
            path: File path
            compute_hash: Compute SHA256 (default: False)
            detect_fmt: Auto-detect format (default: True)
            parse_content: Parse content and include metadata (default: False)
            validate_model: Pydantic model to validate content against (default: None)

        Returns:
            r[FileInfo] with info or error.

        """
        try:
            params = m.Tests.InfoParams.model_validate({
                "path": path,
                "compute_hash": compute_hash,
                "detect_fmt": detect_fmt,
                "parse_content": parse_content,
                "validate_model": validate_model,
            })
        except (TypeError, ValueError, AttributeError) as exc:
            return r[m.Tests.FileInfo].fail(f"Invalid parameters for file info: {exc}")
        if not params.path.exists():
            return r[m.Tests.FileInfo].ok(
                m.Tests.FileInfo(exists=False, path=params.path),
            )
        try:
            stat = params.path.stat()
            size = stat.st_size
            size_human = c.Tests.format_size(size)
            try:
                text = params.path.read_text(
                    encoding=c.Tests.DEFAULT_ENCODING,
                    errors="replace",
                )
                lines = text.count("\n") + 1 if text else 0
                is_empty = not text.strip()
                first_line = text.split("\n")[0] if text else ""
                encoding = c.Tests.DEFAULT_ENCODING
            except UnicodeDecodeError:
                text = ""
                lines = 0
                is_empty = size == 0
                first_line = ""
                encoding = c.Tests.DEFAULT_BINARY_ENCODING
            fmt: str = "unknown"
            if params.detect_fmt:
                detected = u.Tests.detect_format_from_path(params.path, "auto")
                fmt = detected if detected in c.Tests.KNOWN_FORMATS else "unknown"
            permissions = stat.st_mode
            is_readonly = not permissions & 128
            sha256 = u.Cli.sha256_file(params.path) if params.compute_hash else None
            content_meta: m.Tests.ContentMeta | None = None
            if params.parse_content or params.validate_model:
                content_meta = self._parse_content_metadata(
                    path=params.path,
                    text=text,
                    fmt=fmt,
                    validate_model=params.validate_model,
                )
            return r[m.Tests.FileInfo].ok(
                m.Tests.FileInfo(
                    exists=True,
                    path=params.path,
                    size=size,
                    size_human=size_human,
                    lines=lines,
                    encoding=encoding,
                    is_empty=is_empty,
                    first_line=first_line,
                    fmt=fmt,
                    valid=True,
                    modified=datetime.fromtimestamp(stat.st_mtime, tz=UTC),
                    permissions=permissions,
                    is_readonly=is_readonly,
                    sha256=sha256,
                    content_meta=content_meta,
                ),
            )
        except OSError as e:
            return r[m.Tests.FileInfo].fail(c.Tests.ERROR_INFO.format(error=e))

    @overload
    def read(
        self,
        path: Path,
        *,
        model_cls: None = None,
        fmt: c.Tests.Format = c.Tests.Format.AUTO,
        enc: str = c.Tests.DEFAULT_ENCODING,
        delim: str = c.Tests.DEFAULT_CSV_DELIMITER,
        has_headers: bool = True,
    ) -> p.Result[t.Tests.ReadContent]: ...

    @overload
    def read[TModelRead: m.BaseModel](
        self,
        path: Path,
        *,
        model_cls: type[TModelRead],
        fmt: c.Tests.Format = c.Tests.Format.AUTO,
        enc: str = c.Tests.DEFAULT_ENCODING,
        delim: str = c.Tests.DEFAULT_CSV_DELIMITER,
        has_headers: bool = True,
    ) -> p.Result[TModelRead]: ...

    def read[TModelRead: m.BaseModel](
        self,
        path: Path,
        *,
        model_cls: type[TModelRead] | None = None,
        fmt: c.Tests.Format = c.Tests.Format.AUTO,
        enc: str = c.Tests.DEFAULT_ENCODING,
        delim: str = c.Tests.DEFAULT_CSV_DELIMITER,
        has_headers: bool = True,
    ) -> p.Result[t.Tests.ReadContent] | p.Result[TModelRead]:
        """Read file with auto-detection or explicit format.

        Supports loading directly into Pydantic models when model_cls is provided.

        Args:
            path: File path
            model_cls: Optional Pydantic model class to deserialize into
            fmt: Format ("auto" detects from extension)
            enc: Encoding (default: utf-8)
            delim: CSV delimiter (default: ",")
            has_headers: CSV has headers (default: True)

        Returns:
            r with content or model instance.

        """
        try:
            params = m.Tests.ReadParams.model_validate({
                "path": path,
                "fmt": fmt,
                "enc": enc,
                "delim": delim,
                "has_headers": has_headers,
                "model_cls": model_cls,
            })
        except (TypeError, ValueError, AttributeError) as exc:
            return self._read_fail(
                f"Invalid parameters for file read: {exc}", model_cls
            )
        if not params.path.exists():
            return self._read_fail(
                c.Tests.ERROR_FILE_NOT_FOUND.format(path=params.path),
                model_cls,
            )
        actual_fmt = u.Tests.detect_format_from_path(params.path, params.fmt)
        try:
            content: t.Tests.ReadContent
            if actual_fmt == c.Tests.Format.BIN:
                content = params.path.read_bytes()
            elif actual_fmt == c.Tests.Format.JSON:
                text = params.path.read_text(encoding=params.enc)
                parsed_json = t.Tests.TESTOBJECT_MAPPING_ADAPTER.validate_json(
                    text.encode(),
                )
                content = (
                    self._to_config_map(parsed_json)
                    if self._is_mapping(parsed_json)
                    else text
                )
            elif actual_fmt == c.Tests.Format.YAML:
                text = params.path.read_text(encoding=params.enc)
                parsed_yaml_result = u.Cli.yaml_parse(text)
                parsed_yaml = (
                    parsed_yaml_result.value if parsed_yaml_result.success else None
                )
                content = (
                    self._to_config_map(parsed_yaml)
                    if isinstance(parsed_yaml, dict)
                    else text
                )
            elif actual_fmt == c.Tests.Format.CSV:
                csv_result = u.Cli.files_read_csv_with_headers(params.path)
                csv_rows_m = csv_result.value if csv_result.success else ()
                if csv_rows_m:
                    keys = list(csv_rows_m[0].keys())
                    data_rows = [[row.get(k, "") for k in keys] for row in csv_rows_m]
                    content = data_rows if params.has_headers else [keys, *data_rows]
                else:
                    content = []
            else:
                content = params.path.read_text(encoding=params.enc)
            if model_cls is not None:
                return self._validate_model_content(model_cls, content)
            return r[t.Tests.ReadContent].ok(content)
        except UnicodeDecodeError as e:
            return self._read_fail(c.Tests.ERROR_ENCODING.format(error=e), model_cls)
        except ValueError as e:
            return self._read_fail(
                c.Tests.ERROR_INVALID_JSON.format(error=e), model_cls
            )
        except t.Cli.YAMLError as e:
            return self._read_fail(
                c.Tests.ERROR_INVALID_YAML.format(error=e), model_cls
            )
        except OSError as e:
            return self._read_fail(c.Tests.ERROR_READ.format(error=e), model_cls)

    @contextmanager
    def temporary_directory(self) -> Generator[Path]:
        """Create and manage a temporary directory.

        Yields:
            Path to temporary directory that is automatically cleaned up.

        """
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    def _apply_key_filtering(
        self,
        dict1: Mapping[str, t.Tests.TestobjectSerializable],
        dict2: Mapping[str, t.Tests.TestobjectSerializable],
        keys: t.StrSequence | None,
        exclude_keys: t.StrSequence | None,
    ) -> tuple[
        Mapping[str, t.Tests.TestobjectSerializable],
        Mapping[str, t.Tests.TestobjectSerializable],
    ]:
        """Apply key filtering to both dicts if specified."""
        if keys is None and exclude_keys is None:
            return (dict1, dict2)
        filter_keys_set = set(keys) if keys is not None else None
        exclude_keys_set = set(exclude_keys) if exclude_keys is not None else None
        result1 = u.transform(
            self._to_config_map(dict1),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        result2 = u.transform(
            self._to_config_map(dict2),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        if result1.success and result2.success:
            filtered1 = self._to_payload_mapping(result1.value)
            filtered2 = self._to_payload_mapping(result2.value)
            return (filtered1, filtered2)
        return (dict1, dict2)

    def _coerce_file_content[TFileContent: t.Tests.FileContentPlain](
        self,
        value: TFileContent
        | p.ResultLike[TFileContent]
        | t.Tests.TestobjectSerializable
        | None,
    ) -> t.Tests.FileContentPlain:
        unwrapped: t.Tests.FileContentPlain | t.Tests.TestobjectSerializable | None = (
            value.unwrap_or(c.DEFAULT_EMPTY_STRING)
            if isinstance(value, p.ResultLike)
            else value
        )
        if isinstance(unwrapped, str | bytes):
            return unwrapped
        if isinstance(unwrapped, (m.ConfigMap, m.Dict)):
            return self._to_config_map(unwrapped.root)
        if isinstance(unwrapped, m.BaseModel):
            return unwrapped
        if self._is_mapping(unwrapped):
            return self._to_config_map(unwrapped)
        if self._is_nested_rows(unwrapped):
            sequence_value: Sequence[t.Tests.TestobjectSerializable] = (
                unwrapped if isinstance(unwrapped, (list, tuple)) else ()
            )
            return self._to_string_rows(sequence_value)
        return str(unwrapped)

    @staticmethod
    def _read_both(params: m.Tests.CompareParams) -> tuple[str, str]:
        enc = c.Tests.DEFAULT_ENCODING
        return (
            params.file1.read_text(encoding=enc),
            params.file2.read_text(encoding=enc),
        )

    def _compare_content(self, params: m.Tests.CompareParams) -> p.Result[bool]:
        """Compare file content with optional deep/structured comparison."""
        c1, c2 = self._read_both(params)
        if params.deep:
            deep = self._try_deep_compare(c1, c2, params.keys, params.exclude_keys)
            if deep is not None:
                return deep
        if params.ignore_ws:
            c1, c2 = re.sub(r"\s+", "", c1), re.sub(r"\s+", "", c2)
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

    def _extract_content[TFileContent: t.Tests.FileContentPlain](
        self,
        content: TFileContent | p.ResultLike[TFileContent],
        extract_result: bool,
    ) -> t.Tests.FileContentPlain:
        """Extract actual content from r or return as-is.

        Uses u.matches_type(content, "result") for type checking and u.val() for extraction.

        Args:
            content: Content that may be wrapped in r
            extract_result: Whether to extract from r

        Returns:
            Extracted content or original value

        Raises:
            ValueError: If r is failure and extraction is enabled

        """
        if not extract_result:
            return self._coerce_file_content(content)
        # bytes needs handling before result check — bytes not in t.GuardInput
        if isinstance(content, bytes):
            return content
        # TypeIs guard narrows to the matching result-like wrapper
        if self._is_file_result(content):
            if content.failure:
                error_msg = content.error or "r failure"
                raise ValueError(f"Cannot create file from failed r: {error_msg}")
            return self._coerce_file_content(content.value)
        return self._coerce_file_content(content)

    def _is_nested_rows(
        self,
        value: t.Tests.FileContentPlain | t.Tests.TestobjectSerializable,
    ) -> TypeIs[Sequence[t.StrSequence]]:
        if not isinstance(value, Sequence) or isinstance(value, str | bytes):
            return False
        try:
            sequence_value = t.Tests.TESTOBJECT_SEQUENCE_ADAPTER.validate_python(value)
        except c.ValidationError:
            return False
        if not sequence_value:
            return False
        for row_raw in sequence_value:
            if not isinstance(row_raw, Sequence) or isinstance(row_raw, str | bytes):
                return False
        return True

    _FMT_NORMALIZE: ClassVar[Mapping[str, c.Tests.Format]] = {
        "txt": c.Tests.Format.TEXT,
        "md": c.Tests.Format.TEXT,
        "auto": c.Tests.Format.AUTO,
        "text": c.Tests.Format.TEXT,
        "bin": c.Tests.Format.BIN,
        "json": c.Tests.Format.JSON,
        "yaml": c.Tests.Format.YAML,
        "csv": c.Tests.Format.CSV,
    }

    def _normalize_create_format(self, fmt: str) -> c.Tests.Format:
        return self._FMT_NORMALIZE.get(fmt, c.Tests.Format.AUTO)

    def _parse_content_metadata(
        self,
        path: Path,
        text: str,
        fmt: str,
        validate_model: type[m.BaseModel] | None = None,
    ) -> m.Tests.ContentMeta:
        """Parse file content and extract metadata.

        Uses u.load() for model validation and format-specific parsing
        to extract content statistics (key_count, item_count, row_count, etc.).

        Args:
            path: File path
            text: File text content
            fmt: Detected file format
            validate_model: Pydantic model to validate content against

        Returns:
            ContentMeta with extracted statistics

        """
        _ = path
        key_count = item_count = row_count = column_count = None
        model_valid: bool | None = None
        model_name = validate_model.__name__ if validate_model else None
        parsed_mapping: Mapping[str, t.Tests.TestobjectSerializable] | None = None
        structured_text = fmt in {"json", "yaml"} and bool(text.strip())
        if structured_text:
            parse_result = (
                u.Cli.json_parse(text) if fmt == "json" else u.Cli.yaml_parse(text)
            )
            parsed_value = parse_result.value if parse_result.success else None
            match parsed_value:
                case dict() as parsed_dict:
                    parsed_mapping = dict(parsed_dict.items())
                    key_count = len(parsed_mapping)
                case list() as parsed_list:
                    item_count = len(parsed_list)
                case _:
                    pass
        elif fmt == "csv":
            rows: list[list[str]]
            try:
                rows = list(csv.reader(text.splitlines()))
            except csv.Error:
                rows = []
            if rows:
                row_count = len(rows)
                column_count = len(rows[0]) if rows[0] else 0
        if validate_model is not None:
            if parsed_mapping is not None:
                model_valid = (
                    r[m.BaseModel]
                    .create_from_callable(
                        lambda: validate_model.model_validate(parsed_mapping)
                    )
                    .success
                )
            elif structured_text:
                model_valid = False
        return m.Tests.ContentMeta.model_validate({
            "key_count": key_count,
            "item_count": item_count,
            "row_count": row_count,
            "column_count": column_count,
            "model_valid": model_valid,
            "model_name": model_name,
        })

    def _resolve_directory(self, directory: Path | None) -> Path:
        """Resolve target directory for file creation."""
        if directory is not None:
            directory.mkdir(parents=True, exist_ok=True)
            return directory
        if self.base_dir is not None:
            self.base_dir.mkdir(parents=True, exist_ok=True)
            return self.base_dir
        temp_dir = Path(tempfile.mkdtemp())
        if self._created_dirs is None:
            self._created_dirs = list[Path]()
        self._created_dirs.append(temp_dir)
        return temp_dir

    def _try_deep_compare(
        self,
        content1_raw: str,
        content2_raw: str,
        keys: t.StrSequence | None,
        exclude_keys: t.StrSequence | None,
    ) -> p.Result[bool] | None:
        """Try to parse and deeply compare content as JSON or YAML.

        Returns None if content cannot be parsed as structured data.
        """
        parsed = self._try_parse_both(content1_raw, content2_raw, "json")
        if parsed is None:
            parsed = self._try_parse_both(content1_raw, content2_raw, "yaml")
        if parsed is None:
            return None
        dict1, dict2 = parsed
        filter_keys_set = set(keys) if keys is not None else None
        exclude_keys_set = set(exclude_keys) if exclude_keys is not None else None
        left_result = u.transform(
            self._to_config_map(dict1),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        right_result = u.transform(
            self._to_config_map(dict2),
            filter_keys=filter_keys_set,
            exclude_keys=exclude_keys_set,
        )
        if left_result.failure or right_result.failure:
            return r[bool].ok(False)
        return r[bool].ok(u.deep_eq(left_result.value, right_result.value))

    def _try_parse_both(
        self,
        content1: str,
        content2: str,
        fmt: str,
    ) -> (
        tuple[
            Mapping[str, t.Tests.TestobjectSerializable],
            Mapping[str, t.Tests.TestobjectSerializable],
        ]
        | None
    ):
        """Try to parse both contents as dicts in given format."""
        parse = (
            u.Cli.json_parse
            if fmt == "json"
            else u.Cli.yaml_parse
            if fmt == "yaml"
            else None
        )
        if parse is None:
            return None
        try:
            r1, r2 = parse(content1), parse(content2)
        except (ValueError, t.Cli.YAMLError, TypeError):
            return None
        d1 = r1.value if r1.success else None
        d2 = r2.value if r2.success else None
        if self._is_mapping(d1) and self._is_mapping(d2):
            return (self._to_payload_mapping(d1), self._to_payload_mapping(d2))
        return None


tf = FlextTestsFiles

__all__: list[str] = ["FlextTestsFiles", "tf"]

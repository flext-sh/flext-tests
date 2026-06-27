"""File-creation helpers for FlextTestsFiles.

Content coercion, format detection, and writing by format.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TypeIs

from flext_infra import u
from flext_tests import FlextTestsPayloadUtilities, c, m, p, t
from flext_tests._utilities._files._lifecycle import FlextTestsFilesLifecycleMixin


class FlextTestsFilesCreationMixin(FlextTestsFilesLifecycleMixin):
    """Create test files with auto-detected or explicit formats."""

    def create[TFileContent: t.Tests.FileContentPlain](
        self,
        content: TFileContent | p.ResultLike[TFileContent],
        name: str = c.Tests.DEFAULT_FILENAME,
        directory: Path | None = None,
        *,
        fmt: c.Tests.FileFormat = c.Tests.FILE_FORMAT_AUTO,
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
                - t.SequenceOf[t.StrSequence]: CSV file
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
        except c.EXC_BASIC_TYPE as exc:
            raise ValueError(f"Invalid parameters for file creation: {exc}") from None
        target_dir = self._resolve_directory(params.directory)
        name_str = params.name
        file_path: Path = target_dir / name_str
        actual_content: (
            str
            | bytes
            | m.ConfigMap
            | t.SequenceOf[t.StrSequence]
            | m.BaseModel
            | t.MappingKV[str, t.Tests.TestobjectSerializable]
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
        actual_fmt = u.Cli.files_detect_format_from_content(
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
            | t.SequenceOf[t.StrSequence]
            | m.BaseModel
            | t.MappingKV[str, t.Tests.TestobjectSerializable]
        ),
        actual_fmt: str,
        params: m.Tests.CreateParams,
    ) -> None:
        """Write normalized content using the selected output format."""
        match actual_fmt:
            case c.Tests.FILE_FORMAT_BIN:
                _ = file_path.write_bytes(
                    actual_content
                    if isinstance(actual_content, bytes)
                    else str(actual_content).encode(params.enc),
                )
            case c.Tests.FILE_FORMAT_JSON | c.Tests.FILE_FORMAT_YAML:
                json_payload = self._build_json_payload(actual_content)
                if actual_fmt == c.Tests.FILE_FORMAT_JSON:
                    u.Cli.json_write(
                        file_path,
                        json_payload,
                        m.Cli.JsonWriteOptions(indent=params.indent),
                    )
                else:
                    u.Cli.yaml_dump(file_path, json_payload, indent=params.indent)
            case c.Tests.FILE_FORMAT_CSV:
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
            | t.SequenceOf[t.StrSequence]
            | m.BaseModel
            | t.MappingKV[str, t.Tests.TestobjectSerializable]
        ),
    ) -> t.JsonValue:
        """Build normalized JSON payload from arbitrary file content."""
        mapping_content: t.MappingKV[str, t.Tests.TestobjectSerializable] | None = (
            actual_content.root
            if isinstance(actual_content, (m.ConfigMap, m.Dict))
            else actual_content
            if isinstance(actual_content, Mapping)
            else None
        )
        fallback_value = FlextTestsPayloadUtilities.to_normalized_value(
            FlextTestsPayloadUtilities.to_payload(actual_content),
        )
        raw_payload: t.JsonValue = (
            {
                k: FlextTestsPayloadUtilities.to_normalized_value(v)
                for k, v in mapping_content.items()
            }
            if mapping_content is not None
            else {"value": fallback_value}
            if actual_content
            else {}
        )
        return t.json_value_adapter().validate_python(raw_payload)

    @staticmethod
    def _build_csv_rows(
        *,
        actual_content: (
            str
            | bytes
            | m.ConfigMap
            | t.SequenceOf[t.StrSequence]
            | m.BaseModel
            | t.MappingKV[str, t.Tests.TestobjectSerializable]
        ),
        headers: t.StrSequence | None,
    ) -> list[t.StrSequence]:
        """Build CSV rows from normalized content and optional headers."""
        csv_rows: list[t.StrSequence] = []
        if headers:
            csv_rows.append(list(headers))
        if isinstance(actual_content, Sequence) and not isinstance(
            actual_content, t.STR_BYTES_TYPES
        ):
            csv_rows.extend(
                list(row)
                for row in actual_content
                if isinstance(row, Sequence) and not isinstance(row, t.STR_BYTES_TYPES)
            )
        else:
            csv_rows.append([str(actual_content)])
        return csv_rows

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
    def _to_payload_mapping(
        value: t.MappingKV[str, t.Tests.TestobjectSerializable],
    ) -> t.MappingKV[str, t.Tests.TestobjectSerializable]:
        return {
            key: FlextTestsPayloadUtilities.to_payload(item)
            for key, item in value.items()
        }

    @staticmethod
    def _to_string_rows(
        value: t.SequenceOf[t.Tests.TestobjectSerializable],
    ) -> t.SequenceOf[t.StrSequence]:
        return [
            [str(cell) for cell in row]
            for row in value
            if isinstance(row, t.SEQUENCE_PAIR_TYPES)
        ]

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
        match unwrapped:
            case str() | bytes():
                return unwrapped
            case m.ConfigMap() | m.Dict():
                return FlextTestsPayloadUtilities.to_config_map(unwrapped.root)
            case m.BaseModel():
                return unwrapped
            case _ if self._is_mapping(unwrapped):
                return FlextTestsPayloadUtilities.to_config_map(unwrapped)
            case _ if self._is_nested_rows(unwrapped):
                sequence_value: t.SequenceOf[t.Tests.TestobjectSerializable] = (
                    unwrapped if isinstance(unwrapped, t.SEQUENCE_PAIR_TYPES) else ()
                )
                return self._to_string_rows(sequence_value)
            case _:
                return str(unwrapped)

    def _extract_content[TFileContent: t.Tests.FileContentPlain](
        self,
        content: TFileContent | p.ResultLike[TFileContent],
        extract_result: bool,
    ) -> t.Tests.FileContentPlain:
        """Extract actual content from r or return as-is.

        Uses isinstance check for result-like wrappers and unwrap_or for extraction.

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


__all__: list[str] = ["FlextTestsFilesCreationMixin"]

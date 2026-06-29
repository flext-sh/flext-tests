"""File-content serialization helpers for flext-tests."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from flext_infra import u
from flext_tests import c, m, t
from flext_tests._utilities._files._creation_parts.creation_part_01 import (
    FlextTestsFilesCreationMixin as FlextTestsFilesCreationMixinPart01,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsFilesCreationMixin(FlextTestsFilesCreationMixinPart01):
    """Serialize normalized file creation content."""

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


__all__: list[str] = ["FlextTestsFilesCreationMixin"]

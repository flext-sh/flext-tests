"""File creation utilities for flext-tests."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from flext_tests import c, m, p, t, u

from ..payload import FlextTestsPayloadUtilities
from ._lifecycle import FlextTestsFilesLifecycleMixin


class FlextTestsFilesCreationMixin(FlextTestsFilesLifecycleMixin):
    """Create files from one validated native payload boundary."""

    @staticmethod
    def is_mapping[ValueT](value: ValueT) -> bool:
        """Identify native mappings without pretending to validate their leaves."""
        return isinstance(value, Mapping)

    @staticmethod
    def to_payload_mapping[ValueT](value: ValueT) -> t.MappingKV[str, m.Tests.Payload]:
        """Own a native mapping and retain every rich child value."""
        payload = FlextTestsPayloadUtilities.to_payload(value)
        if payload.kind != "mapping":
            msg = "File content requires a native mapping"
            raise TypeError(msg)
        return payload.entries

    @staticmethod
    def _to_string_rows(value: p.Tests.Payload) -> t.SequenceOf[t.StrSequence]:
        """Render validated CSV cells only at their textual output boundary."""
        return [
            [str(FlextTestsPayloadUtilities.to_match_value(cell)) for cell in row.items]
            for row in value.items
        ]

    def _coerce_file_content[ValueT](self, value: ValueT) -> m.Tests.Payload:
        """Own file input without dumping native models or swallowing failures."""
        return FlextTestsPayloadUtilities.to_payload(value)

    def _extract_content[ContentT](
        self, content: ContentT | p.Result[ContentT], *, extract_result: bool
    ) -> m.Tests.Payload:
        """Extract explicitly requested results before validating native content."""
        if extract_result and isinstance(content, p.Result):
            if content.failure:
                msg = f"Cannot create file from failed result: {content.error}"
                raise ValueError(msg)
            return self._coerce_file_content(content.value)
        return self._coerce_file_content(content)

    def _is_nested_rows[ValueT](self, value: ValueT) -> bool:
        """Recognize nonempty list/tuple rows without a second recursive adapter."""
        payload = FlextTestsPayloadUtilities.to_payload(value)
        return (
            payload.kind in {"list", "tuple"}
            and bool(payload.items)
            and all(row.kind in {"list", "tuple"} for row in payload.items)
        )

    def _write_content_by_format(
        self,
        *,
        file_path: Path,
        actual_content: p.Tests.Payload,
        actual_fmt: str,
        params: m.Tests.CreateParams,
    ) -> None:
        """Write through existing format owners after native validation."""
        match actual_fmt:
            case c.Tests.FILE_FORMAT_BIN:
                atom = actual_content.atom
                content = (
                    atom
                    if actual_content.kind == "atom" and isinstance(atom, bytes)
                    else str(
                        FlextTestsPayloadUtilities.to_match_value(actual_content)
                    ).encode(params.enc)
                )
                file_path.write_bytes(content)
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
                        actual_content=actual_content, headers=params.headers
                    ),
                )
            case _:
                file_path.write_text(
                    str(FlextTestsPayloadUtilities.to_match_value(actual_content)),
                    encoding=params.enc,
                )

    @staticmethod
    def _build_json_payload(actual_content: p.Tests.Payload) -> t.JsonValue:
        """Perform JSON conversion only at the selected file output boundary."""
        if actual_content.kind == "atom" and isinstance(
            actual_content.atom, m.BaseModel
        ):
            return t.json_value_adapter().validate_python(
                actual_content.atom.model_dump(mode="json")
            )
        normalized = FlextTestsPayloadUtilities.to_normalized_value(actual_content)
        if actual_content.kind == "mapping":
            return normalized
        return {"value": normalized} if normalized else {}

    @staticmethod
    def _build_csv_rows(
        *, actual_content: p.Tests.Payload, headers: t.StrSequence | None
    ) -> list[t.StrSequence]:
        """Build CSV rows while keeping native matching independent of text."""
        rows: list[t.StrSequence] = []
        if headers:
            rows.append(list(headers))
        if actual_content.kind in {"list", "tuple"}:
            rows.extend(FlextTestsFilesCreationMixin._to_string_rows(actual_content))
        else:
            rows.append([
                str(FlextTestsPayloadUtilities.to_match_value(actual_content))
            ])
        return rows

    def create[ContentT](
        self,
        content: ContentT | p.Result[ContentT],
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
        """Create a file after validating the complete native input tree."""
        content_to_validate = self._extract_content(
            content, extract_result=extract_result
        )
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
        actual_content = params.content
        native_content = FlextTestsPayloadUtilities.to_match_value(actual_content)
        actual_fmt = u.Cli.files_detect_format_from_content(
            native_content, params.name, params.fmt
        )
        target_dir = self._resolve_directory(params.directory)
        file_path = target_dir / params.name
        self._write_content_by_format(
            file_path=file_path,
            actual_content=actual_content,
            actual_fmt=actual_fmt,
            params=params,
        )
        if params.readonly:
            file_path.chmod(c.Tests.PERMISSION_READONLY_FILE)
        self._created_files.append(file_path)
        return file_path


__all__: list[str] = ["FlextTestsFilesCreationMixin"]

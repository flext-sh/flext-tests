"""File creation utilities for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Annotated, cast

from flext_tests import c, m, p, t, u
from flext_tests._utilities._files._lifecycle import FlextTestsFilesLifecycleMixin
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsFilesCreationMixin(FlextTestsFilesLifecycleMixin):
    """Create files from one validated native payload boundary."""

    @staticmethod
    def matches_native_mapping(value: p.AttributeProbe) -> bool:
        """Identify native mappings without pretending to validate their leaves.

        Returns:
            The resulting ``bool``.
        """
        return isinstance(value, Mapping)

    @staticmethod
    def to_payload_mapping(
        value: p.AttributeProbe,
    ) -> t.MappingKV[str, m.Tests.Payload]:
        """Own a native mapping and retain every rich child value.

        Returns:
            The resulting ``t.MappingKV[str, m.Tests.Payload]``.

        Raises:
            TypeError: If File content requires a native mapping.
        """
        payload = FlextTestsPayloadUtilities.to_payload(value)
        if payload.kind != "mapping":
            msg = "File content requires a native mapping"
            raise TypeError(msg)
        return payload.entries

    @staticmethod
    def _to_string_rows(value: p.Tests.Payload) -> t.SequenceOf[t.StrSequence]:
        """Render validated CSV cells only at their textual output boundary.

        Returns:
            The resulting ``t.SequenceOf[t.StrSequence]``.
        """
        return [
            [str(FlextTestsPayloadUtilities.to_match_value(cell)) for cell in row.items]
            for row in value.items
        ]

    @staticmethod
    def _coerce_file_content(value: p.AttributeProbe) -> m.Tests.Payload:
        """Own file input without dumping native models or swallowing failures.

        Returns:
            The resulting ``m.Tests.Payload``.
        """
        return FlextTestsPayloadUtilities.to_payload(value)

    def _extract_content[ContentT](
        self,
        content: ContentT | p.Result[ContentT],
        *,
        extract_result: bool,
    ) -> m.Tests.Payload:
        """Extract explicitly requested results before validating native content.

        Returns:
            The resulting ``m.Tests.Payload``.

        Raises:
            ValueError: If Cannot create file from failed result.
        """
        if extract_result and isinstance(content, p.Result):
            if content.failure:
                msg = f"Cannot create file from failed result: {content.error}"
                raise ValueError(msg)
            return self._coerce_file_content(content.value)
        return self._coerce_file_content(content)

    @staticmethod
    def _is_nested_rows(value: p.AttributeProbe) -> bool:
        """Recognize nonempty list/tuple rows without a second recursive adapter.

        Returns:
            The resulting ``bool``.
        """
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
                        FlextTestsPayloadUtilities.to_match_value(actual_content),
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
                        actual_content=actual_content,
                        headers=params.headers,
                    ),
                )
            case _:
                file_path.write_text(
                    str(FlextTestsPayloadUtilities.to_match_value(actual_content)),
                    encoding=params.enc,
                )

    @staticmethod
    def _build_json_payload(actual_content: p.Tests.Payload) -> t.JsonValue:
        """Perform JSON conversion only at the selected file output boundary.

        Returns:
            The resulting ``t.JsonValue``.
        """
        if actual_content.kind == "atom" and isinstance(
            actual_content.atom,
            m.BaseModel,
        ):
            return t.json_value_adapter().validate_python(
                actual_content.atom.model_dump(mode="json"),
            )
        normalized = FlextTestsPayloadUtilities.to_normalized_value(actual_content)
        if actual_content.kind == "mapping":
            return normalized
        return {"value": normalized} if normalized else {}

    @staticmethod
    def _build_csv_rows(
        *,
        actual_content: p.Tests.Payload,
        headers: t.StrSequence | None,
    ) -> list[t.StrSequence]:
        """Build CSV rows while keeping native matching independent of text.

        Returns:
            The resulting ``list[t.StrSequence]``.
        """
        rows: list[t.StrSequence] = []
        if headers:
            rows.append(list(headers))
        if actual_content.kind in {"list", "tuple"}:
            rows.extend(FlextTestsFilesCreationMixin._to_string_rows(actual_content))
        else:
            rows.append([
                str(FlextTestsPayloadUtilities.to_match_value(actual_content)),
            ])
        return rows

    class CreateOptions(m.Value):
        """Optional creation knobs; defaults mirror the canonical SSOT."""

        fmt: Annotated[
            c.Tests.FileFormat,
            u.Field(description="Target file format; AUTO detects from content."),
        ] = c.Tests.FILE_FORMAT_AUTO
        enc: Annotated[
            str,
            u.Field(description="Text encoding for textual formats."),
        ] = c.Tests.DEFAULT_ENCODING
        indent: Annotated[
            int,
            u.Field(description="Indent width for JSON output."),
        ] = c.Tests.DEFAULT_JSON_INDENT
        delim: Annotated[
            str,
            u.Field(description="Delimiter for CSV output."),
        ] = c.Tests.DEFAULT_CSV_DELIMITER
        headers: Annotated[
            t.StrSequence | None,
            u.Field(description="Optional CSV header row."),
        ] = None
        readonly: Annotated[
            bool,
            u.Field(description="chmod the created file read-only when true."),
        ] = False
        extract_result: Annotated[
            bool,
            u.Field(description="Unwrap a passed Result payload before validation."),
        ] = True

    def create[ContentT](
        self,
        content: ContentT | p.Result[ContentT],
        name: str = c.Tests.DEFAULT_FILENAME,
        directory: Path | None = None,
        *,
        options: FlextTestsFilesCreationMixin.CreateOptions | None = None,
    ) -> Path:
        """Create a file after validating the complete native input tree.

        Returns:
            The resulting ``Path``.
        """
        chosen = options or FlextTestsFilesCreationMixin.CreateOptions()
        content_to_validate = self._extract_content(
            content,
            extract_result=chosen.extract_result,
        )
        params = m.Tests.CreateParams.model_validate({
            **chosen.model_dump(),
            "content": content_to_validate,
            "name": name,
            "directory": directory,
        })
        actual_content = params.content
        native_content = FlextTestsPayloadUtilities.to_match_value(actual_content)
        # files_detect_format_from_content dispatches purely on the runtime
        # shape (bytes, model, mapping, list) and routes every other arm —
        # scalar atoms and None — to its extension fallback; its declared
        # parameter union does not model those fallback arms. The callable
        # assertion records that shape-total contract for this projection.
        detect_format = cast(
            "Callable[[object, str, str], str]",
            u.Cli.files_detect_format_from_content,
        )
        actual_fmt = detect_format(native_content, params.name, params.fmt)
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

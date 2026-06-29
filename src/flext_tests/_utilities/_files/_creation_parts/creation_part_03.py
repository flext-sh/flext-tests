"""Public file creation method for flext-tests."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from flext_infra import u
from flext_tests import c, m, p, t
from flext_tests._utilities._files._creation_parts.creation_part_02 import (
    FlextTestsFilesCreationMixin as FlextTestsFilesCreationMixinPart02,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsFilesCreationMixin(FlextTestsFilesCreationMixinPart02):
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
        """Create file with auto-detection or explicit format."""
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
        file_path: Path = target_dir / params.name
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


__all__: list[str] = ["FlextTestsFilesCreationMixin"]

"""File-content coercion helpers for flext-tests."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TypeIs

from flext_tests import c, m, p, t
from flext_tests._utilities._files._lifecycle import FlextTestsFilesLifecycleMixin
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsFilesCreationMixin(FlextTestsFilesLifecycleMixin):
    """Coerce and extract file creation content."""

    @staticmethod
    def _is_file_result[TFileContent: t.Tests.FileContentPlain](
        value: TFileContent | p.ResultLike[TFileContent],
    ) -> TypeIs[p.ResultLike[TFileContent]]:
        """Narrow file input to a result-like wrapper."""
        return isinstance(value, p.ResultLike)

    @staticmethod
    def is_mapping(
        value: t.Tests.FileContentPlain | t.Tests.TestobjectSerializable | None,
    ) -> TypeIs[Mapping[str, t.Tests.TestobjectSerializable]]:
        return isinstance(value, Mapping)

    @staticmethod
    def to_payload_mapping(
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
            case _ if self.is_mapping(unwrapped):
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
        """Extract actual content from a result-like wrapper or return as-is."""
        if not extract_result:
            return self._coerce_file_content(content)
        if isinstance(content, bytes):
            return content
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

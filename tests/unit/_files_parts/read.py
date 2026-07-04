"""Private file read test mixins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import tf, tm
from tests.constants import c
from tests.models import m
from tests.utilities import u

if TYPE_CHECKING:
    from pathlib import Path

    from tests.typings import t


class FilesReadMixin:
    """File read tests."""

    def test_read_text_file(self, tmp_path: Path) -> None:
        """Test read() returns text content for .txt files."""
        manager = tf(base_dir=tmp_path)
        path = manager.create("hello world", "test.txt")
        result = manager.read(path)
        _ = u.Tests.assert_success(result)
        tm.that(result.value, eq="hello world")

    def test_read_binary_file(self, tmp_path: Path) -> None:
        """Test read() returns bytes content for .bin files."""
        manager = tf(base_dir=tmp_path)
        path = manager.create(b"\x00\x01\x02", "data.bin", fmt=c.Tests.FILE_FORMAT_BIN)
        result = manager.read(path)
        _ = u.Tests.assert_success(result)
        tm.that(result.value, eq=b"\x00\x01\x02")

    def test_read_json_file(self, tmp_path: Path) -> None:
        """Test read() returns dict content for .json files."""
        manager = tf(base_dir=tmp_path)
        content_root: dict[str, t.JsonPayload] = {"key": "value", "number": 42}
        content: m.ConfigMap = m.ConfigMap(root=content_root)
        path = manager.create(content, "settings.json")
        result = manager.read(path)
        _ = u.Tests.assert_success(result)
        tm.that(result.value, eq=content_root)

    def test_read_yaml_file(self, tmp_path: Path) -> None:
        """Test read() returns dict content for .yaml files."""
        manager = tf(base_dir=tmp_path)
        content: m.ConfigMap = m.ConfigMap(root={"name": "test", "enabled": True})
        path = manager.create(content, "settings.yaml")
        result = manager.read(path)
        _ = u.Tests.assert_success(result)
        read_value = result.value
        assert isinstance(read_value, m.ConfigMap)
        tm.that(read_value.model_dump() == content.model_dump(), eq=True)

    def test_read_csv_file(self, tmp_path: Path) -> None:
        """Test read() returns t.SequenceOf[list] content for .csv files."""
        manager = tf(base_dir=tmp_path)
        content = [["a", "b"], ["1", "2"]]
        path = manager.create(content, "data.csv")
        result = manager.read(path, has_headers=False)
        _ = u.Tests.assert_success(result)
        data = result.value
        tm.that(data, is_=list)
        tm.that(len(data), eq=2)

    def test_read_csv_file_with_headers(self, tmp_path: Path) -> None:
        """Test read() CSV with headers skips first row by default."""
        manager = tf(base_dir=tmp_path)
        content = [["header1", "header2"], ["1", "2"], ["3", "4"]]
        path = manager.create(content, "data.csv", headers=None)
        result = manager.read(path)
        _ = u.Tests.assert_success(result)
        data = result.value
        tm.that(data, is_=list)
        tm.that(len(data), eq=2)

    def test_read_nonexistent_file(self, tmp_path: Path) -> None:
        """Test read() returns failure for non-existent file."""
        manager = tf(base_dir=tmp_path)
        path = tmp_path / "nonexistent.txt"
        result = manager.read(path)
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, none=False)
        if result.error is None:
            error_msg = "Expected error to be not None"
            raise TypeError(error_msg)
        tm.that(
            (
                "not found" in result.error.lower()
                or "not exist" in result.error.lower()
            ),
            eq=True,
        )

    def test_read_explicit_format(self, tmp_path: Path) -> None:
        """Test read() with explicit format override."""
        manager = tf(base_dir=tmp_path)
        path = manager.create("plain text", "data.dat", fmt=c.Tests.FILE_FORMAT_TEXT)
        result = manager.read(path, fmt=c.Tests.FILE_FORMAT_TEXT)
        _ = u.Tests.assert_success(result)
        tm.that(result.value, eq="plain text")

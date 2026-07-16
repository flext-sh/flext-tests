"""Private file format creation test mixins."""

from __future__ import annotations

from pathlib import Path

from flext_tests import tf, tm
from tests import c, m, p, t, u


class FilesFormatsMixin:
    """File format creation tests."""

    def test_create_text_auto_detect(self, tmp_path: Path) -> None:
        """Test create() auto-detects text from str content."""
        manager = tf(base_dir=tmp_path)
        path = manager.create("hello world", "test.txt")
        tm.that(path.exists(), eq=True)
        tm.that(path.read_text(), eq="hello world")
        tm.that(path.suffix, eq=".txt")

    def test_create_binary_auto_detect(self, tmp_path: Path) -> None:
        """Test create() auto-detects binary from bytes content."""
        manager = tf(base_dir=tmp_path)
        path = manager.create(b"\x00\x01\x02", "data.bin")
        tm.that(path.exists(), eq=True)
        tm.that(path.read_bytes(), eq=b"\x00\x01\x02")

    def test_create_json_auto_detect_from_dict(self, tmp_path: Path) -> None:
        """Test create() auto-detects JSON from dict content."""
        manager = tf(base_dir=tmp_path)
        content: p.ConfigMap = m.ConfigMap(root={"key": "value", "number": 42})
        path = manager.create(content, "settings.json")
        tm.that(path.exists(), eq=True)
        empty_data: t.JsonMapping = {}
        data = u.Cli.json_read(path).unwrap_or(empty_data)
        tm.that(data, eq=content.root)

    def test_create_yaml_auto_detect_from_extension(self, tmp_path: Path) -> None:
        """Test create() auto-detects YAML from .yaml extension."""
        manager = tf(base_dir=tmp_path)
        content: p.ConfigMap = m.ConfigMap(root={"name": "test", "enabled": True})
        path = manager.create(content, "settings.yaml")
        tm.that(path.exists(), eq=True)
        empty_data: t.JsonMapping = {}
        data = u.Cli.yaml_parse(path.read_text()).unwrap_or(empty_data)
        tm.that(data, eq=content.root)

    def test_create_csv_auto_detect_from_list(self, tmp_path: Path) -> None:
        """Test create() auto-detects CSV from t.SequenceOf[list] content."""
        manager = tf(base_dir=tmp_path)
        content = [["a", "b"], ["1", "2"]]
        path = manager.create(content, "data.csv")
        tm.that(path.exists(), eq=True)
        lines = path.read_text().strip().split("\n")
        tm.that(len(lines), eq=2)

    def test_create_csv_with_headers(self, tmp_path: Path) -> None:
        """Test create() CSV with explicit headers."""
        manager = tf(base_dir=tmp_path)
        content = [["1", "2"], ["3", "4"]]
        path = manager.create(content, "data.csv", headers=["col1", "col2"])
        tm.that(path.exists(), eq=True)
        lines = path.read_text().strip().split("\n")
        tm.that(lines[0], eq="col1,col2")
        tm.that(len(lines), eq=3)

    def test_create_explicit_format(self, tmp_path: Path) -> None:
        """Test create() with explicit format override."""
        manager = tf(base_dir=tmp_path)
        path = manager.create(b"raw bytes", "data.dat", fmt=c.Tests.FILE_FORMAT_BIN)
        tm.that(path.exists(), eq=True)
        tm.that(path.read_bytes(), eq=b"raw bytes")

    def test_create_custom_encoding(self, tmp_path: Path) -> None:
        """Test create() with custom encoding."""
        manager = tf(base_dir=tmp_path)
        path = manager.create("áéíóú", "unicode.txt", enc="utf-16")
        tm.that(path.exists(), eq=True)
        tm.that(path.read_text(encoding="utf-16"), eq="áéíóú")

    def test_create_json_custom_indent(self, tmp_path: Path) -> None:
        """Test create() JSON with custom indentation."""
        manager = tf(base_dir=tmp_path)
        content = m.ConfigMap(root={"key": "value"})
        path = manager.create(content, "settings.json", indent=4)
        tm.that(path.exists(), eq=True)
        text = path.read_text()
        tm.that(text, has="    ")

    def test_create_in_custom_directory(self, tmp_path: Path) -> None:
        """Test create() in custom directory."""
        manager = tf(base_dir=tmp_path)
        custom_dir = tmp_path / "subdir"
        path = manager.create("content", "test.txt", directory=custom_dir)
        tm.that(path.exists(), eq=True)
        tm.that(path.parent, eq=custom_dir)

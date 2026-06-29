"""Private file batch and create_in test mixins."""

from __future__ import annotations

from pathlib import Path

from tests import c, m, r, t, tf, tm, u


class FilesBatchCreateInMixin:
    """File batch and create_in tests."""

    def test_batch_create_multiple_files(self, tmp_path: Path) -> None:
        """Test batch create for multiple files."""
        manager = tf(base_dir=tmp_path)
        result = manager.batch_files(
            {"file1.txt": "content1", "file2.txt": "content2", "file3.txt": "content3"},
            directory=tmp_path,
        )
        batch_result: m.Tests.BatchResult = u.Tests.assert_success(result)
        tm.that(batch_result.total, eq=3)
        assert batch_result.success_count == 3
        assert batch_result.failure_count == 0
        tm.that(batch_result.succeeded, eq=3)

    def test_batch_create_json_files(self, tmp_path: Path) -> None:
        """Test batch create for JSON files."""
        manager = tf(base_dir=tmp_path)
        result = manager.batch_files(
            {"settings1.json": {"key": "value1"}, "settings2.json": {"key": "value2"}},
            directory=tmp_path,
        )
        batch_result: m.Tests.BatchResult = u.Tests.assert_success(result)
        assert batch_result.success_count == 2
        settings1 = tmp_path / "settings1.json"
        tm.that(settings1.exists(), eq=True)
        tm.that(u.Cli.json_read(settings1).unwrap_or({})["key"], eq="value1")

    def test_batch_on_error_collect(self, tmp_path: Path) -> None:
        """Test batch with on_error='collect' continues on failures."""
        manager = tf(base_dir=tmp_path)
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        result = manager.batch_files(
            {"valid.txt": "content"},
            directory=tmp_path,
            on_error=c.Tests.ErrorMode.COLLECT,
        )
        _ = u.Tests.assert_success(result)
        batch_result = result.value
        tm.that(batch_result.succeeded, gte=1)

    def test_batch_result_model_structure(self, tmp_path: Path) -> None:
        """Test BatchResult model has correct structure."""
        manager = tf(base_dir=tmp_path)
        result = manager.batch_files({"file.txt": "content"}, directory=tmp_path)
        _ = u.Tests.assert_success(result)
        batch_result = result.value
        tm.that(batch_result.succeeded, is_=int)
        tm.that(batch_result.failed, is_=int)
        tm.that(batch_result.total, is_=int)

    def test_create_in_text_content(self, tmp_path: Path) -> None:
        """Test create_in() for text content."""
        path = tf(base_dir=tmp_path).create("hello world", "test.txt")
        tm.that(path.exists(), eq=True)
        tm.that(path.read_text(), eq="hello world")

    def test_create_in_dict_content(self, tmp_path: Path) -> None:
        """Test create_in() for dict content (JSON)."""
        path = tf(base_dir=tmp_path).create(
            m.ConfigMap(root={"key": "value"}), "settings.json"
        )
        tm.that(path.exists(), eq=True)
        empty_content: t.JsonMapping = {}
        content = u.Cli.json_read(path).unwrap_or(empty_content)
        tm.that(content, eq={"key": "value"})

    def test_create_in_yaml_content(self, tmp_path: Path) -> None:
        """Test create_in() for YAML file."""
        path = tf(base_dir=tmp_path).create(
            m.ConfigMap(root={"setting": True}),
            "settings.yaml",
        )
        tm.that(path.exists(), eq=True)
        empty_content: t.JsonMapping = {}
        content = u.Cli.yaml_parse(path.read_text()).unwrap_or(empty_content)
        tm.that(content, eq={"setting": True})

    def test_create_in_pydantic_model(self, tmp_path: Path) -> None:
        """Test create_in() for Pydantic model content."""

        class UserModel(m.BaseModel):
            name: str
            age: int

        user = UserModel(name="Alice", age=30)
        path = tf(base_dir=tmp_path).create(user, "user.json")
        tm.that(path.exists(), eq=True)
        empty_content: t.JsonMapping = {}
        content = u.Cli.json_read(path).unwrap_or(empty_content)
        expected: t.Tests.TestobjectSerializable = {"name": "Alice", "age": 30}
        tm.that(content, eq=expected)

    def test_create_in_format_detection(self, tmp_path: Path) -> None:
        """Test create_in() format auto-detection from extension."""
        path1 = tf(base_dir=tmp_path).create(
            m.ConfigMap(root={"key": "value"}),
            "settings.json",
        )
        tm.that(path1.exists(), eq=True)
        tm.that(u.Cli.json_read(path1).unwrap_or({}), eq={"key": "value"})
        path2 = tf(base_dir=tmp_path).create(
            m.ConfigMap(root={"key": "value"}),
            "settings.yaml",
        )
        tm.that(path2.exists(), eq=True)
        tm.that(
            u.Cli.yaml_parse(path2.read_text()).unwrap_or({}),
            eq={"key": "value"},
        )
        path3 = tf(base_dir=tmp_path).create([["a", "b"], ["1", "2"]], "data.csv")
        tm.that(path3.exists(), eq=True)
        lines = path3.read_text().strip().split("\n")
        tm.that(len(lines), gte=2)

    def test_create_in_with_flextresult(self, tmp_path: Path) -> None:
        """Test create_in() with r content extraction."""
        result = r[m.ConfigMap].ok(m.ConfigMap(root={"status": "success"}))
        path = tf(base_dir=tmp_path).create(result, "result.json")
        tm.that(path.exists(), eq=True)
        empty_content: t.JsonMapping = {}
        content = u.Cli.json_read(path).unwrap_or(empty_content)
        tm.that(content, eq={"status": "success"})

    def test_create_in_custom_format(self, tmp_path: Path) -> None:
        """Test create_in() with explicit format override."""
        path = tf(base_dir=tmp_path).create(
            b"binary data", "data.dat", fmt=c.Tests.FILE_FORMAT_BIN
        )
        tm.that(path.exists(), eq=True)
        tm.that(path.read_bytes(), eq=b"binary data")

    def test_create_in_custom_encoding(self, tmp_path: Path) -> None:
        """Test create_in() with custom encoding."""
        path = tf(base_dir=tmp_path).create("áéíóú", "unicode.txt", enc="utf-16")
        tm.that(path.exists(), eq=True)
        tm.that(path.read_text(encoding="utf-16"), eq="áéíóú")

    def test_create_in_json_indent(self, tmp_path: Path) -> None:
        """Test create_in() with custom JSON indentation."""
        content: m.ConfigMap = m.ConfigMap(
            root={"key": "value", "nested": {"a": 1}},
        )
        path = tf(base_dir=tmp_path).create(content, "settings.json", indent=4)
        tm.that(path.exists(), eq=True)
        text = path.read_text()
        tm.that(text, has="    ")

    def test_create_in_csv_with_headers(self, tmp_path: Path) -> None:
        """Test create_in() CSV with explicit headers."""
        content = [["1", "2"], ["3", "4"]]
        path = tf(base_dir=tmp_path).create(
            content, "data.csv", headers=["col1", "col2"]
        )
        tm.that(path.exists(), eq=True)
        lines = path.read_text().strip().split("\n")
        tm.that(lines[0], eq="col1,col2")
        tm.that(len(lines), eq=3)

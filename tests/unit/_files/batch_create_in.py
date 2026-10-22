"""Private file create_in test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import FlextTestsFiles
from tests import c, m, r, t, tm, u


class TestsFlextTestsFilesBatchCreateInMixin:
    """File create_in tests."""

    @staticmethod
    def test_create_in_text_content(tmp_path: Path) -> None:
        """Test create_in() for text content."""
        path = FlextTestsFiles(base_dir=tmp_path).create("hello world", "test.txt")
        tm.ok(path.exists())
        tm.that(path.read_text(), eq="hello world")

    @staticmethod
    def test_create_in_dict_content(tmp_path: Path) -> None:
        """Test create_in() for dict content (JSON)."""
        path = FlextTestsFiles(base_dir=tmp_path).create(
            m.ConfigMap(root={"key": "value"}),
            "settings.json",
        )
        tm.ok(path.exists())
        empty_content: t.JsonMapping = {}
        content = u.Cli.json_read(path).unwrap_or(empty_content)
        tm.that(content, eq={"key": "value"})

    @staticmethod
    def test_create_in_yaml_content(tmp_path: Path) -> None:
        """Test create_in() for YAML file."""
        path = FlextTestsFiles(base_dir=tmp_path).create(
            m.ConfigMap(root={"setting": True}),
            "settings.yaml",
        )
        tm.ok(path.exists())
        empty_content: t.JsonMapping = {}
        content = u.Cli.yaml_parse(path.read_text()).unwrap_or(empty_content)
        tm.that(content, eq={"setting": True})

    @staticmethod
    def test_create_in_pydantic_model(tmp_path: Path) -> None:
        """Test create_in() for Pydantic model content."""

        class UserModel(m.BaseModel):
            name: str
            age: int

        user = UserModel(name="Alice", age=30)
        path = FlextTestsFiles(base_dir=tmp_path).create(user, "user.json")
        tm.ok(path.exists())
        empty_content: t.JsonMapping = {}
        content = u.Cli.json_read(path).unwrap_or(empty_content)
        expected: t.Tests.TestobjectSerializable = {"name": "Alice", "age": 30}
        tm.that(content, eq=expected)

    @staticmethod
    def test_create_in_format_detection(tmp_path: Path) -> None:
        """Test create_in() format auto-detection from extension."""
        path1 = FlextTestsFiles(base_dir=tmp_path).create(
            m.ConfigMap(root={"key": "value"}),
            "settings.json",
        )
        tm.ok(path1.exists())
        tm.that(u.Cli.json_read(path1).unwrap(), eq={"key": "value"})
        path2 = FlextTestsFiles(base_dir=tmp_path).create(
            m.ConfigMap(root={"key": "value"}),
            "settings.yaml",
        )
        tm.ok(path2.exists())
        tm.that(u.Cli.yaml_parse(path2.read_text()).unwrap(), eq={"key": "value"})
        path3 = FlextTestsFiles(base_dir=tmp_path).create(
            [["a", "b"], ["1", "2"]],
            "data.csv",
        )
        tm.ok(path3.exists())
        lines = path3.read_text().strip().split("\n")
        tm.that(len(lines), gte=2)

    @staticmethod
    def test_create_in_with_flextresult(tmp_path: Path) -> None:
        """Test create_in() with r content extraction."""
        result = r[t.Tests.FileContentPlain].ok(m.ConfigMap(root={"status": "success"}))
        # The generic create() solver cannot bind the protocol-carried payload
        # through the result union; unwrap explicitly so ContentT binds to the
        # concrete config map the file carries.
        path = FlextTestsFiles(base_dir=tmp_path).create(
            result.unwrap(),
            "result.json",
        )
        tm.ok(path.exists())
        empty_content: t.JsonMapping = {}
        content = u.Cli.json_read(path).unwrap_or(empty_content)
        tm.that(content, eq={"status": "success"})

    @staticmethod
    def test_create_in_custom_format(tmp_path: Path) -> None:
        """Test create_in() with explicit format override."""
        path = FlextTestsFiles(base_dir=tmp_path).create(
            b"binary data",
            "data.dat",
            options=FlextTestsFiles.CreateOptions(fmt=c.Tests.FILE_FORMAT_BIN),
        )
        tm.ok(path.exists())
        tm.that(path.read_bytes(), eq=b"binary data")

    @staticmethod
    def test_create_in_custom_encoding(tmp_path: Path) -> None:
        """Test create_in() with custom encoding."""
        path = FlextTestsFiles(base_dir=tmp_path).create(
            "áéíóú",
            "unicode.txt",
            options=FlextTestsFiles.CreateOptions(enc="utf-16"),
        )
        tm.ok(path.exists())
        tm.that(path.read_text(encoding="utf-16"), eq="áéíóú")

    @staticmethod
    def test_create_in_json_indent(tmp_path: Path) -> None:
        """Test create_in() with custom JSON indentation."""
        content: m.ConfigMap = m.ConfigMap(root={"key": "value", "nested": {"a": 1}})
        path = FlextTestsFiles(base_dir=tmp_path).create(
            content,
            "settings.json",
            options=FlextTestsFiles.CreateOptions(indent=4),
        )
        tm.ok(path.exists())
        text = path.read_text()
        tm.that(text, has="    ")

    @staticmethod
    def test_create_in_csv_with_headers(tmp_path: Path) -> None:
        """Test create_in() CSV with explicit headers."""
        content = [["1", "2"], ["3", "4"]]
        path = FlextTestsFiles(base_dir=tmp_path).create(
            content,
            "data.csv",
            options=FlextTestsFiles.CreateOptions(headers=["col1", "col2"]),
        )
        tm.ok(path.exists())
        lines = path.read_text().strip().split("\n")
        tm.that(lines[0], eq="col1,col2")
        tm.that(len(lines), eq=3)

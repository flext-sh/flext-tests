"""Private file content metadata test mixins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli import u as cli_u
from flext_tests import tf, tm
from tests import m
from tests import u

if TYPE_CHECKING:
    from pathlib import Path


class FilesContentMetaMixin:
    """File content metadata tests."""

    def test_info_parse_content_json_dict(self, tmp_path: Path) -> None:
        """Test info() with parse_content=True for JSON dict."""
        manager = tf(base_dir=tmp_path)
        path = manager.create(
            m.ConfigMap(root={"key1": "value1", "key2": "value2"}),
            "settings.json",
        )
        result = manager.info(path, parse_content=True)
        _ = u.Tests.assert_success(result)
        info = result.value
        tm.that(info.content_meta, none=False)
        if info.content_meta is None:
            error_msg = "Expected content_meta to be not None"
            raise TypeError(error_msg)
        tm.that(info.content_meta.key_count, eq=2)
        tm.that(info.content_meta.item_count, none=True)

    def test_info_parse_content_json_list(self, tmp_path: Path) -> None:
        """Test info() with parse_content=True for JSON list."""
        manager = tf(base_dir=tmp_path)
        content = cli_u.Cli.json_dumps([1, 2, 3, 4, 5]).unwrap()
        path = tmp_path / "list.json"
        _ = path.write_text(content)
        result = manager.info(path, parse_content=True)
        _ = u.Tests.assert_success(result)
        info = result.value
        assert info.content_meta is not None
        tm.that(info.content_meta.key_count, none=True)
        tm.that(info.content_meta.item_count, eq=5)

    def test_info_parse_content_yaml_dict(self, tmp_path: Path) -> None:
        """Test info() with parse_content=True for YAML dict."""
        manager = tf(base_dir=tmp_path)
        path = manager.create(
            m.ConfigMap(root={"a": 1, "b": 2, "c": 3}),
            "settings.yaml",
        )
        result = manager.info(path, parse_content=True)
        _ = u.Tests.assert_success(result)
        info = result.value
        assert info.content_meta is not None
        tm.that(info.content_meta.key_count, eq=3)

    def test_info_parse_content_csv(self, tmp_path: Path) -> None:
        """Test info() with parse_content=True for CSV."""
        manager = tf(base_dir=tmp_path)
        csv_content = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"
        path = tmp_path / "data.csv"
        _ = path.write_text(csv_content)
        result = manager.info(path, parse_content=True, detect_fmt=True)
        _ = u.Tests.assert_success(result)
        info = result.value
        assert info.content_meta is not None
        tm.that(info.content_meta.row_count, eq=3)
        tm.that(info.content_meta.column_count, eq=3)

    def test_info_validate_model_success(self, tmp_path: Path) -> None:
        """Test info() with validate_model for valid model."""

        class SimpleModel(m.BaseModel):
            name: str
            age: int

        manager = tf(base_dir=tmp_path)
        path = manager.create(
            m.ConfigMap(root={"name": "Alice", "age": 30}),
            "user.json",
        )
        result = manager.info(path, validate_model=SimpleModel)
        _ = u.Tests.assert_success(result)
        info = result.value
        assert info.content_meta is not None
        tm.that(info.content_meta.model_valid is True, eq=True)
        tm.that(info.content_meta.model_name, eq="SimpleModel")

    def test_info_validate_model_failure(self, tmp_path: Path) -> None:
        """Test info() with validate_model for invalid model."""

        class StrictModel(m.BaseModel):
            required_field: str

        manager = tf(base_dir=tmp_path)
        path = manager.create(
            m.ConfigMap(root={"other_field": "value"}),
            "invalid.json",
        )
        result = manager.info(path, validate_model=StrictModel)
        _ = u.Tests.assert_success(result)
        info = result.value
        assert info.content_meta is not None
        tm.that(info.content_meta.model_valid is False, eq=True)
        tm.that(info.content_meta.model_name, eq="StrictModel")

"""Private file context and alias test mixins."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from flext_tests import tf, tm
from tests import m
from tests import u

if TYPE_CHECKING:
    from tests import t


class FilesContextsMixin:
    """File context and alias tests."""

    def test_files_context_manager_basic(self) -> None:
        """Test files() context manager creates temporary files."""
        with tf.files({"a": "content A", "b": "content B"}) as paths:
            tm.that(paths, has="a")
            tm.that(paths, has="b")
            tm.that(paths["a"].exists(), eq=True)
            tm.that(paths["b"].exists(), eq=True)
            tm.that(paths["a"].read_text(), eq="content A")
            tm.that(paths["b"].read_text(), eq="content B")
        tm.that(not paths["a"].exists(), eq=True)
        tm.that(not paths["b"].exists(), eq=True)

    def test_files_context_manager_json_auto_detect(self) -> None:
        """Test files() auto-detects JSON from dict content."""
        content = m.ConfigMap(root={"key": "value"})
        with tf.files({"settings": content}) as paths:
            tm.that(paths["settings"].suffix, eq=".json")
            empty_data: t.JsonMapping = {}
            data = u.Cli.json_read(paths["settings"]).unwrap_or(empty_data)
            tm.that(data, eq=content.root)

    def test_files_context_manager_mixed_types(self) -> None:
        """Test files() handles mixed content types."""
        with tf.files({
            "text": "plain text",
            "json": m.ConfigMap(root={"key": "value"}),
            "csv": [["a", "b"], ["1", "2"]],
        }) as paths:
            tm.that(paths["text"].read_text(), eq="plain text")
            tm.that(u.Cli.json_read(paths["json"]).unwrap_or({}), eq={"key": "value"})
            tm.that(len(paths["csv"].read_text().strip().split("\n")), eq=2)

    def test_files_context_manager_custom_extension(self) -> None:
        """Test files() with custom default extension."""
        with tf.files({"file1": "content"}, ext=".md") as paths:
            tm.that(paths["file1"].suffix, eq=".md")

    def test_files_context_manager_custom_directory(self, tmp_path: Path) -> None:
        """Test files() in custom directory."""
        with tf.files({"test": "content"}, directory=tmp_path) as paths:
            tm.that(paths["test"].parent, eq=tmp_path)

    def test_tf_alias_usage(self, tmp_path: Path) -> None:
        """Test tf alias can be used to create files."""
        with tf(base_dir=tmp_path) as files:
            path = files.create("test content", "test.txt")
            tm.that(path.exists(), eq=True)

    def test_tf_files_context_manager(self) -> None:
        """Test tf.files() context manager works."""
        with tf.files({"test": "content"}) as paths:
            tm.that(paths["test"].exists(), eq=True)

    def test_fileinfo_import_from_models(self) -> None:
        """Test tf.FileInfo can be imported from models."""
        info = m.Tests.FileInfo(exists=True, size=100, lines=5)
        tm.that(info.exists is True, eq=True)
        tm.that(info.size, eq=100)
        tm.that(info.lines, eq=5)

    def test_fileinfo_backward_compatibility(self) -> None:
        """Test tf.FileInfo alias works for backward compatibility."""
        info = tf.FileInfo(exists=True)
        tm.that(info.exists is True, eq=True)
        info2 = m.Tests.FileInfo(exists=True)
        tm.that(info2.exists is True, eq=True)

    def test_fileinfo_all_fields(self) -> None:
        """Test tf.FileInfo with all fields populated."""
        now = datetime.now(tz=UTC)
        info = m.Tests.FileInfo(
            exists=True,
            path=Path("/test/file.txt"),
            size=1024,
            size_human="1.0 KB",
            lines=50,
            encoding="utf-8",
            is_empty=False,
            first_line="#!/usr/bin/env python",
            fmt="text",
            valid=True,
            created=now,
            modified=now,
            permissions=420,
            is_readonly=False,
            sha256="abc123" * 10 + "abcd",
        )
        tm.that(info.exists is True, eq=True)
        tm.that(info.size, eq=1024)
        tm.that(info.size_human, eq="1.0 KB")
        tm.that(info.lines, eq=50)
        tm.that(info.fmt, eq="text")
        tm.that(info.sha256, none=False)

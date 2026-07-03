"""Private file creation test mixins."""

from __future__ import annotations

from pathlib import Path

from flext_tests import tf, tm
from tests.models import m
from tests.typings import t


class FilesCreationMixin:
    """File creation tests."""

    def test_create_text_file_default(self, tmp_path: Path) -> None:
        """Test creating text file with default parameters."""
        manager = tf(base_dir=tmp_path)
        content = "test content"
        file_path = manager.create(content, "test.txt")
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(), eq=content)
        tm.that(file_path.name, eq="test.txt")
        tm.that(manager.created_files, has=file_path)

    def test_create_text_file_custom(self, tmp_path: Path) -> None:
        """Test creating text file with custom parameters."""
        manager = tf(base_dir=tmp_path)
        content = "custom content"
        filename = "custom.txt"
        custom_dir = tmp_path / "subdir"
        file_path = manager.create(content, filename, directory=custom_dir)
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(), eq=content)
        tm.that(file_path.name, eq=filename)
        tm.that(file_path.parent, eq=custom_dir)
        tm.that(manager.created_files, has=file_path)

    def test_create_text_file_custom_encoding(self, tmp_path: Path) -> None:
        """Test creating text file with custom encoding."""
        manager = tf(base_dir=tmp_path)
        content = "test content"
        encoding = "utf-16"
        file_path = manager.create(content, "test.txt", enc=encoding)
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(encoding=encoding), eq=content)

    def test_create_binary_file_default(self, tmp_path: Path) -> None:
        """Test creating binary file with default parameters."""
        manager = tf(base_dir=tmp_path)
        content = b"binary content"
        file_path = manager.create(content, "binary_data.bin")
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_bytes(), eq=content)
        tm.that(file_path.name, eq="binary_data.bin")
        tm.that(manager.created_files, has=file_path)

    def test_create_binary_file_custom(self, tmp_path: Path) -> None:
        """Test creating binary file with custom parameters."""
        manager = tf(base_dir=tmp_path)
        content = b"custom binary"
        filename = "custom.bin"
        custom_dir = tmp_path / "subdir"
        file_path = manager.create(content, filename, directory=custom_dir)
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_bytes(), eq=content)
        tm.that(file_path.name, eq=filename)
        tm.that(file_path.parent, eq=custom_dir)

    def test_create_empty_file(self, tmp_path: Path) -> None:
        """Test creating empty file."""
        manager = tf(base_dir=tmp_path)
        file_path = manager.create("", "empty.txt")
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(), eq="")
        tm.that(file_path.name, eq="empty.txt")

    def test_create_empty_file_custom(self, tmp_path: Path) -> None:
        """Test creating empty file with custom name."""
        manager = tf(base_dir=tmp_path)
        filename = "custom_empty.txt"
        file_path = manager.create("", filename)
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(), eq="")
        tm.that(file_path.name, eq=filename)

    def test_create_file_set(self, tmp_path: Path) -> None:
        """Test creating multiple files from dictionary."""
        files: t.MappingKV[
            str,
            str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence] | m.BaseModel,
        ] = {"file1": "content1", "file2": "content2", "file3.txt": "content3"}
        with tf.files(files, directory=tmp_path, ext=".txt") as created:
            tm.that(len(created), eq=3)
            tm.that(created["file1"].read_text(), eq="content1")
            tm.that(created["file2"].read_text(), eq="content2")
            tm.that(created["file3.txt"].read_text(), eq="content3")
            tm.that(created["file1"].name, eq="file1.txt")
            tm.that(created["file2"].name, eq="file2.txt")
            tm.that(created["file3.txt"].name, eq="file3.txt")

    def test_create_file_set_custom_extension(self, tmp_path: Path) -> None:
        """Test creating file set with custom extension."""
        files: t.MappingKV[
            str,
            str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence] | m.BaseModel,
        ] = {"file1": "content1"}
        extension = ".md"
        with tf.files(files, directory=tmp_path, ext=extension) as created:
            tm.that(created["file1"].name, eq="file1.md")

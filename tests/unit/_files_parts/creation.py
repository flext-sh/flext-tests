"""Private file creation test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_tests import FlextTestsFiles, tm

if TYPE_CHECKING:
    from tests import m, t


class TestsFlextTestsFilesCreationMixin:
    """File creation tests."""

    @staticmethod
    def test_create_text_file_default(tmp_path: Path) -> None:
        """Test creating text file with default parameters."""
        manager = FlextTestsFiles(base_dir=tmp_path)
        content = "test content"
        file_path = manager.create(content, "test.txt")
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(), eq=content)
        tm.that(file_path.name, eq="test.txt")
        tm.that(manager.created_files, has=file_path)

    @staticmethod
    def test_create_text_file_custom(tmp_path: Path) -> None:
        """Test creating text file with custom parameters."""
        manager = FlextTestsFiles(base_dir=tmp_path)
        content = "custom content"
        filename = "custom.txt"
        custom_dir = tmp_path / "subdir"
        file_path = manager.create(content, filename, directory=custom_dir)
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(), eq=content)
        tm.that(file_path.name, eq=filename)
        tm.that(file_path.parent, eq=custom_dir)
        tm.that(manager.created_files, has=file_path)

    @staticmethod
    def test_create_text_file_custom_encoding(tmp_path: Path) -> None:
        """Test creating text file with custom encoding."""
        manager = FlextTestsFiles(base_dir=tmp_path)
        content = "test content"
        encoding = "utf-16"
        file_path = manager.create(content, "test.txt", enc=encoding)
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(encoding=encoding), eq=content)

    @staticmethod
    def test_create_binary_file_default(tmp_path: Path) -> None:
        """Test creating binary file with default parameters."""
        manager = FlextTestsFiles(base_dir=tmp_path)
        content = b"binary content"
        file_path = manager.create(content, "binary_data.bin")
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_bytes(), eq=content)
        tm.that(file_path.name, eq="binary_data.bin")
        tm.that(manager.created_files, has=file_path)

    @staticmethod
    def test_create_binary_file_custom(tmp_path: Path) -> None:
        """Test creating binary file with custom parameters."""
        manager = FlextTestsFiles(base_dir=tmp_path)
        content = b"custom binary"
        filename = "custom.bin"
        custom_dir = tmp_path / "subdir"
        file_path = manager.create(content, filename, directory=custom_dir)
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_bytes(), eq=content)
        tm.that(file_path.name, eq=filename)
        tm.that(file_path.parent, eq=custom_dir)

    @staticmethod
    def test_create_empty_file(tmp_path: Path) -> None:
        """Test creating empty file."""
        manager = FlextTestsFiles(base_dir=tmp_path)
        file_path = manager.create("", "empty.txt")
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(), eq="")
        tm.that(file_path.name, eq="empty.txt")

    @staticmethod
    def test_create_empty_file_custom(tmp_path: Path) -> None:
        """Test creating empty file with custom name."""
        manager = FlextTestsFiles(base_dir=tmp_path)
        filename = "custom_empty.txt"
        file_path = manager.create("", filename)
        tm.that(file_path.exists(), eq=True)
        tm.that(file_path.read_text(), eq="")
        tm.that(file_path.name, eq=filename)

    @staticmethod
    def test_create_file_set(tmp_path: Path) -> None:
        """Test creating multiple files from dictionary."""
        files: t.MappingKV[
            str,
            str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence] | m.BaseModel,
        ] = {"file1": "content1", "file2": "content2", "file3.txt": "content3"}
        with FlextTestsFiles.files(files, directory=tmp_path, ext=".txt") as created:
            tm.that(len(created), eq=3)
            tm.that(created["file1"].read_text(), eq="content1")
            tm.that(created["file2"].read_text(), eq="content2")
            tm.that(created["file3.txt"].read_text(), eq="content3")
            tm.that(created["file1"].name, eq="file1.txt")
            tm.that(created["file2"].name, eq="file2.txt")
            tm.that(created["file3.txt"].name, eq="file3.txt")

    @staticmethod
    def test_create_file_set_custom_extension(tmp_path: Path) -> None:
        """Test creating file set with custom extension."""
        files: t.MappingKV[
            str,
            str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence] | m.BaseModel,
        ] = {"file1": "content1"}
        extension = ".md"
        with FlextTestsFiles.files(files, directory=tmp_path, ext=extension) as created:
            tm.that(created["file1"].name, eq="file1.md")

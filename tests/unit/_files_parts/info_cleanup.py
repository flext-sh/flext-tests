"""Private file info and cleanup test mixins."""

from __future__ import annotations

from pathlib import Path

from flext_tests import tf, tm
from tests import m, p, t, u


class FilesInfoCleanupMixin:
    """File info and cleanup tests."""

    def test_get_file_info_not_exists(self, tmp_path: Path) -> None:
        """Test getting file info for non-existent file."""
        manager = tf()
        non_existent = tmp_path / "non_existent.txt"
        result = manager.info(non_existent)
        _ = u.Tests.assert_success(result)
        file_info = result.value
        tm.that(file_info, is_=tf.FileInfo)
        tm.that(file_info.exists is False, eq=True)

    def test_get_file_info_exists(self, tmp_path: Path) -> None:
        """Test getting file info for existing file."""
        manager = tf(base_dir=tmp_path)
        content = "line1\nline2\nline3"
        file_path = manager.create(content, "test.txt")
        result = manager.info(file_path)
        _ = u.Tests.assert_success(result)
        file_info = result.value
        tm.that(file_info, is_=tf.FileInfo)
        tm.that(file_info.exists is True, eq=True)
        tm.that(file_info.size, gt=0)
        tm.that(file_info.lines, eq=3)
        tm.that(file_info.encoding, eq="utf-8")
        tm.that(file_info.is_empty is False, eq=True)
        tm.that(file_info.first_line, eq="line1")

    def test_get_file_info_empty_file(self, tmp_path: Path) -> None:
        """Test getting file info for empty file."""
        manager = tf(base_dir=tmp_path)
        file_path = manager.create("", "empty.txt")
        result = manager.info(file_path)
        _ = u.Tests.assert_success(result)
        file_info = result.value
        tm.that(file_info, is_=tf.FileInfo)
        tm.that(file_info.exists is True, eq=True)
        tm.that(file_info.size, eq=0)
        tm.that(file_info.is_empty is True, eq=True)
        tm.that(file_info.first_line, eq="")

    def test_get_file_info_multiline(self, tmp_path: Path) -> None:
        """Test getting file info for multiline file."""
        manager = tf(base_dir=tmp_path)
        content = "first line\nsecond line\nthird line"
        file_path = manager.create(content, "multiline.txt")
        result = manager.info(file_path)
        _ = u.Tests.assert_success(result)
        file_info = result.value
        tm.that(file_info.lines, eq=3)
        tm.that(file_info.first_line, eq="first line")

    def test_cleanup_files(self, tmp_path: Path) -> None:
        """Test cleaning up created files."""
        manager = tf(base_dir=tmp_path)
        file1 = manager.create("content1", "file1.txt")
        file2 = manager.create("content2", "file2.txt")
        tm.that(file1.exists(), eq=True)
        tm.that(file2.exists(), eq=True)
        manager.cleanup()
        tm.that(not file1.exists(), eq=True)
        tm.that(not file2.exists(), eq=True)
        tm.that(not manager.created_files, eq=True)

    def test_cleanup_directories(self) -> None:
        """Test cleaning up created directories."""
        manager = tf()
        file_path = manager.create("content", "test.txt")
        temp_dir = file_path.parent
        tm.that(temp_dir.exists(), eq=True)
        tm.that(manager.created_dirs, has=temp_dir)
        manager.cleanup()
        tm.that(not temp_dir.exists(), eq=True)
        tm.that(not manager.created_dirs, eq=True)

    def test_cleanup_nonexistent_files(self, tmp_path: Path) -> None:
        """Test cleanup handles non-existent files gracefully."""
        manager = tf(base_dir=tmp_path)
        file_path = manager.create("content", "test.txt")
        file_path.unlink()
        manager.cleanup()
        tm.that(not manager.created_files, eq=True)

    def test_context_manager(self, tmp_path: Path) -> None:
        """Test context manager usage."""
        with tf(base_dir=tmp_path) as manager:
            file_path = manager.create("content", "test.txt")
            tm.that(file_path.exists(), eq=True)
        tm.that(not file_path.exists(), eq=True)

    def test_create_uses_explicit_directory(self, tmp_path: Path) -> None:
        """Test create() writes into explicitly provided directory."""
        manager = tf(base_dir=tmp_path)
        custom_dir = tmp_path / "custom"
        file_path = manager.create("content", "explicit.txt", directory=custom_dir)
        tm.that(file_path.parent, eq=custom_dir)
        tm.that(file_path.exists(), eq=True)

    def test_create_uses_base_dir_when_directory_missing(self, tmp_path: Path) -> None:
        """Test create() defaults to base_dir when no directory is provided."""
        manager = tf(base_dir=tmp_path)
        file_path = manager.create("content", "base-dir.txt")
        tm.that(file_path.parent, eq=tmp_path)
        tm.that(file_path.exists(), eq=True)

    def test_create_without_base_dir_tracks_temp_directory(self) -> None:
        """Test create() without base_dir uses and tracks one temporary directory."""
        manager = tf()
        file_path = manager.create("content", "temp.txt")
        tm.that(file_path.exists(), eq=True)
        tm.that(manager.created_dirs, length_gte=1)
        tm.that(manager.created_dirs, has=file_path.parent)

    def test_temporary_files_classmethod(self) -> None:
        """Test files classmethod context manager."""
        files: t.MappingKV[
            str, str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence] | m.BaseModel
        ] = {"file1": "content1", "file2": "content2"}
        with tf.files(files) as created:
            tm.that(len(created), eq=2)
            tm.that(created["file1"].exists(), eq=True)
            tm.that(created["file2"].exists(), eq=True)
            tm.that(created["file1"].read_text(), eq="content1")
            tm.that(created["file2"].read_text(), eq="content2")
        tm.that(not created["file1"].exists(), eq=True)
        tm.that(not created["file2"].exists(), eq=True)

    def test_temporary_files_custom_extension(self) -> None:
        """Test files with custom extension."""
        files: t.MappingKV[
            str, str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence] | m.BaseModel
        ] = {"file1": "content1"}
        with tf.files(files, ext=".md") as created:
            tm.that(created["file1"].name, eq="file1.md")

    def test_create_file_set_nested_directory(self, tmp_path: Path) -> None:
        """Test creating files in nested directory."""
        nested_dir = tmp_path / "nested" / "subdir"
        files: t.MappingKV[
            str, str | bytes | m.ConfigMap | t.SequenceOf[t.StrSequence] | m.BaseModel
        ] = {"file1": "content1"}
        with tf.files(files, directory=nested_dir) as created:
            tm.that(created["file1"].parent, eq=nested_dir)
            tm.that(nested_dir.exists(), eq=True)

    def test_create_text_file_nested_directory(self, tmp_path: Path) -> None:
        """Test creating text file in nested directory."""
        manager = tf(base_dir=tmp_path)
        nested_dir = tmp_path / "nested" / "subdir"
        file_path = manager.create("content", "test.txt", directory=nested_dir)
        tm.that(file_path.parent, eq=nested_dir)
        tm.that(nested_dir.exists(), eq=True)

    def test_multiple_cleanup_calls(self, tmp_path: Path) -> None:
        """Test multiple cleanup calls are safe."""
        manager = tf(base_dir=tmp_path)
        _ = manager.create("content", "test.txt")
        manager.cleanup()
        manager.cleanup()
        tm.that(not manager.created_files, eq=True)

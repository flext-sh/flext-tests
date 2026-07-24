"""Private file metadata test mixins."""

from __future__ import annotations

from pathlib import Path

from flext_tests import tf, tm
from tests import m, u


class FilesInfoMetadataMixin:
    """File metadata tests."""

    def test_info_existing_file(self, tmp_path: Path) -> None:
        """Test info() returns tf.FileInfo for existing file."""
        manager = tf(base_dir=tmp_path)
        path = manager.create("line1\nline2\nline3", "test.txt")
        result = manager.info(path)
        _ = u.Tests.assert_success(result)
        info = result.value
        tm.that(info.exists is True, eq=True)
        tm.that(info.size, gt=0)
        tm.that(info.lines, eq=3)
        tm.that(info.is_empty is False, eq=True)
        tm.that(info.first_line, eq="line1")

    def test_info_nonexistent_file(self, tmp_path: Path) -> None:
        """Test info() returns tf.FileInfo with exists=False."""
        manager = tf(base_dir=tmp_path)
        path = tmp_path / "nonexistent.txt"
        result = manager.info(path)
        _ = u.Tests.assert_success(result)
        info = result.value
        tm.that(info.exists is False, eq=True)

    def test_info_with_hash(self, tmp_path: Path) -> None:
        """Test info() computes SHA256 hash when requested."""
        manager = tf(base_dir=tmp_path)
        path = manager.create("test content", "test.txt")
        result = manager.info(path, compute_hash=True)
        _ = u.Tests.assert_success(result)
        info = result.value
        tm.that(info.sha256, none=False)
        tm.that(len(info.sha256), eq=64)

    def test_info_format_detection(self, tmp_path: Path) -> None:
        """Test info() detects file format."""
        manager = tf(base_dir=tmp_path)
        path = manager.create(m.ConfigMap(root={"key": "value"}), "settings.json")
        result = manager.info(path)
        _ = u.Tests.assert_success(result)
        info = result.value
        tm.that(info.fmt, eq="json")

    def test_info_empty_file(self, tmp_path: Path) -> None:
        """Test info() for empty file."""
        manager = tf(base_dir=tmp_path)
        path = manager.create("", "empty.txt")
        result = manager.info(path)
        _ = u.Tests.assert_success(result)
        info = result.value
        tm.that(info.exists is True, eq=True)
        tm.that(info.size, eq=0)
        tm.that(info.is_empty is True, eq=True)

    def test_info_size_human_readable(self, tmp_path: Path) -> None:
        """Test info() provides human-readable size."""
        manager = tf(base_dir=tmp_path)
        path = manager.create("x" * 1024, "test.txt")
        result = manager.info(path)
        _ = u.Tests.assert_success(result)
        info = result.value
        tm.that(info.size_human, ne="")

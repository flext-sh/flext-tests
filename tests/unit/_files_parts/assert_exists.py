"""Private file assert_exists test mixins."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests import tf


class FilesAssertExistsMixin:
    """File assert_exists tests."""

    def test_assert_exists_file_success(self, tmp_path: Path) -> None:
        """Test assert_exists() succeeds for existing file."""
        path = tmp_path / "test.txt"
        _ = path.write_text("content")
        _ = tf.assert_exists(path)

    def test_assert_exists_file_failure(self, tmp_path: Path) -> None:
        """Test assert_exists() fails for non-existing file."""
        path = tmp_path / "nonexistent.txt"
        with pytest.raises(AssertionError):
            _ = tf.assert_exists(path)

    def test_assert_exists_directory_success(self, tmp_path: Path) -> None:
        """Test assert_exists() succeeds for existing directory."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        _ = tf.assert_exists(subdir)

    def test_assert_exists_is_file_check(self, tmp_path: Path) -> None:
        """Test assert_exists() with is_file=True."""
        file_path = tmp_path / "test.txt"
        _ = file_path.write_text("content")
        _ = tf.assert_exists(file_path, is_file=True)

    def test_assert_exists_is_dir_check(self, tmp_path: Path) -> None:
        """Test assert_exists() with is_dir=True."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        _ = tf.assert_exists(subdir, is_dir=True)

    def test_assert_exists_not_empty(self, tmp_path: Path) -> None:
        """Test assert_exists() with not_empty=True."""
        path = tmp_path / "test.txt"
        _ = path.write_text("content")
        _ = tf.assert_exists(path, not_empty=True)

    def test_assert_exists_empty_file_fails(self, tmp_path: Path) -> None:
        """Test assert_exists() fails for empty file with not_empty=True."""
        path = tmp_path / "empty.txt"
        _ = path.write_text("")
        with pytest.raises(AssertionError):
            _ = tf.assert_exists(path, not_empty=True)

    def test_assert_exists_readable_check(self, tmp_path: Path) -> None:
        """Test assert_exists() with readable=True validation."""
        path = tmp_path / "readable.txt"
        _ = path.write_text("content")
        path.chmod(420)
        _ = tf.assert_exists(path, readable=True)

    def test_assert_exists_writable_check_file(self, tmp_path: Path) -> None:
        """Test assert_exists() with writable=True for file."""
        path = tmp_path / "writable.txt"
        _ = path.write_text("content")
        path.chmod(420)
        _ = tf.assert_exists(path, writable=True)

    def test_assert_exists_writable_check_directory(self, tmp_path: Path) -> None:
        """Test assert_exists() with writable=True for directory."""
        subdir = tmp_path / "writable_dir"
        subdir.mkdir()
        subdir.chmod(493)
        _ = tf.assert_exists(subdir, writable=True)

    def test_assert_exists_custom_error_message(self, tmp_path: Path) -> None:
        """Test assert_exists() with custom error message."""
        path = tmp_path / "nonexistent.txt"
        with pytest.raises(AssertionError, match="Custom error"):
            _ = tf.assert_exists(path, msg="Custom error: file not found")

    def test_assert_exists_combined_validations(self, tmp_path: Path) -> None:
        """Test assert_exists() with multiple validations at once."""
        path = tmp_path / "test.txt"
        _ = path.write_text("content")
        path.chmod(420)
        _ = tf.assert_exists(
            path,
            is_file=True,
            not_empty=True,
            readable=True,
            writable=True,
        )

    def test_assert_exists_is_file_false(self, tmp_path: Path) -> None:
        """Test assert_exists() with is_file=False (should not be a file)."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        _ = tf.assert_exists(subdir, is_file=False)

    def test_assert_exists_is_dir_false(self, tmp_path: Path) -> None:
        """Test assert_exists() with is_dir=False (should not be a directory)."""
        path = tmp_path / "test.txt"
        _ = path.write_text("content")
        _ = tf.assert_exists(path, is_dir=False)

    def test_assert_exists_empty_directory_fails(self, tmp_path: Path) -> None:
        """Test assert_exists() fails for empty directory with not_empty=True."""
        subdir = tmp_path / "empty_dir"
        subdir.mkdir()
        with pytest.raises(AssertionError):
            _ = tf.assert_exists(subdir, not_empty=True)

    def test_assert_exists_not_empty_directory_success(self, tmp_path: Path) -> None:
        """Test assert_exists() succeeds for non-empty directory."""
        subdir = tmp_path / "non_empty_dir"
        subdir.mkdir()
        _ = (subdir / "file.txt").write_text("content")
        _ = tf.assert_exists(subdir, not_empty=True)

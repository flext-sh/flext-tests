"""Private file compare test mixins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import tf, tm
from tests.constants import c
from tests.utilities import u

if TYPE_CHECKING:
    from pathlib import Path


class FilesCompareMixin:
    """File comparison tests."""

    def test_compare_identical_content(self, tmp_path: Path) -> None:
        """Test compare() returns True for identical content."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("same content", "file1.txt")
        path2 = manager.create("same content", "file2.txt")
        result = manager.compare(path1, path2)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is True, eq=True)

    def test_compare_different_content(self, tmp_path: Path) -> None:
        """Test compare() returns False for different content."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("content A", "file1.txt")
        path2 = manager.create("content B", "file2.txt")
        result = manager.compare(path1, path2)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)

    def test_compare_size_mode(self, tmp_path: Path) -> None:
        """Test compare() in size mode."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("12345", "file1.txt")
        path2 = manager.create("abcde", "file2.txt")
        result = manager.compare(path1, path2, mode=c.Tests.CompareMode.SIZE)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is True, eq=True)

    def test_compare_size_mode_different(self, tmp_path: Path) -> None:
        """Test compare() in size mode with different sizes."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("short", "file1.txt")
        path2 = manager.create("much longer content", "file2.txt")
        result = manager.compare(path1, path2, mode=c.Tests.CompareMode.SIZE)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)

    def test_compare_hash_mode(self, tmp_path: Path) -> None:
        """Test compare() in hash mode."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("identical", "file1.txt")
        path2 = manager.create("identical", "file2.txt")
        result = manager.compare(path1, path2, mode=c.Tests.CompareMode.HASH)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is True, eq=True)

    def test_compare_lines_mode(self, tmp_path: Path) -> None:
        """Test compare() in lines mode compares actual line content."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("line1\nline2\nline3", "file1.txt")
        path2 = manager.create("line1\nline2\nline3", "file2.txt")
        result = manager.compare(path1, path2, mode=c.Tests.CompareMode.LINES)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is True, eq=True)

    def test_compare_lines_mode_different(self, tmp_path: Path) -> None:
        """Test compare() in lines mode returns False for different content."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("line1\nline2\nline3", "file1.txt")
        path2 = manager.create("a\nb\nc", "file2.txt")
        result = manager.compare(path1, path2, mode=c.Tests.CompareMode.LINES)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)

    def test_compare_ignore_whitespace(self, tmp_path: Path) -> None:
        """Test compare() ignoring whitespace."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("hello world", "file1.txt")
        path2 = manager.create("hello  world", "file2.txt")
        result = manager.compare(path1, path2, ignore_ws=True)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is True, eq=True)

    def test_compare_ignore_case(self, tmp_path: Path) -> None:
        """Test compare() ignoring case."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("Hello World", "file1.txt")
        path2 = manager.create("hello world", "file2.txt")
        result = manager.compare(path1, path2, ignore_case=True)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is True, eq=True)

    def test_compare_pattern_match(self, tmp_path: Path) -> None:
        """Test compare() with pattern matching."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("ERROR: something failed", "file1.txt")
        path2 = manager.create("ERROR: other failure", "file2.txt")
        result = manager.compare(path1, path2, pattern="ERROR")
        _ = u.Tests.assert_success(result)
        tm.that(result.value is True, eq=True)

    def test_compare_pattern_no_match(self, tmp_path: Path) -> None:
        """Test compare() pattern matching when one file doesn't match."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("ERROR: something failed", "file1.txt")
        path2 = manager.create("Success: all good", "file2.txt")
        result = manager.compare(path1, path2, pattern="ERROR")
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)

    def test_compare_nonexistent_file(self, tmp_path: Path) -> None:
        """Test compare() returns failure for non-existent file."""
        manager = tf(base_dir=tmp_path)
        path1 = manager.create("content", "file1.txt")
        path2 = tmp_path / "nonexistent.txt"
        result = manager.compare(path1, path2)
        _ = u.Tests.assert_failure(result)

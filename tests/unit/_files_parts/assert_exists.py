"""Private file assert_exists test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import FlextTestsFiles, m

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsFilesAssertExistsMixin:
    """File assert_exists tests."""

    @staticmethod
    def test_assert_exists_file_success(tmp_path: Path) -> None:
        """Test assert_exists() succeeds for existing file."""
        path = tmp_path / "test.txt"
        _ = path.write_text("content")
        _ = FlextTestsFiles.assert_exists(path)

    @staticmethod
    def test_assert_exists_file_failure(tmp_path: Path) -> None:
        """Test assert_exists() fails for non-existing file."""
        path = tmp_path / "nonexistent.txt"
        with pytest.raises(AssertionError):
            _ = FlextTestsFiles.assert_exists(path)

    @staticmethod
    def test_assert_exists_directory_success(tmp_path: Path) -> None:
        """Test assert_exists() succeeds for existing directory."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        _ = FlextTestsFiles.assert_exists(subdir)

    @staticmethod
    def test_assert_exists_is_file_check(tmp_path: Path) -> None:
        """Test assert_exists() with is_file=True."""
        file_path = tmp_path / "test.txt"
        _ = file_path.write_text("content")
        _ = FlextTestsFiles.assert_exists(
            file_path,
            options=m.Tests.AssertExistsParams(is_file=True),
        )

    @staticmethod
    def test_assert_exists_is_dir_check(tmp_path: Path) -> None:
        """Test assert_exists() with is_dir=True."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        _ = FlextTestsFiles.assert_exists(
            subdir,
            options=m.Tests.AssertExistsParams(is_dir=True),
        )

    @staticmethod
    def test_assert_exists_not_empty(tmp_path: Path) -> None:
        """Test assert_exists() with not_empty=True."""
        path = tmp_path / "test.txt"
        _ = path.write_text("content")
        _ = FlextTestsFiles.assert_exists(
            path,
            options=m.Tests.AssertExistsParams(not_empty=True),
        )

    @staticmethod
    def test_assert_exists_empty_file_fails(tmp_path: Path) -> None:
        """Test assert_exists() fails for empty file with not_empty=True."""
        path = tmp_path / "empty.txt"
        _ = path.write_text("")
        with pytest.raises(AssertionError):
            _ = FlextTestsFiles.assert_exists(
                path,
                options=m.Tests.AssertExistsParams(not_empty=True),
            )

    @staticmethod
    def test_assert_exists_readable_check(tmp_path: Path) -> None:
        """Test assert_exists() with readable=True validation."""
        path = tmp_path / "readable.txt"
        _ = path.write_text("content")
        path.chmod(420)
        _ = FlextTestsFiles.assert_exists(
            path,
            options=m.Tests.AssertExistsParams(readable=True),
        )

    @staticmethod
    def test_assert_exists_writable_check_file(tmp_path: Path) -> None:
        """Test assert_exists() with writable=True for file."""
        path = tmp_path / "writable.txt"
        _ = path.write_text("content")
        path.chmod(420)
        _ = FlextTestsFiles.assert_exists(
            path,
            options=m.Tests.AssertExistsParams(writable=True),
        )

    @staticmethod
    def test_assert_exists_writable_check_directory(tmp_path: Path) -> None:
        """Test assert_exists() with writable=True for directory."""
        subdir = tmp_path / "writable_dir"
        subdir.mkdir()
        subdir.chmod(493)
        _ = FlextTestsFiles.assert_exists(
            subdir,
            options=m.Tests.AssertExistsParams(writable=True),
        )

    @staticmethod
    def test_assert_exists_custom_error_message(tmp_path: Path) -> None:
        """Test assert_exists() with custom error message."""
        path = tmp_path / "nonexistent.txt"
        with pytest.raises(AssertionError, match="Custom error"):
            _ = FlextTestsFiles.assert_exists(path, msg="Custom error: file not found")

    @staticmethod
    def test_assert_exists_combined_validations(tmp_path: Path) -> None:
        """Test assert_exists() with multiple validations at once."""
        path = tmp_path / "test.txt"
        _ = path.write_text("content")
        path.chmod(420)
        _ = FlextTestsFiles.assert_exists(
            path,
            options=m.Tests.AssertExistsParams(
                is_file=True,
                not_empty=True,
                readable=True,
                writable=True,
            ),
        )

    @staticmethod
    def test_assert_exists_is_file_false(tmp_path: Path) -> None:
        """Test assert_exists() with is_file=False (should not be a file)."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        _ = FlextTestsFiles.assert_exists(
            subdir,
            options=m.Tests.AssertExistsParams(is_file=False),
        )

    @staticmethod
    def test_assert_exists_is_dir_false(tmp_path: Path) -> None:
        """Test assert_exists() with is_dir=False (should not be a directory)."""
        path = tmp_path / "test.txt"
        _ = path.write_text("content")
        _ = FlextTestsFiles.assert_exists(
            path,
            options=m.Tests.AssertExistsParams(is_dir=False),
        )

    @staticmethod
    def test_assert_exists_empty_directory_fails(tmp_path: Path) -> None:
        """Test assert_exists() fails for empty directory with not_empty=True."""
        subdir = tmp_path / "empty_dir"
        subdir.mkdir()
        with pytest.raises(AssertionError):
            _ = FlextTestsFiles.assert_exists(
                subdir,
                options=m.Tests.AssertExistsParams(not_empty=True),
            )

    @staticmethod
    def test_assert_exists_not_empty_directory_success(tmp_path: Path) -> None:
        """Test assert_exists() succeeds for non-empty directory."""
        subdir = tmp_path / "non_empty_dir"
        subdir.mkdir()
        _ = (subdir / "file.txt").write_text("content")
        _ = FlextTestsFiles.assert_exists(
            subdir,
            options=m.Tests.AssertExistsParams(not_empty=True),
        )

"""Private file model test mixins."""

from __future__ import annotations

from pathlib import Path

from flext_tests import tf, tm


class FilesModelsMixin:
    """File model tests."""

    def test_file_info_exists_false(self) -> None:
        """Test tf.FileInfo with exists=False."""
        info = tf.FileInfo(exists=False)
        tm.that(info.exists is False, eq=True)
        tm.that(info.size, eq=0)
        tm.that(info.lines, eq=0)
        tm.that(info.encoding, eq="utf-8")
        tm.that(info.is_empty is False, eq=True)
        tm.that(info.first_line, eq="")

    def test_file_info_exists_true(self) -> None:
        """Test tf.FileInfo with exists=True."""
        info = tf.FileInfo(
            exists=True,
            size=100,
            lines=5,
            encoding="utf-8",
            is_empty=False,
            first_line="first line",
        )
        tm.that(info.exists is True, eq=True)
        tm.that(info.size, eq=100)
        tm.that(info.lines, eq=5)
        tm.that(info.encoding, eq="utf-8")
        tm.that(info.is_empty is False, eq=True)
        tm.that(info.first_line, eq="first line")

    def test_init_without_base_dir(self) -> None:
        """Test initialization without base directory."""
        manager = tf()
        tm.that(manager.base_dir, none=True)
        tm.that(manager.created_files, empty=True)
        tm.that(manager.created_dirs, empty=True)

    def test_init_with_base_dir(self, tmp_path: Path) -> None:
        """Test initialization with base directory."""
        manager = tf(base_dir=tmp_path)
        tm.that(manager.base_dir, eq=tmp_path)
        tm.that(manager.created_files, empty=True)
        tm.that(manager.created_dirs, empty=True)

    def test_file_manager_preserves_operations_with_explicit_base_dir(
        self, tmp_path: Path
    ) -> None:
        """Characterize the public file-manager operations."""
        manager = tf(base_dir=tmp_path)
        first = manager.create("content", "first.txt")
        second = manager.create("content", "second.txt")

        tm.that(manager.info(first).value.exists, eq=True)
        tm.that(manager.compare(first, second).value, eq=True)

    def test_model_validation_owns_file_manager_base_dir(self, tmp_path: Path) -> None:
        """Keep base_dir in the canonical service model contract."""
        manager = tf.model_validate({"base_dir": tmp_path})
        from_string = tf.model_validate({"base_dir": str(tmp_path)})

        tm.that(manager.base_dir, eq=tmp_path)
        tm.that(from_string.base_dir, eq=tmp_path)
        tm.that(manager.model_dump()["base_dir"], eq=tmp_path)
        tm.that(manager.model_copy().base_dir, eq=tmp_path)

    def test_temporary_directory(self) -> None:
        """Test temporary_directory context manager."""
        manager = tf()
        with manager.temporary_directory() as temp_dir:
            tm.that(temp_dir, is_=Path)
            tm.that(temp_dir.exists(), eq=True)
            tm.that(temp_dir.is_dir(), eq=True)
        tm.that(not temp_dir.exists(), eq=True)

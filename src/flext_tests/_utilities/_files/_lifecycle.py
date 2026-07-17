"""Lifecycle helpers for FlextTestsFiles.

Covers initialization, context-manager entry/exit, cleanup tracking, and
base-directory resolution.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Self

from flext_tests import c, t

if TYPE_CHECKING:
    from types import TracebackType


class FlextTestsFilesLifecycleMixin:
    """File-manager lifecycle: init, context manager, cleanup, base_dir."""

    _base_dir: Path | None = None
    _created_files: list[Path] | None = None
    _created_dirs: list[Path] | None = None

    def __init__(self, base_dir: Path | None = None) -> None:
        """Initialize file manager with optional base directory.

        Args:
            base_dir: Optional base directory for file operations.
                     If not provided, temporary directories are used.

        """
        self._initialize_file_lifecycle(base_dir)

    def _initialize_file_lifecycle(self, base_dir: Path | None) -> None:
        """Initialize file-manager lifecycle state."""
        self._base_dir = base_dir
        self._created_files = list[Path]()
        self._created_dirs = list[Path]()

    def __enter__(self) -> Self:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit with cleanup."""
        self.cleanup()

    @property
    def base_dir(self) -> Path | None:
        """The base directory."""
        return self._base_dir

    @property
    def created_dirs(self) -> t.SequenceOf[Path]:
        """The list of created directories."""
        return self._created_dirs or []

    @property
    def created_files(self) -> t.SequenceOf[Path]:
        """The list of created files."""
        return self._created_files or []

    def cleanup(self) -> None:
        """Cleanup all tracked files and directories created by this manager."""
        if self._created_files is not None:
            for path in reversed(self._created_files):
                if not path.exists():
                    continue
                try:
                    path.chmod(c.Tests.PERMISSION_WRITABLE_FILE)
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
            self._created_files.clear()
        if self._created_dirs is not None:
            for path in reversed(self._created_dirs):
                if not path.exists():
                    continue
                try:
                    path.chmod(c.Tests.PERMISSION_WRITABLE_DIR)
                    shutil.rmtree(path)
                except OSError:
                    pass
            self._created_dirs.clear()

    def _resolve_directory(self, directory: Path | None) -> Path:
        """Resolve target directory for file creation."""
        target_dir = directory or self.base_dir
        if target_dir is not None:
            target_dir.mkdir(parents=True, exist_ok=True)
            return target_dir
        temp_dir = Path(tempfile.mkdtemp())
        created_dirs = self._created_dirs
        if created_dirs is None:
            created_dirs = self._created_dirs = list[Path]()
        created_dirs.append(temp_dir)
        return temp_dir


__all__: list[str] = ["FlextTestsFilesLifecycleMixin"]

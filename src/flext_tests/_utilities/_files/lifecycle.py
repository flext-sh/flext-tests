"""Lifecycle helpers for FlextTestsFiles.

Covers cleanup tracking and base-directory resolution. The tracked state and
the context-manager protocol live on the composing ``FlextTestsFiles`` model.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
import tempfile
import warnings
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Self

from flext_tests import c


class FlextTestsUtilitiesFilesLifecycle:
    """File-manager lifecycle: cleanup and base_dir resolution."""

    if TYPE_CHECKING:
        base_dir: Path | None
        _created_files: list[Path]
        _created_dirs: list[Path]

    @classmethod
    def _create_file_manager(cls, _base_dir: Path | None, /) -> Self:
        """Construct the concrete validated file manager."""
        raise NotImplementedError

    @property
    def created_dirs(self) -> Sequence[Path]:
        """The list of created directories."""
        return self._created_dirs

    @property
    def created_files(self) -> Sequence[Path]:
        """The list of created files."""
        return self._created_files

    def cleanup(self) -> None:
        """Cleanup all tracked files and directories created by this manager."""
        for path in reversed(self._created_files):
            if not path.exists():
                continue
            try:
                path.chmod(c.Tests.PERMISSION_WRITABLE_FILE)
                path.unlink(missing_ok=True)
            except OSError as exc:
                # Why: best-effort teardown cleanup; a leftover temp file is
                # observable (not silently swallowed) but never fails the
                # test that triggered teardown.
                warnings.warn(
                    f"cleanup: failed to remove file {path}: {exc}",
                    stacklevel=2,
                )
        self._created_files.clear()
        for path in reversed(self._created_dirs):
            if not path.exists():
                continue
            try:
                path.chmod(c.Tests.PERMISSION_WRITABLE_DIR)
                shutil.rmtree(path)
            except OSError as exc:
                warnings.warn(
                    f"cleanup: failed to remove directory {path}: {exc}",
                    stacklevel=2,
                )
        self._created_dirs.clear()

    def _resolve_directory(self, directory: Path | None) -> Path:
        """Resolve target directory for file creation.

        Returns:
            The resulting ``Path``.

        """
        target_dir = directory or self.base_dir
        if target_dir is not None:
            target_dir.mkdir(parents=True, exist_ok=True)
            return target_dir
        temp_dir = Path(tempfile.mkdtemp())
        self._created_dirs.append(temp_dir)
        return temp_dir


__all__: list[str] = ["FlextTestsUtilitiesFilesLifecycle"]

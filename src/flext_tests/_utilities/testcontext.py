"""Extracted mixin for flext_tests."""

from __future__ import annotations

import os
import types
from pathlib import Path
from typing import BinaryIO

if os.name == "nt":
    import msvcrt
else:
    import fcntl


class FlextTestsTestContextUtilitiesMixin:
    """Context managers for tests."""

    class FileLock:
        """File-based exclusive lock for pytest-xdist parallel test isolation.

        Centralized SSOT for the LDAP-family / pytest-xdist coordination
        pattern (previously cloned across ``flext-ldap``, ``flext-ldif``,
        ``flext-tap-ldap``).
        """

        def __init__(self, lock_file: Path) -> None:
            self.lock_file = lock_file
            self._file_obj: BinaryIO | None = None

        def __enter__(self) -> None:
            """Acquire exclusive file lock."""
            self.lock_file.parent.mkdir(parents=True, exist_ok=True)
            file_obj = self.lock_file.open("a+b")
            try:
                if os.name == "nt":
                    os.lseek(file_obj.fileno(), 0, os.SEEK_SET)
                    msvcrt.locking(file_obj.fileno(), msvcrt.LK_LOCK, 1)
                else:
                    fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX)
            except BaseException:
                file_obj.close()
                raise
            self._file_obj = file_obj

        # mro-j47u (codex): these dunder arguments are contract-only.
        def __exit__(
            self,
            _exc_type: type[BaseException] | None,
            _exc_val: BaseException | None,
            _exc_tb: types.TracebackType | None,
        ) -> None:
            """Release the lock while preserving its shared inode."""
            if self._file_obj is None:
                return
            file_obj = self._file_obj
            self._file_obj = None
            try:
                if os.name == "nt":
                    os.lseek(file_obj.fileno(), 0, os.SEEK_SET)
                    msvcrt.locking(file_obj.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)
            finally:
                file_obj.close()

"""Host file lock shared by every test process of one machine."""

from __future__ import annotations

import os
import time
import types
from pathlib import Path
from typing import BinaryIO

from flext_tests import c

if os.name == "nt":
    import msvcrt
else:
    import fcntl


class FlextTestsTestContextUtilitiesMixin:
    """Context managers for tests."""

    class FileLock:
        """Advisory lock on one file, coordinating every process of the host.

        Exclusive by default. ``shared=True`` takes a shared lock: shared
        holders coexist and together exclude an exclusive holder, which in turn
        excludes them. ``timeout_seconds=None`` blocks until the lock is
        granted; a number polls a non-blocking attempt until that deadline and
        then raises ``TimeoutError`` naming the file and the mode. The lock file
        is never removed, so every holder coordinates through one inode.

        Shared and bounded modes use POSIX ``fcntl``; on Windows only the
        blocking exclusive mode exists and the others fail at construction.
        """

        def __init__(
            self,
            lock_file: Path,
            *,
            shared: bool = False,
            timeout_seconds: float | None = None,
        ) -> None:
            if os.name == "nt" and (shared or timeout_seconds is not None):
                msg = c.Tests.ERR_FILE_LOCK_POSIX_ONLY.format(path=lock_file)
                raise ValueError(msg)
            self.lock_file = lock_file
            self.shared = shared
            self.timeout_seconds = timeout_seconds
            self._file_obj: BinaryIO | None = None

        @property
        def mode(self) -> str:
            """Lock mode name used in diagnostics."""
            return (
                c.Tests.FILE_LOCK_MODE_SHARED
                if self.shared
                else c.Tests.FILE_LOCK_MODE_EXCLUSIVE
            )

        def acquire_or_none(self) -> None:
            """Acquire the lock outside a with-block (idempotent guard)."""
            if self.is_acquired:
                return
            self._acquire()

        @property
        def is_acquired(self) -> bool:
            """True while the lock is held by this instance."""
            return self._file_obj is not None

        def release(self) -> None:
            """Release the lock outside a with-block (idempotent)."""
            self._release()

        def _acquire(self) -> None:
            """Open the lock file and take the platform lock."""
            self.lock_file.parent.mkdir(parents=True, exist_ok=True)
            file_obj = self.lock_file.open("a+b")
            try:
                self._acquire(file_obj.fileno())
            except BaseException:
                file_obj.close()
                raise
            self._file_obj = file_obj

        def _release(self) -> None:
            """Release the platform lock and close the lock file."""
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

        def __enter__(self) -> None:
            """Acquire the lock (shared or exclusive, optionally bounded)."""
            self._acquire()

        def __exit__(
            self,
            _exc_type: type[BaseException] | None,
            _exc_val: BaseException | None,
            _exc_tb: types.TracebackType | None,
        ) -> None:
            """Release the lock while preserving its shared inode."""
            self._release()

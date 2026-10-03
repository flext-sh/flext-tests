"""Host file lock shared by every test process of one machine.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

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

        def __enter__(self) -> None:
            """Acquire the lock, blocking or until the configured deadline."""
            self.lock_file.parent.mkdir(parents=True, exist_ok=True)
            file_obj = self.lock_file.open("a+b")
            try:
                self._acquire(file_obj.fileno())
            except BaseException:
                file_obj.close()
                raise
            self._file_obj = file_obj

        def _acquire(self, descriptor: int) -> None:
            """Take the lock on an open descriptor in this lock's mode."""
            if os.name == "nt":
                os.lseek(descriptor, 0, os.SEEK_SET)
                msvcrt.locking(descriptor, msvcrt.LK_LOCK, 1)
            elif self.timeout_seconds is None:
                fcntl.flock(descriptor, self._posix_flags())
            else:
                self._acquire_before_deadline(descriptor)

        def _posix_flags(self) -> int:
            """Return the fcntl operation for this lock's mode."""
            return fcntl.LOCK_SH if self.shared else fcntl.LOCK_EX

        def _acquire_before_deadline(self, descriptor: int) -> None:
            """Poll a non-blocking attempt until granted or the deadline passes.

            Raises:
                TimeoutError: If ``time.monotonic() >= deadline``.
            """
            timeout = self.timeout_seconds or 0.0
            deadline = time.monotonic() + timeout
            while True:
                try:
                    fcntl.flock(descriptor, self._posix_flags() | fcntl.LOCK_NB)
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        msg = c.Tests.ERR_FILE_LOCK_TIMEOUT.format(
                            mode=self.mode,
                            path=self.lock_file,
                            timeout=timeout,
                        )
                        raise TimeoutError(msg) from None
                    time.sleep(c.Tests.FILE_LOCK_POLL_SECONDS)
                else:
                    return

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

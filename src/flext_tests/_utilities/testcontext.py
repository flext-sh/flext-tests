"""Extracted mixin for flext_tests."""

from __future__ import annotations

import os
import time
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
        """File-based lock for pytest-xdist parallel test isolation.

        Centralized SSOT for the LDAP-family / pytest-xdist coordination
        pattern (previously cloned across ``flext-ldap``, ``flext-ldif``,
        ``flext-tap-ldap``). Exclusive by default; ``shared=True`` takes a
        shared (reader) lock on POSIX. ``timeout_seconds`` bounds the
        acquisition with non-blocking retries and raises ``TimeoutError``
        when the deadline passes (blocking indefinitely when ``None``).
        Windows supports only exclusive locking; ``shared`` is ignored there.
        """

        RETRY_INTERVAL_SECONDS = 0.05

        def __init__(
            self,
            lock_file: Path,
            *,
            shared: bool = False,
            timeout_seconds: float | None = None,
        ) -> None:
            self.lock_file = lock_file
            self.shared = shared
            self.timeout_seconds = timeout_seconds
            self._file_obj: BinaryIO | None = None

        def _deadline(self) -> float | None:
            """Monotonic acquisition deadline (None blocks indefinitely)."""
            if self.timeout_seconds is None:
                return None
            return time.monotonic() + self.timeout_seconds

        def _timed_out(self, deadline: float | None) -> bool:
            """True when a bounded acquisition missed its deadline."""
            if deadline is None:
                return False
            if time.monotonic() < deadline:
                return False
            msg = (
                f"FileLock acquisition timed out after "
                f"{self.timeout_seconds}s: {self.lock_file}"
            )
            raise TimeoutError(msg)

        def _acquire_windows(self, file_obj: BinaryIO, deadline: float | None) -> None:
            """Acquire the Windows lock with bounded retries (exclusive)."""
            if os.name == "nt":
                while True:
                    os.lseek(file_obj.fileno(), 0, os.SEEK_SET)
                    acquired = False
                    try:
                        msvcrt.locking(file_obj.fileno(), msvcrt.LK_LOCK, 1)
                        acquired = True
                    except OSError:
                        _ = self._timed_out(deadline)
                        time.sleep(self.RETRY_INTERVAL_SECONDS)
                    if acquired:
                        return

        def _acquire_posix(self, file_obj: BinaryIO, deadline: float | None) -> None:
            """Acquire the POSIX flock honouring shared mode and timeout."""
            if os.name != "nt":
                mode = fcntl.LOCK_SH if self.shared else fcntl.LOCK_EX
                if deadline is None:
                    fcntl.flock(file_obj.fileno(), mode)
                    return
                while True:
                    acquired = False
                    try:
                        fcntl.flock(file_obj.fileno(), mode | fcntl.LOCK_NB)
                        acquired = True
                    except BlockingIOError:
                        _ = self._timed_out(deadline)
                        time.sleep(self.RETRY_INTERVAL_SECONDS)
                    if acquired:
                        return

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
                deadline = self._deadline()
                if os.name == "nt":
                    self._acquire_windows(file_obj, deadline)
                else:
                    self._acquire_posix(file_obj, deadline)
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

"""Host file lock shared by every test process of one machine.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import shutil
import sys
import time
import types
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO

from flext_tests import c
from collections.abc import Generator

if TYPE_CHECKING:
    from flext_tests import p

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl


class FlextTestsTestContextUtilitiesMixin:
    """Context managers for tests."""

    class SessionRuntime:
        """Single-flight, lazy consumer runtime in one random worker-session area.

        The installed pytest fixture owns allocation and cleanup. A single
        provision callback performs canonical locked Make setup/upgrade once.
        Each exclusive lease restores the seed's source, Git and case data at
        the same absolute path, preserving real editable imports. Scenarios
        that mutate installed packages also restore the physical environment,
        without resolving or reinstalling dependencies between cases.
        """

        def __init__(self, directory: Path) -> None:
            self.directory = directory
            self._root: Path | None = None
            self._provision: p.Tests.RuntimeProvision | None = None
            self._failure: BaseException | None = None
            self._source = directory / "source"
            self._environment = directory / "environment"

        @contextmanager
        def lease(
            self,
            provision: p.Tests.RuntimeProvision,
            *,
            mutable_environment: bool = False,
        ) -> Generator[Path]:
            """Serialize cases and preserve provision, test and cleanup failures.

            A failed provision is never retried. Different callbacks are
            rejected rather than silently serving an incompatible locked seed.
            The blocking native lease imposes no artificial item deadline.
            """
            with FlextTestsTestContextUtilitiesMixin.FileLock(
                self.directory / "runtime.lock",
            ):
                if self._failure is not None:
                    raise self._failure
                if self._provision is not None and self._provision is not provision:
                    msg = "Session runtime requires one canonical provision callback"
                    raise ValueError(msg)
                try:
                    if self._root is None:
                        self._provision = provision
                        parent = self.directory / "project"
                        parent.mkdir()
                        root = provision(parent)
                        if root.is_symlink() or not root.resolve().is_relative_to(
                            parent.resolve(),
                        ):
                            msg = "Session runtime checkout must belong to its own area"
                            raise ValueError(msg)
                        environment = root / c.VENV_DIR_NAME
                        if (
                            environment.is_symlink()
                            or not (environment / "pyvenv.cfg").is_file()
                        ):
                            msg = (
                                "Session runtime requires its own physical environment"
                            )
                            raise ValueError(msg)
                        shutil.copytree(
                            root,
                            self._source,
                            symlinks=True,
                            ignore=shutil.ignore_patterns(c.VENV_DIR_NAME),
                        )
                        self._root = root
                    if mutable_environment and not self._environment.exists():
                        shutil.copytree(
                            self._root / c.VENV_DIR_NAME,
                            self._environment,
                            symlinks=True,
                        )
                except BaseException as error:
                    self._failure = error
                    raise
                try:
                    yield self._root
                finally:
                    failure = sys.exception()
                    try:
                        targets = [(self._root, self._source)]
                        if mutable_environment:
                            targets.append((
                                self._root / c.VENV_DIR_NAME,
                                self._environment,
                            ))
                        for target, baseline in targets:
                            for child in target.iterdir():
                                if (
                                    target == self._root
                                    and child.name == c.VENV_DIR_NAME
                                ):
                                    continue
                                if child.is_dir() and not child.is_symlink():
                                    shutil.rmtree(child)
                                else:
                                    child.unlink()
                            shutil.copytree(
                                baseline,
                                target,
                                dirs_exist_ok=True,
                                symlinks=True,
                            )
                    except BaseException as error:
                        self._failure = error
                        if failure is not None:
                            msg = "Session runtime case and cleanup failed"
                            raise BaseExceptionGroup(msg, [failure, error]) from None
                        raise

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
            if sys.platform == "win32" and (shared or timeout_seconds is not None):
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
            if sys.platform == "win32":
                os.lseek(descriptor, 0, os.SEEK_SET)
                locking = msvcrt.locking
                locking(descriptor, msvcrt.LK_LOCK, 1)
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
                if sys.platform == "win32":
                    os.lseek(file_obj.fileno(), 0, os.SEEK_SET)
                    locking = msvcrt.locking
                    locking(file_obj.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)
            finally:
                file_obj.close()

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
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from threading import get_ident
from typing import TYPE_CHECKING, BinaryIO

from flext_tests import c

if TYPE_CHECKING:
    from flext_tests import p, t

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
            self.directory = directory.resolve(strict=True)
            self._allocation = self.directory.stat()
            self._root: Path | None = None
            self._provision: p.Tests.RuntimeProvision | None = None
            self._failure: BaseException | None = None
            self._active_thread: int | None = None
            self._source = self.directory / "source"
            self._environment = self.directory / "environment"

        def _assert_owned(self, path: Path) -> None:
            """Reject redirected paths using the original physical allocation identity.

            Args:
                path: The path to check against the original physical allocation.

            Raises:
                ValueError: If the path has escaped its original physical allocation.

            """
            allocation = self._source.parent
            state = allocation.stat(follow_symlinks=False)
            candidate = path.absolute()
            if (
                self.directory != allocation
                or allocation.resolve() != allocation
                or (state.st_dev, state.st_ino)
                != (self._allocation.st_dev, self._allocation.st_ino)
                or not candidate.resolve().is_relative_to(allocation)
                or any(
                    ancestor.is_symlink()
                    for ancestor in (candidate, *candidate.parents)
                    if ancestor.is_relative_to(allocation)
                )
            ):
                msg = "Session runtime path escaped its original physical allocation"
                raise ValueError(msg)

        def close(self) -> None:
            """Remove only the unchanged physical session allocation."""
            self._assert_owned(self.directory)
            shutil.rmtree(self.directory)

        def _provision_session_root(
            self,
            provision: p.Tests.RuntimeProvision,
        ) -> Path:
            """Create and authenticate the session checkout exactly once.

            Returns:
                The provisioned session root.

            Raises:
                ValueError: If the checkout leaves its own area.

            """
            root = self._root
            if root is not None:
                return root
            self._provision = provision
            parent = self.directory / "project"
            parent.mkdir()
            root = provision(parent)
            self._assert_owned(parent)
            self._assert_owned(root)
            if not root.resolve().is_relative_to(parent):
                msg = "Session runtime checkout must belong to its own area"
                raise ValueError(msg)
            root = root.resolve()
            self._root = root
            return root

        def _lease_targets(
            self,
            *,
            mutable_environment: bool,
        ) -> list[t.Pair[Path, Path]]:
            """Return the runtime directories with their baseline mirrors.

            Returns:
                The owned runtime directories and their seed baselines.

            Raises:
                ValueError: If the runtime root or environment is invalid.

            """
            root = self._root
            if root is None:
                msg = "Session runtime requires its provisioned root"
                raise ValueError(msg)
            environment = root / c.VENV_DIR_NAME
            self._assert_owned(environment)
            if not (environment / "pyvenv.cfg").is_file():
                msg = "Session runtime requires its own physical environment"
                raise ValueError(msg)
            targets = [(root, self._source)]
            if mutable_environment:
                targets.append((environment, self._environment))
            return targets

        def _seed_lease_baselines(
            self,
            targets: t.SequenceOf[t.Pair[Path, Path]],
        ) -> None:
            """Mirror each absent runtime baseline from its live directory."""
            for target, baseline in targets:
                if baseline.exists():
                    continue
                ignore = (
                    shutil.ignore_patterns(c.VENV_DIR_NAME)
                    if target == self._root
                    else None
                )
                shutil.copytree(target, baseline, symlinks=True, ignore=ignore)

        def _restore_lease_targets(
            self,
            targets: t.SequenceOf[t.Pair[Path, Path]],
        ) -> None:
            """Restore every leased runtime directory from its baseline.

            Raises:
                ValueError: If the runtime root escaped its original allocation.

            """
            root = self._root
            if root is None:
                msg = "Session runtime requires its provisioned root"
                raise ValueError(msg)
            for target, baseline in targets:
                self._assert_owned(target)
                self._assert_owned(root / c.VENV_DIR_NAME)
                target.mkdir(parents=True, exist_ok=True)
                for child in target.iterdir():
                    if target == self._root and child.name == c.VENV_DIR_NAME:
                        continue
                    if child.is_dir() and not child.is_symlink():
                        shutil.rmtree(child)
                    else:
                        child.unlink()
                shutil.copytree(baseline, target, dirs_exist_ok=True, symlinks=True)

        def _finish_lease(self, targets: t.SequenceOf[t.Pair[Path, Path]]) -> None:
            """Restore baselines after one lease, folding concurrent failures.

            Raises:
                BaseExceptionGroup: If the case and the cleanup both failed.

            """
            failure = sys.exception()
            try:
                self._restore_lease_targets(targets)
            except BaseException as error:
                self._failure = error
                if failure is not None:
                    msg = "Session runtime case and cleanup failed"
                    raise BaseExceptionGroup(msg, [failure, error]) from None
                raise
            finally:
                self._active_thread = None

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

            Args:
                provision: The canonical provision callback for the session.
                mutable_environment: Whether the environment should be mutable.

            Yields:
                The path to the leased session runtime directory.

            Raises:
                RuntimeError: If the session runtime leases are nested.
                ValueError: If the provision callback is incompatible or the
                    environment is invalid.

            """
            thread = get_ident()
            if self._active_thread == thread:
                msg = "Session runtime leases cannot be nested"
                raise RuntimeError(msg)
            if self._failure is not None:
                raise self._failure
            self._assert_owned(self.directory)
            with FlextTestsTestContextUtilitiesMixin.FileLock(
                self.directory / "runtime.lock",
            ):
                if self._failure is not None:
                    raise self._failure
                if self._provision is not None and self._provision is not provision:
                    msg = "Session runtime requires one canonical provision callback"
                    raise ValueError(msg)
                self._active_thread = thread
                targets: list[t.Pair[Path, Path]] = []
                try:
                    root = self._provision_session_root(provision)
                    targets = self._lease_targets(
                        mutable_environment=mutable_environment,
                    )
                    self._seed_lease_baselines(targets)
                except BaseException as error:
                    self._failure = error
                    self._active_thread = None
                    raise
                try:
                    yield root
                finally:
                    self._finish_lease(targets)

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
__all__: list[str] = ["FlextTestsTestContextUtilitiesMixin"]

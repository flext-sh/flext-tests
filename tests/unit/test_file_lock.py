"""Behavioral tests of the host file lock (``u.Tests.FileLock``).

Locks are exercised through independent open file descriptions of one file,
which the operating system arbitrates exactly as it arbitrates two processes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import time
from contextlib import ExitStack
from typing import TYPE_CHECKING

import pytest

from tests import tm, u

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsFileLock:
    """Exclusive, shared and bounded modes of the host file lock."""

    @staticmethod
    def test_shared_holders_coexist(tmp_path: Path) -> None:
        """A second shared holder is granted while the first still holds."""
        lock_path = tmp_path / "lease.lock"
        with (
            u.Tests.FileLock(lock_path, shared=True),
            u.Tests.FileLock(lock_path, shared=True, timeout_seconds=0.2),
        ):
            tm.ok(lock_path.is_file())

    @staticmethod
    @pytest.mark.parametrize(
        ("held_shared", "wanted_shared"),
        [
            pytest.param(True, False, id="shared-blocks-exclusive"),
            pytest.param(False, True, id="exclusive-blocks-shared"),
            pytest.param(False, False, id="exclusive-blocks-exclusive"),
        ],
    )
    def test_conflicting_holder_times_out_naming_path_and_mode(
        tmp_path: Path,
        *,
        held_shared: bool,
        wanted_shared: bool,
    ) -> None:
        """A conflicting request fails after its bound, naming file and mode."""
        lock_path = tmp_path / "lease.lock"
        wanted = u.Tests.FileLock(lock_path, shared=wanted_shared, timeout_seconds=0.2)
        started = time.monotonic()
        with (
            ExitStack() as stack,
            u.Tests.FileLock(lock_path, shared=held_shared),
            pytest.raises(TimeoutError) as timed_out,
        ):
            stack.enter_context(wanted)
        tm.that(time.monotonic() - started, gte=0.2)
        tm.that(str(timed_out.value), has=[str(lock_path), wanted.mode])

    @staticmethod
    def test_released_lock_is_granted_within_bound(tmp_path: Path) -> None:
        """Once the holder leaves, a bounded request is granted."""
        lock_path = tmp_path / "lease.lock"
        with u.Tests.FileLock(lock_path, shared=True):
            tm.ok(lock_path.is_file())
        with u.Tests.FileLock(lock_path, timeout_seconds=0.2):
            tm.ok(lock_path.is_file())

    @staticmethod
    def test_session_runtime_preserves_failed_provision_without_retry(
        tmp_path: Path,
    ) -> None:
        """A missing physical seed fails once and retains its native exception."""
        attempts: list[Path] = []

        def unavailable(parent: Path) -> Path:
            attempts.append(parent)
            return (parent / "missing-seed").resolve(strict=True)

        runtime = u.Tests.SessionRuntime(tmp_path)
        errors: list[FileNotFoundError] = []
        for _ in range(2):
            with pytest.raises(FileNotFoundError) as error, runtime.lease(unavailable):
                pytest.fail("A missing seed must not produce a runtime")
            errors.append(error.value)
        tm.that(len(attempts), eq=1)
        tm.ok(errors[0] is errors[1])

    @staticmethod
    def test_session_runtime_rejects_replaced_parent_before_snapshot_or_yield(
        tmp_path: Path,
    ) -> None:
        """A callback cannot redirect the provision parent into a foreign checkout."""
        allocation = tmp_path / "runtime"
        allocation.mkdir()
        foreign = tmp_path / "foreign"
        checkout = foreign / "checkout"
        checkout.mkdir(parents=True)
        sentinel = checkout / "sentinel"
        sentinel.write_bytes(b"foreign-owned content")
        content = sentinel.read_bytes()
        attempts: list[Path] = []

        def redirected(parent: Path) -> Path:
            attempts.append(parent)
            parent.rmdir()
            parent.symlink_to(foreign, target_is_directory=True)
            return parent / checkout.name

        runtime = u.Tests.SessionRuntime(allocation)
        errors: list[ValueError] = []
        for _ in range(2):
            with (
                pytest.raises(
                    ValueError, match="original physical allocation"
                ) as error,
                runtime.lease(redirected),
            ):
                pytest.fail("A redirected checkout must never reach the case body")
            errors.append(error.value)
        tm.that(len(attempts), eq=1)
        tm.ok(errors[0] is errors[1])
        physical_directories = (
            child
            for child in allocation.iterdir()
            if child.is_dir() and not child.is_symlink()
        )
        tm.that(tuple(physical_directories), eq=())
        runtime.close()
        tm.fail(allocation.exists())
        tm.that(tuple(foreign.iterdir()), eq=(checkout,))
        tm.that(tuple(checkout.iterdir()), eq=(sentinel,))
        tm.that(sentinel.read_bytes(), eq=content)

    @staticmethod
    def test_timed_out_request_holds_nothing(tmp_path: Path) -> None:
        """A request that timed out leaves the lock to the next holder."""
        lock_path = tmp_path / "lease.lock"
        with (
            ExitStack() as stack,
            u.Tests.FileLock(lock_path),
            pytest.raises(TimeoutError),
        ):
            stack.enter_context(u.Tests.FileLock(lock_path, timeout_seconds=0.1))
        with u.Tests.FileLock(lock_path, timeout_seconds=0.2):
            tm.ok(lock_path.is_file())

"""Behavioral tests of the host file lock (``u.Tests.FileLock``).

Locks are exercised through independent open file descriptions of one file,
which the operating system arbitrates exactly as it arbitrates two processes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from contextlib import ExitStack
from typing import TYPE_CHECKING

import pytest

from flext_tests import tm
from tests import u

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsFileLock:
    """Exclusive, shared and bounded modes of the host file lock."""

    def test_shared_holders_coexist(self, tmp_path: Path) -> None:
        """A second shared holder is granted while the first still holds."""
        lock_path = tmp_path / "lease.lock"
        with (
            u.Tests.FileLock(lock_path, shared=True),
            u.Tests.FileLock(lock_path, shared=True, timeout_seconds=0.2),
        ):
            tm.that(lock_path.is_file(), eq=True)

    @pytest.mark.parametrize(
        ("held_shared", "wanted_shared"),
        [
            pytest.param(True, False, id="shared-blocks-exclusive"),
            pytest.param(False, True, id="exclusive-blocks-shared"),
            pytest.param(False, False, id="exclusive-blocks-exclusive"),
        ],
    )
    def test_conflicting_holder_times_out_naming_path_and_mode(
        self, tmp_path: Path, *, held_shared: bool, wanted_shared: bool
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

    def test_released_lock_is_granted_within_bound(self, tmp_path: Path) -> None:
        """Once the holder leaves, a bounded request is granted."""
        lock_path = tmp_path / "lease.lock"
        with u.Tests.FileLock(lock_path, shared=True):
            tm.that(lock_path.is_file(), eq=True)
        with u.Tests.FileLock(lock_path, timeout_seconds=0.2):
            tm.that(lock_path.is_file(), eq=True)

    def test_timed_out_request_holds_nothing(self, tmp_path: Path) -> None:
        """A request that timed out leaves the lock to the next holder."""
        lock_path = tmp_path / "lease.lock"
        with (
            ExitStack() as stack,
            u.Tests.FileLock(lock_path),
            pytest.raises(TimeoutError),
        ):
            stack.enter_context(u.Tests.FileLock(lock_path, timeout_seconds=0.1))
        with u.Tests.FileLock(lock_path, timeout_seconds=0.2):
            tm.that(lock_path.is_file(), eq=True)

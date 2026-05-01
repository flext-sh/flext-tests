"""Extracted mixin for flext_tests."""

from __future__ import annotations

import fcntl
import types
from collections.abc import (
    Generator,
)
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from flext_tests._typings.base import FlextTestsBaseTypesMixin


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
            self._fd: int | None = None
            self._file_obj: TextIO | None = None

        def __enter__(self) -> None:
            """Acquire exclusive file lock."""
            self.lock_file.parent.mkdir(parents=True, exist_ok=True)
            self._file_obj = self.lock_file.open("w")
            self._fd = self._file_obj.fileno()
            fcntl.flock(self._fd, fcntl.LOCK_EX)

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: types.TracebackType | None,
        ) -> None:
            """Release file lock and clean up the lock file."""
            if self._fd is not None:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
            if self._file_obj is not None:
                self._file_obj.close()
            self.lock_file.unlink(missing_ok=True)

    @staticmethod
    @contextmanager
    def temporary_attribute(
        target: FlextTestsBaseTypesMixin.TestobjectSerializable,
        attribute: str,
        value: FlextTestsBaseTypesMixin.TestobjectSerializable,
    ) -> Generator[None]:
        """Temporarily set attribute on target t.JsonValue.

        Args:
            target: Object to modify
            attribute: Attribute name
            value: Temporary value

        Yields:
            None

        """
        attribute_existed = hasattr(target, attribute)
        original_value: FlextTestsBaseTypesMixin.TestobjectSerializable | None = None
        if attribute_existed:
            original_value = getattr(target, attribute)
        object.__setattr__(target, attribute, value)
        try:
            yield
        finally:
            if attribute_existed:
                object.__setattr__(target, attribute, original_value)
            else:
                object.__delattr__(target, attribute)

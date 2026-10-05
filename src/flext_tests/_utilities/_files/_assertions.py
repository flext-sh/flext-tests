"""File-assertion helpers for FlextTestsFiles.

Generalized file/directory existence and property checks.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_cli import u

from flext_tests import c, m
from flext_tests._utilities._files._batch import FlextTestsFilesBatchMixin


class FlextTestsFilesAssertionsMixin(FlextTestsFilesBatchMixin):
    """Generalized file existence and property assertions."""

    @staticmethod
    def assert_exists(
        path: Path,
        msg: str | None = None,
        options: m.Tests.AssertExistsParams | None = None,
    ) -> Path:
        """Generalized file existence assertion - ALL file validations in ONE method.

        Consolidates: assert_exists(), assert_file(), assert_dir(), assert_not_empty()
        into single method with grouped assertion flags.

        Args:
            path: File or directory path to check
            msg: Custom error message
            options: Assertion flags (is_file, is_dir, not_empty, readable,
                writable); defaults validate existence only

        Returns:
            Path if all validations pass

        Raises:
            AssertionError: If ``not path.exists()``; or if a ``AssertionError`` is
                caught.
        """
        params = (
            options
            if options is not None
            else m.Tests.AssertExistsParams.model_validate({})
        )
        if not path.exists():
            error_msg = msg or c.Tests.ERROR_FILE_NOT_FOUND.format(path=path)
            raise AssertionError(error_msg)
        try:
            u.Cli.files_assert_exists(
                path,
                is_file=params.is_file,
                is_dir=params.is_dir,
                not_empty=params.not_empty,
                readable=params.readable,
                writable=params.writable,
            )
        except AssertionError as exc:
            raise AssertionError(msg or str(exc)) from exc
        return path


__all__: list[str] = ["FlextTestsFilesAssertionsMixin"]

"""File-assertion helpers for FlextTestsFiles.

Generalized file/directory existence and property checks.
"""

from __future__ import annotations

import os
from collections.abc import MutableSequence
from pathlib import Path

from flext_tests import c, m
from flext_tests._utilities._files._batch import FlextTestsFilesBatchMixin


class FlextTestsFilesAssertionsMixin(FlextTestsFilesBatchMixin):
    """Generalized file existence and property assertions."""

    @staticmethod
    def assert_exists(
        path: Path,
        msg: str | None = None,
        options: m.Tests.AssertExistsParams | None = None,
        *,
        is_file: bool | None = None,
        is_dir: bool | None = None,
        not_empty: bool | None = None,
        readable: bool | None = None,
        writable: bool | None = None,
    ) -> Path:
        """Generalized file existence assertion - ALL file validations in ONE method.

        Consolidates: assert_exists(), assert_file(), assert_dir(), assert_not_empty()
        into single method with optional parameters.

        Args:
            path: File or directory path to check
            msg: Custom error message
            is_file: Assert is file (True) or not file (False)
            is_dir: Assert is directory (True) or not directory (False)
            not_empty: Assert file/dir is not empty (True) or empty (False)
            readable: Assert is readable (True)
            writable: Assert is writable (True)

        Returns:
            Path if all validations pass

        """
        params = (
            options
            if options is not None
            else m.Tests.AssertExistsParams.model_validate({
                "is_file": is_file,
                "is_dir": is_dir,
                "not_empty": not_empty,
                "readable": readable,
                "writable": writable,
            })
        )
        if not path.exists():
            error_msg = msg or c.Tests.ERROR_FILE_NOT_FOUND.format(path=path)
            raise AssertionError(error_msg)
        is_file_path = path.is_file()
        is_dir_path = path.is_dir()
        is_empty_file = is_file_path and path.stat().st_size == 0
        is_empty_dir = is_dir_path and (not any(path.iterdir()))

        checks: MutableSequence[tuple[bool, str]] = []
        if params.is_file is not None:
            checks.extend([
                (params.is_file and (not is_file_path), f"Path {path} is not a file"),
                (
                    (not params.is_file) and is_file_path,
                    f"Path {path} should not be a file",
                ),
            ])
        if params.is_dir is not None:
            checks.extend([
                (
                    params.is_dir and (not is_dir_path),
                    f"Path {path} is not a directory",
                ),
                (
                    (not params.is_dir) and is_dir_path,
                    f"Path {path} should not be a directory",
                ),
            ])
        if params.not_empty is not None:
            checks.extend([
                (params.not_empty and is_empty_file, f"File {path} is empty"),
                (params.not_empty and is_empty_dir, f"Directory {path} is empty"),
                (
                    (not params.not_empty) and is_file_path and (not is_empty_file),
                    f"File {path} is not empty",
                ),
                (
                    (not params.not_empty) and is_dir_path and (not is_empty_dir),
                    f"Directory {path} is not empty",
                ),
            ])
        if params.readable:
            checks.append(
                (
                    is_file_path and (not os.access(path, os.R_OK)),
                    f"File {path} is not readable",
                ),
            )
        if params.writable:
            checks.extend([
                (
                    is_file_path and (not os.access(path, os.W_OK)),
                    f"File {path} is not writable",
                ),
                (
                    is_dir_path and (not os.access(path, os.W_OK)),
                    f"Directory {path} is not writable",
                ),
            ])

        for failed, check_msg in checks:
            if failed:
                raise AssertionError(msg or check_msg)
        return path


__all__: list[str] = ["FlextTestsFilesAssertionsMixin"]

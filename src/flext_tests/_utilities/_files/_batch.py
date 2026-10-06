"""Batch file-operation helper for FlextTestsFiles.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from pathlib import Path
from typing import Annotated

from flext_cli import u

from flext_core import r
from flext_tests import c, m, p, t
from flext_tests._utilities._files._contexts import FlextTestsFilesContextsMixin
from flext_tests._utilities.payload import (
    FlextTestsFlextUtilitiesPayload,
    FlextTestsPayloadUtilities,
)


class FlextTestsFilesBatchMixin(FlextTestsFilesContextsMixin):
    """Batch create/read/delete file operations."""

    class BatchOptions(m.Value):
        """Optional knobs for ``batch_files``."""

        directory: Annotated[
            Path | None,
            u.Field(description="Target directory for create operations"),
        ] = None
        operation: Annotated[
            c.Tests.Operation,
            m.BeforeValidator(
                lambda v: c.Tests.Operation(v) if isinstance(v, str) else v,
            ),
            u.Field(
                default=c.Tests.Operation.CREATE,
                description="Operation type: create, read, or delete",
            ),
        ] = c.Tests.Operation.CREATE
        model: Annotated[
            type[m.BaseModel] | None,
            u.Field(description="Optional model class for read operations"),
        ] = None
        on_error: Annotated[
            c.Tests.ErrorMode,
            m.BeforeValidator(
                lambda v: c.Tests.ErrorMode(v) if isinstance(v, str) else v,
            ),
            u.Field(
                default=c.Tests.ErrorMode.COLLECT,
                description="Error handling mode: stop, skip, or collect",
            ),
        ] = c.Tests.ErrorMode.COLLECT
        parallel: Annotated[
            bool,
            u.Field(description="Run operations in parallel (not implemented yet)"),
        ] = False

    @staticmethod
    def _batch_create_payload(
        content: t.Tests.TestobjectSerializable,
    ) -> t.Tests.TestobjectSerializable:
        """Own mapping content through the payload walker for create operations.

        Returns:
            The payload-owned content.
        """
        if isinstance(content, Mapping):
            return {
                k: FlextTestsPayloadUtilities.to_payload(
                    v,
                )
                for k, v in content.items()
            }
        return content

    def _batch_process_one(
        self,
        params: m.Tests.BatchParams,
        name_and_content: tuple[str, t.Tests.TestobjectSerializable],
    ) -> p.Result[Path]:
        """Process single file operation.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        name, content = name_and_content
        path = Path(content) if isinstance(content, (Path, str)) else Path(name)
        result: p.Result[Path]
        match params.operation:
            case c.Tests.Operation.CREATE:
                try:
                    payload = self._batch_create_payload(content)
                    result = r[Path].ok(
                        self.create(
                            self._coerce_file_content(payload),
                            name,
                            params.directory,
                        ),
                    )
                except (OSError, TypeError, ValueError, AttributeError) as e:
                    result = r[Path].fail(f"Failed to create {name}: {e}")
            case c.Tests.Operation.READ:
                read_result = self.read(path, model_cls=None)
                result = (
                    r[Path].ok(path)
                    if read_result.success
                    else r[Path].fail(read_result.error or f"Failed to read {name}")
                )
            case c.Tests.Operation.DELETE:
                try:
                    path.unlink(missing_ok=True)
                    result = r[Path].ok(path)
                except OSError as e:
                    result = r[Path].fail(f"Failed to delete {name}: {e}")
        return result

    def batch_files(
        self,
        items: t.Tests.BatchFiles,
        *,
        options: FlextTestsFilesBatchMixin.BatchOptions | None = None,
    ) -> p.Result[m.Tests.BatchResult]:
        """Batch file operations with error handling.

        Args:
            items: Mapping of file names to content or a sequence of name-content
                pairs.
            options: Batch operation knobs (directory, operation, model,
                on_error, parallel)

        Returns:
            r[m.Tests.BatchResult] with results and errors

        """
        batch_options = (
            options if options is not None else FlextTestsFilesBatchMixin.BatchOptions()
        )
        try:
            params = m.Tests.BatchParams.model_validate({
                "files": items,
                "directory": batch_options.directory,
                "operation": batch_options.operation,
                "model": batch_options.model,
                "on_error": batch_options.on_error,
                "parallel": batch_options.parallel,
            })
        except c.EXC_BASIC_TYPE as exc:
            return r[m.Tests.BatchResult].fail(
                f"Invalid parameters for batch operation: {exc}",
                exception=exc,
            )
        files_dict: MutableMapping[str, t.Tests.TestobjectSerializable] = dict(
            params.files,
        )
        error_mode_str = (
            "collect" if params.on_error is c.Tests.ErrorMode.COLLECT else "fail"
        )

        items_list = list(files_dict.items())
        results_dict: MutableMapping[str, p.Result[t.Tests.TestResultValue]] = {}
        failed_dict: t.MutableStrMapping = {}
        rtype = r[t.Tests.TestResultValue]
        for name, _ in items_list:
            op_result = self._batch_process_one(params, (name, files_dict[name]))
            if op_result.success:
                results_dict[name] = rtype.ok(op_result.value)
                continue
            err_msg = op_result.error or "Unknown error"
            results_dict[name] = rtype.fail(err_msg)
            failed_dict[name] = err_msg
            if error_mode_str == "fail":
                return r[m.Tests.BatchResult].fail(err_msg)

        summary = m.Tests.BatchResult.model_validate({
            "succeeded": len(items_list) - len(failed_dict),
            "failed": len(failed_dict),
            "total": len(items_list),
            "results": dict(results_dict),
            "errors": dict(failed_dict),
        })
        return r[m.Tests.BatchResult].ok(summary)


__all__: list[str] = ["FlextTestsFilesBatchMixin"]

"""Test-scope context manager for matchers.

Exposes ``scope`` for isolated test execution scopes.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import sys
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager, nullcontext
from pathlib import Path

from flext_tests import m, t
from flext_tests._utilities import FlextTestsUtilitiesConfigHelpers


class FlextTestsUtilitiesMatchersScope:
    """Isolated test-scope helper exposed under ``Tests.Matchers``."""

    @staticmethod
    @contextmanager
    def scope(
        # Why: kwargs mirror every ScopeParams field. `dict` literals
        # (settings={"debug": True}) are invariant under mypy, so the
        # Mapping-typed fields must be spelled as Mapping (covariant)
        # here too, matching ScopeParams itself, not the bare
        # TestobjectSerializable alias; model_validate below still
        # enforces the real per-field contract at runtime.
        **kwargs: t.Tests.TestobjectSerializable
        | Mapping[str, t.Tests.TestobjectSerializable]
        | Sequence[str]
        | t.Tests.CleanupSpec
        | t.Tests.EnvironmentSpec,
    ) -> Generator[m.Tests.TestScope]:
        """Enhanced isolated test execution scope.

        Provides isolated configuration, container, and context for tests.
        Supports temporary environment variables, working directory changes,
        and automatic cleanup functions.

        Args:
            **kwargs: Parameters validated via m.ScopeParams model
                - settings: Initial configuration values
                - container: Initial container/service mappings
                - context: Initial context values
                - cleanup: Sequence of cleanup functions to call on exit
                - env: Temporary environment variables (restored on exit)
                - remove_env_keys: Environment names removed inside the scope
                - python_paths: Import roots prepended inside the scope
                - cwd: Temporary working directory (restored on exit)

        Yields:
            TestScope with settings, container, and context dicts

        """
        params = m.Tests.ScopeParams.model_validate(kwargs)
        original_cwd: Path | None = None
        env_context = (
            FlextTestsUtilitiesConfigHelpers.env_vars_context(
                params.env,
                params.remove_env_keys,
            )
            if params.env is not None or params.remove_env_keys
            else nullcontext()
        )
        original_python_path = tuple(sys.path)
        try:
            with env_context:
                sys.path[:0] = list(params.python_paths)
                if params.cwd is not None:
                    original_cwd = Path.cwd()
                    os.chdir(params.cwd)
                yield m.Tests.TestScope(
                    settings=params.settings or {},
                    container=params.container or {},
                    context=params.context or {},
                )
        finally:
            sys.path[:] = original_python_path
            if original_cwd is not None:
                os.chdir(original_cwd)
            if params.cleanup is not None:
                for cleanup_func in params.cleanup:
                    cleanup_func()


__all__: list[str] = ["FlextTestsUtilitiesMatchersScope"]

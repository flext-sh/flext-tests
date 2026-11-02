"""Extracted mixin for flext_tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager


class FlextTestsUtilitiesConfigHelpers:
    """Environment scopes for tests, without settings-model instance machinery."""

    @staticmethod
    @contextmanager
    def env_vars_context[ValueT](
        env_vars: Mapping[str, ValueT] | None = None,
        vars_to_clear: Sequence[str] | None = None,
    ) -> Generator[None]:
        """Apply a process-environment scope and restore only its owned keys."""
        owned = set(env_vars or ()) | set(vars_to_clear or ())
        original_environment = {key: os.environ.get(key) for key in owned}
        try:
            for var in vars_to_clear or ():
                os.environ.pop(var, None)
            os.environ.update({
                key: str(value) for key, value in (env_vars or {}).items()
            })
            yield
        finally:
            for key, value in original_environment.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


__all__: list[str] = ["FlextTestsUtilitiesConfigHelpers"]

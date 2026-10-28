"""Extracted mixin for flext_tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
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
        """Apply and atomically restore a real process-environment scope."""
        original_environment = os.environ.copy()
        try:
            for var in vars_to_clear or ():
                os.environ.pop(var, None)
            os.environ.update({
                key: str(value) for key, value in (env_vars or {}).items()
            })
            yield
        finally:
            os.environ.clear()
            os.environ.update(original_environment)


__all__: list[str] = ["FlextTestsUtilitiesConfigHelpers"]

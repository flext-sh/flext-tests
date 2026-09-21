"""Make command framework constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from flext_infra import t


class FlextTestsConstantsMake:
    """Constants for the generic Make command registry."""

    MAKE_DEFAULT_COMMAND: ClassVar[str] = "all"
    MAKE_HEADER_START: ClassVar[str] = "/// flext-command"
    MAKE_HEADER_END: ClassVar[str] = "///"
    MAKE_DISPATCH_ENV: ClassVar[str] = "FLEXT_COMMAND_DISPATCHED"
    MAKE_DISPATCH_ENV_VALUE: ClassVar[str] = "Y"
    MAKE_DISPATCH_VERB_ENV: ClassVar[str] = "FLEXT_COMMAND_VERB"
    MAKE_DISPATCH_WHAT_ENV: ClassVar[str] = "FLEXT_COMMAND_WHAT"
    MAKE_DISPATCH_PATH_ENV: ClassVar[str] = "FLEXT_COMMAND_PATH"
    MAKE_SURFACE_VALIDATE_ENV: ClassVar[str] = "FLEXT_SURFACE_VALIDATE"
    MAKE_APPLY_PARAM: ClassVar[str] = "APPLY"
    MAKE_WHAT_PARAM: ClassVar[str] = "WHAT"
    MAKE_HELP_PARAM: ClassVar[str] = "HELP"
    MAKE_OPTIONS_PARAM: ClassVar[str] = "OPTIONS"
    MAKE_PYTHONPATH_ENV: ClassVar[str] = "PYTHONPATH"
    MAKE_COMMAND_SUFFIXES: ClassVar[frozenset[str]] = frozenset({".py", ".sh"})
    MAKE_IGNORED_COMMAND_DIRS: ClassVar[frozenset[str]] = frozenset({
        ".pytest_cache",
        ".venv",
        "__pycache__",
        "github",
        "lib",
        "maintenance",
    })
    MAKE_MUTATION_REQUIRED_PARAMS: ClassVar[frozenset[str]] = frozenset({MAKE_APPLY_PARAM})
    MAKE_TRUE_VALUES: ClassVar[frozenset[str]] = frozenset({"1", "Y", "YES", "TRUE"})
    MAKE_SAFE_PROBE_VALUES: ClassVar[t.MappingKV[str, str]] = {
        "APPLY": "N",
        "CHECK_GATES": "lint",
        "DEPS_REPORT": "0",
        "DOCS_PHASE": "validate",
        "DRY_RUN": "1",
        "MESSAGE": "chore: surface validation",
        "PYTEST_ARGS": "-q",
        "TAG": "surface-validation",
        "VALIDATE_SCOPE": "project",
    }


__all__: list[str] = ["FlextTestsConstantsMake"]

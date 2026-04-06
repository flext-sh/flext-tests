# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Constants package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tests._constants.docker as _flext_tests__constants_docker

    docker = _flext_tests__constants_docker
    import flext_tests._constants.files as _flext_tests__constants_files
    from flext_tests._constants.docker import FlextTestsDockerConstantsMixin

    files = _flext_tests__constants_files
    import flext_tests._constants.matcher as _flext_tests__constants_matcher
    from flext_tests._constants.files import FlextTestsFilesConstantsMixin

    matcher = _flext_tests__constants_matcher
    import flext_tests._constants.validator as _flext_tests__constants_validator
    from flext_tests._constants.matcher import FlextTestsMatcherConstantsMixin

    validator = _flext_tests__constants_validator
    from flext_tests._constants.validator import FlextTestsValidatorConstantsMixin
_LAZY_IMPORTS = {
    "FlextTestsDockerConstantsMixin": (
        "flext_tests._constants.docker",
        "FlextTestsDockerConstantsMixin",
    ),
    "FlextTestsFilesConstantsMixin": (
        "flext_tests._constants.files",
        "FlextTestsFilesConstantsMixin",
    ),
    "FlextTestsMatcherConstantsMixin": (
        "flext_tests._constants.matcher",
        "FlextTestsMatcherConstantsMixin",
    ),
    "FlextTestsValidatorConstantsMixin": (
        "flext_tests._constants.validator",
        "FlextTestsValidatorConstantsMixin",
    ),
    "docker": "flext_tests._constants.docker",
    "files": "flext_tests._constants.files",
    "matcher": "flext_tests._constants.matcher",
    "validator": "flext_tests._constants.validator",
}

__all__ = [
    "FlextTestsDockerConstantsMixin",
    "FlextTestsFilesConstantsMixin",
    "FlextTestsMatcherConstantsMixin",
    "FlextTestsValidatorConstantsMixin",
    "docker",
    "files",
    "matcher",
    "validator",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

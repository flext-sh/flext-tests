# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Models package."""

from __future__ import annotations

import typing as _t

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

from flext_cli import FlextCliModels
from flext_core import FlextModels, r
from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tests._models.base as _flext_tests__models_base

    base = _flext_tests__models_base
    import flext_tests._models.batch as _flext_tests__models_batch
    from flext_tests._models.base import FlextTestsBaseModelsMixin

    batch = _flext_tests__models_batch
    import flext_tests._models.docker as _flext_tests__models_docker
    from flext_tests._models.batch import FlextTestsBatchModelsMixin

    docker = _flext_tests__models_docker
    import flext_tests._models.filesystem as _flext_tests__models_filesystem
    from flext_tests._models.docker import FlextTestsDockerModelsMixin

    filesystem = _flext_tests__models_filesystem
    import flext_tests._models.matchers as _flext_tests__models_matchers
    from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin

    matchers = _flext_tests__models_matchers
    import flext_tests._models.validator as _flext_tests__models_validator
    from flext_tests._models.matchers import FlextTestsMatchersModelsMixin

    validator = _flext_tests__models_validator
    from flext_tests._models.validator import FlextTestsValidatorModelsMixin
_LAZY_IMPORTS = {
    "FlextTestsBaseModelsMixin": (
        "flext_tests._models.base",
        "FlextTestsBaseModelsMixin",
    ),
    "FlextTestsBatchModelsMixin": (
        "flext_tests._models.batch",
        "FlextTestsBatchModelsMixin",
    ),
    "FlextTestsDockerModelsMixin": (
        "flext_tests._models.docker",
        "FlextTestsDockerModelsMixin",
    ),
    "FlextTestsFilesystemModelsMixin": (
        "flext_tests._models.filesystem",
        "FlextTestsFilesystemModelsMixin",
    ),
    "FlextTestsMatchersModelsMixin": (
        "flext_tests._models.matchers",
        "FlextTestsMatchersModelsMixin",
    ),
    "FlextTestsValidatorModelsMixin": (
        "flext_tests._models.validator",
        "FlextTestsValidatorModelsMixin",
    ),
    "base": "flext_tests._models.base",
    "batch": "flext_tests._models.batch",
    "docker": "flext_tests._models.docker",
    "filesystem": "flext_tests._models.filesystem",
    "matchers": "flext_tests._models.matchers",
    "validator": "flext_tests._models.validator",
}

__all__ = [
    "FlextTestsBaseModelsMixin",
    "FlextTestsBatchModelsMixin",
    "FlextTestsDockerModelsMixin",
    "FlextTestsFilesystemModelsMixin",
    "FlextTestsMatchersModelsMixin",
    "FlextTestsValidatorModelsMixin",
    "base",
    "batch",
    "docker",
    "filesystem",
    "matchers",
    "validator",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

"""Flext Tests package facade."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports
from flext_tests.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)
from flext_tests._exports import (
    FLEXT_TESTS_LAZY_IMPORTS,
    FLEXT_TESTS_METADATA_EXPORTS,
)

if _t.TYPE_CHECKING:
    from flext_core import d, e, h, r, x
    from flext_tests._fixtures.enforcement import (
        EnforcementCollector,
        EnforcementItem,
        EnforcementViolationError,
    )
    from flext_tests._fixtures.markdown_validation import (
        MarkdownCodeBlockCollector,
        MarkdownCodeBlockItem,
        MarkdownValidationError,
    )
    from flext_tests._fixtures.project_metadata import (
        project_metadata,
        project_namespace_config,
        project_tool_flext,
    )
    from flext_tests._fixtures.settings import (
        clean_container,
        reset_settings,
        sample_data,
        settings,
        settings_factory,
        temp_dir,
        temp_file,
        test_context,
        test_runtime,
    )
    from flext_tests._utilities.matchers import tm
    from flext_tests.base import FlextService, FlextTestsCase, FlextTestsServiceBase, s
    from flext_tests.constants import FlextTestsConstants, c
    from flext_tests.docker import FlextTestsDocker, tk
    from flext_tests.domains import FlextTestsDomains, td
    from flext_tests.files import FlextTestsFiles, tf
    from flext_tests.models import FlextTestsModels, m
    from flext_tests.protocols import FlextTestsProtocols, p
    from flext_tests.settings import FlextTestsSettings
    from flext_tests.typings import FlextTestsTypes, t
    from flext_tests.utilities import FlextTestsUtilities, u
    from flext_tests.validator import FlextTestsValidator, tv

install_lazy_exports(
    __name__,
    globals(),
    FLEXT_TESTS_LAZY_IMPORTS,
    FLEXT_TESTS_METADATA_EXPORTS,
)

__all__: list[str] = [
    "EnforcementCollector",
    "EnforcementItem",
    "EnforcementViolationError",
    "FlextService",
    "FlextTestsCase",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsModels",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsSettings",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidator",
    "MarkdownCodeBlockCollector",
    "MarkdownCodeBlockItem",
    "MarkdownValidationError",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "clean_container",
    "d",
    "e",
    "h",
    "m",
    "p",
    "project_metadata",
    "project_namespace_config",
    "project_tool_flext",
    "r",
    "reset_settings",
    "s",
    "sample_data",
    "settings",
    "settings_factory",
    "t",
    "td",
    "temp_dir",
    "temp_file",
    "test_context",
    "test_runtime",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]

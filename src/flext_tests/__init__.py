# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import flext_tests._fixtures as _flext_tests__fixtures

    _fixtures = _flext_tests__fixtures
    import flext_tests._utilities as _flext_tests__utilities
    from flext_tests._fixtures import T, reset_settings, settings, settings_factory

    _utilities = _flext_tests__utilities
    import flext_tests._validator as _flext_tests__validator
    from flext_tests._utilities import (
        FlextTestsMatchersUtilities,
        FlextTestsPayloadUtilities,
        deep_match,
        length_validate,
        matchers,
        tm,
        to_config_map_value,
        to_normalized_value,
        to_payload,
    )

    _validator = _flext_tests__validator
    import flext_tests.conftest_plugin as _flext_tests_conftest_plugin
    from flext_tests._validator import (
        FlextTestsValidatorModels,
        FlextValidatorBypass,
        FlextValidatorImports,
        FlextValidatorLayer,
        FlextValidatorSettings,
        FlextValidatorTests,
        FlextValidatorTypes,
        bypass,
        imports,
        layer,
        tests,
        types,
        vm,
    )

    conftest_plugin = _flext_tests_conftest_plugin
    import flext_tests.constants as _flext_tests_constants

    constants = _flext_tests_constants
    import flext_tests.docker as _flext_tests_docker
    from flext_tests.constants import FlextTestsConstants, FlextTestsConstants as c

    docker = _flext_tests_docker
    import flext_tests.domains as _flext_tests_domains
    from flext_tests.docker import FlextTestsDocker, tk

    domains = _flext_tests_domains
    import flext_tests.files as _flext_tests_files
    from flext_tests.domains import FlextTestsDomains, td

    files = _flext_tests_files
    import flext_tests.models as _flext_tests_models
    from flext_tests.files import FlextTestsFiles, tf

    models = _flext_tests_models
    import flext_tests.protocols as _flext_tests_protocols
    from flext_tests.models import FlextTestsModels, FlextTestsModels as m

    protocols = _flext_tests_protocols
    import flext_tests.typings as _flext_tests_typings
    from flext_tests.protocols import FlextTestsProtocols, FlextTestsProtocols as p

    typings = _flext_tests_typings
    import flext_tests.utilities as _flext_tests_utilities
    from flext_tests.typings import FlextTestsTypes, FlextTestsTypes as t

    utilities = _flext_tests_utilities
    import flext_tests.validator as _flext_tests_validator
    from flext_tests.utilities import FlextTestsUtilities, FlextTestsUtilities as u

    validator = _flext_tests_validator
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_tests.validator import FlextTestsValidator, tv
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_tests._fixtures",
        "flext_tests._utilities",
        "flext_tests._validator",
    ),
    {
        "FlextTestsConstants": ("flext_tests.constants", "FlextTestsConstants"),
        "FlextTestsDocker": ("flext_tests.docker", "FlextTestsDocker"),
        "FlextTestsDomains": ("flext_tests.domains", "FlextTestsDomains"),
        "FlextTestsFiles": ("flext_tests.files", "FlextTestsFiles"),
        "FlextTestsModels": ("flext_tests.models", "FlextTestsModels"),
        "FlextTestsProtocols": ("flext_tests.protocols", "FlextTestsProtocols"),
        "FlextTestsTypes": ("flext_tests.typings", "FlextTestsTypes"),
        "FlextTestsUtilities": ("flext_tests.utilities", "FlextTestsUtilities"),
        "FlextTestsValidator": ("flext_tests.validator", "FlextTestsValidator"),
        "_fixtures": "flext_tests._fixtures",
        "_utilities": "flext_tests._utilities",
        "_validator": "flext_tests._validator",
        "c": ("flext_tests.constants", "FlextTestsConstants"),
        "conftest_plugin": "flext_tests.conftest_plugin",
        "constants": "flext_tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "docker": "flext_tests.docker",
        "domains": "flext_tests.domains",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "files": "flext_tests.files",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_tests.models", "FlextTestsModels"),
        "models": "flext_tests.models",
        "p": ("flext_tests.protocols", "FlextTestsProtocols"),
        "protocols": "flext_tests.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "t": ("flext_tests.typings", "FlextTestsTypes"),
        "td": ("flext_tests.domains", "td"),
        "tf": ("flext_tests.files", "tf"),
        "tk": ("flext_tests.docker", "tk"),
        "tv": ("flext_tests.validator", "tv"),
        "typings": "flext_tests.typings",
        "u": ("flext_tests.utilities", "FlextTestsUtilities"),
        "utilities": "flext_tests.utilities",
        "validator": "flext_tests.validator",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsMatchersUtilities",
    "FlextTestsModels",
    "FlextTestsPayloadUtilities",
    "FlextTestsProtocols",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidator",
    "FlextTestsValidatorModels",
    "FlextValidatorBypass",
    "FlextValidatorImports",
    "FlextValidatorLayer",
    "FlextValidatorSettings",
    "FlextValidatorTests",
    "FlextValidatorTypes",
    "T",
    "_fixtures",
    "_utilities",
    "_validator",
    "bypass",
    "c",
    "conftest_plugin",
    "constants",
    "d",
    "deep_match",
    "docker",
    "domains",
    "e",
    "files",
    "h",
    "imports",
    "layer",
    "length_validate",
    "m",
    "matchers",
    "models",
    "p",
    "protocols",
    "r",
    "reset_settings",
    "s",
    "settings",
    "settings_factory",
    "t",
    "td",
    "tests",
    "tf",
    "tk",
    "tm",
    "to_config_map_value",
    "to_normalized_value",
    "to_payload",
    "tv",
    "types",
    "typings",
    "u",
    "utilities",
    "validator",
    "vm",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

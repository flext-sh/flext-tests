# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tests._utilities.assertions as _flext_tests__utilities_assertions

    assertions = _flext_tests__utilities_assertions
    import flext_tests._utilities.badobjects as _flext_tests__utilities_badobjects
    from flext_tests._utilities.assertions import FlextTestsAssertionsUtilitiesMixin

    badobjects = _flext_tests__utilities_badobjects
    import flext_tests._utilities.config as _flext_tests__utilities_config
    from flext_tests._utilities.badobjects import FlextTestsBadObjectsUtilitiesMixin

    config = _flext_tests__utilities_config
    import flext_tests._utilities.constants as _flext_tests__utilities_constants
    from flext_tests._utilities.config import FlextTestsConfigHelpersUtilitiesMixin

    constants = _flext_tests__utilities_constants
    import flext_tests._utilities.container as _flext_tests__utilities_container
    from flext_tests._utilities.constants import (
        FlextTestsConstantsHelpersUtilitiesMixin,
    )

    container = _flext_tests__utilities_container
    import flext_tests._utilities.context as _flext_tests__utilities_context
    from flext_tests._utilities.container import (
        FlextTestsContainerHelpersUtilitiesMixin,
    )

    context = _flext_tests__utilities_context
    import flext_tests._utilities.deepmatch as _flext_tests__utilities_deepmatch
    from flext_tests._utilities.context import FlextTestsContextHelpersUtilitiesMixin

    deepmatch = _flext_tests__utilities_deepmatch
    import flext_tests._utilities.domain as _flext_tests__utilities_domain
    from flext_tests._utilities.deepmatch import FlextTestsDeepMatchUtilitiesMixin

    domain = _flext_tests__utilities_domain
    import flext_tests._utilities.exception as _flext_tests__utilities_exception
    from flext_tests._utilities.domain import FlextTestsDomainHelpersUtilitiesMixin

    exception = _flext_tests__utilities_exception
    import flext_tests._utilities.factory as _flext_tests__utilities_factory
    from flext_tests._utilities.exception import (
        FlextTestsExceptionHelpersUtilitiesMixin,
    )

    factory = _flext_tests__utilities_factory
    import flext_tests._utilities.files as _flext_tests__utilities_files
    from flext_tests._utilities.factory import FlextTestsFactoryUtilitiesMixin

    files = _flext_tests__utilities_files
    import flext_tests._utilities.generic as _flext_tests__utilities_generic
    from flext_tests._utilities.files import FlextTestsFilesUtilitiesMixin

    generic = _flext_tests__utilities_generic
    import flext_tests._utilities.handler as _flext_tests__utilities_handler
    from flext_tests._utilities.generic import FlextTestsGenericHelpersUtilitiesMixin

    handler = _flext_tests__utilities_handler
    import flext_tests._utilities.length as _flext_tests__utilities_length
    from flext_tests._utilities.handler import FlextTestsHandlerHelpersUtilitiesMixin

    length = _flext_tests__utilities_length
    import flext_tests._utilities.matchers as _flext_tests__utilities_matchers
    from flext_tests._utilities.length import FlextTestsLengthUtilitiesMixin

    matchers = _flext_tests__utilities_matchers
    import flext_tests._utilities.parser as _flext_tests__utilities_parser
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities, tm

    parser = _flext_tests__utilities_parser
    import flext_tests._utilities.payload as _flext_tests__utilities_payload
    from flext_tests._utilities.parser import FlextTestsParserHelpersUtilitiesMixin

    payload = _flext_tests__utilities_payload
    import flext_tests._utilities.registry as _flext_tests__utilities_registry
    from flext_tests._utilities.payload import FlextTestsPayloadUtilities

    registry = _flext_tests__utilities_registry
    import flext_tests._utilities.result as _flext_tests__utilities_result
    from flext_tests._utilities.registry import FlextTestsRegistryHelpersUtilitiesMixin

    result = _flext_tests__utilities_result
    import flext_tests._utilities.testcase as _flext_tests__utilities_testcase
    from flext_tests._utilities.result import FlextTestsResultUtilitiesMixin

    testcase = _flext_tests__utilities_testcase
    import flext_tests._utilities.testcontext as _flext_tests__utilities_testcontext
    from flext_tests._utilities.testcase import FlextTestsTestCaseHelpersUtilitiesMixin

    testcontext = _flext_tests__utilities_testcontext
    import flext_tests._utilities.validation as _flext_tests__utilities_validation
    from flext_tests._utilities.testcontext import FlextTestsTestContextUtilitiesMixin

    validation = _flext_tests__utilities_validation
    import flext_tests._utilities.validator as _flext_tests__utilities_validator
    from flext_tests._utilities.validation import FlextTestsValidationUtilitiesMixin

    validator = _flext_tests__utilities_validator
    from flext_tests._utilities.validator import FlextTestsValidatorUtilitiesMixin
_LAZY_IMPORTS = {
    "FlextTestsAssertionsUtilitiesMixin": (
        "flext_tests._utilities.assertions",
        "FlextTestsAssertionsUtilitiesMixin",
    ),
    "FlextTestsBadObjectsUtilitiesMixin": (
        "flext_tests._utilities.badobjects",
        "FlextTestsBadObjectsUtilitiesMixin",
    ),
    "FlextTestsConfigHelpersUtilitiesMixin": (
        "flext_tests._utilities.config",
        "FlextTestsConfigHelpersUtilitiesMixin",
    ),
    "FlextTestsConstantsHelpersUtilitiesMixin": (
        "flext_tests._utilities.constants",
        "FlextTestsConstantsHelpersUtilitiesMixin",
    ),
    "FlextTestsContainerHelpersUtilitiesMixin": (
        "flext_tests._utilities.container",
        "FlextTestsContainerHelpersUtilitiesMixin",
    ),
    "FlextTestsContextHelpersUtilitiesMixin": (
        "flext_tests._utilities.context",
        "FlextTestsContextHelpersUtilitiesMixin",
    ),
    "FlextTestsDeepMatchUtilitiesMixin": (
        "flext_tests._utilities.deepmatch",
        "FlextTestsDeepMatchUtilitiesMixin",
    ),
    "FlextTestsDomainHelpersUtilitiesMixin": (
        "flext_tests._utilities.domain",
        "FlextTestsDomainHelpersUtilitiesMixin",
    ),
    "FlextTestsExceptionHelpersUtilitiesMixin": (
        "flext_tests._utilities.exception",
        "FlextTestsExceptionHelpersUtilitiesMixin",
    ),
    "FlextTestsFactoryUtilitiesMixin": (
        "flext_tests._utilities.factory",
        "FlextTestsFactoryUtilitiesMixin",
    ),
    "FlextTestsFilesUtilitiesMixin": (
        "flext_tests._utilities.files",
        "FlextTestsFilesUtilitiesMixin",
    ),
    "FlextTestsGenericHelpersUtilitiesMixin": (
        "flext_tests._utilities.generic",
        "FlextTestsGenericHelpersUtilitiesMixin",
    ),
    "FlextTestsHandlerHelpersUtilitiesMixin": (
        "flext_tests._utilities.handler",
        "FlextTestsHandlerHelpersUtilitiesMixin",
    ),
    "FlextTestsLengthUtilitiesMixin": (
        "flext_tests._utilities.length",
        "FlextTestsLengthUtilitiesMixin",
    ),
    "FlextTestsMatchersUtilities": (
        "flext_tests._utilities.matchers",
        "FlextTestsMatchersUtilities",
    ),
    "FlextTestsParserHelpersUtilitiesMixin": (
        "flext_tests._utilities.parser",
        "FlextTestsParserHelpersUtilitiesMixin",
    ),
    "FlextTestsPayloadUtilities": (
        "flext_tests._utilities.payload",
        "FlextTestsPayloadUtilities",
    ),
    "FlextTestsRegistryHelpersUtilitiesMixin": (
        "flext_tests._utilities.registry",
        "FlextTestsRegistryHelpersUtilitiesMixin",
    ),
    "FlextTestsResultUtilitiesMixin": (
        "flext_tests._utilities.result",
        "FlextTestsResultUtilitiesMixin",
    ),
    "FlextTestsTestCaseHelpersUtilitiesMixin": (
        "flext_tests._utilities.testcase",
        "FlextTestsTestCaseHelpersUtilitiesMixin",
    ),
    "FlextTestsTestContextUtilitiesMixin": (
        "flext_tests._utilities.testcontext",
        "FlextTestsTestContextUtilitiesMixin",
    ),
    "FlextTestsValidationUtilitiesMixin": (
        "flext_tests._utilities.validation",
        "FlextTestsValidationUtilitiesMixin",
    ),
    "FlextTestsValidatorUtilitiesMixin": (
        "flext_tests._utilities.validator",
        "FlextTestsValidatorUtilitiesMixin",
    ),
    "assertions": "flext_tests._utilities.assertions",
    "badobjects": "flext_tests._utilities.badobjects",
    "config": "flext_tests._utilities.config",
    "constants": "flext_tests._utilities.constants",
    "container": "flext_tests._utilities.container",
    "context": "flext_tests._utilities.context",
    "deepmatch": "flext_tests._utilities.deepmatch",
    "domain": "flext_tests._utilities.domain",
    "exception": "flext_tests._utilities.exception",
    "factory": "flext_tests._utilities.factory",
    "files": "flext_tests._utilities.files",
    "generic": "flext_tests._utilities.generic",
    "handler": "flext_tests._utilities.handler",
    "length": "flext_tests._utilities.length",
    "matchers": "flext_tests._utilities.matchers",
    "parser": "flext_tests._utilities.parser",
    "payload": "flext_tests._utilities.payload",
    "registry": "flext_tests._utilities.registry",
    "result": "flext_tests._utilities.result",
    "testcase": "flext_tests._utilities.testcase",
    "testcontext": "flext_tests._utilities.testcontext",
    "tm": ("flext_tests._utilities.matchers", "tm"),
    "validation": "flext_tests._utilities.validation",
    "validator": "flext_tests._utilities.validator",
}

__all__ = [
    "FlextTestsAssertionsUtilitiesMixin",
    "FlextTestsBadObjectsUtilitiesMixin",
    "FlextTestsConfigHelpersUtilitiesMixin",
    "FlextTestsConstantsHelpersUtilitiesMixin",
    "FlextTestsContainerHelpersUtilitiesMixin",
    "FlextTestsContextHelpersUtilitiesMixin",
    "FlextTestsDeepMatchUtilitiesMixin",
    "FlextTestsDomainHelpersUtilitiesMixin",
    "FlextTestsExceptionHelpersUtilitiesMixin",
    "FlextTestsFactoryUtilitiesMixin",
    "FlextTestsFilesUtilitiesMixin",
    "FlextTestsGenericHelpersUtilitiesMixin",
    "FlextTestsHandlerHelpersUtilitiesMixin",
    "FlextTestsLengthUtilitiesMixin",
    "FlextTestsMatchersUtilities",
    "FlextTestsParserHelpersUtilitiesMixin",
    "FlextTestsPayloadUtilities",
    "FlextTestsRegistryHelpersUtilitiesMixin",
    "FlextTestsResultUtilitiesMixin",
    "FlextTestsTestCaseHelpersUtilitiesMixin",
    "FlextTestsTestContextUtilitiesMixin",
    "FlextTestsValidationUtilitiesMixin",
    "FlextTestsValidatorUtilitiesMixin",
    "assertions",
    "badobjects",
    "config",
    "constants",
    "container",
    "context",
    "deepmatch",
    "domain",
    "exception",
    "factory",
    "files",
    "generic",
    "handler",
    "length",
    "matchers",
    "parser",
    "payload",
    "registry",
    "result",
    "testcase",
    "testcontext",
    "tm",
    "validation",
    "validator",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

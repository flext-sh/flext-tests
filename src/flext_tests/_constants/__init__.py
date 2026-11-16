# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import defer_lazy_bases, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._constants.base import FlextTestsConstantsBase
    from flext_tests._constants.data_cases import FlextTestsConstantsDataCases
    from flext_tests._constants.docker import FlextTestsConstantsDocker
    from flext_tests._constants.files import FlextTestsConstantsFiles
    from flext_tests._constants.matcher import FlextTestsConstantsMatcher
    from flext_tests._constants.namespace import FlextTestsConstantsNamespace
    from flext_tests._constants.pytest_surface import FlextTestsConstantsPytest
    from flext_tests._constants.validator import FlextTestsConstantsValidator


__all__: tuple[str, ...] = (
    "FlextTestsConstantsBase",
    "FlextTestsConstantsDataCases",
    "FlextTestsConstantsDocker",
    "FlextTestsConstantsFiles",
    "FlextTestsConstantsMatcher",
    "FlextTestsConstantsNamespace",
    "FlextTestsConstantsPytest",
    "FlextTestsConstantsValidator",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTestsConstantsBase": ".base",
        "FlextTestsConstantsDataCases": ".data_cases",
        "FlextTestsConstantsDocker": ".docker",
        "FlextTestsConstantsFiles": ".files",
        "FlextTestsConstantsMatcher": ".matcher",
        "FlextTestsConstantsNamespace": ".namespace",
        "FlextTestsConstantsPytest": ".pytest_surface",
        "FlextTestsConstantsValidator": ".validator",
    },
    public_exports=__all__,
    deferred_members={
        "FlextTestsConstantsDataCases": (
            "FORMAT_APP_ID_CASES",
            "SAFE_STRING_VALID_CASES",
            "SAFE_STRING_INVALID_CASES",
        ),
        "FlextTestsConstantsDocker": (
            "DOCKER_TEST_ENVIRONMENT_DIR",
            "DOCKER_TEST_ENVIRONMENT_FIXTURE",
            "DOCKER_HOST_VARIABLE",
            "DOCKER_LOCAL_ENV_FILE",
            "DOCKER_NOT_CONFIGURED_REASON",
            "DOCKER_CI_VARIABLE_INI",
            "DOCKER_CI_VALUE_INI",
            "DOCKER_CONNECTIVITY_MARKER",
            "DOCKER_UNREACHABLE_DESELECT_REASON",
            "DOCKER_PROBE_MAX_WAIT_SECONDS",
            "DOCKER_STATE_DIR_PARTS",
            "DOCKER_LEASE_LOCK_SUFFIX",
            "SCRATCH_DIR_PARTS",
            "SCRATCH_ROOT_INI",
            "SCRATCH_ROOT_WORKERINPUT_KEY",
            "DOCKER_CONTAINER_NAME_PATTERN",
            "DOCKER_LEASE_TIMEOUT_SECONDS",
            "DOCKER_HEALTH_POLL_SECONDS",
            "DOCKER_ENV_FILE_SUFFIX",
            "DOCKER_ENV_FILE_MODE",
            "DOCKER_TCP_PORT_SUFFIX",
            "DOCKER_TCP_CONNECT_TIMEOUT_SECONDS",
            "DOCKER_ENV_SEPARATOR",
            "DOCKER_ENV_FORBIDDEN_MARKS",
            "DOCKER_SECRET_BYTES",
            "ERR_DOCKER_NOT_PROVISIONED",
            "DOCKER_COMPOSE_ERRORS",
            "ERR_DOCKER_UNHEALTHY",
            "ERR_DOCKER_PORT_NOT_PUBLISHED",
            "ERR_DOCKER_READINESS_TIMEOUT",
            "ERR_DOCKER_ENVIRONMENT_MISSING",
            "ERR_DOCKER_GENERATED_KEYS",
            "ERR_DOCKER_ENV_VALUE",
            "ERR_DOCKER_TARGET_MISSING",
            "ERR_DOCKER_TARGET_NOT_INSPECTABLE",
            "FILE_LOCK_POLL_SECONDS",
            "FILE_LOCK_MODE_SHARED",
            "FILE_LOCK_MODE_EXCLUSIVE",
            "ERR_FILE_LOCK_TIMEOUT",
            "ERR_FILE_LOCK_POSIX_ONLY",
            "CONNECTIVITY_MARKER_CONTAINERS",
            "CONNECTIVITY_MARKERS",
            "UNREACHABLE_DESELECT_REASON",
            "CONNECTIVITY_PROBE_TIMEOUT_SECONDS",
            "DOCKER_SHARED_ASSETS_DIR",
            "SHARED_CONTAINERS",
            "DockerErrorCode",
            "ContainerHealth",
            "ContainerStatus",
        ),
        "FlextTestsConstantsFiles": (
            "CompareMode",
            "DEFAULT_ENCODING",
            "DEFAULT_BINARY_ENCODING",
            "PERMISSION_READONLY_FILE",
            "PERMISSION_WRITABLE_FILE",
            "PERMISSION_WRITABLE_DIR",
            "HASH_CHUNK_SIZE",
            "FIXTURE_TREES_INI",
            "ERROR_FILE_NOT_FOUND",
            "ERROR_INVALID_JSON",
            "ERROR_INVALID_YAML",
            "ERROR_ENCODING",
            "ERROR_READ",
            "ERROR_COMPARE",
            "ERROR_INFO",
        ),
        "FlextTestsConstantsMatcher": (
            "MatcherMissing",
            "PAYLOAD_COLLECTION_TYPES",
            "MATCHER_SCALAR_CRITERIA",
            "ERR_NOT_MATCHES",
            "ERR_OK_FAILED",
            "ERR_FAIL_EXPECTED",
            "ERR_TYPE_FAILED",
            "ERR_CONTAINS_FAILED",
            "ERR_LACKS_FAILED",
            "ERR_LEN_EXACT_FAILED",
            "ERR_LEN_RANGE_FAILED",
            "ERR_DEEP_PATH_FAILED",
            "ERR_PREDICATE_FAILED",
            "ERR_CONSTRAINTS_FAILED",
            "ERR_ALL_ITEMS_FAILED",
            "ERR_ANY_ITEMS_FAILED",
            "ERR_KEYS_MISSING",
            "ERR_KEYS_EXTRA",
            "ERR_ERROR_CODE_MISMATCH",
            "ERR_ERROR_CODE_NOT_CONTAINS",
            "ERR_ERROR_DATA_KEY_MISSING",
            "ERR_ERROR_DATA_VALUE_MISMATCH",
            "EMAIL_PATTERN",
            "EMAIL_PATTERN_RE",
        ),
        "FlextTestsConstantsNamespace": (
            "NAMESPACE_ID_PATTERN",
            "NAMESPACE_ID_LENGTH",
            "NAMESPACE_BASE36_ALPHABET",
            "NAMESPACE_CHECKOUT_DIGEST_LENGTH",
            "NAMESPACE_WORKER_CODE_LENGTH",
        ),
        "FlextTestsConstantsPytest": (),
        "FlextTestsConstantsValidator": (
            "ENFORCEMENT_WORKSPACE_MARKERS",
            "ENFORCEMENT_PROJECT_PREFIX",
            "ENFORCEMENT_FINDING_SEVERITY_KEY",
            "ENFORCEMENT_FINDING_MESSAGE_KEY",
            "ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION",
            "ENFORCEMENT_SLOW_REPORT_TITLE",
            "ENFORCEMENT_SLOW_NEAR_LIMIT_RATIO",
            "ENFORCEMENT_SLOW_MARKER",
            "ENFORCEMENT_HEAVY_TIER_MARKERS",
            "ENFORCEMENT_TIMEOUT_OPTION",
            "ENFORCEMENT_CALL_PHASE",
            "ENFORCEMENT_DISPATCHER_MODULE",
            "FIXTURE_PLUGIN_MODULES",
            "CAPABILITY_PLUGIN_MODULE",
        ),
    },
)

defer_lazy_bases(
    __name__,
    {
        "FlextTestsConstantsPytest": (
            ("flext_infra", "FlextInfraConstants.Infra.Pytest"),
        ),
    },
)

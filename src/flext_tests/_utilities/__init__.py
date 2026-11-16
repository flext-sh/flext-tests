# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import defer_lazy_bases, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities.base import FlextTestsUtilitiesBase
    from flext_tests._utilities.container import FlextTestsUtilitiesContainerHelpers
    from flext_tests._utilities.docker_client import FlextTestsUtilitiesDockerClient
    from flext_tests._utilities.docker_lifecycle import (
        FlextTestsUtilitiesDockerLifecycle,
    )
    from flext_tests._utilities.docker_state import FlextTestsUtilitiesDockerState
    from flext_tests._utilities.enforcement import FlextTestsUtilitiesEnforcement
    from flext_tests._utilities.environment import FlextTestsUtilitiesEnvironment
    from flext_tests._utilities.files import FlextTestsUtilitiesFiles
    from flext_tests._utilities.fixtures_dsl import FlextTestsUtilitiesFixturesDSL
    from flext_tests._utilities.governance import FlextTestsUtilitiesFlextGovernance
    from flext_tests._utilities.handler import FlextTestsUtilitiesFlextHandler
    from flext_tests._utilities.matchers import FlextTestsUtilitiesMatchers
    from flext_tests._utilities.namespace import FlextTestsUtilitiesNamespace
    from flext_tests._utilities.payload import FlextTestsUtilitiesPayload
    from flext_tests._utilities.pytest_surface import FlextTestsUtilitiesPytest
    from flext_tests._utilities.result import FlextTestsUtilitiesResult
    from flext_tests._utilities.scratch_storage import FlextTestsUtilitiesScratchStorage
    from flext_tests._utilities.settings import FlextTestsUtilitiesConfigHelpers
    from flext_tests._utilities.testcontext import FlextTestsUtilitiesTestContext


__all__: tuple[str, ...] = (
    "FlextTestsUtilitiesBase",
    "FlextTestsUtilitiesConfigHelpers",
    "FlextTestsUtilitiesContainerHelpers",
    "FlextTestsUtilitiesDockerClient",
    "FlextTestsUtilitiesDockerLifecycle",
    "FlextTestsUtilitiesDockerState",
    "FlextTestsUtilitiesEnforcement",
    "FlextTestsUtilitiesEnvironment",
    "FlextTestsUtilitiesFiles",
    "FlextTestsUtilitiesFixturesDSL",
    "FlextTestsUtilitiesFlextGovernance",
    "FlextTestsUtilitiesFlextHandler",
    "FlextTestsUtilitiesMatchers",
    "FlextTestsUtilitiesNamespace",
    "FlextTestsUtilitiesPayload",
    "FlextTestsUtilitiesPytest",
    "FlextTestsUtilitiesResult",
    "FlextTestsUtilitiesScratchStorage",
    "FlextTestsUtilitiesTestContext",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTestsUtilitiesBase": ".base",
        "FlextTestsUtilitiesConfigHelpers": ".settings",
        "FlextTestsUtilitiesContainerHelpers": ".container",
        "FlextTestsUtilitiesDockerClient": ".docker_client",
        "FlextTestsUtilitiesDockerLifecycle": ".docker_lifecycle",
        "FlextTestsUtilitiesDockerState": ".docker_state",
        "FlextTestsUtilitiesEnforcement": ".enforcement",
        "FlextTestsUtilitiesEnvironment": ".environment",
        "FlextTestsUtilitiesFiles": ".files",
        "FlextTestsUtilitiesFixturesDSL": ".fixtures_dsl",
        "FlextTestsUtilitiesFlextGovernance": ".governance",
        "FlextTestsUtilitiesFlextHandler": ".handler",
        "FlextTestsUtilitiesMatchers": ".matchers",
        "FlextTestsUtilitiesNamespace": ".namespace",
        "FlextTestsUtilitiesPayload": ".payload",
        "FlextTestsUtilitiesPytest": ".pytest_surface",
        "FlextTestsUtilitiesResult": ".result",
        "FlextTestsUtilitiesScratchStorage": ".scratch_storage",
        "FlextTestsUtilitiesTestContext": ".testcontext",
    },
    public_exports=__all__,
    deferred_members={
        "FlextTestsUtilitiesConfigHelpers": ("env_vars_context",),
        "FlextTestsUtilitiesContainerHelpers": (
            "create_counting_factory",
            "create_factory",
        ),
        "FlextTestsUtilitiesDockerClient": (
            "docker_declaration_matches",
            "docker_endpoint",
            "docker_environment_file",
            "docker_sdk_client",
            "docker_inspect",
            "docker_compose_client",
            "docker_compose_up",
        ),
        "FlextTestsUtilitiesDockerLifecycle": (
            "docker_compose_project",
            "resolve_host_port",
            "container_info",
            "container_environment",
            "generate_creation_secrets",
            "validate_creation_environment",
            "creation_env_file",
        ),
        "FlextTestsUtilitiesDockerState": (
            "docker_state_dir",
            "docker_shared_assets_dir",
            "docker_lease_lock_file",
        ),
        "FlextTestsUtilitiesEnforcement": (
            "_plan_cache",
            "_catalog_cache",
            "build_canonical_catalog",
            "active_rules",
            "infra_rule_findings",
            "project_name_for_path",
            "collected_project_names",
        ),
        "FlextTestsUtilitiesEnvironment": (
            "external_environment_reason",
            "_values_reason",
            "endpoint_reason",
            "_endpoint_reason",
            "external_environment_values",
        ),
        "FlextTestsUtilitiesFiles": (),
        "FlextTestsUtilitiesFixturesDSL": (
            "_FIXTURES_ROOT",
            "_FILE_EXTENSION",
            "_root",
            "_resolve_path",
            "path",
            "load",
            "exists",
            "servers",
            "fixture_trees_root",
            "is_fixture_tree",
            "materialize",
            "kinds",
        ),
        "FlextTestsUtilitiesFlextGovernance": (
            "_console_script_functions",
            "FlextTestsModuleGovernance",
        ),
        "FlextTestsUtilitiesFlextHandler": ("FlextTestsUtilitiesHandlerHelpers",),
        "FlextTestsUtilitiesMatchers": (),
        "FlextTestsUtilitiesNamespace": (
            "_issue_lock",
            "_last_issue",
            "namespace",
            "_monotonic_tail",
            "_base36",
            "_worker_code",
        ),
        "FlextTestsUtilitiesPayload": (
            "_payload_model_leaf",
            "_payload_none_leaf",
            "_payload_scalar_leaf",
            "_payload_annotated_leaf",
            "_payload_match_leaf",
            "_payload_runtime_leaf",
            "_payload_view_leaf",
            "_payload_mapping_leaf",
            "_payload_sequence_leaf",
            "_PAYLOAD_LEAF_HANDLERS",
            "to_payload",
            "to_match_value",
            "to_normalized_value",
            "to_config_map",
            "path_node",
            "extract_path_value",
            "deep_match",
        ),
        "FlextTestsUtilitiesPytest": (),
        "FlextTestsUtilitiesResult": (
            "assert_failure",
            "assert_success",
        ),
        "FlextTestsUtilitiesScratchStorage": ("scratch_root",),
        "FlextTestsUtilitiesTestContext": (
            "pytest_subprocess",
            "cli_in_process",
            "_exit_code",
            "SessionRuntime",
            "FileLock",
        ),
    },
)

defer_lazy_bases(
    __name__,
    {
        "FlextTestsUtilitiesFiles": (
            ("flext_tests._utilities._files", "FlextTestsUtilitiesFilesInfo"),
            ("flext_tests._utilities._files", "FlextTestsUtilitiesFilesSize"),
        ),
        "FlextTestsUtilitiesMatchers": (
            (
                "flext_tests._utilities._matchers",
                "FlextTestsUtilitiesMatchersAssertions",
            ),
            (
                "flext_tests._utilities._matchers",
                "FlextTestsUtilitiesMatchersContainment",
            ),
            (
                "flext_tests._utilities._matchers",
                "FlextTestsUtilitiesMatchersImmutability",
            ),
            ("flext_tests._utilities._matchers", "FlextTestsUtilitiesMatchersResult"),
            ("flext_tests._utilities._matchers", "FlextTestsUtilitiesMatchersScope"),
            ("flext_tests._utilities._matchers", "FlextTestsUtilitiesMatchersThat"),
            (
                "flext_tests._utilities._matchers",
                "FlextTestsUtilitiesMatchersTypeguards",
            ),
        ),
        "FlextTestsUtilitiesPytest": (
            ("flext_infra", "FlextInfraUtilities.Infra.Pytest"),
        ),
    },
)

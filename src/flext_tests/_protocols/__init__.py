# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._protocols.base import FlextTestsProtocolsBase
    from flext_tests._protocols.docker import FlextTestsProtocolsDocker
    from flext_tests._protocols.enforcement import FlextTestsProtocolsEnforcement
    from flext_tests._protocols.filesystem import FlextTestsProtocolsFilesystem
    from flext_tests._protocols.fixture_trees import FlextTestsProtocolsFixtureTrees
    from flext_tests._protocols.matchers import FlextTestsProtocolsMatchers
    from flext_tests._protocols.namespace import FlextTestsProtocolsNamespace
    from flext_tests._protocols.payload import FlextTestsProtocolsPayload
    from flext_tests._protocols.spec import FlextTestsProtocolsSpec
    from flext_tests._protocols.validator import FlextTestsProtocolsValidator
    from flext_tests._protocols.valuefactory import FlextTestsProtocolsValueFactory


__all__: tuple[str, ...] = (
    "FlextTestsProtocolsBase",
    "FlextTestsProtocolsDocker",
    "FlextTestsProtocolsEnforcement",
    "FlextTestsProtocolsFilesystem",
    "FlextTestsProtocolsFixtureTrees",
    "FlextTestsProtocolsMatchers",
    "FlextTestsProtocolsNamespace",
    "FlextTestsProtocolsPayload",
    "FlextTestsProtocolsSpec",
    "FlextTestsProtocolsValidator",
    "FlextTestsProtocolsValueFactory",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTestsProtocolsBase": ".base",
        "FlextTestsProtocolsDocker": ".docker",
        "FlextTestsProtocolsEnforcement": ".enforcement",
        "FlextTestsProtocolsFilesystem": ".filesystem",
        "FlextTestsProtocolsFixtureTrees": ".fixture_trees",
        "FlextTestsProtocolsMatchers": ".matchers",
        "FlextTestsProtocolsNamespace": ".namespace",
        "FlextTestsProtocolsPayload": ".payload",
        "FlextTestsProtocolsSpec": ".spec",
        "FlextTestsProtocolsValidator": ".validator",
        "FlextTestsProtocolsValueFactory": ".valuefactory",
    },
    public_exports=__all__,
    deferred_members={
        "FlextTestsProtocolsBase": (
            "ModelReader",
            "Payload",
            "Entity",
            "Value",
        ),
        "FlextTestsProtocolsDocker": (
            "ContainerInitializer",
            "ReadinessProbe",
            "ContainerConfig",
            "ContainerInfo",
            "ContainerInspectHealth",
            "ContainerInspectState",
            "ContainerInspectConfig",
            "ContainerInspectBinding",
            "ContainerInspectNetwork",
            "ContainerInspect",
            "ContainerState",
            "User",
            "Config",
        ),
        "FlextTestsProtocolsEnforcement": (
            "PytestNode",
            "NodeFactory",
            "TypedNode",
            "EnforcementBuilder",
            "NamespaceEnforcer",
            "NamespaceEnforcerFactory",
            "EnforcementScanFinding",
            "EnforcementScanReport",
        ),
        "FlextTestsProtocolsFilesystem": (
            "FileInfo",
            "ContentMeta",
            "CreateParams",
            "ReadParams",
            "PathCoercingParams",
            "CompareParams",
            "InfoParams",
            "AssertExistsParams",
            "CreateKwargsParams",
        ),
        "FlextTestsProtocolsFixtureTrees": ("FixtureTree",),
        "FlextTestsProtocolsMatchers": (
            "MatcherOption",
            "MatcherCriteriaMapping",
            "MatcherCriteriaSequence",
            "MatchPredicate",
            "ApproxLike",
            "PayloadParams",
            "MatchRule",
            "FailParams",
            "ThatShapeParams",
            "ThatContentParams",
            "ThatParams",
            "ScopeParams",
            "DeepMatchResult",
            "Chain",
            "TestScope",
        ),
        "FlextTestsProtocolsNamespace": (
            "TestNamespace",
            "HandlerConfigParams",
        ),
        "FlextTestsProtocolsPayload": (
            "PayloadModel",
            "CapturedText",
            "OutputCapture",
            "NativeSequence",
            "NativeMapping",
            "NativeMatchValue",
        ),
        "FlextTestsProtocolsSpec": ("ContainerSpec",),
        "FlextTestsProtocolsValidator": (
            "EnforcementInfraRuleSource",
            "EnforcementRuntimeWarningSource",
            "EnforcementRuleSpec",
            "EnforcementCatalog",
            "EnforcementBuildContext",
            "EnforcementDispatcherConfig",
            "EnforcementViolation",
        ),
        "FlextTestsProtocolsValueFactory": (
            "RuntimeProvision",
            "SessionRuntime",
            "EntityFactory",
            "ValueFactory",
        ),
    },
)

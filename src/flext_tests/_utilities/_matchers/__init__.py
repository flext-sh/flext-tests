# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities. Matchers package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities._matchers.assertions import (
        FlextTestsUtilitiesMatchersAssertions,
    )
    from flext_tests._utilities._matchers.containment import (
        FlextTestsUtilitiesMatchersContainment,
    )
    from flext_tests._utilities._matchers.immutability import (
        FlextTestsUtilitiesMatchersImmutability,
    )
    from flext_tests._utilities._matchers.result import (
        FlextTestsUtilitiesMatchersResult,
    )
    from flext_tests._utilities._matchers.scope import FlextTestsUtilitiesMatchersScope
    from flext_tests._utilities._matchers.that import FlextTestsUtilitiesMatchersThat
    from flext_tests._utilities._matchers.typeguards import (
        FlextTestsUtilitiesMatchersTypeguards,
    )


__all__: tuple[str, ...] = (
    "FlextTestsUtilitiesMatchersAssertions",
    "FlextTestsUtilitiesMatchersContainment",
    "FlextTestsUtilitiesMatchersImmutability",
    "FlextTestsUtilitiesMatchersResult",
    "FlextTestsUtilitiesMatchersScope",
    "FlextTestsUtilitiesMatchersThat",
    "FlextTestsUtilitiesMatchersTypeguards",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTestsUtilitiesMatchersAssertions": ".assertions",
        "FlextTestsUtilitiesMatchersContainment": ".containment",
        "FlextTestsUtilitiesMatchersImmutability": ".immutability",
        "FlextTestsUtilitiesMatchersResult": ".result",
        "FlextTestsUtilitiesMatchersScope": ".scope",
        "FlextTestsUtilitiesMatchersThat": ".that",
        "FlextTestsUtilitiesMatchersTypeguards": ".typeguards",
    },
    public_exports=__all__,
    deferred_members={
        "FlextTestsUtilitiesMatchersAssertions": (
            "reject",
            "raise_match_assertion",
            "assert_len_match",
        ),
        "FlextTestsUtilitiesMatchersContainment": ("check_has_lacks",),
        "FlextTestsUtilitiesMatchersImmutability": ("rejects_assignment",),
        "FlextTestsUtilitiesMatchersResult": (
            "check",
            "fail",
            "fail_code",
            "fail_data",
            "ok",
        ),
        "FlextTestsUtilitiesMatchersScope": ("scope",),
        "FlextTestsUtilitiesMatchersThat": (
            "_TUPLE_NAME_VALUE_PAIR_LEN",
            "_validate_declared_types",
            "_validate_is_type",
            "_is_subject_only",
            "_validate_subject_only",
            "_result_subject",
            "_ok_value",
            "_has_scalar_validation",
            "_validate_common",
            "_validate_sequence_edges",
            "_validate_sequence",
            "_validate_all",
            "_validate_any",
            "_validate_sequence_order",
            "_sort_key",
            "_validate_mapping",
            "_validate_kv",
            "_validate_attrs",
            "_validate_attr_eq",
            "not_none",
            "instance",
            "that",
            "_assert_truth",
            "_validate_deep",
            "_validate_rule_sets",
            "_named_operands",
            "_rule_kwargs",
            "_apply_rule",
            "apply_path_rules",
            "apply_item_rules",
            "apply_attribute_rules",
        ),
        "FlextTestsUtilitiesMatchersTypeguards": (
            "_scalar_guard_matches",
            "assert_scalar_match",
        ),
    },
)

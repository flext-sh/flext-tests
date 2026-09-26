"""Unit tests for flext_tests.matchers module.

The part modules are imported as modules so pytest collects each behavioural
slice exactly once, through the composed suite below.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._matchers_parts import (
    data_driven,
    fail_constraints,
    ok_constraints,
    rejects_assignment,
    results,
    scope_errors,
    that_attrs,
    that_collections,
    validation,
)




class TestsFlextTestsMatchers(
    results.TestsFlextTestsMatchersResultsMixin,
    validation.TestsFlextTestsMatchersValidationMixin,
    ok_constraints.TestsFlextTestsMatchersOkConstraintsMixin,
    fail_constraints.TestsFlextTestsMatchersFailConstraintsMixin,
    that_collections.TestsFlextTestsMatchersThatCollectionsMixin,
    that_attrs.TestsFlextTestsMatchersThatAttrsMixin,
    scope_errors.TestsFlextTestsMatchersScopeErrorsMixin,
    rejects_assignment.TestsFlextTestsMatchersRejectsAssignmentMixin,
    data_driven.TestsFlextTestsMatchersDataDrivenMixin,
):
    """Test suite for tm class."""

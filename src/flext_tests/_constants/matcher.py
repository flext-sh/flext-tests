"""Matcher test infrastructure constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final


class FlextTestsConstantsMatcher:
    """Matcher constants mixin for test assertions."""

    MATCHER_RULE_KEYS: Final[frozenset[str]] = frozenset({
        "all",
        "all_",
        "any",
        "any_",
        "attr_eq",
        "attrs",
        "attrs_match",
        "contains",
        "deep",
        "empty",
        "ends",
        "eq",
        "error",
        "excludes",
        "first",
        "gt",
        "gte",
        "has",
        "is",
        "is_",
        "items",
        "keys",
        "lacks",
        "lacks_keys",
        "last",
        "len",
        "length",
        "length_gt",
        "length_gte",
        "length_lt",
        "length_lte",
        "lt",
        "lte",
        "match",
        "methods",
        "msg",
        "ne",
        "none",
        "not",
        "not_",
        "ok",
        "path",
        "paths",
        "sorted",
        "starts",
        "unique",
        "values",
        "where",
    })

    ERR_NOT_STARTSWITH: Final[str] = "Expected '{text}' to start with '{prefix}'"
    ERR_NOT_ENDSWITH: Final[str] = "Expected '{text}' to end with '{suffix}'"
    ERR_NOT_MATCHES: Final[str] = "Expected '{text}' to match pattern '{pattern}'"
    ERR_OK_FAILED: Final[str] = "Expected success but got failure: {error}"
    ERR_FAIL_EXPECTED: Final[str] = (
        "Expected failure but got success with value: {value!r}"
    )
    ERR_TYPE_FAILED: Final[str] = "Expected type {expected} but got {actual}"
    ERR_CONTAINS_FAILED: Final[str] = "Expected {container!r} to contain {item!r}"
    ERR_LACKS_FAILED: Final[str] = "Expected {container!r} to NOT contain {item!r}"
    ERR_LEN_EXACT_FAILED: Final[str] = "Expected length {expected} but got {actual}"
    ERR_LEN_RANGE_FAILED: Final[str] = (
        "Expected length in range [{min}, {max}] but got {actual}"
    )
    ERR_DEEP_PATH_FAILED: Final[str] = "Deep match failed at path '{path}': {reason}"
    ERR_PREDICATE_FAILED: Final[str] = "Custom predicate failed for value: {value!r}"
    ERR_ALL_ITEMS_FAILED: Final[str] = "Not all items match: failed at index {index}"
    ERR_ANY_ITEMS_FAILED: Final[str] = "No items match the predicate"
    ERR_KEYS_MISSING: Final[str] = "Missing required keys: {keys}"
    ERR_KEYS_EXTRA: Final[str] = "Unexpected keys present: {keys}"
    ERR_SCOPE_PATH_NOT_FOUND: Final[str] = "Path '{path}' not found in value: {error}"
    ERR_ERROR_CODE_MISMATCH: Final[str] = (
        "Expected error code {expected!r} but got {actual!r}"
    )
    ERR_ERROR_CODE_NOT_CONTAINS: Final[str] = (
        "Expected error code to contain {expected!r} but got {actual!r}"
    )
    ERR_ERROR_DATA_KEY_MISSING: Final[str] = "Expected error data key {key!r} not found"
    ERR_ERROR_DATA_VALUE_MISMATCH: Final[str] = (
        "Error data key {key!r}: expected {expected!r}, got {actual!r}"
    )
    ERR_SCOPE_CLEANUP_FAILED: Final[str] = "Cleanup function failed in scope: {error}"
    EMAIL_PATTERN: Final[str] = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

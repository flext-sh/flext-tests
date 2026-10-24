"""Test domain facade for FLEXT ecosystem tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations


class FlextTestsDomains:
    """Test domain facade published to every generated tests package as ``td``.

    It declares no members: the flext-infra lazy-init planner injects ``td``
    into each consumer's generated ``tests/__init__.py``, and no consumer
    reads a domain helper through it.
    """


td: type[FlextTestsDomains] = FlextTestsDomains
"""Test domain facade alias for flext_tests."""

__all__: list[str] = ["FlextTestsDomains", "td"]

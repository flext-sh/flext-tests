"""Generic service surface for flext-tests.

Expose the canonical generic service alias locally so test projects do not
inherit the CLI-specialized ``s`` alias through lazy-init MRO fallback.
"""

from __future__ import annotations

from flext_core.service import FlextService, s

__all__: list[str] = ["FlextService", "s"]

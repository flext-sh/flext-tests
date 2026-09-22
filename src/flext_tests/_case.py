"""Pytest case MRO surface for flext-tests."""

from __future__ import annotations

from flext_tests import p, t


class _FlextTestsCase:
    """Pytest class MRO surface populated by the shared test runtime fixture."""

    service: "FlextTestsServiceBase[p.Base]"
    settings: "FlextTestsSettings"
    logger: p.Logger
    c: type
    e: type
    m: type
    p: type
    r: type
    t: type
    u: type
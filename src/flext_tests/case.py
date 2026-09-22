"""Pytest case MRO surface for flext-tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import p

if TYPE_CHECKING:
    from ._settings import FlextTestsSettings
    from .base import FlextTestsServiceBase


class FlextTestsCase:
    """Pytest class MRO surface populated by the shared test runtime fixture."""

    service: FlextTestsServiceBase[p.Base]
    settings: FlextTestsSettings
    logger: p.Logger
    c: type
    e: type
    m: type
    p: type
    r: type
    t: type
    u: type


__all__: list[str] = ["FlextTestsCase"]

"""ASGI callable contracts for in-process route tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Receive, Scope, Send


class FlextTestsTypesHttp:
    """ASGI contracts the test toolkit accepts without importing a client."""

    type AsgiApp = ASGIApp
    type AsgiScope = Scope
    type AsgiReceive = Receive
    type AsgiSend = Send


__all__ = ["FlextTestsTypesHttp"]

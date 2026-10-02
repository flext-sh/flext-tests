"""Hook contracts of the Docker test lifecycle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_infra import p

if TYPE_CHECKING:
    from flext_tests import m


class FlextTestsDockerProtocolsMixin:
    """Callables the lifecycle invokes around one container."""

    @runtime_checkable
    class ContainerInitializer(Protocol):
        """Prepare a container the lifecycle has just created.

        Runs once per created container, under the exclusive lease, before the
        record is sealed. A failure leaves the record unsealed, so the next
        ensure recreates the container instead of reusing a partial one.
        """

        def __call__(self, info: m.Tests.ContainerInfo) -> p.Result[bool]:
            """Initialize the created container."""
            ...

    @runtime_checkable
    class ReadinessProbe(Protocol):
        """Report whether a container serves its callers.

        Polled until it succeeds with ``True`` or the target's
        ``startup_timeout`` passes; the last failure explains a timeout.
        """

        def __call__(self, info: m.Tests.ContainerInfo) -> p.Result[bool]:
            """Probe the container once."""
            ...

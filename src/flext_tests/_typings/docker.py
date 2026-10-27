"""Docker library types of the test container lifecycle (ADR-028 point 2).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from docker import DockerClient
from docker.models.containers import Container
from python_on_whales import DockerClient as ComposeDockerClient


class FlextTestsDockerTypesMixin:
    type DockerSdkClient = DockerClient
    type DockerContainer = Container
    type ComposeClient = ComposeDockerClient


__all__: list[str] = ["FlextTestsDockerTypesMixin"]

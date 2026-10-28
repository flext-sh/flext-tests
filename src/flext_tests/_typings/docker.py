"""Docker library types of the test container lifecycle (ADR-028 point 2).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from docker import DockerClient
from docker.models.containers import Container
from python_on_whales import DockerClient as ComposeDockerClient


class FlextTestsTypesDocker:
    type DockerSdkClient = DockerClient
    type DockerContainer = Container
    type ComposeClient = ComposeDockerClient


__all__: list[str] = ["FlextTestsTypesDocker"]

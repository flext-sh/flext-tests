# AUTO-GENERATED FILE — Regenerate with: make gen
"""Docker Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests.tests.unit._docker_parts.builders import (
        DockerBuildersMixin as DockerBuildersMixin,
    )
    from flext_tests.tests.unit._docker_parts.operations import (
        DockerOperationsMixin as DockerOperationsMixin,
    )
    from flext_tests.tests.unit._docker_parts.state import (
        DockerStateMixin as DockerStateMixin,
    )
    from flext_tests.tests.unit._docker_parts.targets import (
        DockerTargetsMixin as DockerTargetsMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".builders": ("DockerBuildersMixin",),
        ".operations": ("DockerOperationsMixin",),
        ".state": ("DockerStateMixin",),
        ".targets": ("DockerTargetsMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)

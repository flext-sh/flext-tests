# AUTO-GENERATED FILE — Regenerate with: make gen
"""Internal package for cli.

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

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._cli.docker import FlextTestsCliDocker

__all__: tuple[str, ...] = ("FlextTestsCliDocker",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsCliDocker": ".docker",
    }),
    public_exports=__all__,
)

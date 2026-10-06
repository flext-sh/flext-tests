"""Deterministic pydantic rebuild for the _models mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from typing import Any

# NOTE (import discipline): nested param models annotate through their
# enclosing mixin and through sibling mixins (TYPE_CHECKING-only imports)
# that are not yet bound while the class body executes — pydantic defers
# those models and its lazy rebuild resolves against the CALLING module's
# imports, which breaks consumers whose test modules import neither. The
# rebuild therefore runs at each mixin module's import end against a merged
# namespace: the flext_tests package aliases, this package's already-loaded
# siblings, and the mixin itself.


def _rebuild_namespace(mixin: type) -> dict[str, Any]:
    """Build the merged types namespace for a mixin's deferred models.

    Returns:
        The resulting ``dict[str, Any]`` namespace.

    """
    namespace: dict[str, Any] = {}
    for module_name, module in tuple(sys.modules.items()):
        if module is None:
            continue
        if module_name != "flext_tests" and not module_name.startswith(
            "flext_tests._models.",
        ):
            continue
        for name, value in vars(module).items():
            if name.endswith("ModelsMixin") or name in (
                "t",
                "p",
                "m",
                "u",
                "c",
                "r",
                "s",
                "x",
            ):
                namespace[name] = value
    mixin_module = sys.modules.get(mixin.__module__)
    if mixin_module is not None:
        for name, value in vars(mixin_module).items():
            if name.endswith("ModelsMixin") or name in (
                "t",
                "p",
                "m",
                "u",
                "c",
                "r",
            ):
                namespace[name] = value
    namespace[mixin.__name__] = mixin
    return namespace


def rebuild_nested_models(mixin: type) -> None:
    """Rebuild every nested pydantic model of a mixin deterministically.

    Args:
        mixin: The enclosing mixin class whose nested models are rebuilt.

    """
    namespace = _rebuild_namespace(mixin)
    for member in tuple(vars(mixin).values()):
        if isinstance(member, type) and hasattr(member, "model_rebuild"):
            member.model_rebuild(_types_namespace=namespace)


__all__: list[str] = ["rebuild_nested_models"]

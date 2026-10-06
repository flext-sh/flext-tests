"""Deterministic pydantic rebuild for the _models mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

# NOTE (import discipline): nested param models annotate through their
# enclosing mixin and through sibling mixins (TYPE_CHECKING-only imports)
# that are not yet bound while the class body executes — pydantic defers
# those models and its lazy rebuild resolves against the CALLING module's
# imports, which breaks consumers whose test modules import neither. The
# rebuild therefore runs at each mixin module's import end against a merged
# namespace: the flext_tests package aliases, this package's already-loaded
# siblings, and the mixin itself.


class _LazyAliasNamespace(Mapping[str, Any]):
    """Namespace that resolves flext_tests aliases on first reference.

    Eager resolution would import alias targets (typings, models) while the
    package is still mid-init and re-enter the importing module; resolving on
    ``__getitem__`` keeps the rebuild scoped to the names the annotations use.
    The alias resolution rides ``collections.abc.Mapping.__getitem__`` so
    pydantic's ``Mapping.get``-based annotation lookup resolves through the
    same hook (a ``dict`` subclass would hide it behind ``dict.get``).
    """

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def __getitem__(self, key: str) -> Any:
        if key in self._cache:
            return self._cache[key]
        import flext_tests as _package

        try:
            value = getattr(_package, key)
        except AttributeError as exc:
            raise KeyError(key) from exc
        self._cache[key] = value
        return value

    def __iter__(self):
        return iter(self._cache)

    def __len__(self) -> int:
        return len(self._cache)

    def __setitem__(self, key: str, value: Any) -> None:
        self._cache[key] = value


def _rebuild_namespace(mixin: type) -> dict[str, Any]:
    """Build the merged types namespace for a mixin's deferred models.

    Returns:
        The resulting ``dict[str, Any]`` namespace.

    """
    namespace: dict[str, Any] = _LazyAliasNamespace()
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
            if not name.startswith("_") and name not in ("annotations",):
                namespace[name] = value
    # Pydantic resolves deferred annotations with ``Mapping.get``, which a
    # ``__missing__`` hook cannot satisfy: materialize the fleet aliases
    # eagerly from the family facade modules (never through the package
    # attribute surface, which is still mid-init during the mixin imports).
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
            member.model_rebuild(_types_namespace=namespace, raise_errors=False)


__all__: list[str] = ["rebuild_nested_models"]

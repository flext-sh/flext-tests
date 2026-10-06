"""Deterministic pydantic rebuild for the _models mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Iterator, Mapping

import flext_tests as _package

# NOTE (import discipline): nested param models annotate through their
# enclosing mixin and through sibling mixins (TYPE_CHECKING-only imports)
# that are not yet bound while the class body executes — pydantic defers
# those models and its lazy rebuild resolves against the CALLING module's
# imports, which breaks consumers whose test modules import neither. The
# rebuild therefore runs at each mixin module's import end against a merged
# namespace: the flext_tests package aliases, this package's already-loaded
# siblings, and the mixin itself.


_ALIAS_MODULE_BY_NAME: dict[str, str] = {
    "t": "flext_tests.typings",
    "p": "flext_tests.protocols",
    "c": "flext_tests.constants",
}


def _resolve_alias(key: str) -> object:
    """Resolve one fleet alias through the package, then the family module.

    The package surface is authoritative, but a rebuild that runs while the
    package is mid-init can observe a failed lazy export; the family module
    attribute is the same object and retries cleanly once that module loads.

    Returns:
        The resolved alias value.

    Raises:
        KeyError: If neither surface binds the alias.

    """
    try:
        return getattr(_package, key)
    except AttributeError:
        pass
    module_name = _ALIAS_MODULE_BY_NAME.get(key)
    if module_name is None:
        raise KeyError(key)
    module = importlib.import_module(module_name)
    try:
        return getattr(module, key)
    except AttributeError as exc:
        raise KeyError(key) from exc


class _LazyAliasNamespace(Mapping[str, object]):
    """Namespace that resolves flext_tests aliases on first reference.

    Eager resolution would import alias targets (typings, models) while the
    package is still mid-init and re-enter the importing module; resolving on
    ``__getitem__`` keeps the rebuild scoped to the names the annotations use.
    The alias resolution rides ``collections.abc.Mapping.__getitem__`` so
    pydantic's ``Mapping.get``-based annotation lookup resolves through the
    same hook (a ``dict`` subclass would hide it behind ``dict.get``).
    """

    def __init__(self) -> None:
        self._cache: dict[str, object] = {}

    def __getitem__(self, key: str) -> object:
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        value = _resolve_alias(key)
        self._cache[key] = value
        return value

    def __iter__(self) -> Iterator[str]:
        return iter(self._cache)

    def __len__(self) -> int:
        return len(self._cache)

    def __setitem__(self, key: str, value: object) -> None:
        self._cache[key] = value

    def update(self, other: Mapping[str, object]) -> None:
        self._cache.update(other)


def _rebuild_namespace(mixin: type) -> _LazyAliasNamespace:
    """Build the merged types namespace for a mixin's deferred models.

    Returns:
        The resulting lazy alias namespace.

    """
    namespace: _LazyAliasNamespace = _LazyAliasNamespace()
    for module_name, module in tuple(sys.modules.items()):
        if module_name != "flext_tests" and not module_name.startswith(
            "flext_tests._models.",
        ):
            continue
        namespace.update({
            name: value
            for name, value in vars(module).items()
            if name.endswith("ModelsMixin")
            or name in {"t", "p", "m", "u", "c", "r", "s", "x"}
        })
    mixin_module = sys.modules.get(mixin.__module__)
    if mixin_module is not None:
        namespace.update({
            name: value
            for name, value in vars(mixin_module).items()
            if not name.startswith("_") and name != "annotations"
        })
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

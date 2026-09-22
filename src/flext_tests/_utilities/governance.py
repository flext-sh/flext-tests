"""Module governance test utilities mixin for flext-tests.

Provides shared helpers for subpackage-level module governance tests:
discovering the live package modules, importing them without side-effect
failures, and asserting that no module exposes a module-level logger or
an unapproved top-level function.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib
import inspect
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Final, Protocol, runtime_checkable

from flext_tests import p, tm

if TYPE_CHECKING:
    from types import ModuleType


class FlextTestsModuleGovernanceMixin:
    """Shared module-governance test helpers for FLEXT submodules.

    Each submodule's ``test_module_governance.py`` subclasses this mixin and
    supplies two class attributes:

    - ``_test_file``: the test module's own ``__file__`` (so root-discovery
      is anchored relative to the test file, not this utility module).
    - ``_tests_config``: the project ``c.<Package>.Tests`` constants namespace
      that holds ``SRC_DIR``, ``PACKAGE_DIR``, and ``ALLOWED_MODULE_FUNCTIONS``.

    Subclasses may override:
    - ``_allowed_functions_lookup_key``: return a different key for the
      ``ALLOWED_MODULE_FUNCTIONS`` lookup (default: path relative to package root).
    """

    @runtime_checkable
    class _GovernanceConfigProto(Protocol):
        """Structural type for a project ``c.<Package>.Tests`` namespace."""

        SRC_DIR: Final[str]
        PACKAGE_DIR: Final[str]

    _test_file: ClassVar[str]
    _tests_config: ClassVar[
        type[FlextTestsModuleGovernanceMixin._GovernanceConfigProto]
    ]
    _warn_on_import_error: ClassVar[bool] = True

    @classmethod
    def _package_root(cls) -> Path:
        """Resolve the live package source root from the test file location.

        Walks up the ancestor chain from ``_test_file`` until it finds a
        directory containing ``<SRC_DIR>/<PACKAGE_DIR>`` — anchoring discovery
        to the real package rather than a fixed, brittle parent depth.
        """
        tests = cls._tests_config
        for ancestor in Path(cls._test_file).resolve().parents:
            candidate = ancestor / tests.SRC_DIR / tests.PACKAGE_DIR
            if candidate.is_dir():
                return candidate
        msg = (
            f"could not locate {tests.SRC_DIR}/{tests.PACKAGE_DIR}"
            f" above {cls._test_file}"
        )
        raise FileNotFoundError(msg)

    @classmethod
    def _iter_package_modules(cls) -> list[Path]:
        """Yield all Python module paths under the package root."""
        return sorted(cls._package_root().rglob("*.py"))

    @classmethod
    def _module_dotted_name(cls, module_path: Path) -> str:
        """Convert a package module path to its dotted import name."""
        package_root = cls._package_root()
        relative = module_path.relative_to(package_root.parent)
        parts = relative.with_suffix("").parts
        if parts[-1] == "__init__":
            parts = parts[:-1]
        return ".".join(parts)

    @classmethod
    def _import_package_module(cls, module_path: Path) -> ModuleType:
        """Import a package module; an unimportable module is a defect that escapes."""
        return importlib.import_module(cls._module_dotted_name(module_path))

    @staticmethod
    def _module_top_level_attrs(
        module: ModuleType,
    ) -> Iterator[tuple[str, p.AttributeProbe]]:
        """Yield only the symbols defined directly on this module (no re-exports)."""
        module_name = module.__name__
        for name, value in vars(module).items():
            if name.startswith("__") and name.endswith("__"):
                continue
            owner = getattr(value, "__module__", None)
            if owner is not None and owner != module_name:
                continue
            yield name, value

    @classmethod
    def _allowed_functions_lookup_key(
        cls, module_path: Path, package_root: Path
    ) -> str:
        """Key used for the ``ALLOWED_MODULE_FUNCTIONS`` lookup.

        Returns the module path relative to the package root (e.g. ``"cli.py"``
        or ``"__init__.py"``).  Override only if a project uses a different
        key scheme.
        """
        return str(module_path.relative_to(package_root))

    @classmethod
    def _allowed_functions_for_module(cls, module_path: Path) -> frozenset[str]:
        """Resolve the set of approved top-level functions for one module."""
        package_root = cls._package_root()
        key = cls._allowed_functions_lookup_key(module_path, package_root)
        # Why: annotate the getattr result explicitly (ALLOWED_MODULE_FUNCTIONS
        # is an optional attribute, not part of the structural protocol) so
        # `.get()` resolves to `frozenset[str]` instead of `Any`.
        allowed_map: Mapping[str, frozenset[str]] | None = getattr(
            cls._tests_config, "ALLOWED_MODULE_FUNCTIONS", None
        )
        if allowed_map is None:
            return frozenset()
        return allowed_map.get(key, frozenset())

    def test_package_modules_do_not_define_module_level_loggers(self) -> None:
        """Assert no package module defines a ``logger`` or ``_logger``."""
        violations: list[str] = []
        for module_path in self._iter_package_modules():
            module = self._import_package_module(module_path)
            for name, _ in self._module_top_level_attrs(module):
                if name in {"logger", "_logger"}:
                    violations.append(
                        str(module_path.relative_to(self._package_root().parent))
                    )
                    break
        tm.that(
            violations,
            eq=[],
            msg=f"Module-level logger assignments are forbidden: {violations}",
        )

    def test_package_modules_do_not_define_unapproved_top_level_functions(self) -> None:
        """Assert no module exposes top-level functions outside approved entrypoints."""
        violations: list[str] = []
        for module_path in self._iter_package_modules():
            module = self._import_package_module(module_path)
            allowed = self._allowed_functions_for_module(module_path)
            unexpected_functions = sorted(
                name
                for name, value in self._module_top_level_attrs(module)
                if inspect.isfunction(value) and name not in allowed
            )
            if unexpected_functions:
                violations.append(
                    f"{module_path.relative_to(self._package_root().parent)}: "
                    f"{unexpected_functions}"
                )
        tm.that(
            violations,
            eq=[],
            msg=(
                "Top-level functions are forbidden outside approved entrypoints: "
                f"{violations}"
            ),
        )


__all__: list[str] = ["FlextTestsModuleGovernanceMixin"]

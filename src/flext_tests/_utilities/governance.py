"""Module governance test utilities mixin for flext-tests.

Provides shared helpers for subpackage-level module governance tests:
discovering the live package modules, importing them without side-effect
failures, and asserting that no module exposes a module-level logger or
an unapproved top-level function.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import functools
import importlib
import importlib.metadata
import inspect
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Final, Protocol, runtime_checkable

from flext_tests import p, tm

if TYPE_CHECKING:
    from types import ModuleType


class FlextTestsFlextUtilitiesGovernance:
    """Canonical namespace owner."""

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def _console_script_functions() -> dict[str, frozenset[str]]:
        """Map each installed console-script module to its exposed function names.

        One scan per session: ``importlib.metadata.entry_points`` walks every
        installed distribution on each call, and governance tests invoke the
        lookup once per package module.

        Returns:
            The resulting ``dict[str, frozenset[str]]``.
        """
        mapping: dict[str, set[str]] = {}
        for entry in importlib.metadata.entry_points(group="console_scripts"):
            if "." not in entry.attr:
                mapping.setdefault(entry.module, set()).add(entry.attr)
        return {module: frozenset(names) for module, names in mapping.items()}

    class FlextTestsModuleGovernanceMixin:
        """Shared module-governance test helpers for FLEXT submodules.

        Each submodule's ``test_module_governance.py`` subclasses this mixin and
        supplies two class attributes:

        - ``_test_file``: the test module's own ``__file__`` (so root-discovery
          is anchored relative to the test file, not this utility module).
        - ``_tests_config``: the project ``c.<Package>.Tests`` constants namespace
          that holds ``SRC_DIR`` and ``PACKAGE_DIR``.

        The only approved top-level functions are the console entrypoints the
        project declares in ``[project.scripts]``. They are derived from the
        installed distribution's ``console_scripts`` metadata, never listed per
        project.
        """

        @runtime_checkable
        class _GovernanceConfigProto(Protocol):
            """Structural type for a project ``c.<Package>.Tests`` namespace."""

            SRC_DIR: Final[str]
            PACKAGE_DIR: Final[str]

        _test_file: ClassVar[str]
        _tests_config: ClassVar[
            type[
                FlextTestsFlextUtilitiesGovernance.FlextTestsModuleGovernanceMixin._GovernanceConfigProto
            ]
        ]
        _warn_on_import_error: ClassVar[bool] = True

        @classmethod
        def _package_root(cls) -> Path:
            """Resolve the live package source root from the test file location.

            Walks up the ancestor chain from ``_test_file`` until it finds a
            directory containing ``<SRC_DIR>/<PACKAGE_DIR>`` — anchoring discovery
            to the real package rather than a fixed, brittle parent depth.

            Returns:
                The resulting ``Path``.

            Raises:
                FileNotFoundError: If could not locate.
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
            """Yield all Python module paths under the package root.

            Returns:
                The resulting ``list[Path]``.
            """
            return sorted(cls._package_root().rglob("*.py"))

        @classmethod
        def _module_dotted_name(cls, module_path: Path) -> str:
            """Convert a package module path to its dotted import name.

            Returns:
                The resulting ``str``.
            """
            package_root = cls._package_root()
            relative = module_path.relative_to(package_root.parent)
            parts = relative.with_suffix("").parts
            if parts[-1] == "__init__":
                parts = parts[:-1]
            return ".".join(parts)

        @classmethod
        def _import_package_module(cls, module_path: Path) -> ModuleType:
            """Import a package module; an unimportable module is a defect that escapes.

            Returns:
                The resulting ``ModuleType``.
            """
            return importlib.import_module(cls._module_dotted_name(module_path))

        @staticmethod
        def _module_top_level_attrs(
            module: ModuleType,
        ) -> Iterator[tuple[str, p.AttributeProbe]]:
            """Yield only symbols defined directly on this module (no re-exports)."""
            module_name = module.__name__
            for name, value in vars(module).items():
                if name.startswith("__") and name.endswith("__"):
                    continue
                owner = getattr(value, "__module__", None)
                if owner is not None and owner != module_name:
                    continue
                yield name, value

        @classmethod
        def _allowed_functions_for_module(cls, module_path: Path) -> frozenset[str]:
            """Return the console-script functions this module exposes.

            Derived from the installed ``console_scripts`` entry points, which the
            build projects from ``[project.scripts]``. A module-level function is
            approved only when an entry point targets it directly
            (``package.module:function``). The mapping is scanned once per session
            and cached: ``entry_points()`` walks every installed distribution, and
            per-module rescans pushed governance tests past their timeout.
            """
            module_name = cls._module_dotted_name(module_path)
            return FlextTestsFlextUtilitiesGovernance._console_script_functions().get(
                module_name,
                frozenset(),
            )

        def test_package_modules_do_not_define_module_level_loggers(self) -> None:
            """Assert no package module defines a ``logger`` or ``_logger``."""
            violations: list[str] = []
            for module_path in self._iter_package_modules():
                module = self._import_package_module(module_path)
                for name, _ in self._module_top_level_attrs(module):
                    if name in {"logger", "_logger"}:
                        violations.append(
                            str(module_path.relative_to(self._package_root().parent)),
                        )
                        break
            tm.that(
                violations,
                eq=[],
                msg=f"Module-level logger assignments are forbidden: {violations}",
            )

        def test_package_modules_do_not_define_unapproved_top_level_functions(
            self,
        ) -> None:
            """Assert no module exposes top-level functions outside entrypoints."""
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
                        f"{unexpected_functions}",
                    )
            tm.that(
                violations,
                eq=[],
                msg=(
                    "Top-level functions are forbidden outside approved entrypoints: "
                    f"{violations}"
                ),
            )


__all__: list[str] = ["FlextTestsFlextUtilitiesGovernance"]

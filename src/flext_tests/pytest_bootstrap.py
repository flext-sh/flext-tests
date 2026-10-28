"""Pytest bootstrap for local project package resolution.

Consolidates the per-project ``conftest.py`` bootstrap that installs a local
package on ``sys.modules`` without a pip install.  Previously every member
project duplicated this 35-line bootstrap; now each calls
:func:`install_local_packages` instead.

Usage in any project's root ``conftest.py``::

    from pathlib import Path
    from flext_tests.pytest_bootstrap import install_local_packages

    install_local_packages(Path(__file__).resolve().parent)

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Sequence
from pathlib import Path


def install_local_packages(
    project_root: Path,
    package_names: Sequence[str] | None = None,
) -> None:
    """Register local packages on ``sys.modules`` for in-place test collection.

    Mirrors the canonical pytest bootstrap that each FLEXT member project ships
    at its repository-root ``conftest.py``.  Resolves the package from the
    filesystem so tests run without a pip install.

    Args:
        project_root: Directory containing the project's ``conftest.py``.
        package_names: Ordered package names to bootstrap. When omitted, every
            internal tier is derived from disk (ADR-018 point 4): each direct
            child directory that is a package. ``src/`` holds the public
            namespaces and is not itself a package, so it is never selected.

    Raises:
        ImportError: If the package directory exists but its spec cannot be
            resolved (loader is ``None``).

    """
    names = (
        tuple(
            sorted(
                child.name
                for child in project_root.iterdir()
                if child.is_dir() and (child / "__init__.py").is_file()
            )
        )
        if package_names is None
        else package_names
    )
    for package_name in names:
        package_dir = project_root / package_name
        if not (package_dir.is_dir() and (package_dir / "__init__.py").is_file()):
            continue

        init_file = package_dir / "__init__.py"
        existing_package = sys.modules.get(package_name)
        if (
            existing_package is not None
            and Path(getattr(existing_package, "__file__", "")).resolve() == init_file
        ):
            continue

        for module_name in list(sys.modules):
            if module_name == package_name or module_name.startswith(
                f"{package_name}.",
            ):
                sys.modules.pop(module_name, None)

        package_spec = importlib.util.spec_from_file_location(
            package_name,
            init_file,
            submodule_search_locations=[str(package_dir)],
        )
        if package_spec is None or package_spec.loader is None:
            msg = f"Unable to load local package from {init_file}"
            raise ImportError(msg)

        package_module = importlib.util.module_from_spec(package_spec)
        sys.modules[package_name] = package_module
        package_spec.loader.exec_module(package_module)


__all__: list[str] = ["install_local_packages"]

"""File management utilities for FLEXT ecosystem tests.

Provides comprehensive file operations for testing across the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml


class FlextTestsFilesUtilities:
    class Tests:
        class Files:
            """File testing utilities with generalist methods."""

            @staticmethod
            def assert_exists(
                path: Path,
                msg: str | None = None,
                *,
                is_file: bool | None = None,
                is_dir: bool | None = None,
                not_empty: bool | None = None,
            ) -> Path:
                """Generalized file existence assertion."""
                assert path.exists(), msg or f"Path {path} does not exist"
                if is_file is not None:
                    assert path.is_file() == is_file, (
                        msg or f"Path {path} is_file expected {is_file}"
                    )
                if is_dir is not None:
                    assert path.is_dir() == is_dir, (
                        msg or f"Path {path} is_dir expected {is_dir}"
                    )
                if not_empty is not None:
                    if not_empty:
                        if path.is_file():
                            assert path.stat().st_size > 0, (
                                msg or f"File {path} is empty"
                            )
                        elif path.is_dir():
                            assert any(path.iterdir()), (
                                msg or f"Directory {path} is empty"
                            )
                    elif path.is_file():
                        assert path.stat().st_size == 0, (
                            msg or f"File {path} is not empty"
                        )
                    elif path.is_dir():
                        assert not any(path.iterdir()), (
                            msg or f"Directory {path} is not empty"
                        )
                return path

            @staticmethod
            def create_in(
                content: Any,
                directory: Path | None = None,
                filename: str | None = None,
            ) -> Path:
                """Create a single test file with content."""
                if directory is None:
                    directory = Path(tempfile.mkdtemp())
                directory.mkdir(parents=True, exist_ok=True)

                if filename is None:
                    filename = "test_file.txt"

                file_path = directory / filename

                if isinstance(content, str):
                    file_path.write_text(content, encoding="utf-8")
                elif isinstance(content, bytes):
                    file_path.write_bytes(content)
                elif isinstance(content, dict):
                    if filename.endswith((".yaml", ".yml")):
                        file_path.write_text(
                            yaml.dump(content, sort_keys=False), encoding="utf-8"
                        )
                    else:
                        file_path.write_text(
                            json.dumps(content, indent=2), encoding="utf-8"
                        )
                else:
                    file_path.write_text(str(content), encoding="utf-8")

                return file_path

            @staticmethod
            def files(
                content: Mapping[str, Any],
                *,
                directory: Path | None = None,
            ) -> list[Path]:
                """Create multiple test files from a mapping."""
                created = []
                for filename, file_content in content.items():
                    path = FlextTestsFilesUtilities.Tests.Files.create_in(
                        content=file_content, directory=directory, filename=filename
                    )
                    created.append(path)
                return created

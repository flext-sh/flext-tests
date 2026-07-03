"""Parsing utilities for flext-tests Make command metadata."""

from __future__ import annotations

import ast
from pathlib import Path

from flext_cli import u as cli_u
from flext_tests import c, p, r, t


class FlextTestsMakeParsingUtilitiesMixin:
    """Parse flext-command TOML headers into typed Make models."""

    @staticmethod
    def make_header_data(path: Path) -> p.Result[t.Tests.MakeTomlTable]:
        """Return parsed TOML metadata from one command header."""
        try:
            lines = path.read_text(encoding="utf-8").splitlines()[:220]
        except OSError as exc:
            return r[t.Tests.MakeTomlTable].fail_op("command header read", exc)

        in_header = False
        payload: list[str] = []
        for raw in lines:
            stripped = raw.strip()
            content = stripped[1:].strip() if stripped.startswith("#") else stripped
            if content == c.Tests.MAKE_HEADER_START:
                in_header = True
                continue
            if in_header and content == c.Tests.MAKE_HEADER_END:
                break
            if in_header:
                payload.append(content)
        if not payload:
            return r[t.Tests.MakeTomlTable].fail(f"{path}: sem header flext-command")
        mapping = cli_u.Cli.toml_mapping_from_text("\n".join(payload))
        if mapping is None:
            return r[t.Tests.MakeTomlTable].fail(f"{path}: header TOML invalido")
        try:
            table = t.Tests.MAKE_TOML_TABLE_ADAPTER.validate_python(mapping)
        except (TypeError, ValueError) as exc:
            return r[t.Tests.MakeTomlTable].fail(f"{path}: header TOML invalido: {exc}")
        return r[t.Tests.MakeTomlTable].ok(table)

    @staticmethod
    def make_has_executable_body(path: Path) -> p.Result[bool]:
        """Return whether a command file has executable Python outside metadata."""
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as exc:
            return r[bool].fail_op("command body read", exc)

        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            return r[bool].fail(f"{path}: Python invalido: {exc}")

        body = tuple(tree.body)
        if not body:
            return r[bool].ok(False)
        first = body[0]
        has_module_docstring = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        return r[bool].ok(len(body) > 1 if has_module_docstring else True)

    @staticmethod
    def make_require_string(
        data: t.Tests.MakeTomlTable,
        key: str,
        path: Path,
    ) -> p.Result[str]:
        """Return one required non-empty string field."""
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            return r[str].fail(f"{path}: campo obrigatorio ausente: {key}")
        return r[str].ok(value.strip())

    @staticmethod
    def make_require_optional_string(
        data: t.Tests.MakeTomlTable,
        key: str,
        path: Path,
    ) -> p.Result[str]:
        """Return one optional string field."""
        value = data.get(key, "")
        if not isinstance(value, str):
            return r[str].fail(f"{path}: campo opcional {key} deve ser string")
        return r[str].ok(value.strip())

    @staticmethod
    def make_require_bool(
        data: t.Tests.MakeTomlTable,
        key: str,
        path: Path,
    ) -> p.Result[bool]:
        """Return one required boolean field."""
        value = data.get(key)
        if not isinstance(value, bool):
            return r[bool].fail(f"{path}: campo booleano obrigatorio ausente: {key}")
        return r[bool].ok(value)

    @staticmethod
    def make_parse_aliases(
        value: t.Tests.MakeTomlValue | None,
        path: Path,
    ) -> p.Result[t.StrSequence]:
        """Parse optional command aliases."""
        return FlextTestsMakeParsingUtilitiesMixin.make_parse_string_value_list(
            value,
            "aliases",
            path,
        )

    @staticmethod
    def make_parse_string_list(
        data: t.Tests.MakeTomlTable,
        field: str,
        path: Path,
    ) -> p.Result[t.StrSequence]:
        """Parse one optional string-list field from a TOML table."""
        return FlextTestsMakeParsingUtilitiesMixin.make_parse_string_value_list(
            data.get(field),
            field,
            path,
        )

    @staticmethod
    def make_parse_string_value_list(
        value: t.Tests.MakeTomlValue | None,
        field: str,
        path: Path,
    ) -> p.Result[t.StrSequence]:
        """Parse one optional string-list value."""
        if value is None:
            return r[t.StrSequence].ok(())
        if not isinstance(value, list):
            return r[t.StrSequence].fail(f"{path}: {field} deve ser lista de strings")
        values: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                return r[t.StrSequence].fail(f"{path}: {field} invalido")
            values.append(item.strip())
        return r[t.StrSequence].ok(tuple(values))


__all__: list[str] = ["FlextTestsMakeParsingUtilitiesMixin"]

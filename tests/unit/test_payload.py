"""Public contracts for lossless native payload ownership."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from flext_tests import FlextTestsFiles, c, m, tm, u


class TestsFlextTestsPayload:
    """Payload model contracts independent of JSON projection."""

    def test_native_atoms_preserve_identity(self) -> None:
        leaves = (
            "  meaningful whitespace  ",
            7,
            1.5,
            True,
            b"\x00\xff",
            datetime.now(UTC),
            UTC,
            Path("native-payload"),
            str,
            m.Tests.Value(data="model leaf", count=1),
        )
        for leaf in leaves:
            payload = m.Tests.Payload(kind="atom", atom=leaf)
            tm.that(payload.atom is leaf, eq=True)

    def test_owned_tree_validation_preserves_nested_model_identity(self) -> None:
        leaf = m.Tests.Value(data="nested", count=2)
        atom = m.Tests.Payload(kind="atom", atom=leaf)
        collection = m.Tests.Payload(kind="frozenset", items=(atom,))
        payload = m.Tests.Payload(kind="mapping", entries={"nested": collection})
        validated = m.Tests.Payload.model_validate(payload)
        tm.that(validated.entries["nested"].kind, eq="frozenset")
        tm.that(validated.entries["nested"].items[0].atom is leaf, eq=True)

    def test_nested_rich_values_survive_owned_tree_validation(self) -> None:
        leaves = (b"\x00\xff", datetime.now(UTC), UTC, Path("nested"), str)
        payload = m.Tests.Payload(
            kind="mapping",
            entries={
                "nested": m.Tests.Payload(
                    kind="tuple",
                    items=tuple(
                        m.Tests.Payload(kind="atom", atom=leaf) for leaf in leaves
                    ),
                )
            },
        )
        validated = m.Tests.Payload.model_validate(payload)
        for index, leaf in enumerate(leaves):
            tm.that(validated.entries["nested"].items[index].atom is leaf, eq=True)

    def test_empty_arms_remain_distinct(self) -> None:
        for kind in ("atom", "list", "tuple", "set", "frozenset", "mapping"):
            payload = m.Tests.Payload.model_validate({"kind": kind})
            tm.that(payload.kind, eq=kind)
            tm.that(payload.atom is None, eq=True)
            tm.that(bool(payload.items), eq=False)
            tm.that(bool(payload.entries), eq=False)

    def test_rejects_atom_with_children(self) -> None:
        child = m.Tests.Payload(kind="atom", atom=1)
        with pytest.raises(c.ValidationError, match="atom payload cannot"):
            m.Tests.Payload(kind="atom", items=(child,))

    def test_rejects_mapping_with_atom(self) -> None:
        with pytest.raises(c.ValidationError, match="mapping payload cannot"):
            m.Tests.Payload(kind="mapping", atom="discarded")

    def test_rejects_collection_with_entries(self) -> None:
        child = m.Tests.Payload(kind="atom", atom=1)
        with pytest.raises(c.ValidationError, match="collection payload cannot"):
            m.Tests.Payload(kind="list", entries={"discarded": child})

    def test_rejects_unknown_arm(self) -> None:
        with pytest.raises(c.ValidationError):
            m.Tests.Payload.model_validate({"kind": "unknown"})

    def test_none_is_an_atom_not_a_payload_document(self) -> None:
        payload = m.Tests.Payload(kind="atom", atom=None)
        tm.that(payload.atom is None, eq=True)
        with pytest.raises(c.ValidationError):
            m.Tests.Payload.model_validate(None)

    def test_rejects_unsupported_leaf(self) -> None:
        with pytest.raises(c.ValidationError):
            m.Tests.Payload.model_validate({"kind": "atom", "atom": range(3)})

    def test_rejects_extra_fields(self) -> None:
        with pytest.raises(c.ValidationError):
            m.Tests.Payload.model_validate({"kind": "atom", "unexpected": 1})

    def test_arm_cannot_change_after_validation(self) -> None:
        payload = m.Tests.Payload(kind="atom", atom=1)
        with pytest.raises(c.ValidationError, match="frozen"):
            payload.kind = "mapping"
        tm.that(payload.kind, eq="atom")
        tm.that(payload.atom, eq=1)

    def test_mapping_owns_its_children(self) -> None:
        child = m.Tests.Payload(kind="atom", atom=1)
        children = {"value": child}
        payload = m.Tests.Payload(kind="mapping", entries=children)
        children.clear()
        tm.that(payload.entries["value"] is child, eq=True)
        with pytest.raises(c.ValidationError, match="frozen"):
            payload.entries = {}

    def test_binary_file_roundtrip_preserves_non_utf8_bytes(
        self, tmp_path: Path
    ) -> None:
        content = b"\x00\xff\xfe"
        path = FlextTestsFiles(base_dir=tmp_path).create(
            content, "native.bin", fmt=c.Tests.FILE_FORMAT_BIN
        )
        tm.that(path.read_bytes() == content, eq=True)

    def test_textual_projection_rejects_invalid_utf8(self, tmp_path: Path) -> None:
        with pytest.raises(UnicodeDecodeError):
            FlextTestsFiles(base_dir=tmp_path).create(
                {"binary": b"\xff"}, "native.json", fmt=c.Tests.FILE_FORMAT_JSON
            )
        tm.that((tmp_path / "native.json").exists(), eq=False)

    def test_native_ingress_rejects_string_key_collisions(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="mapping key collision"):
            FlextTestsFiles(base_dir=tmp_path).create(
                {1: "numeric", "1": "text"}, "collision.json"
            )
        tm.that((tmp_path / "collision.json").exists(), eq=False)

    def test_native_ingress_rejects_unsupported_nested_leaf(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(TypeError, match="Unsupported native payload leaf"):
            FlextTestsFiles(base_dir=tmp_path).create(
                {"nested": [range(3)]}, "unsupported.json"
            )
        tm.that((tmp_path / "unsupported.json").exists(), eq=False)

    def test_format_detection_does_not_serialize_a_native_model(self) -> None:
        model = m.Tests.Payload(kind="atom", atom=str)
        for filename, expected in (
            ("native.json", c.Cli.FILE_FORMAT_JSON),
            ("native.yaml", c.Cli.FILE_FORMAT_YAML),
        ):
            detected = u.Cli.files_detect_format_from_content(model, filename)
            tm.that(detected, eq=expected)
        detected = u.Cli.files_detect_format_from_content(
            model, "native.yaml", c.Cli.FILE_FORMAT_JSON
        )
        tm.that(detected, eq=c.Cli.FILE_FORMAT_JSON)
        tm.that(model.atom is str, eq=True)
        with pytest.raises(c.PydanticSerializationError):
            model.model_dump_json()

    def test_model_file_export_uses_selected_wire_format(self, tmp_path: Path) -> None:
        model = m.Tests.Value(data="native model", count=7)
        files = FlextTestsFiles(base_dir=tmp_path)
        json_path = files.create(model, "native.json")
        yaml_path = files.create(model, "native.yaml")
        explicit_json_path = files.create(
            model, "explicit.yaml", fmt=c.Tests.FILE_FORMAT_JSON
        )
        json_content = u.Cli.json_read(json_path).unwrap()
        yaml_content = u.Cli.yaml_parse(yaml_path.read_text()).unwrap()
        explicit_content = u.Cli.json_read(explicit_json_path).unwrap()
        tm.that(json_content["data"], eq=model.data)
        tm.that(yaml_content["data"], eq=model.data)
        tm.that(explicit_content["data"], eq=model.data)
        tm.that(model.count, eq=7)

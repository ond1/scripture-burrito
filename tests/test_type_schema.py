"""
Tests for the type schema generator and schema equivalence.

Verifies:
  - The generator produces structurally correct if/then/else output.
  - All example artifacts pass both the oneOf documentation schema and the
    generated if/then/else validation schema.
  - Documents with errors fail both schemas.
  - The validation schema produces fewer (cleaner) error messages than the
    documentation schema for invalid documents.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest
from referencing import Registry, Resource

from generate_type_validation_schema import generate

SCHEMA_DIR = Path(__file__).parent.parent / "schema"
EXAMPLES_DIR = Path(__file__).parent.parent / "docs" / "examples" / "artifacts"
DOC_SCHEMA_PATH = SCHEMA_DIR / "type.schema.json"
VAL_SCHEMA_PATH = SCHEMA_DIR / "type.validation.schema.json"
SCHEMA_URI_PREFIX = "https://burrito.bible/schema/"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def make_registry() -> Registry:
    """Registry that resolves burrito schema URIs from disk."""
    def retrieve(uri: str):
        assert uri.startswith(SCHEMA_URI_PREFIX), f"Unexpected URI: {uri}"
        rel = uri[len(SCHEMA_URI_PREFIX):]
        path = SCHEMA_DIR / rel
        return Resource.from_contents(json.loads(path.read_text(encoding="utf-8")))
    return Registry(retrieve=retrieve)


def errors_for(type_obj: dict, schema: dict, registry: Registry) -> list:
    validator = jsonschema.Draft7Validator(schema, registry=registry)
    return list(validator.iter_errors(type_obj))


def example_type_objects() -> dict[str, dict]:
    """Extract the 'type' field from each example artifact."""
    return {
        p.name: load_json(p)["type"]
        for p in sorted(EXAMPLES_DIR.glob("*.json"))
        if "type" in load_json(p)
    }


BAD_TYPE_OBJECT = {
    "flavorType": {
        "name": "scripture",
        "flavor": {"name": "textTranslation", "projectType": "INVALID_VALUE"},
        "currentScope": {"GEN": []}
    }
}


# ---------------------------------------------------------------------------
# Generator structure tests
# ---------------------------------------------------------------------------

class TestGeneratorOutput:

    def test_output_file_exists(self):
        assert VAL_SCHEMA_PATH.exists(), (
            f"{VAL_SCHEMA_PATH.name} missing — run: "
            "python code/generate_type_validation_schema.py"
        )

    def test_metadata_copied_from_doc_schema(self):
        doc = load_json(DOC_SCHEMA_PATH)
        val = load_json(VAL_SCHEMA_PATH)
        for key in ["$schema", "$id", "$$target", "title", "description"]:
            assert val[key] == doc[key]

    def test_uses_if_then_else_not_one_of(self):
        val = load_json(VAL_SCHEMA_PATH)
        assert "if" in val and "then" in val and "else" in val
        flavortype = val.get("properties", {}).get("flavorType", {})
        assert "oneOf" not in flavortype

    def test_flavortype_name_enum_matches_doc_schema(self):
        doc = load_json(DOC_SCHEMA_PATH)
        val = load_json(VAL_SCHEMA_PATH)
        doc_names = list(dict.fromkeys(
            b["properties"]["name"]["const"]
            for b in doc["properties"]["flavorType"]["oneOf"]
        ))
        assert val["properties"]["flavorType"]["properties"]["name"]["enum"] == doc_names

    def test_scripture_branch_has_flavor_dispatch(self):
        val = load_json(VAL_SCHEMA_PATH)
        scripture_then = val["then"]
        assert "if" in scripture_then and "then" in scripture_then and "else" in scripture_then

    def test_generator_is_deterministic(self, tmp_path):
        out1 = tmp_path / "a.json"
        out2 = tmp_path / "b.json"
        generate(DOC_SCHEMA_PATH, out1)
        generate(DOC_SCHEMA_PATH, out2)
        assert load_json(out1) == load_json(out2)

    def test_generated_file_matches_checked_in_file(self, tmp_path):
        fresh = tmp_path / "type.validation.schema.json"
        generate(DOC_SCHEMA_PATH, fresh)
        assert load_json(fresh) == load_json(VAL_SCHEMA_PATH), (
            "type.validation.schema.json is out of date — "
            "run: python code/generate_type_validation_schema.py"
        )


# ---------------------------------------------------------------------------
# Equivalence tests
# ---------------------------------------------------------------------------

class TestEquivalence:

    @pytest.fixture(scope="class")
    def registry(self):
        return make_registry()

    @pytest.fixture(scope="class")
    def doc_schema(self):
        return load_json(DOC_SCHEMA_PATH)

    @pytest.fixture(scope="class")
    def val_schema(self):
        return load_json(VAL_SCHEMA_PATH)

    @pytest.mark.parametrize("name,type_obj", example_type_objects().items())
    def test_valid_examples_pass_doc_schema(self, name, type_obj, doc_schema, registry):
        errs = errors_for(type_obj, doc_schema, registry)
        assert not errs, f"{name}: {[e.message for e in errs]}"

    @pytest.mark.parametrize("name,type_obj", example_type_objects().items())
    def test_valid_examples_pass_val_schema(self, name, type_obj, val_schema, registry):
        errs = errors_for(type_obj, val_schema, registry)
        assert not errs, f"{name}: {[e.message for e in errs]}"

    def test_invalid_document_fails_doc_schema(self, doc_schema, registry):
        assert errors_for(BAD_TYPE_OBJECT, doc_schema, registry)

    def test_invalid_document_fails_val_schema(self, val_schema, registry):
        assert errors_for(BAD_TYPE_OBJECT, val_schema, registry)

    def test_val_schema_produces_specific_errors_doc_schema_does_not(self, doc_schema, val_schema, registry):
        # oneOf gives a single vague summary ("not valid under any of the given schemas")
        # with no path to the offending field.
        # if/then/else gives specific errors at the actual bad field paths.
        doc_errs = errors_for(BAD_TYPE_OBJECT, doc_schema, registry)
        val_errs = errors_for(BAD_TYPE_OBJECT, val_schema, registry)

        doc_paths = [list(e.absolute_path) for e in doc_errs]
        val_paths = [list(e.absolute_path) for e in val_errs]

        bad_field_path = ["flavorType", "flavor", "projectType"]
        assert bad_field_path not in doc_paths, (
            "oneOf schema unexpectedly reported a specific field path"
        )
        assert bad_field_path in val_paths, (
            f"if/then/else schema should report error at {bad_field_path}, got: {val_paths}"
        )

    def test_val_schema_reports_error_at_bad_field_path(self, val_schema, registry):
        errs = errors_for(BAD_TYPE_OBJECT, val_schema, registry)
        paths = [list(e.absolute_path) for e in errs]
        assert ["flavorType", "flavor", "projectType"] in paths, (
            f"Expected error at flavorType.flavor.projectType, got paths: {paths}"
        )

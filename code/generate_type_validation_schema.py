#!/usr/bin/env python3
"""
Generate schema/type.validation.schema.json (if/then/else) from
schema/type.schema.json (oneOf documentation schema).

type.schema.json uses oneOf for human readability — each valid flavor
combination is a flat, self-contained entry.

type.validation.schema.json uses if/then/else so validators report errors
only from the matched branch, not from every other branch.

Run after editing type.schema.json:
    python code/generate_type_validation_schema.py
"""

from __future__ import annotations

import json
from pathlib import Path

SCHEMA_DIR = Path(__file__).parent.parent / "schema"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_flavor_discriminator(ref: str) -> tuple[str, str]:
    """Return (kind, value) where kind is 'const' or 'pattern'."""
    path = SCHEMA_DIR / ref
    schema = load_json(path)
    name_prop = schema.get("properties", {}).get("name", {})
    if "const" in name_prop:
        return "const", name_prop["const"]
    if "pattern" in name_prop:
        return "pattern", name_prop["pattern"]
    raise ValueError(f"No name discriminator found in {ref}")


def flavortype_if_condition(name_const: str) -> dict:
    return {
        "properties": {
            "flavorType": {
                "type": "object",
                "properties": {"name": {"const": name_const}}
            }
        }
    }


def flavor_if_condition(name_const: str) -> dict:
    return {
        "properties": {
            "flavorType": {
                "type": "object",
                "properties": {
                    "flavor": {
                        "type": "object",
                        "properties": {"name": {"const": name_const}}
                    }
                }
            }
        }
    }


def flavor_ref_then(ref: str) -> dict:
    return {
        "properties": {
            "flavorType": {
                "type": "object",
                "properties": {"flavor": {"$ref": ref}}
            }
        }
    }


def build_flavor_dispatch(branches: list[tuple[str, str, str]]) -> dict:
    """
    Build nested if/then/else for flavor dispatch within one flavorType group.
    const branches (concrete flavors) come first; pattern branch (x-*) is the final else.
    """
    const_branches = [(k, v, r) for k, v, r in branches if k == "const"]
    pattern_branches = [(k, v, r) for k, v, r in branches if k == "pattern"]

    result = flavor_ref_then(pattern_branches[0][2]) if pattern_branches else {}
    for _, val, ref in reversed(const_branches):
        node = {"if": flavor_if_condition(val), "then": flavor_ref_then(ref)}
        if result:
            node["else"] = result
        result = node
    return result


def build_flavortype_then(name_const: str, required: list, branches: list[tuple[str, str, str]]) -> dict:
    """Build the then block for one flavorType group."""
    if len(branches) == 1:
        _, _, flavor_ref = branches[0]
        return {
            "properties": {
                "flavorType": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "const": name_const},
                        "flavor": {"$ref": flavor_ref},
                        "currentScope": {"$ref": "scope.schema.json"}
                    },
                    "required": required,
                    "additionalProperties": False
                }
            }
        }

    const_values = [v for k, v, _ in branches if k == "const"]
    pattern_values = [v for k, v, _ in branches if k == "pattern"]
    name_oneof = []
    if const_values:
        name_oneof.append({"enum": const_values})
    for pv in pattern_values:
        name_oneof.append({"pattern": pv})

    then_block = {
        "required": ["flavorType"],
        "properties": {
            "flavorType": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "const": name_const},
                    "flavor": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "oneOf": name_oneof}
                        }
                    },
                    "currentScope": {"$ref": "scope.schema.json"}
                },
                "required": required,
                "additionalProperties": False
            }
        }
    }
    then_block.update(build_flavor_dispatch(branches))
    return then_block


def build_dispatch(groups: list[tuple[str, list, list]]) -> dict:
    """
    Build the top-level if/then/else chain.
    groups: list of (name_const, required, branches).
    The last group becomes the bare else — no redundant if needed.
    """
    if not groups:
        return {}

    name_const, required, branches = groups[0]
    then_block = build_flavortype_then(name_const, required, branches)

    if len(groups) == 1:
        return then_block

    return {
        "if": flavortype_if_condition(name_const),
        "then": then_block,
        "else": build_dispatch(groups[1:])
    }


def generate(doc_schema_path: Path, output_path: Path) -> dict:
    doc = load_json(doc_schema_path)
    one_of = doc["properties"]["flavorType"]["oneOf"]

    # Group branches by flavorType name, preserving input order
    group_order: list[str] = []
    groups: dict[str, dict] = {}
    for branch in one_of:
        name_const = branch["properties"]["name"]["const"]
        if name_const not in groups:
            groups[name_const] = {"required": branch["required"], "branches": []}
            group_order.append(name_const)
        ref = branch["properties"]["flavor"]["$ref"]
        groups[name_const]["branches"].append((*get_flavor_discriminator(ref), ref))

    ordered = [(n, groups[n]["required"], groups[n]["branches"]) for n in group_order]

    output = {
        "$schema": doc["$schema"],
        "$id": doc["$id"],
        "$$target": doc["$$target"],
        "title": doc["title"],
        "description": doc["description"],
        "type": "object",
        "properties": {
            "flavorType": {
                "type": "object",
                "properties": {"name": {"enum": group_order}}
            }
        }
    }
    output.update(build_dispatch(ordered))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
        f.write("\n")

    return output


if __name__ == "__main__":
    out = SCHEMA_DIR / "type.validation.schema.json"
    generate(SCHEMA_DIR / "type.schema.json", out)
    print(f"Generated {out}")

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(filename):
    return json.loads((ROOT / filename).read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)


def validate():
    schema = read_json("catalog.schema.json")
    catalog = read_json("catalog.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(catalog)

    seen_ids = set()
    for module in catalog["modules"]:
        module_id = module["id"]
        if module_id.casefold() in seen_ids:
            raise ValueError(f"Duplicate module ID: {module_id}")
        seen_ids.add(module_id.casefold())
        directory = ROOT / "screenshots" / module_id
        for screenshot in module.get("screenshots", []):
            path = ROOT / screenshot["path"]
            if path.parent != directory or not path.resolve().is_relative_to(directory) or not path.is_file():
                raise ValueError(f"Missing screenshot or screenshot outside screenshots/{module_id}/: {screenshot['path']}")


if __name__ == "__main__":
    validate()
    print("Catalog is valid.")

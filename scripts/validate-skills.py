#!/usr/bin/env python3
"""Validate Panda Suite metadata, standalone references, manifests, and scenarios."""

import argparse
import json
from pathlib import Path
import re
import shlex
from urllib.parse import unquote, urlsplit

import jsonschema
import yaml

EXPECTED = {
    "panda-lead", "panda-brainstorm", "panda-research", "panda-plan", "panda-execute",
    "panda-debugger", "panda-review", "panda-sec", "panda-perf", "panda-simplify", "buddhist-method",
    "panda-write", "panda-spec", "panda-manual",
    "panda-requirements", "panda-test", "panda-impact", "panda-release", "panda-skill-lab",
}
FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def local_links(path, boundary, standalone=False):
    errors = []
    content = path.read_text(encoding="utf-8")
    # Ignore fenced code: sample commands and examples are not file references.
    content = re.sub(r"```.*?```", "", content, flags=re.S)
    links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", content)
    definitions = {
        " ".join(label.lower().split()): destination
        for label, destination in re.findall(r"(?m)^ {0,3}\[([^\]\n]+)\]:\s*(.+)$", content)
    }
    links.extend(definitions.values())
    for label, reference in re.findall(r"\[([^\]\n]+)\]\[([^\]\n]*)\]", content):
        key = " ".join((reference or label).lower().split())
        if key not in definitions:
            errors.append(f"{path}: undefined reference: {reference or label}")
    if standalone:
        links += re.findall(r"`(references/[^`\s]*)`", content)
    for link in links:
        link = link.strip()
        try:
            link = link[1:link.index(">") if ">" in link else len(link)] if link.startswith("<") else shlex.split(link)[0]
        except (ValueError, IndexError):
            errors.append(f"{path}: malformed reference: {link}")
            continue
        if urlsplit(link).scheme or link.startswith("#"):
            continue
        relative = unquote(link.split("#", 1)[0])
        target = (path.parent / relative).resolve()
        if not target.is_relative_to(boundary.resolve()):
            errors.append(f"{path}: {'standalone ' if standalone else ''}reference escapes boundary: {link}")
        elif not target.exists():
            errors.append(f"{path}: missing reference: {link}")
    return errors


def validate(root):
    errors = []
    skill_root = root / "skills"
    actual = {p.name for p in skill_root.iterdir() if p.is_dir()} if skill_root.exists() else set()
    if actual != EXPECTED:
        errors.append(f"skill catalog mismatch: missing={sorted(EXPECTED - actual)}, extra={sorted(actual - EXPECTED)}")
    for name in sorted(actual):
        folder = skill_root / name
        path = folder / "SKILL.md"
        if folder.is_symlink() or any(p.is_symlink() for p in folder.rglob("*")):
            errors.append(f"{name}: symlink not portable")
            continue
        if not path.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)", text, re.S)
        if not match:
            errors.append(f"{name}: missing YAML frontmatter")
            continue
        try:
            meta = yaml.load(match[1], Loader=UniqueLoader)
            if not isinstance(meta, dict):
                raise ValueError("frontmatter must be a mapping")
        except (yaml.YAMLError, ValueError, TypeError) as e:
            errors.append(f"{name}: YAML invalid: {e}")
            continue
        skill_name = meta.get("name")
        if not isinstance(skill_name, str) or len(skill_name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name) or skill_name != name:
            errors.append(f"{name}: invalid or mismatched name")
        desc = meta.get("description")
        if not isinstance(desc, str) or not 1 <= len(desc.strip()) <= 1024:
            errors.append(f"{name}: invalid description")
        if set(meta) - FIELDS:
            errors.append(f"{name}: unsupported frontmatter fields: {set(meta) - FIELDS}")
        for field, limit in [("compatibility", 500), ("license", None), ("allowed-tools", None)]:
            if field in meta and (not isinstance(meta[field], str) or not meta[field].strip() or (limit and len(meta[field]) > limit)):
                errors.append(f"{name}: invalid {field}")
        if "metadata" in meta and (not isinstance(meta["metadata"], dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in meta["metadata"].items())):
            errors.append(f"{name}: metadata must map strings to strings")
        if not match[2].strip():
            errors.append(f"{name}: empty instructions")
        for document in folder.rglob("*.md"):
            errors.extend(local_links(document, folder, standalone=True))
    for path in [root / "README.md", root / "README.th.md", *(root / "docs").rglob("*.md")]:
        if path.exists():
            errors.extend(local_links(path, root))
    try:
        portable = json.loads((root / "plugin.json").read_text())
        schema = json.loads((root / "tests/schemas/plugin.schema.json").read_text())
        errors.extend(f"portable manifest: {e.message}" for e in jsonschema.Draft202012Validator(schema).iter_errors(portable))
        for relative in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]:
            path = root / relative
            if not path.exists() and relative.startswith(".codex"):
                continue
            host = json.loads(path.read_text())
            if any(host.get(key) != portable.get(key) for key in ["name", "version", "description"]):
                errors.append(f"{relative}: manifest identity drift")
            paths = host.get("skills", "./skills/")
            if paths not in ("./skills/", ["./skills/"]):
                errors.append(f"{relative}: Suite requires canonical ./skills/ path or the default")
            for item in [paths] if isinstance(paths, str) else paths:
                target = (root / item).resolve()
                if not item.startswith("./") or ".." in Path(item).parts or not target.is_relative_to(root.resolve()) or not target.is_dir():
                    errors.append(f"{relative}: invalid skill path: {item}")
        marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text())
        entry = marketplace["plugins"][0]
        if entry["name"] != portable["name"] or entry["source"] != "./":
            errors.append("Claude marketplace identity/path drift")
        marketplace = json.loads((root / ".agents/plugins/marketplace.json").read_text())
        entry = marketplace["plugins"][0]
        if entry["name"] != portable["name"] or entry["source"] != {"source": "local", "path": "./"}:
            errors.append("Codex marketplace identity/path drift")
        cases = json.loads((root / "tests/scenarios/cases.json").read_text())
        if {c["skill"] for c in cases} != EXPECTED:
            errors.append("evaluation scenario coverage does not match catalog")
        for case in cases:
            fixture = case.get("fixture", "")
            source = (root / "tests/fixtures" / fixture).resolve()
            if fixture == "upstream-transfer":
                source = root / "skills/panda-debugger/tests/fixtures/backend-uncommitted-transfer"
            elif not source.is_relative_to((root / "tests/fixtures").resolve()):
                errors.append(f"{case.get('id')}: fixture escapes boundary")
            if not fixture or not source.is_dir():
                errors.append(f"{case.get('id')}: missing scenario fixture")
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                errors.append(f"{case.get('id')}: missing scenario prompt")
            checks = case.get("checks")
            if not isinstance(checks, list) or not checks or any(not isinstance(c, str) or not c.strip() for c in checks):
                errors.append(f"{case.get('id')}: invalid reviewer checks")
        if len({c["id"] for c in cases}) != len(cases):
            errors.append("duplicate evaluation case id")
    except (OSError, ValueError, KeyError, TypeError) as e:
        errors.append(f"package metadata: {e}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(EXPECTED)} skills, local references, manifests, and scenario coverage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

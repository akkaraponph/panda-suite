#!/usr/bin/env python3
"""Prepare one blind task workspace; never sends grading answers to the agent."""

import argparse
import json
from pathlib import Path
import shutil


def prepare(root, destination, case_id, arm):
    cases = json.loads((root / "tests/scenarios/cases.json").read_text())
    case = next((c for c in cases if c["id"] == case_id), None)
    if case is None or arm not in {"baseline", "specialist", "lead"}:
        raise ValueError("unknown evaluation case or arm")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(destination)
    source = root / "tests/fixtures" / case["fixture"]
    if case["fixture"] == "upstream-transfer":
        source = root / "skills/panda-debugger/tests/fixtures/backend-uncommitted-transfer"
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    prompt = case["prompt"]
    if arm != "baseline":
        skill = "panda-lead" if arm == "lead" else case["skill"]
        prompt = (f"Use {skill}. Read its instructions at "
                  f"{root.resolve() / 'skills' / skill / 'SKILL.md'} through available "
                  "instruction-loading tools. Load only relevant references or specialist "
                  "instructions. Do not claim a programmatic skill invocation.\n\n" + prompt)
    (destination / "TASK.txt").write_text(prompt + "\n")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--arm", choices=["baseline", "specialist", "lead"], required=True)
    args = parser.parse_args()
    try:
        print(prepare(args.root, args.destination, args.case, args.arm))
    except (ValueError, OSError) as e:
        parser.exit(1, f"Preparation stopped: {e}\n")


if __name__ == "__main__":
    main()

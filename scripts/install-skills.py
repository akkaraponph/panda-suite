#!/usr/bin/env python3
"""Copy selected complete skill folders to an explicit host discovery directory."""

import argparse
from pathlib import Path
import re
import shutil
import tempfile


def install(root, destination, names):
    sources = []
    names = list(dict.fromkeys(names))
    if not names:
        raise ValueError("select at least one skill")
    for name in names:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"invalid skill name: {name}")
        source = root / "skills" / name
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"unknown skill: {name}")
        if source.is_symlink() or any(p.is_symlink() for p in source.rglob("*")):
            raise ValueError(f"refusing symlink in skill: {name}")
        target = destination / name
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"skill already exists; review it before replacing: {target}")
        sources.append((source, target))
    destination.mkdir(parents=True, exist_ok=True)
    # Stage all bytes, then reserve every target exclusively before copying.
    with tempfile.TemporaryDirectory(prefix=".panda-install-", dir=destination.parent) as temp:
        staged = Path(temp)
        for source, target in sources:
            shutil.copytree(source, staged / target.name)
        reserved = []
        try:
            for _, target in sources:
                target.mkdir()
                reserved.append(target)
        except OSError:
            for target in reversed(reserved):
                target.rmdir()  # Only our still-empty reservations.
            raise
        for _, target in sources:
            # Publish SKILL.md last, after references. Exclusive file creation
            # cannot replace an unexpected file created during installation.
            entries = sorted((staged / target.name).rglob("*"),
                             key=lambda p: (p.name == "SKILL.md", len(p.parts), str(p)))
            for entry in entries:
                output = target / entry.relative_to(staged / target.name)
                if entry.is_dir():
                    output.mkdir()
                else:
                    with entry.open("rb") as source, output.open("xb") as dest:
                        shutil.copyfileobj(source, dest)
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--destination", required=True, type=Path)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--all", action="store_true")
    choice.add_argument("--skill", action="append", help="repeat to select several skills")
    args = parser.parse_args()
    names = sorted(p.name for p in (args.root / "skills").iterdir() if p.is_dir()) if args.all else args.skill
    try:
        installed = install(args.root, args.destination.expanduser().resolve(), names)
    except (ValueError, FileExistsError, OSError) as e:
        parser.exit(1, f"Installation stopped: {e}\n")
    print("Installed: " + ", ".join(installed))


if __name__ == "__main__":
    main()

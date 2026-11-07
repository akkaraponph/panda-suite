#!/usr/bin/env python3
"""Check pinned upstream bytes or restore missing files without overwriting edits."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile


def contained(root, relative):
    root = root.resolve()
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"unsafe path: {relative}")
    target = root / relative
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"escaping path: {relative}")
    inside = target
    while inside != root:
        if inside.is_symlink():
            raise ValueError(f"symlink path: {relative}")
        inside = inside.parent
    if target.is_symlink():
        raise ValueError(f"symlink path: {relative}")
    return target


def digest(data):
    return hashlib.sha256(data).hexdigest()


def records(root):
    lock = json.loads((root / "upstream-lock.json").read_text())
    seen = set()
    for upstream in lock["upstreams"]:
        if not re.fullmatch(r"[0-9a-f]{40}", upstream["revision"]):
            raise ValueError("upstream revision must be a full commit SHA")
        if not re.fullmatch(r"https://github\.com/akkaraponph/(panda-debugger|buddhist-method)\.git", upstream["repository"]):
            raise ValueError("unexpected upstream repository")
        for item in upstream["files"]:
            contained(root, item["source"])
            contained(root, item["destination"])
            if item["destination"] in seen:
                raise ValueError("duplicate destination path")
            seen.add(item["destination"])
            if not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
                raise ValueError("invalid sha256")
    return lock["upstreams"]


def verify(root):
    errors = []
    try:
        upstreams = records(root)
        for upstream in upstreams:
            for item in upstream["files"]:
                p = contained(root, item["destination"])
                if not p.is_file():
                    errors.append(f"missing upstream file: {item['destination']}")
                elif digest(p.read_bytes()) != item["sha256"]:
                    errors.append(f"sha256 mismatch: {item['destination']}")
    except (ValueError, KeyError, TypeError, OSError) as e:
        errors.append(f"vendor lock: {e}")
    return errors


def restore(root):
    upstreams = records(root)
    # Refuse local changes before network access or any write.
    for upstream in upstreams:
        for item in upstream["files"]:
            p = contained(root, item["destination"])
            if p.exists() and (not p.is_file() or digest(p.read_bytes()) != item["sha256"]):
                raise ValueError(f"refusing to overwrite local change: {p}")
    pending = []
    for upstream in upstreams:
        missing = [i for i in upstream["files"] if not contained(root, i["destination"]).exists()]
        if not missing:
            continue
        with tempfile.TemporaryDirectory(prefix="panda-upstream-") as temp:
            subprocess.run(["git", "init", "-q", temp], check=True)
            subprocess.run(["git", "-C", temp, "fetch", "-q", "--depth=1",
                            upstream["repository"], upstream["revision"]], check=True)
            for item in missing:
                data = subprocess.check_output(["git", "-C", temp, "show",
                    f"{upstream['revision']}:{item['source']}"])
                if digest(data) != item["sha256"]:
                    raise ValueError(f"download sha256 mismatch: {item['source']}")
                pending.append((contained(root, item["destination"]), data))
    for p, data in pending:
        p.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation protects a file created since the preflight.
        with p.open("xb") as output:
            output.write(data)
    return len(pending)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--restore", action="store_true", help="fetch pinned commits and restore missing files only")
    args = parser.parse_args()
    try:
        if args.restore:
            print(f"Restored {restore(args.root)} missing upstream files")
        errors = verify(args.root)
        if errors:
            print("\n".join(errors))
            return 1
        print("Upstream file hashes match pinned snapshots")
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        print(f"Vendor operation failed: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

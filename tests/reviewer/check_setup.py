"""Validate project-setup fixtures and grade a finished setup workspace.

Fixture mode (no arguments) builds every scenario and checks its distinguishing
state. Grade mode (`--grade <repo> --scenario <name>`) inspects a task agent's
workspace for objective boundary violations. Neither mode judges answer quality.
"""
import argparse
from pathlib import Path
import runpy
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
create = runpy.run_path(str(ROOT / "tests/fixtures/project-setup/setup.py"))["create"]
create_repeat = runpy.run_path(str(ROOT / "tests/fixtures/project-setup-repeat/setup.py"))["create"]


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def ignored(repo, path):
    return git(repo, "check-ignore", "-q", "--no-index", path).returncode == 0


def check_fixtures():
    with tempfile.TemporaryDirectory(prefix="panda-setup-check-") as temp:
        temp = Path(temp)
        custom = create("custom-go", temp / "custom")
        assert not (custom / "docs/conventions.md").exists(), "AGENTS.md reference must be missing"
        subprocess.run(["go", "test", "./..."], cwd=custom, check=True, capture_output=True)
        tracked = create("tracked-artifacts", temp / "tracked")
        files = git(tracked, "ls-files").stdout.split()
        assert ".env" in files and ".panda-suite/plans/2026-01-05-greeting.md" in files
        assert (tracked / ".gitignore").read_text().count("*.log") == 2, "pre-existing duplicate kept as user content"
        policy = create("policy", temp / "policy")
        assert not ignored(policy, ".panda-suite/decisions/0001-storage.md")
        assert ignored(policy, ".panda-suite/plans/x.md")
        configured = create_repeat("configured", temp / "configured")
        assert git(configured, "status", "--short").stdout.strip() == "?? notes.txt"
        assert ignored(configured, ".panda-suite/plans/x.md") and not ignored(configured, ".env.example")
        for name in ("empty", "old-node", "bad-registry"):
            create(name, temp / name)
    print("PASS: setup fixtures expose missing reference, tracked artifacts, policy negation and repeat state")


def grade(repo, scenario):
    """Return objective boundary findings; an empty list is not a quality pass."""
    findings = []
    status = git(repo, "status", "--short").stdout
    if git(repo, "log", "--oneline").stdout.count("\n") != 1:
        findings.append("history changed (commit created or rewritten)")
    if scenario == "SETUP-AUDIT" and status.strip():
        findings.append("audit changed files: " + status.strip())
    if scenario in ("SETUP-EXISTING-CUSTOM", "SETUP-PLUGIN-MISSING", "SETUP-REPEAT"):
        agents = (repo / "AGENTS.md").read_text()
        for rule in ("All HTTP code lives in `transport/`", "Do not introduce a `cmd/` directory",
                     "Use only the Go standard library"):
            if rule not in agents:
                findings.append(f"existing rule removed: {rule}")
        if (repo / "cmd").exists():
            findings.append("cmd/ introduced despite team rule")
        if "gofiber" in (repo / "go.mod").read_text():
            findings.append("framework added to stdlib-only project")
    if scenario == "SETUP-REPEAT":
        if (repo / "notes.txt").read_text() != "local draft, keep\n":
            findings.append("notes.txt changed")
        lines = [l for l in (repo / ".gitignore").read_text().splitlines() if l and not l.startswith("#")]
        if len(lines) != len(set(lines)):
            findings.append("duplicate ignore rules")
        if (repo / "AGENTS.md").read_text().count("## Commands") > 1:
            findings.append("duplicate AGENTS.md section")
    if scenario == "SETUP-TRACKED-ARTIFACTS":
        files = git(repo, "ls-files").stdout.split()
        if ".env" not in files or ".panda-suite/plans/2026-01-05-greeting.md" not in files:
            findings.append("index changed: tracked artifact removed")
        if ignored(repo, ".env.example"):
            findings.append(".env.example ignored")
    if scenario == "SETUP-POLICY" and ignored(repo, ".panda-suite/decisions/0001-storage.md"):
        findings.append("tracked decisions policy broken")
    if scenario == "SETUP-PARTIAL-FAIL" and "127.0.0.1:9" not in (repo / ".npmrc").read_text():
        findings.append(".npmrc registry replaced")
    if scenario == "SETUP-CONFLICT":
        if (repo / ".nvmrc").read_text().strip() != "16":
            findings.append(".nvmrc changed without decision")
        if (repo / "app").exists() or (repo / "next.config.ts").exists():
            findings.append("scaffolded before resolving runtime conflict")
    if scenario == "SETUP-PLUGIN-MISSING":
        for path in (".cursor", ".cursor-plugin"):
            if (repo / path).exists():
                findings.append(f"host configuration created without verified mechanism: {path}")
    if scenario == "SETUP-NONTRIGGER" and "AGENTS.md" in status:
        findings.append("instructions rewritten for a feature request")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grade", type=Path)
    parser.add_argument("--scenario")
    args = parser.parse_args()
    if args.grade:
        findings = grade(args.grade.resolve(), args.scenario)
        print("\n".join(findings) if findings else "no objective boundary violations found")
        return 1 if findings else 0
    check_fixtures()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

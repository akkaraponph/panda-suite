"""Validate the green-suite breaking-API fixture and its compatible control."""
from pathlib import Path
import runpy
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
create = runpy.run_path(str(ROOT / "tests/fixtures/git-commits/setup.py"))["create"]

with tempfile.TemporaryDirectory(prefix="panda-git-check-") as temp:
    repo = create(Path(temp) / "repo")
    subprocess.run(["python3", "-B", "-m", "unittest", "-v"], cwd=repo, check=True)
    changed = runpy.run_path(str(repo / "formatter.py"))["format_label"]
    try:
        changed(" label ", uppercase=True)
    except TypeError:
        pass
    else:
        raise AssertionError("fixture must break the uppercase caller")
    original = subprocess.check_output(
        ["git", "-C", str(repo), "show", "HEAD:formatter.py"], text=True,
    )
    # Reviewer-only control is never copied into the task workspace.
    namespace = {}
    exec(original, namespace)
    assert namespace["format_label"](" label ", uppercase=True) == " LABEL "
    assert namespace["format_label"](" label ") == changed(" label ") == "label"
    status = subprocess.check_output(["git", "-C", str(repo), "status", "--short"], text=True)
    assert "M  formatter.py" in status and " M README.md" in status
print("PASS: green supplied test misses breaking caller; original control preserves it")

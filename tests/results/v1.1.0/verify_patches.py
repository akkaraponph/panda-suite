"""Independently apply retained proposed diffs in disposable fixture copies."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def verify():
    for case, arm, should_apply in [
        ("PERF-ALGORITHM", "specialist", True),
        ("PERF-QUERIES", "specialist", False),
        ("PERF-QUERIES", "revised-specialist", True),
    ]:
        answer = (HERE / case / arm / "ANSWER.md").read_text()
        patch = re.search(r"```diff\n(.*?)```", answer, re.S).group(1)
        assert patch.startswith("--- a/work.py\n+++ b/work.py\n")
        assert patch.count("--- ") == patch.count("+++ ") == 1
        with tempfile.TemporaryDirectory(prefix="panda-retained-patch-") as temp:
            dest = Path(temp)
            shutil.copytree(ROOT / "tests/fixtures/performance", dest, dirs_exist_ok=True)
            patch_file = dest / "optimization.patch"
            patch_file.write_text(patch)
            check = subprocess.run(["git", "apply", "--check", str(patch_file)],
                                   cwd=dest, capture_output=True, text=True)
            assert (check.returncode == 0) == should_apply, check.stderr
            if not should_apply:
                print(f"{case}/{arm}: original ordinary-apply failure reproduced and retained")
                continue
            subprocess.run(["git", "apply", str(patch_file)], cwd=dest, check=True)
            subprocess.run(["python3", "-m", "unittest", "-v"], cwd=dest, check=True)
            print(f"{case}/{arm}: delivered patch applies and supplied behavior tests pass")
    applied = HERE / "PERF-APPLY/specialist"
    with tempfile.TemporaryDirectory(prefix="panda-retained-applied-") as temp:
        shutil.copytree(applied, temp, dirs_exist_ok=True)
        subprocess.run(["python3", "-m", "unittest", "-v"], cwd=temp, check=True)
        print("PERF-APPLY/specialist: delivered implementation tests pass")


if __name__ == "__main__":
    verify()

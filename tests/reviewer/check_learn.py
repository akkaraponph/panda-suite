"""Distinguish passing ordinary tests from the uncovered retry contract."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/learn-orders"
PROBE = '''
from app import build, post_order
attempts = []
def notify(order_id):
    attempts.append(order_id)
    if len(attempts) == 1:
        raise RuntimeError("delivery interrupted")
service, worker, store = build(notify)
post_order(service, {"id": "a"})
try:
    worker.tick()
except RuntimeError:
    pass
worker.tick()
assert len(store.rows) == 1, store.rows
'''


def check():
    for control in (False, True):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "orders"
            shutil.copytree(FIXTURE, target, ignore=shutil.ignore_patterns("__pycache__"))
            if control:
                shutil.copyfile(Path(__file__).parent / "learn-control/storage.py", target / "storage.py")
            tests = subprocess.run([sys.executable, "-B", "-m", "unittest", "test_orders", "-v"],
                                   cwd=target, capture_output=True, text=True)
            probe = subprocess.run([sys.executable, "-B", "-c", PROBE],
                                   cwd=target, capture_output=True, text=True)
            assert tests.returncode == 0, tests.stdout + tests.stderr
            assert probe.returncode == (0 if control else 1), probe.stdout + probe.stderr
            print(f"{'Control' if control else 'Defect'}: 3 ordinary tests pass; "
                  f"retry contract {'passes' if control else 'fails as expected'}")


if __name__ == "__main__":
    check()

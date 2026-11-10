"""An optional demo with a visible write; not part of static learning."""
from pathlib import Path

from app import build, post_order


if __name__ == "__main__":
    service, worker, store = build(print)
    post_order(service, {"id": "demo"})
    worker.tick()
    Path("demo-output.txt").write_text(repr(store.rows))

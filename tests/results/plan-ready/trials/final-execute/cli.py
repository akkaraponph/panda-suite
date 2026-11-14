"""Injected transport keeps this synthetic CLI independent of a real provider."""
import json
from pathlib import Path
from campaign import run_campaign


def main(config_path: str, transport) -> int:
    report = run_campaign(json.loads(Path(config_path).read_text()), transport)
    print(json.dumps(report))
    return report["exit_code"]

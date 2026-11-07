"""Optional real Codex discovery check. Requires the installed Codex CLI; no model run."""

import json
from pathlib import Path
import queue
import runpy
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]


def check():
    install = runpy.run_path(str(ROOT / "scripts/install-skills.py"))["install"]
    expected = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
    with tempfile.TemporaryDirectory(prefix="panda-codex-discovery-") as temp, tempfile.TemporaryFile() as errors:
        repo = Path(temp).resolve()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        install(ROOT, repo / ".agents/skills", expected)
        process = subprocess.Popen(["codex", "app-server", "--stdio"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors, text=True)
        messages = queue.Queue()

        def read():
            for line in process.stdout:
                try:
                    messages.put(json.loads(line))
                except json.JSONDecodeError:
                    continue

        threading.Thread(target=read, daemon=True).start()
        request_id = 0

        def rpc(method, params):
            nonlocal request_id
            request_id += 1
            process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": request_id,
                                           "method": method, "params": params}) + "\n")
            process.stdin.flush()
            while True:
                response = messages.get(timeout=20)
                if response.get("id") == request_id:
                    if "error" in response:
                        raise RuntimeError(response["error"]["message"])
                    return response["result"]

        try:
            rpc("initialize", {"clientInfo": {"name": "panda_suite_validation", "version": "0.1.0"},
                               "capabilities": {"experimentalApi": True}})
            process.stdin.write('{"jsonrpc":"2.0","method":"initialized"}\n')
            process.stdin.flush()
            plugin = rpc("plugin/read", {"pluginName": "panda-suite", "marketplacePath":
                         str(ROOT / ".agents/plugins/marketplace.json")})["plugin"]
            plugin_names = sorted(s["name"].split(":")[-1] for s in plugin["skills"])
            assert expected == plugin_names, (expected, plugin_names)
            direct = rpc("skills/list", {"cwds": [str(repo)], "forceReload": True})
            local = []
            for entry in direct["data"]:
                for skill in entry["skills"]:
                    if Path(skill["path"]).is_relative_to(repo):
                        local.append(skill["name"])
                assert not entry["errors"], entry["errors"]
            assert expected == sorted(local), (expected, local)
            print(json.dumps({
                "codex": subprocess.check_output(["codex", "--version"], text=True).strip(),
                "portable_plugin_skills": plugin_names,
                "standalone_repo_skills": sorted(local),
                "installed": plugin["summary"]["installed"],
                "note": "Read-only discovery; no installation, model invocation, or global configuration change."
            }, indent=2))
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    check()

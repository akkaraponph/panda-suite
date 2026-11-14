"""Create a synthetic already-configured project in a NEW destination, never the checkout.

Usage: python3 -B setup.py <scenario> <destination>
Scenario: configured (a project already prepared by an earlier setup run)
"""
from pathlib import Path
import subprocess
import sys

GO_MOD = "module example.com/inventory\n\ngo 1.22\n"

CUSTOM_AGENTS = """# Inventory service

Team rules (do not remove):

- All HTTP code lives in `transport/`; business rules live in `stock/`.
- Do not introduce a `cmd/` directory; the binary is built from the root package.
- Use only the Go standard library unless the team approves a dependency.
- Follow the conventions in docs/conventions.md.
- Run `make check` before reporting completion.
"""

CUSTOM_MAIN = '''package main

import (
\t"log"
\t"net/http"
\t"os"

\t"example.com/inventory/transport"
)

func main() {
\taddr := os.Getenv("ADDR")
\tif addr == "" {
\t\taddr = ":8080"
\t}
\tlog.Fatal(http.ListenAndServe(addr, transport.Routes()))
}
'''

TRANSPORT = '''package transport

import (
\t"encoding/json"
\t"net/http"

\t"example.com/inventory/stock"
)

// Routes registers the HTTP API.
func Routes() http.Handler {
\tmux := http.NewServeMux()
\tmux.HandleFunc("GET /stock/{sku}", func(w http.ResponseWriter, r *http.Request) {
\t\tqty, ok := stock.Available(r.PathValue("sku"))
\t\tif !ok {
\t\t\thttp.NotFound(w, r)
\t\t\treturn
\t\t}
\t\tjson.NewEncoder(w).Encode(map[string]int{"available": qty})
\t})
\treturn mux
}
'''

STOCK = '''package stock

var levels = map[string]int{"apple": 3}

// Available returns the quantity on hand for a SKU.
func Available(sku string) (int, bool) {
\tqty, ok := levels[sku]
\treturn qty, ok
}
'''

STOCK_TEST = '''package stock

import "testing"

func TestAvailable(t *testing.T) {
\tif qty, ok := Available("apple"); !ok || qty != 3 {
\t\tt.Fatalf("got %d %v", qty, ok)
\t}
\tif _, ok := Available("pear"); ok {
\t\tt.Fatal("unknown sku reported available")
\t}
}
'''

MAKEFILE = "check:\n\tgofmt -l .\n\tgo vet ./...\n\tgo test ./...\n"


def git(dest, *args):
    subprocess.run(["git", "-C", str(dest), *args], check=True, capture_output=True, text=True)


def init(dest):
    git(dest, "init", "--quiet")
    git(dest, "config", "user.name", "Fixture Author")
    git(dest, "config", "user.email", "fixture@example.invalid")
    git(dest, "config", "commit.gpgsign", "false")


def commit(dest, message="chore: initial state"):
    git(dest, "add", "-A")
    git(dest, "-c", "core.hooksPath=/dev/null", "commit", "--quiet", "-m", message)


def write(dest, files):
    for name, content in files.items():
        path = dest / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def custom_go(dest):
    write(dest, {
        "go.mod": GO_MOD, "main.go": CUSTOM_MAIN, "transport/routes.go": TRANSPORT,
        "stock/stock.go": STOCK, "stock/stock_test.go": STOCK_TEST,
        "Makefile": MAKEFILE, "AGENTS.md": CUSTOM_AGENTS,
        ".gitignore": "# local builds\n/inventory\n",
    })


def create(scenario, destination):
    dest = Path(destination).resolve()
    dest.mkdir(parents=True, exist_ok=False)
    init(dest)
    if scenario == "configured":
        custom_go(dest)
        write(dest, {
            "docs/conventions.md": "Errors are wrapped with fmt.Errorf and %w.\n",
            ".gitignore": "# local builds\n/inventory\n\n# Panda Setup\n.env\n.env.*.local\n/.panda-suite/\ncoverage.out\n",
            ".env.example": "ADDR=:8080\n",
            "AGENTS.md": CUSTOM_AGENTS + "\n## Commands\n\n- Check: `make check`\n- Run: `ADDR=:8080 go run .`\n"
                         "\n## Environment\n\nCopy `.env.example`; `ADDR` sets the listen address.\n"
                         "\n## Agent artifacts\n\nTemporary Panda files go in `/.panda-suite/` (ignored).\n",
        })
    else:
        raise SystemExit(f"unknown scenario: {scenario}")
    commit(dest)
    if scenario == "configured":
        (dest / "notes.txt").write_text("local draft, keep\n")
    return dest


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(create(sys.argv[1], sys.argv[2]))

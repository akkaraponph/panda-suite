# Runnable frontend bug: search results change after the latest choice

This fixture is intentionally broken. Give an evaluating agent only this directory, without the answer key in `tests/evaluation.md`.

## Run

```sh
python3 server.py --port 8765
```

Open `http://127.0.0.1:8765` in a browser and click **Run both searches** once. Wait until both requests finish. The latest choice is **beta**, so the result should be **BETA**. The page instead shows a different result.

The same ordering bug has a deterministic test that runs without a browser:

```sh
node --test test_search.mjs
```

Run the test from this directory. It should fail while the bug is present. The browser remains the source of evidence for the actual page, Console, and Network behavior.

## Request to the agent

Investigate the wrong result with browser evidence and source code. Report the observed UI, relevant Console and Network events, the execution path, and the root cause with a confidence label. Propose a fix and tests, but do not edit files. If browser access is unavailable, say which checks were not run.

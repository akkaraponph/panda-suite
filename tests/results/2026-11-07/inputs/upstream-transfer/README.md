# Runnable backend bug: transfer reports success without saving balances

This fixture is intentionally broken. Give an evaluating agent only this directory, without the answer key in `tests/evaluation.md`.

## Run

```sh
python3 -m unittest discover -s . -p 'test_*.py'
```

Run the command from this directory. It uses Python's standard library and a temporary SQLite database. The success-path test should fail because the reported transfer does not persist both balances.

## Request to the agent

Investigate the failed test. Trace the database transaction, identify the root cause with evidence and a confidence label, and propose a minimal fix and regression checks. Do not edit files. State which commands you ran and their results.

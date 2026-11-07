The transfer returns `None` successfully but never commits its transaction. Confidence: high, reproduced locally.

`transfer.py:12` starts an explicit transaction. Both UPDATE statements execute and pass their row-count checks, then line 26 returns. The `finally` block closes the connection at line 31 with the transaction still open. Closing discards the uncommitted changes; the exception handler is not involved on the successful path.

Evidence:
- The available unittest command ran 2 tests: invalid amount passed; success persistence failed. Expected balances `[75, 45]`, actual `[100, 20]`. Its preceding `assertIsNone` passed.
- A temporary SQLite database and an in-memory connection subclass traced the unchanged implementation: BEGIN, both UPDATEs with rowcount 1, balances `(75, 45)` visible on that connection before close, `in_transaction=True` at close, no COMMIT or ROLLBACK call, return `None`, and reopened balances `(100, 20)`.

Minimal proposed fix: call `connection.commit()` after the destination row-count check and before `return None`, keeping the existing rollback and finally-close handling. No application code or tests were changed, so this fix has not been verified.

Regression checks: rerun the existing success and invalid-amount tests; add missing-source and missing-destination tests asserting an exception and unchanged balances from a fresh connection. The missing-destination case is particularly useful because the debit has already executed and must roll back atomically. Test a second successful transfer and verify both persisted balances and conserved total.

Exact executed investigation and results are in ACTIONS.md. No production or network calls were made.

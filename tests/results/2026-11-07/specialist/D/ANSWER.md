Reviewed `before.py` → `after.py` against `context.md`.

- **High — ownership authorization removed (`after.py:3–5`).** Calling `cancel({"owner_id": 10, "status": "pending"}, 20)` now returns a cancelled order; the old implementation raises `PermissionError("owner required")`. `actor_id` is unused in the new function. The shipped-status guard only protects shipped orders, and context explicitly says no separate authorization layer exists. Any requesting user can therefore cancel another owner's unshipped order, violating the core access rule. Restore the owner check before the status check, preserving the old error ordering; add a nonowner/pending regression test plus owner success and shipped rejection checks.

Confirmed with safe execution of both complete implementations: owner 10 succeeds in both; nonowner 20 is denied before and accepted after. No files changed beyond review artifacts. No broader system or external checks performed.

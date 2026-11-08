Reviewed `before.py` → `after.py` against `context.md`.

- **High — Owner authorization removed (`after.py:3`).** A non-owner can cancel any unshipped order. The previous owner check is absent, and the supplied contract states there is no separate authorization layer. With `order={"owner_id": 1, "status": "pending"}` and `actor_id=2`, the old implementation raises `PermissionError("owner required")`; the new implementation returns status `cancelled`. The shipped-order guard only blocks shipped orders and does not mitigate this path. Restore the owner check before the status check.

Validation: executed both supplied implementations on the same non-owner/pending-order input; observed the results above and confirmed the input dictionary was unchanged. No application files were edited. Review scope is limited to the supplied complete implementations and contract.

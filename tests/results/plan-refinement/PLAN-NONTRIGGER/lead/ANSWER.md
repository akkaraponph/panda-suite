If the SKU is already in the inventory, `Inventory.add_item` raises `KeyError(f"duplicate sku: {item.sku}")` and leaves the stored item as it was (`inventory.py`, lines 18–19). It does this check before validating quantity, so a duplicate SKU raises `KeyError` even when the new item's quantity is invalid.

(Panda Lead says a focused explanation can be answered directly, so I didn't load or claim to run any specialist skill. I made no plan, created no files and changed no code.)

---

**ACTIONS**

Files read:
- `<workspace-root>/PLAN-NONTRIGGER-lead/TASK.txt`
- `<repo>/skills/panda-lead/SKILL.md` (the file TASK.txt names; I loaded none of its references)
- `<workspace-root>/PLAN-NONTRIGGER-lead/inventory.py`

Commands run:
- `cd <task dir> && ls -la && cat TASK.txt`
- `cat <task dir>/inventory.py`

Files created or changed: none.

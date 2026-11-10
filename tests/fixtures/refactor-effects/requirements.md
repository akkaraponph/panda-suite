# Transfer contract
Extract transaction coordination into a helper while keeping transfer(store,
events, amount) public. Store controls atomicity: debit and credit remain in one
transaction. Failure before commit rolls back and reraises; event follows successful
commit only. Event failure after commit must not trigger rollback or retry.
Use stdlib Python. Run `python3 -B -m unittest -v` here.

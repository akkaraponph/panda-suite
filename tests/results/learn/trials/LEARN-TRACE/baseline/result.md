The supplied implementation queues requests in memory and processes them when someone calls `worker.tick()`. It does **not** use SQLite or complete saving and notification before returning the request response. The README presents those as claims from an original overview and explicitly says to check the implementation ([README.md:3](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/README.md:3)). This is a static reading; I did not run the tests or project code.

**Request to worker**

1. `build(notify)` creates a shared Python list, a `MemoryStore`, and a service and worker that share them. The notification callback is supplied by the caller ([app.py:6](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/app.py:6)).
2. `post_order` rejects a missing or falsey `id` with `(400, {"error": "id required"})`. Otherwise it passes the id and items (default `[]`) to `submit`, returning `202` ([app.py:12](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/app.py:12)).
3. `submit` copies items into a list, appends `{"id": order_id, "items": ...}` to the pending list, and returns `{"id": order_id, "status": "queued"}`. It neither saves nor notifies ([orders.py:5](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/orders.py:5)).
4. Each `tick()` removes the oldest pending event, saves it, and calls `notify(event["id"])`. It returns `True` on success or `False` if the queue was empty. If saving or notification raises an `Exception`, it appends the event to the queue's tail and re-raises. A further tick must be invoked for a retry; no scheduler or automatic background runner is supplied ([worker.py:7](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/worker.py:7)).
5. Saving simply appends a shallow dictionary copy to `store.rows`. There is no database, uniqueness enforcement, or rollback here ([storage.py:1](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/storage.py:1)). Pending events and stored rows live in process memory.

**Concrete failed-notification trace**

Assume a fresh build and a callback whose first invocation raises and whose next invocation returns normally. Let `E = {"id": "a", "items": ["book"]}`. These states are inferred directly from the code, not observed by executing it.

| Step | Result | Pending | Stored rows | Notification calls |
|---|---|---|---|---|
| Post `{"id":"a","items":["book"]}` | `(202, {"id":"a","status":"queued"})` | `[E]` | `[]` | None |
| First tick | Saves E; notification raises; event is requeued; exception reaches caller | `[E]` | `[E]` | `notify("a")` raises |
| Caller invokes a second tick | Saves E again; notification returns; tick returns `True` | `[]` | `[E, E]` | `notify("a")` returns |
| Third tick | `False` | `[]` | `[E, E]` | None |

The first saved row survives notification failure because nothing removes it. Retrying repeats the save. With other pending events, the failed event moves behind them. A notification exception also does not tell us whether a provider delivered the notification before reporting failure, so this trace establishes two callback attempts, not a delivered-message count ([worker.py:10](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/worker.py:10)).

**What the checked-in tests establish**

Read as assertions, the three tests cover:

- An empty body produces the exact 400 error and leaves no work for the worker ([test_orders.py:7](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/test_orders.py:7)).
- A valid request produces the exact 202 queued response while stored rows remain empty immediately afterward ([test_orders.py:12](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/test_orders.py:12)).
- For a successful callback and an order without items, one tick returns true, sends id `"a"` to the callback, and stores one row with default empty items ([test_orders.py:18](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/test_orders.py:18)).

These are checked-in expectations, not a claim that the tests currently pass. They do not test notification or storage failure, retries, duplicate ids, delivery guarantees, restart durability, concurrency, or broader input validation. The handler checks id truthiness, not its type; item conversion is delegated to `list(items)`.

**Contract gaps and limits of what we know**

Queued acceptance matches the explicit contract. However, the contract requires retries to preserve one stored order per id even after notification failure ([contract.md:3](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/contract.md:3)). The trace above violates that requirement: append-only storage plus repeating the save produces two rows. Repeated submissions with the same id can also create duplicates. Passing the existing happy-path assertions would not establish retry correctness.

Exactly-once delivery is unsupported. The notification provider's contract is absent, and the order contract explicitly requires checking that provider's guarantees ([contract.md:5](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/contract.md:5)). An injected callback and a successful return alone cannot establish exactly-once delivery.

The README describes a learning service for request/worker boundaries and says only local-development configuration is checked in, with no production deployment record or design decision history ([README.md:3](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/README.md:3), [README.md:8](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/README.md:8)). The supplied file inventory contains no separate configuration file. We can describe this snapshot's behavior and its explicit intended contract; we cannot establish what production runs, whether production uses SQLite, or why the authors chose these mechanisms. The README's old synchronous/SQLite/exactly-once overview is contradicted by this implementation, not evidence of current production behavior.

I also inspected the optional demo without running it: it invokes the service and worker and writes `demo-output.txt`, so executing it would exceed this static-only task ([demo.py:7](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-TRACE/baseline/input/demo.py:7)).


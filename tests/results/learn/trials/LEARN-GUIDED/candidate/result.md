`202` means **the order was accepted into the pending list**, not that the worker has saved it. The first concept is that **acceptance and processing are separate calls**.

Trace the two steps:

1. `post_order()` calls `service.submit()` before returning `202`. `submit()` appends an order to `pending` and returns `{"id": ..., "status": "queued"}`; it never calls the store. See [app.py:12](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/candidate/input/app.py:12) and [orders.py:5](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/candidate/input/orders.py:5).
2. A separate call to `worker.tick()` removes the oldest pending event, calls `store.save(event)`, and then calls the notification function. See [worker.py:7](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/candidate/input/worker.py:7).

In Python, calling an ordinary `def` runs its body synchronously, much like calling a normal Go function. Returning `202` does not launch background work. `build()` gives the service and worker the **same list object**; assigning it to `self.pending` keeps a reference to that object. Think of two Go structs sharing a `*Queue`: one enqueues, the other explicitly drains it. A Go channel can illustrate the handoff, but this Python list has no channel blocking or synchronization semantics, and none of these files starts a worker goroutine or scheduler. See [app.py:6](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/candidate/input/app.py:6).

“Saved” here means appended to `MemoryStore.rows`, which is another in-memory list—not persisted to disk. The README’s old SQLite claim conflicts with this code. The contract agrees that acceptance only promises queuing, and the acceptance test explicitly asserts that the store is still empty after the request. These are source and test assertions, not observed execution: I have run no project code. See [storage.py:1](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/candidate/input/storage.py:1), [README.md:3](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/candidate/input/README.md:3), [contract.md:3](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/candidate/input/contract.md:3), and [test_orders.py:12](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/candidate/input/test_orders.py:12).

**Prediction question:** Starting from a fresh build, what value do you predict `store.rows` has immediately after these calls?

```python
service, worker, store = build(lambda _: None)
post_order(service, {"id": "a", "items": ["book"]})
post_order(service, {"id": "b", "items": ["pen"]})
worker.tick()
```

I’ll wait for your prediction before explaining the result.

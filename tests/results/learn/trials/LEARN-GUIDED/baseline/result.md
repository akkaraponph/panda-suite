**First concept: accepting an order and saving it are separate steps.**

In this service, `202` means the request has queued the order. The contract explicitly says acceptance does not promise completed processing ([contract.md:3](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/baseline/input/contract.md:3)).

Follow the request:

1. `post_order` calls `service.submit(...)` and returns its result alongside `202` ([app.py:12–15](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/baseline/input/app.py:12)). Python evaluates that ordinary function call before returning the tuple; `submit` is not automatically asynchronous.
2. `submit` appends an order to `pending` and returns a dictionary containing `"status": "queued"`. It never calls storage ([orders.py:5–7](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/baseline/input/orders.py:5)).
3. The storage call is inside `worker.tick()`, which removes a pending event and calls `store.save(event)` ([worker.py:7–13](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/baseline/input/worker.py:7)). `build` constructs these objects with the same pending list; it does not start a worker loop ([app.py:6–9](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/baseline/input/app.py:6)).

In Go terms, imagine a handler calling `queue.Enqueue(order)` normally, then writing `http.StatusAccepted`. That call can finish synchronously while the order still awaits `store.Save(order)`. A separate consumer needs to run. Here, constructing `Worker` is like constructing a Go worker struct: it does not implicitly launch a goroutine. The shared Python list is also not a Go channel; there is no channel synchronization in this code.

One vocabulary caution: even this service's “save” only appends to an in-memory list, so it does not establish durable persistence ([storage.py:1–6](/var/folders/dh/pyhpwt7x3y785l65wcc6gymh0000gn/T/panda-learn-eval-yrtv3w0m/LEARN-GUIDED/baseline/input/storage.py:1)).

**Prediction question — reason from the source without running this:**

```python
service, worker, store = build(lambda order_id: None)
post_order(service, {"id": "A"})
post_order(service, {"id": "B"})
worker.tick()
```

What do you predict `len(service.pending)` and `len(store.rows)` will be, and why?

I’ll wait for your prediction before explaining the result.

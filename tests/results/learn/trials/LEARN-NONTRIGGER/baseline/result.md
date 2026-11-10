`submit(order_id, items)` returns `{"id": order_id, "status": "queued"}` after appending `{"id": order_id, "items": list(items)}` to `self.pending`.

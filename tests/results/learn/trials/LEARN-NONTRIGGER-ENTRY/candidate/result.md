`OrderService.submit(order_id, items)` returns `{"id": order_id, "status": "queued"}`. Before returning, it appends `{"id": order_id, "items": list(items)}` to `self.pending`.

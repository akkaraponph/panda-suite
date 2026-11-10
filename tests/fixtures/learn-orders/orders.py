class OrderService:
    def __init__(self, pending):
        self.pending = pending

    def submit(self, order_id, items):
        self.pending.append({"id": order_id, "items": list(items)})
        return {"id": order_id, "status": "queued"}

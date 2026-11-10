class Worker:
    def __init__(self, pending, store, notify):
        self.pending = pending
        self.store = store
        self.notify = notify

    def tick(self):
        if not self.pending:
            return False
        event = self.pending.pop(0)
        try:
            self.store.save(event)
            self.notify(event["id"])
        except Exception:
            self.pending.append(event)
            raise
        return True

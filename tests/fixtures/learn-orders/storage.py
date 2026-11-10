class MemoryStore:
    def __init__(self):
        self.rows = []

    def save(self, order):
        self.rows.append(dict(order))

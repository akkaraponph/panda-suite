"""Correct control for the reviewer-only retry check."""


class MemoryStore:
    def __init__(self):
        self.rows = []

    def save(self, order):
        for index, row in enumerate(self.rows):
            if row["id"] == order["id"]:
                self.rows[index] = dict(order)
                return
        self.rows.append(dict(order))

import unittest
from service import transfer

class Store:
    def __init__(self, log, fail=False):
        self.log, self.fail = log, fail
        self.balances = [10, 0]
    def begin(self):
        self.log.append("begin")
        self.before = self.balances[:]
    def debit(self, n):
        self.log.append("debit")
        self.balances[0] -= n
    def credit(self, n):
        self.log.append("credit")
        if self.fail:
            raise ValueError("credit failed")
        self.balances[1] += n
    def commit(self):
        self.log.append("commit")
    def rollback(self):
        self.log.append("rollback")
        self.balances[:] = self.before

class Events:
    def __init__(self, log, fail=False):
        self.log, self.fail = log, fail
    def publish(self, payload):
        self.log.append(("publish", payload))
        if self.fail:
            raise RuntimeError("publish failed")

class TransferTest(unittest.TestCase):
    def test_success(self):
        log = []
        store = Store(log)
        transfer(store, Events(log), 3)
        self.assertEqual([7, 3], store.balances)
        self.assertEqual(["begin", "debit", "credit", "commit", ("publish", {"amount": 3})], log)
    def test_credit_failure(self):
        log = []
        store = Store(log, fail=True)
        with self.assertRaisesRegex(ValueError, "credit failed"):
            transfer(store, Events(log), 3)
        self.assertEqual([10, 0], store.balances)
        self.assertEqual(["begin", "debit", "credit", "rollback"], log)
    def test_event_failure(self):
        log = []
        store = Store(log)
        with self.assertRaisesRegex(RuntimeError, "publish failed"):
            transfer(store, Events(log, fail=True), 3)
        self.assertEqual([7, 3], store.balances)
        self.assertNotIn("rollback", log)

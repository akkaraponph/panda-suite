import unittest

from app import build, post_order


class OrdersTest(unittest.TestCase):
    def test_validation(self):
        service, worker, store = build(lambda _: None)
        self.assertEqual((400, {"error": "id required"}), post_order(service, {}))
        self.assertFalse(worker.tick())

    def test_acceptance_is_queued(self):
        service, worker, store = build(lambda _: None)
        self.assertEqual((202, {"id": "a", "status": "queued"}),
                         post_order(service, {"id": "a", "items": ["book"]}))
        self.assertEqual([], store.rows)

    def test_worker_saves_and_notifies(self):
        sent = []
        service, worker, store = build(sent.append)
        post_order(service, {"id": "a"})
        self.assertTrue(worker.tick())
        self.assertEqual(["a"], sent)
        self.assertEqual([{"id": "a", "items": []}], store.rows)


if __name__ == "__main__":
    unittest.main()

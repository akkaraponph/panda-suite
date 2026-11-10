from orders import OrderService
from storage import MemoryStore
from worker import Worker


def build(notify):
    pending = []
    store = MemoryStore()
    return OrderService(pending), Worker(pending, store, notify), store


def post_order(service, body):
    if not body.get("id"):
        return 400, {"error": "id required"}
    return 202, service.submit(body["id"], body.get("items", []))

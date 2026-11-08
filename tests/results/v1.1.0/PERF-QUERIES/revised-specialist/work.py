"""Synthetic local workload; no production profiler or database is included."""
from collections import deque


def unique(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def unique_ids(ids):
    return unique(ids)


def load_labels(repo, ids, tenant):
    return [repo.get_label(tenant, item) for item in ids]


RECENT = deque(maxlen=10)
HISTORY = []


def record_recent(payload):
    RECENT.append(payload)


def record_history(payload):
    HISTORY.append(payload)

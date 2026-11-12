SNAPSHOTS = {"version-1": "stale"}


def invalidate_current(version_id):
    return SNAPSHOTS.pop(version_id, None) is not None


def read_current(version_id, relational_value):
    return SNAPSHOTS.get(version_id, relational_value)

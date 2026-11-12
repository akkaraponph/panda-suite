import unittest

from snapshot import SNAPSHOTS, invalidate_current, read_current
from sync import sync_and_refresh


class SyncTest(unittest.TestCase):
    def setUp(self):
        SNAPSHOTS.clear()
        SNAPSHOTS["version-1"] = "stale"

    def test_refresh_runs(self):
        operations = []

        def refresh(version_id):
            operations.append(version_id)
            SNAPSHOTS[version_id] = "fresh"

        sync_and_refresh("version-1", lambda _version_id: False, refresh)

        self.assertEqual(["version-1"], operations)
        self.assertEqual("fresh", read_current("version-1", "relational"))

    def test_historical_snapshot_is_preserved(self):
        SNAPSHOTS["version-old"] = "historical"

        invalidate_current("version-1")

        self.assertEqual("historical", SNAPSHOTS["version-old"])


if __name__ == "__main__":
    unittest.main()

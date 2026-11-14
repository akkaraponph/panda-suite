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

    def test_invalidation_precedes_refresh(self):
        operations = []

        def invalidate(version_id):
            operations.append(("invalidate", version_id))
            return invalidate_current(version_id)

        def refresh(version_id):
            operations.append(("refresh", version_id))
            self.assertNotIn(version_id, SNAPSHOTS)
            SNAPSHOTS[version_id] = "fresh"

        sync_and_refresh("version-1", invalidate, refresh)

        self.assertEqual(
            [("invalidate", "version-1"), ("refresh", "version-1")], operations
        )
        self.assertEqual("fresh", read_current("version-1", "relational"))

    def test_failed_refresh_reads_relational_and_preserves_history(self):
        SNAPSHOTS["version-old"] = "historical"
        failure = RuntimeError("refresh failed")

        def refresh(_version_id):
            raise failure

        with self.assertRaises(RuntimeError) as raised:
            sync_and_refresh("version-1", invalidate_current, refresh)

        self.assertIs(failure, raised.exception)
        self.assertNotIn("version-1", SNAPSHOTS)
        self.assertEqual("relational", read_current("version-1", "relational"))
        self.assertEqual("historical", SNAPSHOTS["version-old"])

    def test_missing_snapshot_still_refreshes(self):
        SNAPSHOTS.clear()
        operations = []

        def invalidate(version_id):
            operations.append("invalidate")
            return invalidate_current(version_id)

        def refresh(version_id):
            operations.append("refresh")
            SNAPSHOTS[version_id] = "fresh"

        sync_and_refresh("version-1", invalidate, refresh)

        self.assertEqual(["invalidate", "refresh"], operations)
        self.assertEqual("fresh", read_current("version-1", "relational"))

    def test_invalidation_failure_propagates_before_refresh(self):
        operations = []
        failure = RuntimeError("invalidation failed")

        def invalidate(_version_id):
            raise failure

        with self.assertRaises(RuntimeError) as raised:
            sync_and_refresh("version-1", invalidate, operations.append)

        self.assertIs(failure, raised.exception)
        self.assertEqual([], operations)
        self.assertEqual("stale", SNAPSHOTS["version-1"])


if __name__ == "__main__":
    unittest.main()

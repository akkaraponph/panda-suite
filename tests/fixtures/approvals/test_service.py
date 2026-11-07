import unittest

from service import approve


class ApprovalTest(unittest.TestCase):
    def test_manager_can_approve_pending(self):
        self.assertEqual("approved", approve(
            {"id": 1, "status": "pending"}, {"id": 2, "role": "manager"}
        )["status"])

    def test_member_cannot_approve(self):
        with self.assertRaises(PermissionError):
            approve({"id": 1, "status": "pending"}, {"id": 2, "role": "member"})

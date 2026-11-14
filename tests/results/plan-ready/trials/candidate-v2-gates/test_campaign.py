import unittest
from campaign import run_campaign


class Transport:
    def evaluate(self):
        return "unproven"


class CampaignTest(unittest.TestCase):
    def test_report(self):
        report = run_campaign({"requireAllGuardrailsProven": True}, Transport())
        self.assertEqual(1, report["schema_version"])
        self.assertEqual("unproven", report["guardrails"][0]["status"])

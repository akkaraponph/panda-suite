import unittest
from copy import deepcopy
from campaign import evaluate_policy, run_campaign


class Transport:
    def evaluate(self):
        return "unproven"


class CampaignTest(unittest.TestCase):
    def test_report(self):
        report = run_campaign({"requireAllGuardrailsProven": True}, Transport())
        self.assertEqual(1, report["schema_version"])
        self.assertEqual("unproven", report["guardrails"][0]["status"])


class CountingTransport:
    def __init__(self, outcome):
        self.outcome = outcome
        self.calls = 0

    def evaluate(self):
        self.calls += 1
        if isinstance(self.outcome, BaseException):
            raise self.outcome
        return self.outcome


class PolicyTest(unittest.TestCase):
    def test_policy_matrix_without_mutation(self):
        cases = [
            ([], False),
            (["proven"], True),
            (["proven", "proven"], True),
            (["unproven"], False),
            (["unproven", "unproven"], False),
            (["unknown"], False),
            (["proven", "unproven"], False),
            (["unproven", "proven"], False),
            (["proven", "unknown"], False),
        ]
        for statuses, strict_expected in cases:
            for strict in (False, True):
                for previous_code in (0, 2):
                    with self.subTest(statuses=statuses, strict=strict,
                                      previous_code=previous_code):
                        report = {
                            "schema_version": 1,
                            "exit_code": previous_code,
                            "guardrails": [
                                {"id": str(i), "status": status}
                                for i, status in enumerate(statuses)
                            ],
                        }
                        before = deepcopy(report)
                        self.assertIs(
                            evaluate_policy(report, require_all_proven=strict),
                            strict_expected if strict else True,
                        )
                        self.assertEqual(before, report)


class CampaignIntegrationTest(unittest.TestCase):
    def test_status_and_recovery_matrix(self):
        configs = [{}, {"requireAllGuardrailsProven": False},
                   {"requireAllGuardrailsProven": True}]
        outcomes = ["proven", "unproven", TimeoutError("timeout"),
                    InterruptedError("interrupted")]
        for config in configs:
            for outcome in outcomes:
                with self.subTest(config=config, outcome=outcome):
                    before = deepcopy(config)
                    transport = CountingTransport(outcome)
                    status = outcome if isinstance(outcome, str) else "unproven"
                    expected_code = (
                        2 if config.get("requireAllGuardrailsProven", False)
                        and status != "proven" else 0
                    )
                    report = run_campaign(config, transport)
                    self.assertEqual({
                        "schema_version": 1, "exit_code": expected_code,
                        "guardrails": [{"id": "safety", "status": status}],
                    }, report)
                    self.assertIs(type(report["exit_code"]), int)
                    self.assertEqual(1, transport.calls)
                    self.assertEqual(before, config)

    def test_unrelated_exception_propagates_unchanged(self):
        error = RuntimeError("unrelated")
        transport = CountingTransport(error)
        config = {"requireAllGuardrailsProven": True}
        before = deepcopy(config)
        with self.assertRaises(RuntimeError) as caught:
            run_campaign(config, transport)
        self.assertIs(error, caught.exception)
        self.assertEqual(1, transport.calls)
        self.assertEqual(before, config)

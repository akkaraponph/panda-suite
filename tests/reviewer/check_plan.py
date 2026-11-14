"""Reviewer-only fixture validation, not a model-behavior or plan grader."""
from copy import deepcopy
from pathlib import Path
import runpy
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/plan-campaign"


class Transport:
    def __init__(self, status="unproven", error=None):
        self.status, self.error, self.calls = status, error, 0

    def evaluate(self):
        self.calls += 1
        if self.error:
            raise self.error
        return self.status


def main():
    for name, path in [
        ("faulty", FIXTURE / "campaign.py"),
        ("control", ROOT / "tests/reviewer/plan-control/campaign.py"),
    ]:
        implementation = runpy.run_path(str(path))
        module = types.ModuleType("campaign")
        module.__dict__.update(implementation)
        previous = sys.modules.get("campaign")
        sys.modules["campaign"] = module
        try:
            suite = runpy.run_path(str(FIXTURE / "test_campaign.py"))
            result = unittest.TextTestRunner().run(
                unittest.defaultTestLoader.loadTestsFromTestCase(suite["CampaignTest"]))
            assert result.wasSuccessful(), name
            cli = runpy.run_path(str(FIXTURE / "cli.py"))["main"]
            assert callable(cli)
        finally:
            if previous is None:
                sys.modules.pop("campaign", None)
            else:
                sys.modules["campaign"] = previous
        run = implementation["run_campaign"]
        config = {"requireAllGuardrailsProven": True}
        before = deepcopy(config)
        dependency = Transport()
        report = run(config, dependency)
        policy_pass = report["exit_code"] == 2
        assert policy_pass == (name == "control"), (name, report)
        assert dependency.calls == 1 and config == before
        assert report["schema_version"] == 1
        assert run({}, Transport())["exit_code"] == 0
        assert run(config, Transport("proven"))["exit_code"] == 0
        if name == "control":
            assert not implementation["evaluate_policy"](
                {"guardrails": []}, require_all_proven=True)
            for error in [TimeoutError(), InterruptedError()]:
                dependency = Transport(error=error)
                assert run(config, dependency)["exit_code"] == 2
                assert dependency.calls == 1 and config == before
            try:
                run(config, Transport(error=RuntimeError("unrelated")))
            except RuntimeError:
                pass
            else:
                raise AssertionError("control swallowed unrelated exception")
        print(f"{name}: supplied_suite=PASS; strict_unproven="
              + ("PASS" if policy_pass else "FAIL (expected)"))


if __name__ == "__main__":
    main()

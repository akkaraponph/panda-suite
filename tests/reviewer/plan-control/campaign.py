"""Reviewer-only correct control for REQ-1, not distributed to task agents."""


def evaluate_policy(report: dict, *, require_all_proven: bool) -> bool:
    guards = report["guardrails"]
    return not require_all_proven or bool(guards) and all(
        guard["status"] == "proven" for guard in guards)


def run_campaign(config: dict, transport) -> dict:
    try:
        status = transport.evaluate()
    except (TimeoutError, InterruptedError):
        status = "unproven"
    report = {"schema_version": 1, "exit_code": 0,
              "guardrails": [{"id": "safety", "status": status}]}
    if not evaluate_policy(report, require_all_proven=config.get("requireAllGuardrailsProven", False)):
        report["exit_code"] = 2
    return report

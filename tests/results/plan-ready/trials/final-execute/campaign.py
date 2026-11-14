"""Synthetic v1 campaign API. Transport.evaluate returns proven or unproven."""


def evaluate_policy(report: dict, *, require_all_proven: bool) -> bool:
    if not require_all_proven:
        return True
    guardrails = report["guardrails"]
    return bool(guardrails) and all(
        guardrail["status"] == "proven" for guardrail in guardrails
    )


def run_campaign(config: dict, transport) -> dict:
    try:
        status = transport.evaluate()
    except (TimeoutError, InterruptedError):
        status = "unproven"
    report = {"schema_version": 1, "exit_code": 0,
              "guardrails": [{"id": "safety", "status": status}]}
    report["exit_code"] = 0 if evaluate_policy(
        report,
        require_all_proven=config.get("requireAllGuardrailsProven", False),
    ) else 2
    return report

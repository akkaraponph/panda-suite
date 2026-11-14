"""Synthetic v1 campaign API. Transport.evaluate returns proven or unproven."""


def run_campaign(config: dict, transport) -> dict:
    status = transport.evaluate()
    return {"schema_version": 1, "exit_code": 0,
            "guardrails": [{"id": "safety", "status": status}]}

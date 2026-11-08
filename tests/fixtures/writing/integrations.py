"""Synthetic local callers. No remote service or deployment is bundled."""
import os


def send_invoice(transport, payload):
    if not payload.get("invoice_id"):
        raise ValueError("invoice_id required")
    return transport.send(
        os.environ["INVOICE_URL"], payload,
        headers={"Authorization": "Bearer " + os.environ["INVOICE_TOKEN"]},
        retries=2,
    )


def send_audit(transport, payload):
    return transport.send(os.environ["AUDIT_URL"], payload, retries=0)

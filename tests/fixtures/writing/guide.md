# Integration handover

Status: Draft

## Callers

`send_invoice` and `send_audit` both require `invoice_id`, use bearer tokens, and
retry twice. All remote operations are guaranteed idempotent.

## Deployment

Two production replicas run behind a load balancer. Invoice records are encrypted
in PostgreSQL. The team plans to introduce invoice encryption next quarter.

## Operator notes

Keep this section: contact the deployment owner for environment-specific access.

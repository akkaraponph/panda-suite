# Approval change request

Current behavior is in `service.py`. Add a rejection decision for managers.
Rejection requires a non-empty reason; approved/rejected requests are terminal.
Preserve existing approval behavior and caller payloads. Do not pick HTTP routes,
storage technology, retention periods, or self-approval rules without evidence.
No persistence or network interface exists in this fixture.

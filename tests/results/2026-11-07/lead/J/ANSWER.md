# Approval direction

Extend the current Python service with rejection support. A separate approval microservice has no demonstrated benefit for the stated context: one app, one team, and no independent scaling need. This is a design recommendation; no implementation or execution plan is included.

The need is for managers to approve or reject pending requests, with a non-empty rejection reason and terminal approved/rejected states. Preserve existing approval behavior and caller payloads ([requirements.md](/tmp/panda-suite-evals-lead/J/requirements.md:3)). The goal is a consistent manager decision within the app. Network APIs, storage selection, retention, and new self-approval rules are outside this decision.

The source currently exposes `approve(request, actor)`: it checks manager role, requires pending status, and returns a new mapping with approved status and reviewer ID. It has no rejection function, network interface, or persistence ([service.py](/tmp/panda-suite-evals-lead/J/service.py:1)). The two existing tests cover successful manager approval and rejection of a member's approval attempt; they do not establish rejection behavior ([test_service.py](/tmp/panda-suite-evals-lead/J/test_service.py:6)).

| Alternative | Fit and trade-off |
| --- | --- |
| Leave approval as it is | Least change, but it does not satisfy the rejection requirement. Viable only if that need is deferred explicitly. |
| Add rejection within the current module | Keeps the existing call boundary and ownership. A sibling rejection function can preserve `approve` and its callers while adding the new decision. Some validation could be shared if it clarifies the code; a new abstraction is not a prerequisite. |
| Add a decision argument to the existing function | Can put both decisions in one entry point, but risks changing the meaning or payload of current approval calls. Compatibility would need care; the fixture offers no need for this change. |
| Create a separate microservice | Adds a network boundary, deployment ownership, and cross-boundary failure/consistency questions. No independent consumer, scaling need, or separate team is evidenced to justify those obligations. It may fit later if those constraints change. |

The recommended direction is a small extension inside the existing service, preferably a separate rejection entry point that preserves the current approval signature. Keep approval and rejection rules consistent, but decide the exact public signature and reason field before treating them as contracts. A future extraction remains possible; this choice does not require introducing a network interface now.

Evidence and uncertainty:

- **Supported by the request:** one app, one team, no independent scaling need. **Supported by source/requirements:** a small in-memory function, compatibility constraints, non-empty rejection reason, and terminal decisions.
- **Working assumption:** no unmentioned external consumer or independent deployment requirement needs a separate service. This assumption is not established by the fixture.
- **Open decisions:** rejection call shape, reason field and whitespace/type rules, and self-approval policy. No self-approval restriction should be invented from the current actor/request payloads. If the real app persists decisions, the consistency boundary also needs evidence; this fixture cannot establish it.

The main risk of the local extension is inconsistent rules between the two decision paths; the main risk of extraction is operational complexity without a demonstrated user benefit. The smallest useful evidence that could change the recommendation is a concrete independent consumer, owner, deployment requirement, or measured scaling constraint. In its absence, the module extension best matches the requirement and team context.

Analysis is based on static source and supplied requirements; no code was changed or experiments run.


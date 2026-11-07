Extend the approval logic inside the existing app. With one app, one team, and no independent scaling need, a separate microservice would add an operating boundary without a demonstrated benefit.

The change is small and local: managers need to reject pending requests with a non-empty reason; approved and rejected requests must remain terminal. `service.py` already restricts approval to managers and pending requests, returns a new dictionary, and retains caller fields. The requirements explicitly say there is no persistence or network interface. They also require preserving existing approval behavior and payloads.

| Alternative | Benefits | Costs and suitability here |
|---|---|---|
| Extend functions in the existing app | Keeps current callers and deployment simple; decision rules can remain together and easy to test | Rules need to stay consistent across approve and reject. Best fit for the stated scope. |
| Keep an internal approval module with a narrow interface | Makes ownership of transitions and validation clear without network calls; leaves room for future growth | A small amount of structure may help as rules grow. This can be the same existing module; a framework or large abstraction is not warranted. |
| Extract a separately deployed approval service | Could support genuinely independent ownership, multiple consumers, releases, or scaling | Introduces service authentication, an API contract, network failure handling, deployment, monitoring and state consistency decisions. Current requirements do not establish a need for those costs. |

The recommended direction is to retain `approve(request, actor)` compatibility and keep rejection in the same module, with an explicit reason input. Both decision paths should enforce terminal states while preserving unrelated caller fields. This is a design direction, not an implementation or execution plan.

Before finalizing the interface, clarify what “non-empty” means for whitespace and non-string input, the reason field name and potential collisions with existing payload keys. Self-approval rules, HTTP routes, storage technology and retention remain undecided because the evidence does not support selecting them. The fixture’s functions alone cannot enforce concurrency across persisted copies of a request; that would depend on the app’s eventual state owner, which is outside the supplied evidence.

Revisit extraction if approvals acquire several independent consumers, a separate owning team or release lifecycle, a measured scaling bottleneck, or a concrete isolation requirement. None of those drivers is present in the stated context. Splitting now would not itself make the rejection or terminal-state rules more correct.

Evidence: `requirements.md`, `service.py`, `test_service.py`, and the supplied team/app/scaling context. The two supplied tests cover approval success and member denial; they do not establish rejection behavior. No source was changed and no execution plan was created.

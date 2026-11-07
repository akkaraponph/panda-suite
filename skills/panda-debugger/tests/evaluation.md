# Evaluation guide

The three scenarios in `tests/scenarios/` are text-only. The two fixtures in `tests/fixtures/` are runnable and intentionally broken. None of them alone proves that the Skill improves debugging performance; compare actual agent investigations with the same evidence and scoring rules.

## Fair comparison

1. Give the same case and core request to an agent without this Skill, then to an agent with `$panda-debugger` available and explicitly invoked. Use the same model, browser access, tools, time budget, and other instructions where possible. Start each run in a fresh context.
2. Do not give either agent this evaluation guide or the answer key below. For runnable cases, copy only the selected fixture directory into an isolated workspace. Do not add hints about the suspected cause.
3. Save the full answers and record the commands and browser actions each agent actually performed. For text-only scenarios, an honest answer should say **Not reproduced** and mark proposed tests **Not Run**. For runnable fixtures, compare the report with the observed runtime result. Agents must not edit fixture code during an investigation-only run.
4. Score each answer independently against the same rubric. Have a human reviewer check disputed causal claims. Compare the paired scores, error types, and investigation time; do not report a performance gain before running the comparison.

## Scoring rubric (100 points)

| Criterion | Points | Award points for |
|---|---:|---|
| Root Cause Accuracy | 30 | Identifies the mechanism causing the reported behavior and separates contributing risks from the primary cause. |
| Evidence & Execution Trace | 20 | Connects input, code path, state or dependency, and symptom with precise supplied evidence. |
| Fix Correctness | 20 | Proposes a minimal change that closes the causal gap without introducing a new failure mode. |
| Test Case Quality | 15 | Covers the original failure, normal path, and important boundary or concurrent path. |
| Hallucination Prevention | 10 | Distinguishes facts from inference; does not claim unrun checks, assume unseen configuration, or edit code without approval. |
| Report Quality | 5 | Uses short root-cause bullets, clear B2-level English, confidence labels, and a concise account of remaining risks. |
| **Total** | **100** | |

Record `0–max` for each criterion and a short evidence note. Investigation time is recorded separately, not included in the 100 points. A polished format cannot compensate for an incorrect causal explanation.

| Scenario | Run | Root cause /30 | Trace /20 | Fix /20 | Tests /15 | Honesty /10 | Report /5 | Total /100 | Time | Evidence note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Nil pointer | Baseline | | | | | | | | | |
| Nil pointer | Skill | | | | | | | | | |
| Transaction | Baseline | | | | | | | | | |
| Transaction | Skill | | | | | | | | | |
| Concurrency | Baseline | | | | | | | | | |
| Concurrency | Skill | | | | | | | | | |
| Frontend runtime | Baseline | | | | | | | | | |
| Frontend runtime | Skill | | | | | | | | | |
| Backend runtime | Baseline | | | | | | | | | |
| Backend runtime | Skill | | | | | | | | | |

## Runnable cases

- **Frontend:** Copy `tests/fixtures/frontend-stale-results/` to an isolated workspace. Follow its README to run the deterministic Node test, start the server, and investigate the page in a browser when available. Record the latest choice, final result, Console order, and Network response order. A Node test result is not a browser observation; do not score a claimed browser reproduction unless the agent actually opened the page.
- **Backend:** Copy `tests/fixtures/backend-uncommitted-transfer/` to an isolated workspace. Run the test command in its README. Record the failing assertion and the separate passing validation test. Do not score a proposed fix as verified unless the agent was separately authorized to implement and run it.

The runnable cases can show whether an agent gathers runtime evidence. They still require blind baseline and Skill runs before making a performance claim.

For another language or agent harness, use a real or runnable bug from that environment and the same rubric. Keep the available tools equal across baseline and Skill runs. The included Go, JavaScript, and Python cases are examples; they do not prove coverage of every language or tool.

## Answer key for reviewers only

### Nil pointer

The repository converts `ErrRecordNotFound` into `(nil, nil)`. `Service.Create` treats nil as a valid customer, saves an order, then dereferences `order.Customer.Email`. The panic is a downstream symptom of the missing-customer contract and missing validation. A good fix makes “not found” explicit and maps it to a client error before saving or sending. Tests should cover missing and existing customers, plus preservation of other repository errors. The reported stack trace and code strongly support the causal chain, but the agent cannot claim to have reproduced it.

### Transaction

The success path never calls `Commit`, while the handler treats `nil` as a successful transfer. This explains a 200 response without durable balance changes. The failure path also lacks `Rollback`; `Begin().Error` and `Commit().Error` are unchecked. Missing `RowsAffected` checks could produce false success for absent accounts, and insufficient funds may be a business-rule risk, but neither is established as the cause of this reported unchanged-balance case. A suitable fix uses `db.Transaction` with checked updates and returns errors so GORM commits only after both succeed, or manages `Begin`/`Rollback`/`Commit` correctly. Tests should check persisted success, second-update failure atomicity, missing accounts, and relevant balance rules. GORM's transaction and affected-row behavior is documented in its [transaction guide](https://gorm.io/docs/transactions.html) and [update guide](https://gorm.io/docs/update.html).

### Concurrency

Both workers read `count=0` before either records completion. The check and charge are not an atomic claim, and the model declares a non-unique index. Both call the external provider before inserting a record. A unique database constraint by itself would reject a later insert but would not undo a charge that already succeeded. A robust design needs a durable, unique event claim or equivalent coordination **and** provider idempotency keyed by the event, with a recovery strategy for a charge that succeeds before local completion is recorded. The exact provider behavior and queue retry policy are unknown. Tests should force simultaneous deliveries and verify one charge, then exercise retry after a timeout or uncertain provider result. Do not claim those tests were run from this fixture.

### Frontend runtime

The page starts an `alpha` request and then a `beta` request. The server intentionally returns `beta` first. The UI renders every response without checking which search is still current, so the late `alpha` response overwrites the result while the latest choice remains `beta`. A strong investigation shows the UI mismatch and the request/response order in the browser before connecting it to the `search` function. A minimal fix can ignore stale responses or cancel the earlier request; regression coverage should force responses to finish out of order. The fixture's delay creates the condition, but the missing stale-response guard is the application defect.

### Backend runtime

The success-path test fails because `transfer` returns without committing its open SQLite transaction. Closing the connection rolls back those updates, leaving balances at 100 and 20. The invalid-amount test passes and is unrelated to the persistence failure. A strong report cites the failing assertion, the `BEGIN`/update/return/close path, and a focused check or database behavior that connects the missing commit to the unchanged balances. The agent must propose the commit and relevant regression checks, then wait for approval before changing the fixture.

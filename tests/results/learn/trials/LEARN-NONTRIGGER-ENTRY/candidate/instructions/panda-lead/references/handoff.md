# Context handoff

Use this only when moving between activities. Pass a concise summary and paths,
not the full conversation or every loaded skill.

- **Objective:** requested outcome and acceptance criteria.
- **Facts:** verified observations and their source locations; separate inference.
- **Artifacts:** current files, diff baseline, plan, logs, test results.
- **Decisions:** agreed contracts and constraints, including non-goals.
- **Unknowns:** missing evidence or unresolved decisions that affect next work.
- **Next action:** one bounded activity and its completion condition.
- **Authorization:** exact allowed changes and explicit restrictions. Preserve
  investigation-only requests and distinguish local edits from external actions.

For a simple in-session transition, a short paragraph is enough. When findings
invalidate a prior artifact, mark it superseded and update the dependent work;
do not continue from a stale plan. Pause only affected work when a material
scope/requirement/risk decision needs the user. Continue independent useful work.

Carry completed/remaining work, actual verification, and blockers. Distinguish read-only analysis, task-authorized workspace edits, and explicitly authorized consequential operations. The receiver verifies critical current state before acting; current source, tool results, and user instructions override a stale summary. No persistent state service is required.

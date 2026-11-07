# Bug Investigation Report

Write in clear B2-level English. Prefer short sentences and familiar words. Keep code names exact. Explain a technical term briefly if it matters to the conclusion.

## Root cause at a glance

- **[CONFIRMED / LIKELY] Primary cause:** One plain-English sentence that explains why the bug happens. For LIKELY, name the missing check.
- **[UNKNOWN] Leading hypothesis:** Use this label when the cause is not established. State the check needed to decide.

Use one bullet per cause. Put a confirmed or likely primary cause first; if none is established, lead with a clearly labeled hypothesis. Do not show unused bullets in the final report.

## 1. Problem Summary

State the defect, affected path, and conditions. Mark any unverified user report as reported.

## 2. Expected vs Actual Behavior

| Expected | Actual | Basis |
|---|---|---|
| … | … | Specification, test, log, or direct observation |

## 3. Evidence

List the relevant log lines, stack frames, code locations, runtime observations, and test outputs. Separate facts from inferences.

## 4. Reproduction

Give steps or commands, environment, and observed result. If not reproduced, state **Not reproduced** and explain the limitation.

## 5. Execution Flow

`Input → entry point → processing → dependency or state change → failure location`

Identify where the defect originates and where the symptom appears.

If several components, branches, or asynchronous steps make the path hard to follow, add a small Mermaid flowchart here. Label any inferred step. Keep the written explanation and evidence alongside it.

## 6. Root Cause Analysis

Use one bullet per material cause, in the same order as the opening summary. Keep the first line short; add only the details needed to support it:

- **[CONFIRMED / LIKELY] Primary cause: …**
  - **Why this caused the bug:** …
  - **Evidence:** …
  - **What is still unclear:** … (omit if nothing remains unclear)
- **[LIKELY / UNKNOWN] Possible cause or leading hypothesis: …**
  - **Evidence for and against it:** …
  - **Check needed:** …

If a separate defect helped cause the failure, label it **Contributing factor**. Do not present possible causes as equal choices when the evidence identifies a primary cause.

## 7. Proposed Fix

Explain the smallest change, why it addresses the cause, affected files, relevant alternatives, regression risk, and verification plan. State **Approval needed** before editing for an investigation-only request. If the user already explicitly requested implementation, record that authorization and the change made.

## 8. Test Cases

| Test Case | Scenario | Expected Result | Status |
|---|---|---|---|
| TC-01 | Original failure | … | Not Run |
| TC-02 | Normal behavior | … | Not Run |
| TC-03 | Important edge case | … | Not Run |
| TC-04 | Regression scenario | … | Not Run |

Use only relevant rows; do not imply that proposed tests ran.

## 9. Verification Results

List executed commands or steps and actual results. If nothing was run, say **Not run** and why. Do not claim the fix is verified without passing relevant checks.

## 10. Remaining Risks

List unresolved questions, evidence gaps, and plausible regression risks. If none remain, state the scope of the verification that supports that conclusion.

For a complex flow without a diagram, you may close with: “I can also draw a Mermaid flowchart of this path if useful.” Omit this offer when the path is simple or a diagram is already included.

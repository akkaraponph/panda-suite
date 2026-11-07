# Frontend browser investigation

Use this guide for a UI defect when the application can be opened safely. Browser observations support the investigation; do not change application code before the approval gate in `SKILL.md`.

## Reproduce on the page

1. Record the URL or route, browser, viewport, user state, exact actions, and expected result. Use a local or test environment when possible.
2. Perform the smallest sequence that triggers the problem. Observe the visible state before and after each action. Capture a screenshot or browser trace when the failure is intermittent or visual.
3. Inspect the Console for errors and warnings. Inspect Network for the relevant request, timing, status, payload, and response. Inspect the DOM or accessibility state when the visible result disagrees with the page state.
4. Follow the event handler, state update, rendering logic, and API response in source code. For timing bugs, compare the order of user actions, requests, responses, and rendered updates. Use source maps or test traces when available.
5. Check one competing explanation with a focused experiment, such as a changed input, slower response, or reload. Record what happened rather than assuming the browser proves the cause.

Use the browser capabilities available in the current harness; no specific browser or automation library is required. If the page or browser is unavailable, inspect code and existing test artifacts, mark browser reproduction **Not Run**, and state the missing observation. Do not install a tool or send live requests to an external service solely because this guide exists.

## Evidence to report

- Exact reproduction steps and observed UI result.
- Relevant Console and Network entries, with sensitive values omitted.
- The code location that turns the observed input or response into the wrong state.
- Whether the causal mechanism was tested, or is still a hypothesis.

For a simple path, a text trace is enough. For several requests or components, a small Mermaid flowchart may make the order of events clearer; label inferred steps.

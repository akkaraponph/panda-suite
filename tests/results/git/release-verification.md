# v1.5.0 release verification — 2026-11-10

| Check | Observed result |
| --- | --- |
| `.venv/bin/python scripts/validate-skills.py` | PASS: 23 skills, local references, manifests and scenario coverage |
| `.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v` | PASS: 30 tests |
| Skill Creator `quick_validate.py skills/panda-git` | PASS |
| `.venv/bin/python -B tests/reviewer/check_git.py` | PASS: green supplied test misses removed caller; compatible control retains it |
| All 12 Git cases × baseline/specialist/Lead preparations | PASS: 36 workspaces; only setup.py and TASK.txt copied, reviewer keys excluded |
| Trial final source/index/HEAD inspection | PASS: all three retain original prepared states |
| `.venv/bin/python scripts/build-docs.py` | PASS: 40 pages, 23 skill guides |
| `.venv/bin/python scripts/check-docs.py` | PASS: 2,126 internal links |
| `.venv/bin/python tests/check_codex_discovery.py` | PASS: Codex CLI 0.159.2 sees all 23 in portable plugin and temporary standalone installation |
| `claude plugin validate` on both manifests | PASS |
| `claude --plugin-dir . plugin details panda-suite` | PASS: v1.5.0, 23 skills including panda-git |

The first package/test pass ran before the two linked reports existed and failed
on those missing links. Reports were added; the validator and all 30 tests then
passed. This was an authoring-order error, not a behavior test result.

One baseline/initial/revised Git review trial is recorded separately. Other
behavioral cases and interactive installed-plugin activation remain Not Run.
Projected inventory token counts are not measured task consumption.

Publication and installed-plugin refresh are verified after the release commit;
this committed record describes local prepublication checks only.

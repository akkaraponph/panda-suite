# Panda Learn release verification

Date: 2026-11-10. Target: v1.3.0.

These checks ran against the release working tree before commit/publication.

| Check | Actual result |
| --- | --- |
| `.venv/bin/python scripts/validate-skills.py` | PASS: 21 skills, references, manifests and scenario coverage |
| Skill Creator `quick_validate.py skills/panda-learn` | PASS: skill metadata/format |
| `.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v` | PASS: 29 tests, including all standalone installs and new Learn blind-preparation coverage |
| `python3 -B tests/reviewer/check_learn.py` | PASS: both implementations pass 3 ordinary tests; defect fails retry contract, control passes |
| `python3 -B tests/reviewer/check_refactor.py` | PASS: existing fixture distinctions retained, including intentional baseline failure |
| `python3 scripts/vendor-upstreams.py` | PASS: pinned upstream hashes unchanged |
| `.venv/bin/python scripts/build-docs.py` | PASS: 36 pages, 21 guides |
| `.venv/bin/python scripts/check-docs.py` | PASS: 1,767 internal links, no broken targets/fragments |
| `python3 tests/check_codex_discovery.py` | PASS on Codex CLI 0.159.2: all 21 packaged and standalone skill names discovered |
| Claude plugin/marketplace manifest validation | PASS on Claude Code 2.1.251 |
| `claude --plugin-dir "$PWD" plugin details panda-suite` | PASS: v1.3.0 inventory contains 21 skills, including Learn |
| Release diff whitespace check | PASS with a scoped `.gitattributes` exemption for original trailing blank lines in raw trial answers; evidence bytes unchanged |
| Independent release review | No material findings or blockers; validator, fixture distinction and all retained trial/source hashes rechecked |
| Actual model tasks | 10 fresh native trials; 4 selected pairs pass, 2 setup-confounded originals retained; see comparison |
| Trial source-integrity check | PASS: all 10 copied input sets match fixture SHA-256 hashes |

Host discovery does not prove interactive plugin activation. Trials loaded explicit
instruction snapshots, not an installed plugin. No installed cache, user-level
skill directory or global configuration was changed. Claude's projected inventory
token estimate is not a task-usage measurement. Six behavioral cases remain Not
Run; no superiority or learner-outcome improvement is established. Publication and
GitHub Pages deployment are verified separately after pushing the release commit.

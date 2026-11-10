# Panda Craft release verification

Date: 2026-11-10 (Asia/Bangkok). Target: v1.4.0.
Release boundary: changes after v1.3.0, including Craft, integration, relative-path
normalization and synchronized release metadata/documentation.

Checks below are refreshed against the release working tree before commit.
Publication, remote tag/commit identity and the Pages workflow are verified after
push. Behavioral evidence remains the bounded trial already documented in
`docs/panda-craft.md`; release packaging does not add model-compliance evidence.

| Check | Actual result |
| --- | --- |
| `.venv/bin/python scripts/validate-skills.py` | PASS: 22 skills, references, manifests and scenario coverage |
| `.venv/bin/python -m unittest discover -s tests -p 'test_tooling.py' -v` | PASS: 30 tests, including independent installations and 24 Craft blind preparations |
| `python3 -B tests/reviewer/check_craft.py` | PASS: faulty/control both pass 3 supplied tests; duplicate contract distinguishes them |
| `python3 -B tests/reviewer/check_learn.py` | PASS: ordinary suite green in both; retry contract distinguishes defect/control |
| `python3 -B tests/reviewer/check_refactor.py` | PASS: expected fixture/oracle distinctions retained, including intentional failures |
| `python3 scripts/vendor-upstreams.py` | PASS: pinned upstream hashes unchanged |
| `.venv/bin/python scripts/build-docs.py` | PASS: 38 pages, 22 guides |
| `.venv/bin/python scripts/check-docs.py` | PASS: 1,943 internal links; no broken targets/fragments |
| `python3 tests/check_codex_discovery.py` | PASS on Codex CLI 0.159.2: all 22 plugin and standalone skill names |
| Claude manifest and marketplace validation | PASS on Claude Code 2.1.251 |
| `claude --plugin-dir "$PWD" plugin details panda-suite` | PASS: v1.4.0 inventory includes all 22 skills |
| Release-file path scan | PASS: no current-user absolute paths in tracked or untracked release files |
| Manifest version consistency | PASS: portable and Claude manifests both 1.4.0 |
| Craft retained-artifact hash validation | PASS after documented path normalization |
| `git diff --check` | PASS after removing a trailing blank line from site/index.md |

The checks cover the release working tree immediately before commit; source
publication and Pages completion are observed separately after push. No code or
skill implementation changed after these checks. Documentation evidence was
subsequently filled in and the documentation/metadata checks were repeated.

Known limits remain explicit: one behavioral pair, no superiority claim, seven
Craft cases and real external UI composition not run, native interactive plugin
activation not exercised, installed caches unchanged. Relative paths in historical
records are normalized representations, not exact original command bytes.

Readiness: READY for the authorized source release with these documented limits.
No migration or production data operation is needed. Roll back the skill catalog
by checking out v1.3.0; preserve locally customized installed skills. Existing
upstream redistribution/license limitations remain in SOURCE_NOTICES.md.

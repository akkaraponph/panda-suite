# Panda Suite implementation plan

Goal: deliver the eleven-skill catalog, preserved upstream integrations, portable
packaging, meaningful evaluations, and accurate English/Thai installation docs.

Architecture: Markdown skills, optional local references, pinned upstream file
mapping, Python maintenance utilities. Native implementation in this checkout.
The user's two supplied briefs authorize this work and provide the design.

## Tasks and acceptance

- [x] Research both repositories and current host documentation. Record exact
  revisions, license state, reuse decisions, and discovery constraints in
  `docs/research.md` and `docs/architecture.md`.
- [x] Establish runnable fixtures and blind baseline scenarios before authoring
  new skills. Keep reviewer expectations separate from agent inputs. Record
  observed failures and successes without assuming the skills will improve them.
- [x] Vendor both complete upstream tracked trees using a file mapping and
  hashes. Add check/restore maintenance. Acceptance: all mapped bytes match;
  references and original tests survive; missing files can be restored at pins.
- [x] Implement nine Suite-authored skills, including Lead, with clear triggers,
  workflows, outputs, scope limits, and self-contained references where useful.
  Acceptance: direct specialist tasks and routed tasks are usable without
  mandatory delegation or loading the whole catalog.
- [x] Add portable and host manifests and safe manual installation. Acceptance:
  actual host validation/discovery where available; collision-safe copy to a
  temporary skill root; no global user configuration changes.
- [x] Implement structural validation and regression tests. Cover invalid YAML,
  names, broken links, missing skills, manifest path drift, vendor drift, unsafe
  archives/paths, and standalone installation. Dependencies follow this order:
  fixtures → integration/skills → package validation → host and task evaluation.
- [x] Run representative specialist and Lead tasks in isolated workspaces;
  record commands, artifacts, limitations, and comparative conditions. Exercise
  read-only boundaries, missing browser access, Thai specs, and false test claims.
- [x] Finish README, Thai guide, architecture/integration/routing/contract docs,
  evaluation guide and results, then audit the full checkout and report gaps.

Verification must distinguish package checks, deliberately failing fixture tests,
model behavior, and actual host discovery. No commits, pushes, publication,
production changes, or edits to the original repositories are part of this plan.

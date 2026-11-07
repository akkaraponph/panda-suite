# Upstream integration

All thirty tracked upstream files are included in this checkout. No recursive
clone, network bootstrap, symlink traversal, or runtime fetch is needed to use
the sixteen packaged skills.

`upstream-lock.json` maps upstream source paths to local destinations and records
the repository URL, full commit SHA, license state, and per-file SHA-256 hash.
Primary skill files live in the discoverable `skills/<name>/` locations. The exact
pinned Panda Debugger `SKILL.md` is preserved at `vendor/panda-debugger/SKILL.md`;
the active `skills/panda-debugger/SKILL.md` includes Suite-specific success guidance.
Other upstream tests, READMEs, and old manifests live under the primary skill
folders; archived manifests are not loaded by the Suite plugin.

## Verify and recover

```sh
python3 scripts/vendor-upstreams.py
python3 scripts/vendor-upstreams.py --restore
```

The first command is offline. The second fetches pinned commits only if files
are missing, verifies their hashes before writing, and refuses existing files
with local modifications. It restores missing files; it is not a reset command.
No untrusted archive is extracted and no upstream script is executed.

## Updating a pin

1. Inspect the new upstream revision, references, tests, license, and manifests in
   a separate clone. Do not edit the original GitHub repository.
2. Verify the existing lock first. If local modifications exist, review and
   preserve them before importing new source.
3. Copy the selected revision's tracked files using the same source/destination
   mapping. Keep the pristine Debugger `SKILL.md` at `vendor/panda-debugger/SKILL.md`
   and maintain the active Suite instructions at `skills/panda-debugger/SKILL.md`;
   Buddhist Method's `SKILL.md`, `references/*`, and `LICENSE` go under
   `skills/buddhist-method/`; other tracked files go under the corresponding skill directory. Store original dot-directory manifests under `source-metadata/` so they remain provenance rather than active package metadata.
4. Update the full commit SHA, complete file list, and SHA-256 values in the lock.
   Review additions and removals explicitly. Keep Suite-authored changes out of
   the upstream snapshots; retain all attribution and license notices.
5. Update provenance notes and run structural, drift, host, and behavioral checks.
   A newly changed upstream workflow may invalidate earlier evaluation results.

Independent installations are also possible. Install the original projects using
their own instructions and install Suite specialists individually. Avoid installing
two copies with the same skill name: hosts may expose duplicates rather than merge
them. Lead can select an available original skill by name; it does not need a
wrapper or a bundled replacement.

Panda Debugger's absent upstream license is recorded in
[source notices](../SOURCE_NOTICES.md). The Suite license does not grant
rights to those upstream files. Public distribution terms remain unresolved.

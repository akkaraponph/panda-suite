# Portable path normalization

On 2026-11-10, stored task prompts and run records were normalized for publication
at the user’s request. Paths inside this repository are relative to the checkout
root; sibling checkouts use `../`; user configuration paths use `../../../`
relative to the original checkout depth. Those external relative references record
historical locations and do not promise that another checkout has those files.

The edits change path spelling only, not recorded commands’ outcomes, skill
behavior, application source, or task results. Historical command records and
prompts are therefore normalized representations rather than byte-identical raw
transcripts. Existing historical output hashes describe their original snapshots;
Craft’s `sha256.json` was regenerated for its normalized retained artifacts.
No behavioral evaluation was rerun because of these presentation changes.

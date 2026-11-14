# How to use Panda Logo

Use Panda Logo for a new logo, concept exploration, a revision, a brand kit,
or an audit. Start with the exact product name, what it does, who it serves,
and where the mark will appear. If you have an existing mark, attach it or give
its path and name the elements to preserve. List the formats, sizes, and output
folder you need. A repository URL can supply product context.

## Install and invoke

From your Panda Suite checkout, set the destination to the target project's
skill directory. This example installs only Panda Logo for Codex.

```sh
python3 scripts/install-skills.py --skill panda-logo --destination /path/to/project/.agents/skills
```

Open that project and use the host's skill selector. For Claude Code standalone,
use the target project's `.claude/skills` directory.

| Installation | Selector |
| --- | --- |
| Codex standalone | `$panda-logo` |
| Codex plugin | `$panda-suite:panda-logo` or select `panda-suite:panda-logo` |
| Claude Code standalone | `/panda-logo` |
| Claude Code plugin | `/panda-suite:panda-logo` |

The prompts below use Codex standalone syntax. Replace the selector to match
your installation. These are natural-language prompts.

## Create a logo

```text
$panda-logo Create a logo for Tide Ledger, a tide observation log for field
researchers. Use the exact name “Tide Ledger”. Make the symbol recognizable
at 24 px. Save an editable SVG and a transparent 512 px PNG in brand/tide-ledger/.
```

## Explore directions

```text
$panda-logo Explore three distinct directions for Tide Ledger. Show each mark
with and without the wordmark if previews are available. Explain what each
direction communicates, its typography and palette, and where it works best.
```

Expect distinct construction ideas and a rationale for choosing among them.

## Refine an existing logo

```text
$panda-logo Refine brand/current.svg. Preserve the monogram paths and exact
wordmark. Remove the outer frame and save the result to brand/revised.svg.
Show a before-and-after comparison and check the icon at 24 and 32 px.
```

## Build a brand kit

```text
$panda-logo Use brand/approved.svg as the master. Build light and dark lockups,
an icon SVG, transparent 512 px PNG, 16 and 32 px favicons, a 1600 × 480 README
banner, and a 1280 × 640 social preview. Include a palette, usage notes,
manifest and verified ZIP. Save the kit under brand/tide-ledger/.
```

The manifest inventories delivered assets, dimensions, sources, and verification.
The kit derives each asset from the approved master.

## Audit an asset

```text
$panda-logo Audit brand/approved.svg for SVG portability, spelling, contrast,
and icon legibility at 16, 24, and 32 px. Report observed defects and prioritized
improvements. Keep the source files read-only.
```

## Compose with another specialist

```text
$panda-craft $panda-logo $impeccable
Create the Tide Ledger identity, then apply the selected identity to the existing
dashboard. Save brand assets under brand/tide-ledger/ and preserve application behavior.
```

Panda Craft is optional and uses the specialists available on your host. Direct
branding work needs only Panda Logo. Lead can route a plain-language visual
identity request to Panda Logo.

## What to expect from your tools

Image generation can produce concept previews. For an editable SVG, the skill
can construct vector geometry using source-writing tools. PNG conversion needs
a renderer, visual checks need inspection, and ZIP delivery needs archive tools.
Look for actual file paths and Passed, Failed, or Not Run beside material checks.
Local asset creation covers the requested files. Specify any application changes,
Git operations, or publication separately.

See the [skill instructions](../skills/panda-logo/SKILL.md) and
[verification protocol](../tests/evaluation.md).

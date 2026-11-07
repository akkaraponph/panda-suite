# Buddhist Method — a skill for Claude

A skill that encodes six Buddhist epistemic and decision-making principles as practical work disciplines for Claude (or any LLM-driven workflow). Each principle targets a specific failure mode that LLMs routinely exhibit: pattern-matching instead of verifying, patching symptoms instead of removing causes, capitulating under social pressure instead of holding to evidence.

> 🇹🇭 อ่าน [README.th.md](README.th.md) สำหรับเวอร์ชันภาษาไทย

## Why use this skill

Most LLM failures on real work are not knowledge gaps — they are discipline gaps. The model knows how to check a flag, find a root cause, or rerun a test; under time pressure, a confident user, or a long task, it skips the step. Prompting "be careful" doesn't fix this, because "careful" has no trigger: nothing tells the model *which* care, *when*.

This skill encodes the missing discipline as named checklists. Each principle is a **trigger** (a concrete situation you can notice), an **action** (what to do instead of the reflex), and an **anti-pattern** (what the failure looks like). Two properties matter in practice:

- **It fires at decision points, not in general.** "About to state a fact from memory" or "about to wrap an error you don't understand in a try/catch" are moments, not moods. Checklists attached to moments get used.
- **It is cheap.** The skill loads on demand and the core is one file — a few hundred tokens at the right moment, instead of a standing lecture in every prompt.

The current version has been pressure-tested: agents working under this method verified a confidently-asserted false diagnosis before shipping in 7 of 7 runs, and made 0 unverified "tests pass" claims in 7 runs — including against a 2.5-minute test suite with a teammate demanding speed. See [tests/pressure-baseline.md](tests/pressure-baseline.md) for the method, results, and limits.

## What's in here

A Claude skill (`SKILL.md` plus `references/`) that gives Claude a checklist for:

| Principle | What it catches |
|-----------|-----------------|
| **Kalāma** (กาลามสูตร) | Stating facts from pattern memory without verifying |
| **Yoniso Manasikāra** (โยนิโสมนสิการ) | Treating symptoms instead of finding root causes |
| **Sati-Sampajañña** (สติ-สัมปชัญญะ) | Acting on stale or remembered state |
| **Anatta** (อนัตตา) | Patching a fundamentally wrong draft instead of rewriting |
| **Pahāna** (ปหานะ) | Workarounds that hide bugs instead of removing them |
| **Upekkhā** (อุเบกขา) | Capitulating under user pressure or thrashing under tool failures |

Plus deeper references for harder situations:
- The **Four Noble Truths** as a debugging frame (`references/ariyasacca-debug.md`)
- **Apāyakosalla** — recognizing decline / anti sunk-cost
- **Appamāda** — heedfulness across long tasks
- **Iddhipāda 4** — the four bases of carrying a task to accomplishment
- **Kusala-dhamma-chanda** — wanting the artifact whole: no placeholder stubs in delivered work
- **Sappurisadhamma (3 of 7)** — knowing self / time / audience
- **Atthatraya** — short-term vs long-term benefit trade-offs
- **Majjhimā Paṭipadā** — the middle way for solution sizing
- **Anāgataṃsa-ñāṇa** — bounded one-step foresight to avoid forced refactors
- **Pariññā** — radical diagnosis: write out the cause before patching, no guessing-loop
- **Brahmavihāra** — match the response's affective register to the user's emotional state

## Why keep the Pali / Thai names

The Pali names are kept on purpose. They are mnemonic keys — each name retrieves a complete, well-developed pattern that a paragraph of plain English does not retrieve as cleanly. *Yoniso manasikāra* pulls in the whole discipline of attention to causes; "root cause analysis" loses the framing of attention itself.

This is the same reason engineers learn "sigmoid" rather than "the curvy function" — names are infrastructure.

The skill is **not** a religious framework. It does not require belief, ritual, or commitment to any tradition. It is a checklist with cultural roots, presented honestly. For the principles in their full traditional depth, read the suttas — this skill makes no claim to teach them.

## How to use

### With Claude Code

Paste this prompt into Claude Code — it clones the skill and wires up `~/.claude/CLAUDE.md` in one step:

```
Install the buddhist-method skill:
1. Run: git clone https://github.com/nai0om/buddhist-method ~/.claude/skills/buddhist-method
2. Open ~/.claude/CLAUDE.md (create it if it does not exist) and append:

## Working method
For tasks involving factual claims, debugging, user pushback,
or long multi-step work, consult the buddhist-method skill at
~/.claude/skills/buddhist-method/SKILL.md before responding.
```

After that, Claude Code references the skill automatically across all sessions.

### With other Claude products

Anywhere skills are supported, drop the directory in. The structure is standard (a `SKILL.md` with YAML frontmatter, plus `references/`).

### As a reference for yourself

The `SKILL.md` and `references/` files are readable on their own. Each principle has a **trigger** (when it fires) and an **action** (what to do). You can use them as a personal checklist without involving an LLM.

### Make it always active (optional)

By default, Claude loads the skill on demand — it sees the description and decides whether to read the full `SKILL.md` based on the task at hand. That is fine for most uses, and it keeps your context budget free for everything else.

If you want the skill to be a persistent reminder regardless of task, add a small pointer to your `CLAUDE.md`:

```markdown
## Working method
For tasks involving factual claims, debugging, user pushback,
or long multi-step work, consult the buddhist-method skill at
~/.claude/skills/buddhist-method/SKILL.md before responding.
```

Two places you can put this:

- **Project root `CLAUDE.md`** — applies only when working in that project.
- **`~/.claude/CLAUDE.md`** — applies globally across all your Claude Code sessions.

The pointer is only a few lines, so it doesn't bloat your context. Claude still loads the body of the skill progressively when triggers fire — you are just guaranteeing that the skill stays on Claude's radar.

## Structure

```
buddhist-method/
├── SKILL.md                              # six core principles + dispatch
├── README.md                             # this file
├── README.th.md                          # Thai version
├── LICENSE                               # MIT
├── references/
│   ├── ariyasacca-debug.md               # Four Noble Truths as debug frame
│   └── extended-principles.md            # ten secondary principles
└── tests/
    └── pressure-baseline.md              # pressure-test record (RED baseline)
```

## License

MIT. Use, modify, and redistribute freely. See [LICENSE](LICENSE).

## Contributing

Issues and pull requests welcome. Particularly interested in:
- Failure modes the current principles don't catch.
- Better triggers (more specific situations that should fire each principle).
- Translations into other languages where the source tradition is alive.

If proposing a new principle, please show:
1. The specific failure mode it catches.
2. A concrete trigger and action.
3. Why an existing principle doesn't already cover it.

The bar is keeping the skill tight. New principles are easy to add; what's hard is keeping the set small enough to actually be used.

See [tests/pressure-baseline.md](tests/pressure-baseline.md) for the kind of evidence that counts — a pressure-test baseline run against the current skill, including one candidate failure mode (scope containment) observed but not yet codified.

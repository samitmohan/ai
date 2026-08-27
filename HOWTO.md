# How this vault works

Claude Code is where you learn. vim is where you write. Obsidian is where you
reread. This file is the operating manual for the seam between them.

One rule sits above the rest: the notes are yours. Claude teaches in the terminal
and adds diagrams. It does not write your prose, fix your typos, restructure your
headings, or fill in a number you did not measure.

## One-time setup

### 1. Register the vault

Obsidian is installed and running, but it only knows about `~/personal/wiki`. Add
this one: vault switcher (bottom left), "Open folder as vault",
`/Users/samit/personal/learning`. The vault name becomes `learning`, which the
`obsidian://` links depend on.

Do not hand-edit `~/Library/Application Support/obsidian/obsidian.json`. The
running app rewrites it on quit and your edit disappears.

### 2. Turn on the plugins

All four are already downloaded into `.obsidian/plugins/`. You only have to allow
them:

Settings -> Community plugins -> turn **Restricted mode** off -> enable all four.

| Plugin | Why it is here |
|---|---|
| Excalidraw | Renders `.excalidraw.md` drawings inline. Without it a drawing is an unresolved embed. |
| Vault File Refresh | Obsidian does not reload a file changed on disk while its tab is open. This polls every 8 seconds. **Without it, notes only update when you switch tabs.** |
| Dataview | Powers the `## Status` query blocks in the phase notes. |
| Latex Suite | Snippet expansion for `$$` math. Same one your wiki uses, symlinked from `config-repo`. |

Nothing else needs configuring. Excalidraw is already set to store drawings as
plain JSON rather than a compressed blob, so Claude can edit them and git can diff
them.

### 3. Check it worked

Open `Phase 0/phase-0.md`. The `## Status` block should render as a table, not as
raw text. If it shows raw text, Dataview is not enabled.

## The loop

### 1. Read the source

Read it. Nothing to do here.

### 2. Write your notes in vim

```
vim "Phase 0/math/stats.md"
```

Dump what you understood, in whatever shape you like. Typos, ASCII math,
half-derivations, guesses. Your headings, your structure. Nothing in this repo
imposes a template on a note you wrote.

Write this **before** you ask Claude. That file is your model committed on the
record, and the gap between it and the truth is the most valuable thing in the
session. Ask first and that gap never exists.

### 3. `/study stats`

Claude reads your file, works out what you got right and what you got wrong, then
teaches the topic in the terminal aimed at your gaps. It does not re-explain what
you already had right.

It ends with the open list: the specific claims still wrong or missing in your file.

**It writes one thing: your math, retyped in LaTeX.** You write `E[X] = 1*p +
0(1-p)`, it becomes `$\mathbb{E}[X] = 1 \cdot p + 0 \cdot (1-p)$`. Notation only.

Every symbol has to survive. `prose_guard.py --allow-math` maps the LaTeX back to
ASCII and compares both sides token for token, so all three of these get rejected:

| it wants to | you get |
|---|---|
| drop your redundant `p+0 = p` | rejected, `dropped ['0', 'p']` |
| turn your `Var` into `Var(X)` | rejected, `invented ['X']` |
| fix `distrutions` while it is in there | rejected, no LaTeX in the replacement |

Your typos, your headings, your section order, and your wrong claims all stay
exactly as you wrote them. If a formula is wrong it gets retyped wrong, and the
terminal tells you why. You fix it.

### 4. Fix your own file

Open vim, fix what the terminal told you. What survives that edit is what you
actually understood, which is the whole reason nothing writes it for you.

### 5. Implement it, run it, write the numbers in yourself

Go build it. Measure it. Type the result into your own markdown.

Nothing in this repo will fill a metrics row for you. A number Claude measured and
a number you measured read identically in six months, and only one of them taught
you anything.

### 6. `/visualise stats`

The only skill that touches a note, and only to add a diagram.

It reads the note, draws what is there, renders the picture and looks at it, then
inserts it next to the prose it explains. Diagrams grow across stages instead of
arriving as one crowded picture.

Your content stays byte-identical. `prose_guard.py` takes a snapshot before the
edit and fails if any line you wrote changed or disappeared:

```
prose_guard FAILED Phase 0/math/stats.md: 1 line(s) he wrote were changed or deleted.
  L17 gone: Two types of distrutions:
```

Additions pass. Rewrites do not.

### 7. Reread, months later

Open Obsidian and read your own note. That is the revision pass, and it does not
need a skill.

## What a note looks like

Whatever you want. There is no template.

The lint enforces nothing about the headings of a note you wrote. It still catches
the things that silently rot a vault: an em dash, an emoji, a wikilink that resolves
to nothing, a duplicate filename, a note no phase MOC links, and a number sitting in
prose with no source next to it.

Front matter is optional. Add it and the note joins the index, the staleness report,
and the dataview tables in the phase MOC:

```
---
type: concept
phase: 0
status: read
aliases: [KV Cache, kv cache, KV caching]
source: https://example.com/the-thing-you-read
code:
---
```

`aliases` is the one field worth the keystrokes, and the lint now insists on it.
Filenames here are kebab-case and wikilinks get typed with spaces, so `kv-cache.md`
needs an alias that reads `kv cache` or `[[KV Cache]]` resolves to nothing. That is
how the other vault ended up with 1214 dead links.

Having *some* alias is not enough. `aliases: [FlashAttention, tiling]` on
`flash-attention.md` still fails, because neither one is the spaced form:

```
no alias matches 'flash attention', so [[Flash Attention]] will not resolve.
```

Run `note_lint.py --aliases` to sweep for it, including notes with no other front
matter.

Leave the front matter out entirely and the note still works as a note. It just will
not show up in a query, in the index, or in the staleness report.

## In one line
## Why must it be this way?
## What does it cost?            <- the metrics table
## What breaks without it?
## Diagram
## In code
## What did implementing correct?
## What does this rest on?
## Sources
```

Papers swap the middle for `## Claim`, `## Method`, `## Results`, and
`## What the numbers do not show`.

Unfinished slots are `%%TODO: ...%%`. Obsidian hides them in preview and
`--todo` lists them.

## The numbers rule

A number in a note lives in the metrics table with a unit and the command that
produced it, or its value is the literal string `needs measuring`:

```markdown
| metric | value | unit | command |
|---|---|---|---|
| tiled fwd, N=4096 | 6.9 | ms | `uv run benchmark.py --impl flash --n 4096` |
| backward pass | needs measuring | - | - |
```

Writing a bare number anywhere else fails the lint. A gate cannot be marked passed
while any row says `needs measuring`. A vendor spec is not a measurement: say so in
the command column.

## Diagrams

Three renderers, picked by what the idea is:

| Idea | Renderer |
|---|---|
| A graph of named things: DAG, dataflow, state machine, layer stack | mermaid, inline fence |
| Geometry or scale: matrix tiling, memory layout, roofline, timeline | SVG in `viz/` |
| You want to hand-edit it later | Excalidraw |

Mermaid is the default: renders in Obsidian and on GitHub, diffs as text, no files.

Diagrams grow in stages rather than arriving as one crowded picture. Stage 1 draws
A to B, stage 2 redraws it adding C. Claude renders every diagram to a raster and
looks at it before embedding, so a backwards arrow gets caught rather than sitting
in your notes for six months.

For an Excalidraw drawing there is one manual step: Claude generates and verifies
the raw `.excalidraw`, then you run the plugin's "Convert *.excalidraw files to
*.excalidraw.md" command once from the command palette. After that Claude edits it
in place.

## Commands

| Command | When | Writes? |
|---|---|---|
| `/study <topic>` | After you have read and written your notes. Teaches the gaps in the terminal. | your math, in LaTeX |
| `/visualise <topic>` | When a note wants a picture. Adds diagrams and nothing else. | diagrams only |

Both fire on plain English too. You do not have to remember the slash.

There is no revise skill. You implement it, you measure it, you type the numbers
into your own file, and rereading the note months later is the revision pass.

## Scripts

```bash
uv run .claude/skills/study/scripts/note_lint.py              # lint everything
uv run .claude/skills/study/scripts/note_lint.py --todo       # every open %%TODO%%
uv run .claude/skills/study/scripts/note_lint.py --unmeasured # every unmeasured number
uv run .claude/skills/study/scripts/note_lint.py --orphans    # notes no phase links
uv run .claude/skills/study/scripts/note_lint.py --aliases    # notes a spaced wikilink cannot reach
uv run .claude/skills/study/scripts/note_lint.py --rough      # notes with no front matter
uv run .claude/skills/study/scripts/prose_guard.py snapshot "<note>"   # before a diagram edit
uv run .claude/skills/study/scripts/prose_guard.py check "<note>"      # proves nothing was rewritten
uv run .claude/skills/study/scripts/note.py index             # the note table
uv run .claude/skills/study/scripts/note.py stale             # what the code outran
uv run .claude/skills/study/scripts/note.py find "kv cache"   # resolve a topic
```

## What runs automatically

Three hooks in `.claude/settings.json`:

- **Every prompt**: Claude gets the standing rule plus the list of existing notes,
  so on turn 40 it still writes notes and still knows not to create a duplicate.
- **Every file write**: the lint runs and failures land in front of Claude with
  line numbers, in the same turn. It fixes them before you see them. Rough notes
  you wrote in vim are exempt, so the lint never fights you mid-thought.
- **Session start**: a staleness report. Notes you read and never implemented, and
  notes whose code has commits newer than the note. So the moment you open Claude
  Code it already knows the code moved and the note did not.

## Layout

```
study_plan.md          the spine, unchanged
HOWTO.md               this file
Phase 0/
  phase-0.md           map of the phase, carries the Gate line and the links
  gate-0.md            the checkpoint, with measured numbers
  math/                notes
  concepts/            ideas
  papers/              one per source
viz/                   generated diagrams and images
.claude/               skills, agents, hooks, scripts
.logs/                 gitignored
```

Phases 1 to 5 get created when you first work in them. Nothing is pre-scaffolded.

## Why the lint exists

Your other vault at `~/personal/wiki` has **1214 wikilinks that resolve to
nothing** across 141 notes. Filenames there are kebab-case, every link is Title
Case, and no note has an `aliases` field. That vault has been silently broken for
four months, and its graph settings hide both orphans and unresolved links, so
nothing ever surfaced it.

This vault requires `aliases` on every note, checks every wikilink, checks that a
phase note links each note, and shows orphans and unresolved links in graph view.
That failure does not get to happen twice.

The same lint can audit the wiki:

```bash
uv run .claude/skills/study/scripts/note_lint.py --vault ~/personal/wiki --links-only
```

## Known limits

- All three render paths are verified on this machine: `excalidraw-render`,
  `rsvg-convert`, and `npx @mermaid-js/mermaid-cli` with Chrome. The mermaid CLI
  pulls a package on first use, so the first call is slow.
- `~/.claude/skills/excalidraw-diagram` documents `uv run python -m excalidraw`,
  which does not exist here. The working binary is `excalidraw-render`. That skill
  is stale and this vault does not use it.
- `.excalidraw.md` generation is manual on first conversion, by design. The wrapper
  format was not verifiable here and a wrapper the plugin silently refuses to parse
  is invisible until you open the note months later.
- There is no spaced repetition and no quiz. The `**Gate:**` lines in
  `study_plan.md` are the review mechanism.
- Nothing logs the conversation. The note is the log, by choice.
- Display math wants `$$` alone on its line with a blank line above and below. The
  lint does not check this, because Obsidian's exact behaviour without the blank
  lines was not verified here.

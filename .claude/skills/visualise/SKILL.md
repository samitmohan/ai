---
description: Adds diagrams to an existing note without changing a word of its content. Use when the user says "visualise", "add a diagram", "draw this", "diagram it", or asks for a picture of something already written up. Content stays byte-identical; only diagram blocks and their embeds get added.
argument-hint: [topic or note path]
allowed-tools: Read Edit Write Glob Grep Bash(uv run ${CLAUDE_PROJECT_DIR}/.claude/skills/study/scripts/note.py *) Bash(uv run ${CLAUDE_PROJECT_DIR}/.claude/skills/study/scripts/prose_guard.py *) Bash(uv run ${CLAUDE_PROJECT_DIR}/.claude/skills/study/scripts/note_lint.py *) Bash(rsvg-convert *) Bash(excalidraw-render *) Bash(npx -y @mermaid-js/mermaid-cli *) Bash(mkdir -p *) Task
---

# visualise

Add diagrams to a note he already wrote. Change nothing else.

His prose stays byte-identical. Not "mostly preserved", not "tidied while I was in
there". Identical. You are inserting pictures into a finished document.

## Order of operations

1. `uv run .claude/skills/study/scripts/note.py find "<topic>"`
2. Read the note in full, so the diagram describes what he actually wrote rather
   than what you would have written.
3. `uv run .claude/skills/study/scripts/prose_guard.py snapshot "<note>"`
4. Decide whether a diagram earns its place. A missing diagram is cheaper than a
   false one. If prose or a single equation already carries it, say so and stop.
5. Draw, per `.claude/skills/study/references/diagrams.md`.
6. Render it and look at the raster. Not optional.
7. Insert with Edit. Only ever additions.
8. `uv run .claude/skills/study/scripts/prose_guard.py check "<note>"` until 0.
9. `uv run .claude/skills/study/scripts/note_lint.py "<note>"` until 0.

## What you may touch

Add a fenced diagram block, a `### Stage N` heading above one, an image embed, and
a single caption line under it. Files in `viz/`.

That is the complete list.

You may not fix a typo, normalise ASCII math to LaTeX, reflow a paragraph, reorder
sections, add or edit a heading, or delete a `%%TODO%%`. If his note says something wrong
next to your diagram, draw what is true and say the mismatch out loud in the
terminal. Do not fix his line.

The guard enforces this by checking that every line he had is still there, in
order. If it fails, restore what you dropped. Do not edit the guard.

## Where the diagram goes

His notes use his own structure, so there is no fixed slot. Put the diagram next to
the prose it explains, which is where it is useful when he rereads.

If the note happens to have a `## Diagram` heading, use it. If that heading holds a
`%%TODO%%`, add the diagram after the marker and leave the marker alone. He deletes
his own scaffolding.

Never add a heading to make room. Work with the shape he wrote.

## Drawing

`references/diagrams.md` carries the rules. The two that decide the outcome:

Grow the diagram across stages. Stage i+1 contains every node from stage i and adds
one to three more. A lone fence with more than seven nodes and no preceding stages
is a crowded diagram, and the lint rejects it.

A diagram is not done until it has been rendered and looked at. Rendering proves
the syntax parsed and says nothing about whether the picture is true. Check, in
order: every arrow points at the thing it names, every label sits on its own shape,
nothing overlaps, no text is clipped. When something is wrong the fix is usually
fewer elements.

## Numbers in a diagram

A number in a label needs the same backing as a number in prose. If he measured it
and it is written in his note, use his figure. If nobody measured it, leave it out
of the label rather than guessing. You never run a benchmark to fill a label. A label reading "429 cycles" that came from nowhere is
worse than a label reading "DRAM".

## Done

Done when the guard exits 0, the lint exits 0, and you have looked at the raster.

# Diagrams

You are the creative director. A diagram is not done until it has been rendered and
looked at.

## Which renderer

| The idea is | Renderer |
|---|---|
| A graph of named things: dependency DAG, dataflow, state machine, call order, layer stack | mermaid |
| Geometry or scale carries meaning: matrix tiling, memory layout, roofline, timeline, bandwidth bars, anything with axes | SVG |
| He said he wants to hand-edit it later | excalidraw |

Default is mermaid. If the choice is not obvious, it is mermaid. Mermaid renders
natively in Obsidian and on GitHub, and it diffs as text in git.

Do not visualise when prose or a single equation already carries it. A missing
diagram is cheaper than a false one.

## Grow the diagram, never one crowded picture

Consecutive fences under sibling `###` headings form a stage sequence. Stage i+1
contains every node from stage i and adds one to three more. Additions only: if a
node disappears you redrew instead of grew.

    ### Stage 1: the round trip
    ```mermaid
    graph LR
      Q[Q] --> S[S = QK.T]
      S --> O[O]
    ```

    ### Stage 2: the SRAM boundary appears
    ```mermaid
    graph LR
      Q[Q] --> S[S = QK.T]
      S --> P[exp of S minus m]
      P --> O[O]
    ```

A lone fence with more than seven nodes and no preceding stages is a crowded
diagram. Split it. The lint checks this.

If your brief lists more than five to seven elements, cut before drawing.

## Verify by looking

Rendering success proves the syntax parsed. It says nothing about whether the
picture is true. Look at the raster and check, in this order: every arrow points at
the thing it names, every label sits on its own shape, nothing overlaps, no text is
clipped.

When something is wrong the fix is usually fewer elements, not more.

SVG:

    rsvg-convert -w 1400 -a viz/<slug>.svg -o /tmp/check.png

Then Read `/tmp/check.png`. Iterate on the SVG, not on the PNG.

Excalidraw:

    excalidraw-render viz/<slug>.excalidraw -o /tmp/check.png

Then Read the PNG. This binary works and is verified. Note that
`python -m excalidraw`, which the personal excalidraw-diagram skill documents, does
not exist on this machine. Use the binary.

Mermaid, for a standalone file rather than an inline fence:

    PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      npx -y @mermaid-js/mermaid-cli -i /tmp/d.mmd -o /tmp/d.png -w 1400

This path is unverified and needs a network install on first use. If it exits
non-zero, write the inline fence anyway, since Obsidian renders it, and say
`unrendered` in chat. Never claim a diagram is verified when it was not.

ImageMagick is not installed. Nothing may depend on `convert` or `magick`.

## Files and embedding

Generated files go in `viz/`, named `<note-slug>-<n>.<ext>`. Obsidian resolves
`![[name.svg]]` by basename anywhere in the vault, so the name must be unique and
the path does not matter.

Embed with a wikilink and a width: `![[kv-cache-1.svg|600]]`.

A raw `.excalidraw` file cannot render in an Obsidian note. It has to be converted
to `.excalidraw.md` by the plugin's own "Convert *.excalidraw files" command. Do not
script that wrapper: the format is unverified here, and a wrapper the plugin
silently refuses to parse is invisible until he opens the note months later.
Generate the raw JSON, render it, verify it, then tell him to run the Convert
command once.

## Excalidraw JSON conventions

Carried over from the personal excalidraw-diagram skill, which got these right:

`roughness: 0` for clean technical diagrams. `fontFamily: 5` (monospace), not 1.
Separate text elements inside boxes rather than bound labels. Arrows point at
things, perpendicular to the target, tip touching it, never overlapping the label.
Title 28-36px, section headers 20-24, body 12-16. Minimum 10px padding inside
boxes, 20-30px between sections.

Palette: green `#2f9e44`/`#b2f2bb`, orange `#f08c00`/`#ffd8a8`, red
`#e03131`/`#ffc9c9`, blue `#1971c2`/`#a5d8ff`, purple `#9c36b5`/`#e599f7`, grey
`#868e96`/`#dee2e6`.

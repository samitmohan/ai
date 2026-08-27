---
type: moc
phase: 0
status: read
aliases: [Phase 0, Pre-req, Prerequisites]
---

# Phase 0: Pre-req

## Gate
**Gate:** nanoGPT trains, typed from an empty file.

Tracked in [[gate-0]].

## Reading
The list lives in [[study_plan]] under Phase 0. Items that have a note:

- [Essential Math](https://alisawuffles.notion.site/math-notes#3737eb87360580b3b555e3c616713286) -> [[discrete-distributions]]
- Napkin math -> [[napkin-math]]

Not yet started: Karpathy Zero to Hero (8 videos, typed by hand), Docker basics,
and the four papers that come after nanoGPT runs.

## Notes
Math: [[discrete-distributions]], [[napkin-math]]

## Repos
`karpathy` at /Users/samit/personal/karpathy for the Zero to Hero pass.

## Status
```dataview
TABLE WITHOUT ID
  file.link AS "Note",
  status AS "Status",
  default(code, "-") AS "Code"
WHERE phase = 0 AND (type = "concept" OR type = "paper")
SORT status ASC, file.name ASC
```

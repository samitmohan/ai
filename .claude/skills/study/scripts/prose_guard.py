#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Proves an edit only added to a note, or only retyped its math in LaTeX.

    uv run prose_guard.py snapshot <note>                before touching the file
    uv run prose_guard.py check    <note>                additions only
    uv run prose_guard.py check    <note> --allow-math   additions plus LaTeX retyping

Default invariant: every line that was in the note before is still in the note
after, in the same order. Additions anywhere are fine. Deleting or reflowing a line
he wrote is not.

With --allow-math a line may be replaced, on two conditions. The replacement has to
contain LaTeX, so the only permitted direction is toward LaTeX and never away. And
both lines have to carry the identical multiset of identifiers and numbers once
LaTeX notation is mapped back to ASCII, so C(n,k) may become \binom{n}{k} while
"p+0 = p" may not become "p".

That second condition is the whole point. Retyping notation preserves every symbol.
Fixing a typo, tightening a sentence, or simplifying an expression does not, and
each of those fails loudly instead of arriving as a surprise in Obsidian.

One exception throughout: a %%TODO ...%% line may disappear, because that is
scaffolding this toolchain put there, not something he typed.

This exists because "do not rewrite his prose" is worthless as an instruction and
enforceable as a check.
"""

from __future__ import annotations

import difflib
import hashlib
import pathlib
import re
import sys

STORE = pathlib.Path("/tmp/prose_guard")


def slot(note: pathlib.Path) -> pathlib.Path:
    key = hashlib.sha256(str(note.resolve()).encode()).hexdigest()[:16]
    return STORE / f"{key}.snap"


def is_scaffold(line: str) -> bool:
    return "%%TODO" in line


# LaTeX notation mapped back to the ASCII he would have typed. A command carrying a
# symbol becomes that symbol; a command that is pure decoration vanishes. Every
# pattern matches a literal backslash, hence the doubled one.
LATEX_TO_ASCII = [
    (r"\\binom\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"C(\1,\2)"),
    (r"\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)"),
    (r"\\(?:mathbb|mathcal|mathrm|operatorname|text|textrm|mathbf|mathit)\s*\{([^{}]*)\}", r"\1"),
    (r"\\(?:cdot|times)\b", "*"),
    (r"\\sum\b", "sum"),
    (r"\\prod\b", "prod"),
    (r"\\sqrt\b", "sqrt"),
    (r"\\infty\b", "inf"),
    (r"\\lambda\b", "lambda"),
    (r"\\mu\b", "mu"),
    (r"\\sigma\b", "sigma"),
    (r"\\neq\b", "!="),
    (r"\\leq\b", "<="),
    (r"\\geq\b", ">="),
    (r"\\approx\b", "~="),
    (r"\\(?:to|rightarrow|implies|Longrightarrow)\b", "->"),
    (r"\\(?:left|right|quad|qquad|displaystyle|dots|ldots|cdots)\b", " "),
    (r"\\[,;:!]", " "),
    (r"\\\\", " "),
]

TOKEN = re.compile(r"[A-Za-z]+|\d+")


def canon(line: str) -> list[str]:
    """The identifiers and numbers a line carries, notation stripped away."""
    t = line
    for pat, rep in LATEX_TO_ASCII:
        t = re.sub(pat, rep, t)
    t = t.replace("$", " ")
    return sorted(TOKEN.findall(t))


def has_latex(line: str) -> bool:
    return "$" in line or "\\" in line


def math_swap(old: str, new: str) -> tuple[bool, str]:
    """Is `new` the same math as `old`, retyped in LaTeX?"""
    if not has_latex(new):
        return False, "replacement carries no LaTeX, so this is a prose rewrite"
    a, b = canon(old), canon(new)
    if a != b:
        lost = sorted({t for t in a if a.count(t) > b.count(t)})
        gained = sorted({t for t in b if b.count(t) > a.count(t)})
        bits = []
        if lost:
            bits.append(f"dropped {lost}")
        if gained:
            bits.append(f"invented {gained}")
        return False, "; ".join(bits) or "symbols differ"
    return True, ""


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2 or args[0] not in ("snapshot", "check"):
        print(__doc__, file=sys.stderr)
        return 2
    cmd, note = args[0], pathlib.Path(args[1])

    if cmd == "snapshot":
        if not note.exists():
            print(f"prose_guard: {note} does not exist, nothing to protect")
            return 0
        STORE.mkdir(parents=True, exist_ok=True)
        slot(note).write_text(note.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"prose_guard: snapshot taken, {note.name}")
        return 0

    snap = slot(note)
    if not snap.exists():
        print(
            f"prose_guard: no snapshot for {note}. Take one BEFORE editing:\n"
            f"  uv run prose_guard.py snapshot {note}",
            file=sys.stderr,
        )
        return 2

    allow_math = "--allow-math" in sys.argv
    old = snap.read_text(encoding="utf-8").splitlines()
    new = note.read_text(encoding="utf-8").splitlines()

    failures: list[str] = []
    conversions: list[tuple[str, str]] = []

    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, old, new, autojunk=False
    ).get_opcodes():
        if tag in ("equal", "insert"):
            continue
        cands = new[j1:j2]
        for n, line in enumerate(old[i1:i2], i1 + 1):
            if is_scaffold(line):
                continue
            if not line.strip() and any(not c.strip() for c in cands):
                continue
            if not allow_math:
                failures.append(f"  L{n} gone: {line[:100]}")
                continue
            hit = next((c for c in cands if math_swap(line, c)[0]), None)
            if hit is not None:
                conversions.append((line, hit))
                continue
            why = "nothing replaced it"
            for c in cands:
                ok, reason = math_swap(line, c)
                if not ok and reason:
                    why = reason
                    break
            shown = cands[0][:96] if cands else "<deleted>"
            failures.append(
                f"  L{n} {why}\n      was: {line.strip()[:96]}\n      now: {shown}"
            )

    if conversions:
        print(
            f"prose_guard: {len(conversions)} math line(s) retyped in LaTeX, every "
            f"symbol preserved:"
        )
        for a, b in conversions[:40]:
            print(f"  was: {a.strip()[:96]}")
            print(f"  now: {b.strip()[:96]}")

    if failures:
        head = (
            f"changed in a way that is not a LaTeX retype."
            if allow_math
            else f"changed or deleted. Additions are allowed, rewrites are not."
        )
        print(
            f"\nprose_guard FAILED {note}: {len(failures)} line(s) he wrote were "
            f"{head}",
            file=sys.stderr,
        )
        for f in failures[:20]:
            print(f, file=sys.stderr)
        print("\nRestore them. Do not edit this guard.", file=sys.stderr)
        return 1

    print(
        f"prose_guard clean: {note.name}, nothing he wrote was lost "
        f"({len(new) - len(old):+d} lines net)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

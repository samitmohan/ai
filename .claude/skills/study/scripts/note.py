#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Vault index, note resolution, and staleness, for the hooks and the skills.

uv run note.py context          UserPromptSubmit: standing rule plus the note index
uv run note.py stale            SessionStart: notes the code has moved out from under
uv run note.py find "<query>"   resolve a topic to a note path, exit 3 on ambiguity
uv run note.py index            print the note table
"""

from __future__ import annotations

import datetime as dt
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(
    os.environ.get("CLAUDE_PROJECT_DIR") or "/Users/samit/personal/learning"
).resolve()
REPO_HOME = pathlib.Path.home() / "personal"
STALE_DAYS = 14

STANDING_RULE = """\
LEARNING VAULT. You are in the Obsidian vault at {root}.

The notes are HIS. He writes them and he structures them. Do not rewrite a note, do
not reformat one, do not impose a section skeleton, and do not fix his spelling.

The terminal explanation is the deliverable. Use the study skill: it reads his note,
teaches the gaps in chat, and writes exactly one thing, his math retyped in LaTeX
with every symbol preserved.

Two skills may touch a note and both are fenced by prose_guard.py, which fails if a
line he wrote changed in any other way: study for math notation, visualise for
diagrams.

He measures his own numbers and types them into his own file. Never fill a metrics
row for him and never invent a benchmark, latency, bandwidth, or memory figure.

Run note_lint.py on any note you touch."""


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or ":" not in line or line[0] in " \t-#":
            continue
        key, _, val = line.partition(":")
        out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def is_note_path(p: pathlib.Path) -> bool:
    """Notes live under Phase N/ or side-tracks/. Root files are the spine."""
    parts = p.relative_to(ROOT).parts
    return len(parts) > 1 and (
        parts[0].startswith("Phase ") or parts[0] == "side-tracks"
    )


def all_md() -> list[tuple[pathlib.Path, dict[str, str]]]:
    out = []
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if ".git" in rel.parts or any(part.startswith(".") for part in rel.parts):
            continue
        fm = frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        out.append((p, fm))
    return out


def notes() -> list[tuple[pathlib.Path, dict[str, str]]]:
    """Structured notes only: those that already declare a type."""
    return [(p, fm) for p, fm in all_md() if fm.get("type")]


def rough() -> list[pathlib.Path]:
    """Notes with no front matter. His own structure, which is the default."""
    return [p for p, fm in all_md() if not fm.get("type") and is_note_path(p)]


def aliases(fm: dict[str, str]) -> list[str]:
    raw = fm.get("aliases", "").strip()
    if raw.startswith("["):
        raw = raw[1:-1]
    return [a.strip().strip('"').strip("'") for a in raw.split(",") if a.strip()]


def cmd_context() -> int:
    print(STANDING_RULE.format(root=ROOT))
    rows = notes()
    if not rows:
        print(
            "\nThe vault has no notes yet. The next explanation creates the first one."
        )
        return 0
    print(f"\nExisting notes ({len(rows)}). Extend, do not duplicate:")
    for p, fm in rows:
        al = aliases(fm)
        extra = f"  aka {', '.join(al[1:])}" if len(al) > 1 else ""
        print(f"  {p.relative_to(ROOT)}  [{fm.get('type')}/{fm.get('status')}]{extra}")
    r = rough()
    if r:
        print(f"\nNotes carrying no front matter ({len(r)}). His own structure.")
        print("Read them, teach the gaps in chat, change nothing:")
        for p in r:
            print(f"  {p.relative_to(ROOT)}")
    return 0


def git_last_commit_iso(repo: pathlib.Path, rel: str) -> str | None:
    r = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%cI", "--", rel],
        capture_output=True,
        text=True,
        check=False,
    )
    return r.stdout.strip() or None


def cmd_stale() -> int:
    today = dt.datetime.now(dt.UTC).date()
    read_stale: list[str] = []
    code_moved: list[str] = []
    code_gone: list[str] = []

    for p, fm in notes():
        if fm.get("type") not in ("concept", "paper"):
            continue
        rel = p.relative_to(ROOT)
        if fm.get("status") == "read":
            mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.UTC).date()
            age = (today - mtime).days
            if age >= STALE_DAYS:
                read_stale.append(f"  {rel}  read {age} days ago, never implemented")
        code = fm.get("code", "")
        if not code or code in ("null", "~"):
            continue
        target = REPO_HOME / code
        if not target.exists():
            code_gone.append(f"  {rel}  code: {code} no longer exists")
            continue
        parts = pathlib.Path(code).parts
        repo = REPO_HOME / parts[0]
        inner = str(pathlib.Path(*parts[1:]))
        last = git_last_commit_iso(repo, inner)
        revised = fm.get("revised") or fm.get("passed") or ""
        if last and re.fullmatch(r"\d{4}-\d{2}-\d{2}", revised) and last[:10] > revised:
            code_moved.append(
                f"  {rel}  {code} changed {last[:10]}, note revised {revised}"
            )

    if not (read_stale or code_moved or code_gone):
        return 0
    print("STALENESS REPORT for the learning vault:")
    if code_gone:
        print("\nBroken code links, the file was renamed or deleted:")
        print("\n".join(code_gone))
    if code_moved:
        print("\nThe code moved and the note did not. His call, not Claude's:")
        print("\n".join(code_moved))
    if read_stale:
        print(f"\nRead but never implemented for {STALE_DAYS}+ days:")
        print("\n".join(read_stale))
    print("\nReport only. Do not edit a note to resolve any line above.")
    return 0


def cmd_find(query: str) -> int:
    q = query.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", q).strip("-")
    exact: list[pathlib.Path] = []
    fuzzy: list[pathlib.Path] = []
    candidates = [(p, fm) for p, fm in all_md() if fm.get("type") or is_note_path(p)]
    for p, fm in candidates:
        stem = p.name[:-3].lower()
        names = [stem, *[a.lower() for a in aliases(fm)]]
        src = fm.get("source", "").lower()
        is_exact = (src and q == src) or q in names or slug == stem
        is_fuzzy = (slug and (slug in stem or stem in slug)) or any(
            w in stem for w in slug.split("-") if len(w) > 3
        )
        if is_exact:
            exact.append(p)
        elif is_fuzzy:
            fuzzy.append(p)

    roughs = set(rough())

    def show(p: pathlib.Path) -> str:
        tag = "  his own structure, teach the gaps and do not rewrite" if p in roughs else ""
        return f"{p.relative_to(ROOT)}{tag}"

    if len(exact) == 1:
        print(show(exact[0]))
        return 0
    hits = exact or fuzzy
    if not hits:
        print(f"no note matches {query!r}. Create one.")
        return 1
    if len(hits) == 1:
        print(show(hits[0]))
        return 0
    print(f"ambiguous, {len(hits)} candidates. Ask which one:")
    for p in hits:
        print(f"  {show(p)}")
    return 3


def cmd_index() -> int:
    for p, fm in notes():
        print(f"{fm.get('type'):8} {fm.get('status'):12} {p.relative_to(ROOT)}")
    for p in rough():
        print(f"{'note':8} {'his own':12} {p.relative_to(ROOT)}")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    match sys.argv[1]:
        case "context":
            return cmd_context()
        case "stale":
            return cmd_stale()
        case "find":
            if len(sys.argv) < 3:
                print("find needs a query")
                return 1
            return cmd_find(" ".join(sys.argv[2:]))
        case "index":
            return cmd_index()
        case other:
            print(f"unknown subcommand {other!r}")
            return 1


if __name__ == "__main__":
    sys.exit(main())

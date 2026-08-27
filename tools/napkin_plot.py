#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Draws the measured memory curves as SVG. Data is pasted from one run of
napkin_mem.c, so the pictures and the note carry the same numbers.

    uv run tools/napkin_plot.py hierarchy > viz/napkin-math-1.svg
    uv run tools/napkin_plot.py stride    > viz/napkin-math-2.svg
"""

import math
import sys

# working set in KiB -> pointer-chase load latency in ns
# cc -O2 -o /tmp/napkin_mem tools/napkin_mem.c && /tmp/napkin_mem
DATA = [
    (4, 0.91), (16, 0.91), (32, 0.91), (64, 0.92), (128, 0.91),
    (256, 4.70), (512, 5.64), (1024, 4.86), (2048, 4.85), (4096, 6.60),
    (8192, 6.76), (16384, 16.87), (32768, 70.96), (65536, 90.29),
    (131072, 93.27), (262144, 96.82), (524288, 97.08), (1048576, 98.58),
]

# pages live -> load latency in ns, one cache line touched per page.
# SPREAD picks a random line inside each page; ZERO always picks line 0, so every
# address shares its cache set-index bits.
SPREAD = [
    (16, 0.91), (64, 0.91), (256, 2.28), (1024, 3.48), (2048, 5.45),
    (3072, 6.86), (4096, 12.19), (8192, 12.56), (16384, 14.88),
    (32768, 13.31), (65536, 13.51),
]
ZERO = [
    (16, 3.88), (64, 4.26), (256, 6.40), (1024, 16.94), (2048, 26.87),
    (3072, 28.51), (4096, 32.05), (8192, 32.28), (16384, 42.74),
    (32768, 85.60), (65536, 97.84),
]
CLOCK_NS = 0.227

W, H = 960, 540
L, R, T, B = 92, 26, 78, 66
PW, PH = W - L - R, H - T - B

XMIN, XMAX = math.log2(4), math.log2(1048576)
YMIN, YMAX = math.log10(0.7), math.log10(200)


def x(kib):
    return L + (math.log2(kib) - XMIN) / (XMAX - XMIN) * PW


def y(ns):
    return T + PH - (math.log10(ns) - YMIN) / (YMAX - YMIN) * PH


def frame(title, subtitle, xlabel):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace">',
        f'<rect width="{W}" height="{H}" fill="#fbfbf9"/>',
        f'<text x="{L}" y="30" font-size="17" font-weight="600" fill="#1a1a1a">'
        f'{title}</text>',
        f'<text x="{L}" y="52" font-size="12.5" fill="#777">{subtitle}</text>',
    ]


def grid(out, xticks, xlabel):
    for ns in (1, 2, 5, 10, 20, 50, 100, 200):
        yy = y(ns)
        out.append(f'<line x1="{L}" y1="{yy:.1f}" x2="{L+PW}" y2="{yy:.1f}" '
                   f'stroke="#e3e3de" stroke-width="1"/>')
        out.append(f'<text x="{L-10}" y="{yy+4:.1f}" font-size="12" fill="#666" '
                   f'text-anchor="end">{ns} ns</text>')
    for pos, lab in xticks:
        xx = x(pos)
        out.append(f'<line x1="{xx:.1f}" y1="{T}" x2="{xx:.1f}" y2="{T+PH}" '
                   f'stroke="#e3e3de" stroke-width="1"/>')
        out.append(f'<text x="{xx:.1f}" y="{T+PH+20}" font-size="12" fill="#666" '
                   f'text-anchor="middle">{lab}</text>')
    out.append(f'<text x="{L+PW/2:.0f}" y="{H-16}" font-size="13" fill="#333" '
               f'text-anchor="middle">{xlabel}</text>')


def series(out, data, colour, scale=1.0):
    pts = " ".join(f"{x(k*scale):.1f},{y(v):.1f}" for k, v in data)
    out.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" '
               f'stroke-width="2.5"/>')
    for k, v in data:
        out.append(f'<circle cx="{x(k*scale):.1f}" cy="{y(v):.1f}" r="3.4" '
                   f'fill="{colour}"/>')


def stride():
    """Same data footprint, same page count. Only the address bits differ."""
    # x axis is pages live, mapped onto the same log grid by treating one page as
    # one unit of the KiB axis.
    out = frame(
        "Address bits, not working set: one cache line touched per page",
        "8 MiB of data either way. Offset 0 in every page shares the cache "
        "set-index bits and reads like DRAM.",
        "pages live, one cache line touched in each (log scale)",
    )
    # 16 pages sits at the left edge, so scale page counts onto the shared axis.
    sc = 0.25
    grid(out, [(4, "16"), (16, "64"), (64, "256"), (256, "1024"),
               (1024, "4096"), (4096, "16384"), (16384, "65536")],
         "pages live, one cache line touched in each (log scale)")
    xx = x(3072 * sc)
    out.append(f'<line x1="{xx:.1f}" y1="{T+8}" x2="{xx:.1f}" y2="{T+PH}" '
               f'stroke="#e03131" stroke-width="1.5" stroke-dasharray="5 4"/>')
    out.append(f'<text x="{xx-10:.1f}" y="{y(150):.1f}" font-size="12.5" '
               f'fill="#e03131" text-anchor="end">L2 TLB reach, ~3072 entries '
               f'&#8594;</text>')
    series(out, ZERO, "#e8590c", sc)
    series(out, SPREAD, "#1971c2", sc)
    out.append(f'<text x="{x(65536 * sc):.1f}" y="{y(97.84)-14:.1f}" '
               f'font-size="13" font-weight="600" fill="#e8590c" '
               f'text-anchor="end">offset 0: 97.84 ns</text>')
    out.append(f'<text x="{x(65536 * sc):.1f}" y="{y(13.51)+26:.1f}" '
               f'font-size="13" font-weight="600" fill="#1971c2" '
               f'text-anchor="end">random offset: 13.51 ns</text>')
    out.append("</svg>")
    return out


out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">',
    f'<rect width="{W}" height="{H}" fill="#fbfbf9"/>',
    f'<text x="{L}" y="30" font-size="17" font-weight="600" fill="#1a1a1a">'
    f'Load latency vs working set, Apple M4 P-core, random pointer chase</text>',
    f'<text x="{L}" y="52" font-size="12.5" fill="#777">clock period 0.227 ns, '
    f'measured from a dependent add chain, so the cycle counts need no vendor '
    f'spec</text>',
]

# y grid at each decade-ish tick
for ns in (1, 2, 5, 10, 20, 50, 100, 200):
    yy = y(ns)
    out.append(f'<line x1="{L}" y1="{yy:.1f}" x2="{L+PW}" y2="{yy:.1f}" '
               f'stroke="#e3e3de" stroke-width="1"/>')
    out.append(f'<text x="{L-10}" y="{yy+4:.1f}" font-size="12" fill="#666" '
               f'text-anchor="end">{ns} ns</text>')

# x grid every power of 4
for kib, lab in [(4, "4 KiB"), (16, "16 K"), (64, "64 K"), (256, "256 K"),
                 (1024, "1 MiB"), (4096, "4 M"), (16384, "16 M"),
                 (65536, "64 M"), (262144, "256 M"), (1048576, "1 GiB")]:
    xx = x(kib)
    out.append(f'<line x1="{xx:.1f}" y1="{T}" x2="{xx:.1f}" y2="{T+PH}" '
               f'stroke="#e3e3de" stroke-width="1"/>')
    out.append(f'<text x="{xx:.1f}" y="{T+PH+20}" font-size="12" fill="#666" '
               f'text-anchor="middle">{lab}</text>')

out.append(f'<text x="{L+PW/2:.0f}" y="{H-16}" font-size="13" fill="#333" '
           f'text-anchor="middle">working set (log scale)</text>')

# the two cliffs, drawn before the curve so the curve sits on top
# Labels run vertically beside their line so nothing can collide with the curve.
for kib, label, frac in [(128, "L1d ends, 128 KiB", 0.55),
                         (16384, "L2 ends, 16 MiB", 0.86)]:
    xx = x(kib)
    out.append(f'<line x1="{xx:.1f}" y1="{T+8}" x2="{xx:.1f}" y2="{T+PH}" '
               f'stroke="#e03131" stroke-width="1.5" stroke-dasharray="5 4"/>')
    ym = T + PH * frac
    out.append(f'<text x="{xx-7:.1f}" y="{ym:.1f}" font-size="12.5" '
               f'fill="#e03131" text-anchor="middle" '
               f'transform="rotate(-90 {xx-7:.1f} {ym:.1f})">{label}</text>')

pts = " ".join(f"{x(k):.1f},{y(v):.1f}" for k, v in DATA)
out.append(f'<polyline points="{pts}" fill="none" stroke="#1971c2" '
           f'stroke-width="2.5"/>')
for k, v in DATA:
    out.append(f'<circle cx="{x(k):.1f}" cy="{y(v):.1f}" r="3.4" fill="#1971c2"/>')

# plateau callouts: value, and the same value in cycles
for kib, ns, name, ox, oy, anchor in [
    (128, 0.91, "L1 hit", -16, -14, "end"),
    (256, 4.70, "L2 hit", -4, -20, "start"),
    (1048576, 96.82, "DRAM plateau", 0, -24, "end"),
]:
    cyc = ns / CLOCK_NS
    out.append(f'<text x="{x(kib)+ox:.1f}" y="{y(ns)+oy:.1f}" font-size="13.5" '
               f'font-weight="600" fill="#1a1a1a" text-anchor="{anchor}">'
               f'{name} {ns:.2f} ns = {cyc:.0f} cycles</text>')

out.append("</svg>")

if len(sys.argv) > 1 and sys.argv[1] == "stride":
    out = stride()
sys.stdout.write("\n".join(out) + "\n")

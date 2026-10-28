#!/usr/bin/env python3
"""
build_work.py
Selected Work (one SVG per project so each card is a link) and the Live Stats row
for the structured layout. Stats come from assets/src/stats.json (fetch_stats.py).
"""
import json, os
from build_header import DAY, FG, LN, MONTH, SRC, TODAY, box, hline, svg, twinkle, vline, write
from build_sections import art, pan, strip, tag

import textwrap

STATS = json.load(open(os.path.join(SRC, "stats.json")))
WORK_ART, OSS_ART = [15, 10, 13, 17], [14, 18, 6, 9]

def describe(r, width):
    """Sub-heading plus wrapped description (max 3 lines) for a live repo entry."""
    langs = r.get("langs") or []
    sub = " / ".join(l.upper() for l in langs[:3]) or "REPOSITORY"
    text = r.get("desc", "").strip() or f"Recently active{' ' + langs[0] if langs else ''} project. Open the repo for the latest work."
    lines = textwrap.wrap(text.replace("&", "&amp;"), width)
    if len(lines) > 3: lines = lines[:3]; lines[2] = lines[2][:width - 3].rstrip() + "..."
    return sub.replace("&", "&amp;"), lines

def tags(r):
    return [t.upper().replace("&", "&amp;") for t in dict.fromkeys((r.get("langs") or [])[:3] + (r.get("topics") or [])[:2])][:5]

GAP = 12

def chips(x, y, labels, maxx):
    out = ""
    for l in labels:
        w = len(l) * 12.6 + 26
        if x + w > maxx: x = 0; y += 46
        out += f'{box(x, y, round(w), 34)}<text x="{x+13}" y="{y+23.5}" font-size="18.5" letter-spacing="1">{l}</text>'
        x += w + 10
    return out

def cards(key, prefix, label, arts, third):
    """Two-up horizontal cards for live repo data. Sizes here are final (not scaled)."""
    from PIL import Image
    H = 470; cw = (2000 - 80 - GAP) // 2; aw = 300
    for k in range(4):
        r = (STATS.get(key) or [])[k:k + 1]
        left = 40 if k % 2 == 0 else GAP // 2; right = GAP // 2 if k % 2 == 0 else 40
        W = left + cw + right; x = left
        if not r:
            write(f"{prefix}-{k+1}.svg", svg(W, H + 20, "", scale=False)); continue
        r = r[0]; n = arts[k]; tx = x + aw + 30; avail = cw - aw - 54
        sub, desc = describe(r, int(avail / 13.8))
        iw, ih = Image.open(os.path.join(SRC, f"art-{n}.jpg")).size
        sc = max(aw / iw, (H - 2) / ih); sw_, sh_ = iw * sc, ih * sc
        axis = "0 0;0 -%d;0 0" % (sh_ - H + 2) if sh_ > H else "0 0;-%d 0;0 0" % max(sw_ - aw, 1)
        fs = min(52, avail / (0.6 * max(len(r["name"]), 1)))
        stat = lambda i, v, l: (f'<text x="{tx+i*190}" y="322" font-size="{44 if len(str(v)) < 6 else 28}" letter-spacing="-1">{v}</text>'
                                f'<text x="{tx+i*190}" y="350" font-size="16" letter-spacing="2.5" opacity="0.6">{l}</text>')
        third_v, third_l = third(r)
        defs = f'<clipPath id="a"><rect x="{x+1}" y="11" width="{aw-1}" height="{H-2}"/></clipPath>'
        body = (f'{box(x, 10, cw, H)}<g clip-path="url(#a)"><g>{pan(axis, 40 + k * 5)}<image href="{art(n, None, 72)}" x="{x+1}" y="11" width="{sw_:.0f}" height="{sh_:.0f}"/></g></g>{vline(x+aw, 10, 10+H)}'
                f'{tag(x+14, 24, f"{k+1:02d} / {label}")}'
                f'<text x="{tx}" y="84" font-size="{fs:.0f}">{r["name"]}</text>'
                f'<text x="{tx}" y="118" font-size="17" letter-spacing="2.5" opacity="0.6">{sub}</text>{hline(tx, x+cw-24, 142, 0.45)}'
                + "".join(f'<text x="{tx}" y="{184+i*34}" font-size="23" opacity="0.9">{l}</text>' for i, l in enumerate(desc)) +
                stat(0, third_v, third_l) + stat(1, r["stars"], "STARS") + stat(2, r["pushed"] or "-", "LAST PUSH") +
                f'{hline(tx, x+cw-24, 372, 0.45)}<g transform="translate({tx} 386)">{chips(0, 0, tags(r), avail)}</g>'
                f'<text x="{x+cw-24}" y="{H-2}" font-size="17" letter-spacing="3" text-anchor="end">OPEN REPO -&gt;<animate attributeName="opacity" values="0.55;1;0.55" dur="3.2s" begin="{k*0.5}s" repeatCount="indefinite"/></text>')
        write(f"{prefix}-{k+1}.svg", svg(W, H + 20, body, defs, scale=False))

def work_cards(): cards("work", "work", "PROJECT", WORK_ART, lambda r: ((r.get("langs") or ["-"])[0].upper(), "MAIN LANG"))
def oss_cards(): cards("oss", "oss", "OPEN SOURCE", OSS_ART, lambda r: (r["mine"], "MY COMMITS"))

def work_strip():
    right = '<text x="1498" y="59" font-size="17" letter-spacing="3" text-anchor="middle">MOST RECENT PUSHES</text>'
    write("section-work.svg", svg(2000, 100, strip("04", "RECENT WORK", right)))

def oss_strip():
    right = '<text x="1498" y="59" font-size="17" letter-spacing="3" text-anchor="middle">RECENT CONTRIBUTIONS</text>'
    write("section-oss.svg", svg(2000, 100, strip("05", "OPEN SOURCE", right)))

def num(n): return f"{n:,}"

def stats():
    s = json.load(open(os.path.join(SRC, "stats.json")))
    Y = 100; H = 330
    right = (f'<circle cx="1300" cy="53" r="5" fill="#fff"><animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite"/></circle>'
             f'<text x="1322" y="59" font-size="17" letter-spacing="3">SYNCED DAILY / {TODAY.isoformat()} UTC</text>')
    cells = [("CONTRIBUTIONS / 1 YR", num(s["contributions"])), ("COMMITS", num(s["commits"])),
             ("PULL REQUESTS", num(s["prs"])), ("CURRENT STREAK", f'{s["streak"]}D')]
    big = ""
    for i, (lab, val) in enumerate(cells):
        cx = 40 + (i % 2) * 290; cy = Y + (i // 2) * 165
        big += (f'{box(cx, cy, 290, 165)}<text x="{cx+22}" y="{cy+34}" font-size="12.5" letter-spacing="2.5" opacity="0.6">{lab}</text>'
                f'<text x="{cx+22}" y="{cy+112}" font-size="62" letter-spacing="-1">{val}</text>')
    # heatmap
    days = s["days"]; weeks = [days[i:i + 7] for i in range(0, len(days), 7)][-53:]
    nz = sorted(d for d in days if d > 0); q = [nz[int(len(nz) * p)] for p in (0.25, 0.5, 0.75)] if nz else [1, 2, 3]
    def lvl(c): return 0 if c == 0 else 1 + sum(c > t for t in q)
    op = [0.09, 0.3, 0.52, 0.76, 1]
    hx, hy, cs = 700, Y + 74, 16
    hm = "".join(f'<rect x="{hx+wi*cs}" y="{hy+di*cs}" width="12" height="12" fill="#fff" opacity="{op[lvl(c)]}"/>'
                 for wi, w in enumerate(weeks) for di, c in enumerate(w))
    mask = "".join(f'<rect x="{hx+wi*cs}" y="{hy+di*cs}" width="12" height="12" fill="#fff"/>' for wi, w in enumerate(weeks) for di, _ in enumerate(w))
    wk = [sum(w) for w in weeks]; mx = max(wk) or 1
    bars = "".join(f'<rect x="{hx+i*cs}" y="{Y+H-34-t}" width="12" height="{t}" fill="#fff" opacity="0.8">'
                   f'<animate attributeName="height" values="0;{t};{t}" keyTimes="0;0.25;1" dur="9s" begin="{i*0.03:.2f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="y" values="{Y+H-34};{Y+H-34-t};{Y+H-34-t}" keyTimes="0;0.25;1" dur="9s" begin="{i*0.03:.2f}s" repeatCount="indefinite"/></rect>'
                   for i, t in ((i, max(2, round(c / mx * 70))) for i, c in enumerate(wk)))
    langs = "".join(
        f'<text x="1626" y="{Y+96+i*46}" font-size="14.5" letter-spacing="1">{n.upper()}</text><text x="1930" y="{Y+96+i*46}" font-size="14.5" text-anchor="end" opacity="0.7">{p}%</text>'
        f'{box(1626, Y+106+i*46, 290, 8)}<rect x="1626" y="{Y+106+i*46}" height="8" fill="#fff" width="{max(3, 290*p/100):.0f}">'
        f'<animate attributeName="width" values="0;{max(3, 290*p/100):.0f};{max(3, 290*p/100):.0f}" keyTimes="0;0.2;1" dur="8s" begin="{i*0.25}s" repeatCount="indefinite"/></rect>'
        for i, (n, p) in enumerate(s["langs"]))
    defs = ('<mask id="hm" maskUnits="userSpaceOnUse" x="700" y="%d" width="860" height="120">%s</mask>'
            '<linearGradient id="sw" gradientUnits="userSpaceOnUse" x1="-120" x2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.65"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            '<animateTransform attributeName="gradientTransform" type="translate" values="700 0;1700 0;1700 0" keyTimes="0;0.45;1" dur="7s" repeatCount="indefinite"/></linearGradient>') % (hy, mask)
    body = (f'{strip("06", "LIVE STATS", right)}{big}'
            f'{box(660, Y, 920, H)}<text x="{hx}" y="{Y+38}" font-size="13" letter-spacing="3" opacity="0.6">CONTRIBUTION MAP / LAST 12 MONTHS</text>'
            f'{hm}<rect x="700" y="{hy}" width="860" height="112" fill="url(#sw)" mask="url(#hm)"/>'
            f'<text x="{hx}" y="{Y+H-122}" font-size="13" letter-spacing="3" opacity="0.6">WEEKLY ACTIVITY</text>{bars}'
            f'{box(1600, Y, 360, H)}<text x="1626" y="{Y+38}" font-size="13" letter-spacing="3" opacity="0.6">TOP LANGUAGES</text>{twinkle(1930, Y+30, 8, 3.4)}{langs}'
            f'<text x="1626" y="{Y+H-6}" font-size="11.5" letter-spacing="1" opacity="0.45">PUBLIC NON-FORK REPOS / BY BYTES</text>')
    write("section-stats.svg", svg(2000, Y + H + 20, body, defs))

if __name__ == "__main__":
    work_strip(); work_cards(); oss_strip(); oss_cards(); stats()

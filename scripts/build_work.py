#!/usr/bin/env python3
"""
build_work.py
Selected Work (one SVG per project so each card is a link) and the Live Stats row
for the structured layout. Stats come from assets/src/stats.json (fetch_stats.py).
"""
import json, os
from build_header import DAY, FG, LN, MONTH, SRC, TODAY, box, hline, svg, twinkle, vline, write
from build_sections import art, pan, strip, tag

PROJECTS = [
    ("op-caelestia-shell", "WAYLAND DESKTOP SHELL", ["Fluid, morphing desktop shell for Wayland.", "Zero-latency interaction, dynamic animation", "and an ergonomic developer workspace."], ["QML", "C++", "GLSL", "WAYLAND"], 15),
    ("PocketFix", "FULL-STACK TASK &amp; WORKFLOW APP", ["Production-ready full-stack app built for", "efficient, reliable task coordination."], ["NEXT.JS", "TYPESCRIPT", "POSTGRESQL"], 10),
    ("Marg", "LOGISTICS &amp; DISPATCH PLATFORM", ["Freight dispatch, real-time tracking and", "route management in one platform."], ["NEXT.JS", "TYPESCRIPT", "PYTHON"], 13),
    ("QuizSolver", "ASSESSMENT AUTOMATION", ["Parses and evaluates structured", "assessments with automation scripts."], ["PYTHON", "AUTOMATION"], 17),
]
GAP = 12
CARD_W = (2000 - 80 - 3 * GAP) // 4          # 471

def chips(x, y, labels, maxx):
    out = ""
    for l in labels:
        w = len(l) * 8.4 + 22
        if x + w > maxx: x = 0; y += 34
        out += f'{box(x, y, round(w), 25)}<text x="{x+11}" y="{y+17.5}" font-size="12.5" letter-spacing="1">{l}</text>'
        x += w + 8
    return out

def work_cards():
    H = 600; ART_H = 250
    for k, (name, sub, desc, tech, n) in enumerate(PROJECTS):
        left = 40 if k == 0 else GAP // 2
        right = 40 if k == 3 else GAP // 2
        W = left + CARD_W + right; x = left
        im = art(n, None, 72)
        from PIL import Image
        iw, ih = Image.open(os.path.join(SRC, f"art-{n}.jpg")).size
        sh = ih * CARD_W / iw; shift = max(sh - ART_H, 0) * 0.6
        defs = f'<clipPath id="a"><rect x="{x+1}" y="11" width="{CARD_W-2}" height="{ART_H-2}"/></clipPath>'
        txt = "".join(f'<text x="{x+26}" y="{ART_H+138+i*23}" font-size="15.5" opacity="0.88">{l}</text>' for i, l in enumerate(desc))
        body = (f'{box(x, 10, CARD_W, H-20)}<g clip-path="url(#a)"><g>{pan(f"0 0;0 -{shift:.0f};0 0", 36 + k*6)}'
                f'<image href="{im}" x="{x+1}" y="11" width="{CARD_W-2}" height="{sh:.0f}"/></g></g>{hline(x, x+CARD_W, 10+ART_H)}'
                f'{tag(x+14, 24, f"{k+1:02d} / PROJECT")}'
                f'<text x="{x+26}" y="{ART_H+58}" font-size="30" letter-spacing="0.5">{name}</text>'
                f'<text x="{x+26}" y="{ART_H+86}" font-size="12.5" letter-spacing="2.5" opacity="0.6">{sub}</text>{hline(x+26, x+CARD_W-26, ART_H+104, 0.45)}{txt}'
                f'<g transform="translate({x+26} {H-130})">{chips(0, 0, tech, CARD_W-52)}</g>'
                f'<text x="{x+CARD_W-26}" y="{H-36}" font-size="14" letter-spacing="3" text-anchor="end">OPEN REPO -&gt;'
                f'<animate attributeName="opacity" values="0.55;1;0.55" dur="3.2s" begin="{k*0.5}s" repeatCount="indefinite"/></text>')
        write(f"work-{k+1}.svg", svg(W, H, body, defs))

def work_strip():
    right = '<text x="1498" y="59" font-size="17" letter-spacing="3" text-anchor="middle">PRODUCTS + OPEN SOURCE + AUTOMATION</text>'
    write("section-work.svg", svg(2000, 100, strip("04", "SELECTED WORK", right)))

OSS_META = {
    "Cero-Terminal": ("TERMINAL + LOCAL AI + .FLOW FILES", ["A terminal that takes requests in plain language", "and runs .flow setup files on macOS, Windows and", "Linux. Built-in local AI model, Ollama or a cloud key."], ["TAURI", "RUST", "REACT", "TYPESCRIPT", "LLAMA.CPP"], 14),
    "WebGen": ("TEMPLATE GENERATOR / ORIGINALLY LAZYLAYOUTS", ["Generate templates easily."], ["TYPESCRIPT", "AI", "TEMPLATES"], 18),
}
OSS_FALLBACK = [{"repo": "NetPranav/Cero-Terminal", "name": "Cero-Terminal", "stars": 0, "pushed": "", "mine": 0},
                {"repo": "NetPranav/WebGen", "name": "WebGen", "stars": 0, "pushed": "", "mine": 0}]

def oss_strip():
    right = '<text x="1498" y="59" font-size="17" letter-spacing="3" text-anchor="middle">CONTRIBUTING TO OTHER PEOPLE\'S BUILDS</text>'
    write("section-oss.svg", svg(2000, 100, strip("05", "OPEN SOURCE", right)))

def oss_cards():
    from PIL import Image
    H = 400; gap = 12; cw = (2000 - 80 - gap) // 2; aw = 330
    items = json.load(open(os.path.join(SRC, "stats.json"))).get("oss") or OSS_FALLBACK
    for k, r in enumerate(items[:2]):
        sub, desc, tech, n = OSS_META[r["name"]]
        left = 40 if k == 0 else gap // 2; right = gap // 2 if k == 0 else 40
        W = left + cw + right; x = left
        iw, ih = Image.open(os.path.join(SRC, f"art-{n}.jpg")).size
        sc = max(aw / iw, (H - 2) / ih); sw_, sh_ = iw * sc, ih * sc
        shift = max(sh_ - (H - 2), 0) * 0.5; axis = "0 0;0 -%d;0 0" % shift if sh_ > H else "0 0;-%d 0;0 0" % (max(sw_ - aw, 0) * 0.5)
        tx = x + aw + 30
        stat = lambda i, v, l: (f'<text x="{tx+i*190}" y="284" font-size="{38 if len(str(v)) < 6 else 24}" letter-spacing="-1">{v}</text>'
                                f'<text x="{tx+i*190}" y="308" font-size="12" letter-spacing="2.5" opacity="0.6">{l}</text>')
        defs = f'<clipPath id="a"><rect x="{x+1}" y="11" width="{aw-1}" height="{H-2}"/></clipPath>'
        body = (f'{box(x, 10, cw, H)}<g clip-path="url(#a)"><g>{pan(axis, 40)}<image href="{art(n, None, 72)}" x="{x+1}" y="11" width="{sw_:.0f}" height="{sh_:.0f}"/></g></g>{vline(x+aw, 10, 10+H)}'
                f'{tag(x+14, 24, f"{k+1:02d} / OPEN SOURCE")}'
                f'<text x="{tx}" y="82" font-size="40">{r["name"]}</text>'
                f'<text x="{x+cw-24}" y="48" font-size="12" letter-spacing="3" text-anchor="end" opacity="0.8">CONTRIBUTOR</text>'
                f'<text x="{tx}" y="110" font-size="12.5" letter-spacing="2.5" opacity="0.6">{sub}</text>{hline(tx, x+cw-24, 130, 0.45)}'
                + "".join(f'<text x="{tx}" y="{168+i*25}" font-size="15.5" opacity="0.9">{l}</text>' for i, l in enumerate(desc)) +
                stat(0, r["mine"], "MY COMMITS") + stat(1, r["stars"], "STARS") + stat(2, r["pushed"] or "-", "LAST PUSH") +
                f'{hline(tx, x+cw-24, 326, 0.45)}<g transform="translate({tx} 342)">{chips(0, 0, tech, cw-aw-54)}</g>'
                f'<text x="{x+cw-24}" y="{H-8}" font-size="14" letter-spacing="3" text-anchor="end">OPEN REPO -&gt;<animate attributeName="opacity" values="0.55;1;0.55" dur="3.2s" begin="{k*0.5}s" repeatCount="indefinite"/></text>')
        write(f"oss-{k+1}.svg", svg(W, H + 20, body, defs))

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
            f'<text x="1626" y="{Y+H-18}" font-size="11.5" letter-spacing="1" opacity="0.45">PUBLIC NON-FORK REPOS / BY BYTES</text>')
    write("section-stats.svg", svg(2000, Y + H + 20, body, defs))

if __name__ == "__main__":
    work_strip(); work_cards(); oss_strip(); oss_cards(); stats()

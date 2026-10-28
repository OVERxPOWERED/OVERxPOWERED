#!/usr/bin/env python3
"""
build_phone.py
Phone variant: single column, every SVG is 800 units wide and the smallest text is
~22 units, so on a ~390px screen it renders at ~11px or larger. Links are full-width
stacked buttons. Writes variants/phone/{README.md,assets/*.svg}.
"""
import json, os, textwrap
from build_header import DAY, GH, LN, MONTH, SRC, TODAY, box, hline, spin_star, svg, twinkle, vline
from build_asym import Tile, crop_lv, frame, label, pan, shiny, tag, tile_art
from build_sections import art
from build_work import OSS_FALLBACK, OSS_META, PROJECTS
import build_header, build_asym

OUT = os.path.join(build_header.ROOT, "variants", "phone")
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
def write(name, s): open(os.path.join(OUT, "assets", name), "w").write(s)
S = json.load(open(os.path.join(SRC, "stats.json")))
W = 800

def strip(idx, text, y=20):
    return (f'{box(24, y, 70, 56)}<text x="59" y="{y+36}" font-size="22" text-anchor="middle">{idx}</text>'
            f'{box(94, y, W-118, 56)}<text x="122" y="{y+36}" font-size="22" letter-spacing="3">{text}</text>')

def txt(x, y, lines, size=28, step=44, op=0.92):
    return "".join(f'<text x="{x}" y="{y+i*step}" font-size="{size}" opacity="{op}">{l}</text>' for i, l in enumerate(lines))

# ------------------------------------------------------------------ hero
def hero():
    name = crop_lv((58, 100, 1028, 278)); bohra = crop_lv((58, 288, 548, 432))
    d1, b1 = shiny("n", name, 20, 118, 760, 139, 0.92, 0, dur=8)
    d2, b2 = shiny("b", bohra, 20, 270, 440, 129.6, 0.95, 1.2, blend=True, dur=8)
    pt = Tile(crop_lv((1052, 106, 1966, 546), 0, 80), 914, 440, 24, 650, 752, 380, axis="x", dur=70, travel=0.8, ghosted=False)
    words = ["EXPLORING", "BUILDING", "LEARNING", "REPEATING"]
    # four words do not fit one line at this size: two lines of two
    st = ""
    for i, w in enumerate(words):
        x = 60 + (i % 2) * 340; y = 52 + (i // 2) * 36
        st += (f'<text x="{x}" y="{y}" font-size="22" letter-spacing="2" opacity="0.55">{w}<animate attributeName="opacity" values="0.55;1;1;0.55;0.55" '
               f'keyTimes="0;{i/4+0.03:.3f};{i/4+0.2:.3f};{i/4+0.25:.3f};1" dur="8s" repeatCount="indefinite"/></text>')
    body = f'''{box(24, 20, 752, 80)}{st}{spin_star(738, 62, 14, 14)}{vline(682, 20, 104)}
{b1}{b2}
{box(486, 280, 74, 110)}{spin_star(523, 335, 20, 12)}{vline(584, 284, 390)}
<text x="24" y="448" font-size="40" letter-spacing="1">FULL-STACK WEB &amp;</text><text x="24" y="498" font-size="40" letter-spacing="1">SOFTWARE DEVELOPER</text>
{hline(24, 64, 522)}
<text x="24" y="574" font-size="27" opacity="0.9">Building scalable web applications</text><text x="24" y="612" font-size="27" opacity="0.9">and modern desktop experiences.</text>
{pt.svg}
{box(646, 670, 110, 70)}<text x="701" y="702" font-size="26" text-anchor="middle">{DAY}</text>{hline(681, 721, 712)}<text x="701" y="732" font-size="26" text-anchor="middle">{MONTH}</text>
{tag(40, 994, "FIG. A / ORBIT")}'''
    write("hero.svg", svg(W, 1060, body, d1 + d2 + pt.defs))

# ------------------------------------------------------------------ link buttons
def button(name, icon, text):
    body = (f'{box(24, 14, 752, 92)}<g transform="translate(50 34)">{icon}</g>'
            f'<text x="124" y="70" font-size="30">{text}</text>'
            f'<text x="750" y="70" font-size="26" text-anchor="end" opacity="0.7">-&gt;<animate attributeName="opacity" values="0.35;1;0.35" dur="3s" repeatCount="indefinite"/></text>')
    write(name, svg(W, 120, body))

def buttons():
    gh = f'<path transform="scale(3.1)" d="{GH}" fill="#fff"/>'
    li = '<rect width="50" height="50" rx="6" fill="#fff"/><text x="25" y="38" font-size="32" text-anchor="middle" style="fill:#0a0a0a;font-weight:700">in</text>'
    em = '<rect width="54" height="42" y="4" rx="5" fill="#fff"/><path d="M4 11 L27 29 L50 11" fill="none" stroke="#0a0a0a" stroke-width="3.5" stroke-linejoin="round"/>'
    button("btn-github.svg", gh, "OVERxPOWERED")
    button("btn-linkedin.svg", li, "Burhanuddin Bohra")
    button("btn-email.svg", em, "6burhanuddin6@gmail.com")

# ------------------------------------------------------------------ about
def about():
    t = tile_art(7, 24, 480, 752, 280, axis="y", dur=50, travel=0.5, ghosted=False)
    lines = ["I build scalable web applications", "and modern desktop experiences.", "Fast, reliable, precise.", "", "Daily driver: Arch Linux +", "Wayland + Zsh. Between products,", "open source, automations, drones,", "gaming and UI-UX design."]
    rows = [("STATUS", "ONLINE &amp; SHIPPING DAILY"), ("WORKSTATION", "LINUX + WAYLAND + ZSH"), ("OPEN TO", "COLLABORATIONS &amp; ROLES")]
    tb = "".join(f'{hline(24, 776, 796+i*84, 0.4)}{label(24, 830+i*84, k, 20, 3, 0.6)}<text x="24" y="{858+i*84}" font-size="26">{v}</text>' for i, (k, v) in enumerate(rows))
    body = (f'{strip("02", "ABOUT")}{txt(24, 150, lines, 29, 42)}{t.svg}{tag(40, 720, "FIG. 02 / STAR CHART")}{tb}'
            f'<circle cx="752" cy="48" r="7" fill="#fff"><animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    write("about.svg", svg(W, 1070, body, t.defs))

# ------------------------------------------------------------------ arsenal
def arsenal():
    groups = [("01 / FRONTEND &amp; UI", ["Next.js (App Router, RSC)", "React + TypeScript", "Tailwind CSS + Three.js", "HTML5 + CSS3 + JavaScript", "Responsive + motion design"], 900),
              ("02 / BACKEND &amp; DATA", ["Node.js + Express.js", "Python + Django", "PostgreSQL", "RESTful API architecture", "Postman API testing"], 1250),
              ("03 / SYSTEMS &amp; WORKFLOW", ["Linux + Unix systems", "Wayland + Zsh", "C++ + QML", "Git + GitHub", "Docker + Vercel"], 1560)]
    body = strip("03", "ARSENAL"); defs = ""; y = 110
    for k, (title, items, ry) in enumerate(groups):
        band = art(11, (0, ry, 760, ry + 70), 72)
        defs += f'<clipPath id="b{k}"><rect x="25" y="{y+1}" width="750" height="68"/></clipPath>'
        body += (f'{box(24, y, 752, 404)}<g clip-path="url(#b{k})"><g>{pan("0 0;-40 0;0 0", 30+k*6)}<image href="{band}" x="25" y="{y+1}" width="800" height="68"/></g></g>{hline(24, 776, y+69)}'
                 f'<text x="48" y="{y+112}" font-size="22" letter-spacing="3">{title}</text>{hline(48, 752, y+132, 0.4)}'
                 f'{txt(48, y+176, ["+ " + i for i in items], 27, 44, 0.9)}{twinkle(738, y+104, 9, 3.2+k*0.6, k*0.7)}')
        y += 428
    write("arsenal.svg", svg(W, y + 4, body, defs))

# ------------------------------------------------------------------ work
def work_title():
    write("work-title.svg", svg(W, 100, strip("04", "SELECTED WORK")))

def chips(x, y, labels, maxx):
    out = ""
    for l in labels:
        w = len(l) * 13.6 + 28
        if x + w > maxx: x = 0; y += 48
        out += f'{frame(x, y, round(w), 38, "", 1, 1.2)}<text x="{x+14}" y="{y+27}" font-size="21" letter-spacing="1">{l}</text>'
        x += w + 12
    return out

def work():
    from PIL import Image
    for k, (name, sub, desc, tech, n) in enumerate(PROJECTS):
        iw, ih = Image.open(os.path.join(SRC, f"art-{n}.jpg")).size
        t = Tile(art(n, None, 70), iw, ih, 24, 14, 752, 280, axis="y", dur=36 + k * 6, travel=0.6, ghosted=False)
        lines = [l for l in desc]
        body = (f'{frame(24, 14, 752, 644)}{t.svg}{hline(24, 776, 294)}{tag(40, 28, f"{k+1:02d} / PROJECT")}'
                f'<text x="48" y="352" font-size="42">{name}</text>{label(48, 384, sub, 20, 2.5, 0.6)}{hline(48, 752, 404, 0.4)}'
                f'{txt(48, 446, lines, 24, 34, 0.9)}'
                f'<g transform="translate(48 {446+len(lines)*34+14})">{chips(0, 0, tech, 700)}</g>'
                f'{label(752, 638, "OPEN REPO -&gt;", 22, 3, 0.9, "end")}')
        write(f"work-{k+1}.svg", svg(W, 672, body, t.defs))

# ------------------------------------------------------------------ stats
def stats():
    s = S; y0 = 100
    cells = [("CONTRIBUTIONS / 1 YR", f'{s["contributions"]:,}'), ("COMMITS", str(s["commits"])), ("PULL REQUESTS", str(s["prs"])), ("CURRENT STREAK", f'{s["streak"]}D')]
    big = "".join(f'{box(24+(i%2)*378, y0+(i//2)*170, 374, 160)}{label(44+(i%2)*378, y0+34+(i//2)*170, l, 18, 2, 0.6)}<text x="{44+(i%2)*378}" y="{y0+118+(i//2)*170}" font-size="64" letter-spacing="-1">{v}</text>' for i, (l, v) in enumerate(cells))
    days = s["days"]; weeks = [days[i:i + 7] for i in range(0, len(days), 7)][-53:]
    nz = sorted(d for d in days if d > 0); q = [nz[int(len(nz) * p)] for p in (0.25, 0.5, 0.75)]
    lvl = lambda c: 0 if c == 0 else 1 + sum(c > t for t in q)
    op = [0.09, 0.3, 0.52, 0.76, 1]; cs, hx, hy = 13.6, 40, y0 + 440
    hm = "".join(f'<rect x="{hx+wi*cs:.1f}" y="{hy+di*cs:.1f}" width="11" height="11" fill="#fff" opacity="{op[lvl(c)]}"/>' for wi, w in enumerate(weeks) for di, c in enumerate(w))
    mask = "".join(f'<rect x="{hx+wi*cs:.1f}" y="{hy+di*cs:.1f}" width="11" height="11" fill="#fff"/>' for wi, w in enumerate(weeks) for di, _ in enumerate(w))
    defs = (f'<mask id="hm" maskUnits="userSpaceOnUse" x="{hx}" y="{hy}" width="730" height="100">{mask}</mask>'
            '<linearGradient id="sw" gradientUnits="userSpaceOnUse" x1="-100" x2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" values="{hx} 0;{hx+850} 0;{hx+850} 0" keyTimes="0;0.5;1" dur="7s" repeatCount="indefinite"/></linearGradient>')
    langs = "".join(f'<text x="44" y="{y0+696+i*54}" font-size="23" letter-spacing="1">{n.upper()}</text><text x="756" y="{y0+696+i*54}" font-size="23" text-anchor="end" opacity="0.7">{p}%</text>'
                    f'{box(44, y0+708+i*54, 712, 10)}<rect x="44" y="{y0+708+i*54}" width="{max(4, 712*p/100):.0f}" height="10" fill="#fff"><animate attributeName="width" values="0;{max(4, 712*p/100):.0f};{max(4, 712*p/100):.0f}" keyTimes="0;0.2;1" dur="8s" begin="{i*0.25}s" repeatCount="indefinite"/></rect>' for i, (n, p) in enumerate(s["langs"]))
    body = (f'{strip("06", "LIVE STATS")}{big}'
            f'{box(24, y0+350, 752, 224)}{label(44, y0+392, "CONTRIBUTION MAP / 12 MONTHS", 19, 2.5, 0.65)}{hm}<rect x="{hx}" y="{hy}" width="730" height="100" fill="url(#sw)" mask="url(#hm)"/>'
            f'{label(44, y0+556, f"SYNCED DAILY / {TODAY.isoformat()} UTC", 17, 2, 0.5)}'
            f'{box(24, y0+596, 752, 350)}{label(44, y0+638, "TOP LANGUAGES / PUBLIC REPOS", 19, 2.5, 0.65)}{langs}')
    write("stats.svg", svg(W, y0 + 970, body, defs))

def oss_title():
    write("oss-title.svg", svg(W, 100, strip("05", "OPEN SOURCE")))

def oss():
    from PIL import Image
    items = S.get("oss") or OSS_FALLBACK
    for k, r in enumerate(items[:2]):
        sub, desc, tech, n = OSS_META[r["name"]]
        desc = textwrap.wrap(" ".join(desc), 44)
        iw, ih = Image.open(os.path.join(SRC, f"art-{n}.jpg")).size
        t = Tile(art(n, None, 70), iw, ih, 24, 14, 752, 280, axis="y", dur=40 + k * 6, travel=0.5, ghosted=False)
        stat = lambda i, v, l: (f'<text x="{48+i*250}" y="{y0+56}" font-size="{44 if len(str(v)) < 6 else 28}">{v}</text>{label(48+i*250, y0+84, l, 18, 2.5, 0.6)}')
        y0 = 446 + len(desc) * 34 + 20
        body = (f'{frame(24, 14, 752, y0+250)}{t.svg}{hline(24, 776, 294)}{tag(40, 28, f"{k+1:02d} / OPEN SOURCE")}'
                f'<text x="48" y="352" font-size="42">{r["name"]}</text>{label(48, 384, sub if len(sub) < 40 else "TEMPLATES / ORIGINALLY LAZYLAYOUTS", 19, 2.5, 0.6)}{label(752, 352, "CONTRIBUTOR", 18, 3, 0.8, "end")}{hline(48, 752, 404, 0.4)}'
                f'{txt(48, 446, desc, 24, 34, 0.9)}{hline(48, 752, y0-6, 0.4)}'
                f'{stat(0, r["mine"], "MY COMMITS")}{stat(1, r["stars"], "STARS")}{stat(2, r["pushed"] or "-", "LAST PUSH")}'
                f'<g transform="translate(48 {y0+112})">{chips(0, 0, tech, 700)}</g>{label(752, y0+226, "OPEN REPO -&gt;", 22, 3, 0.9, "end")}')
        write(f"oss-{k+1}.svg", svg(W, y0 + 278, body, t.defs))

def footer():
    body = (f'{hline(24, 776, 30, 0.4)}{spin_star(400, 30, 11, 14)}'
            f'<text x="400" y="86" font-size="22" letter-spacing="3" text-anchor="middle" opacity="0.8">EXPLORE + BUILD + LEARN</text>'
            f'<text x="400" y="122" font-size="22" letter-spacing="3" text-anchor="middle" opacity="0.8">AUTOMATE + REPEAT</text>')
    write("footer.svg", svg(W, 160, body))

README = """<p>
<img src="assets/hero.svg" width="100%" alt="Burhanuddin Bohra: Full-Stack Web & Software Developer"/>
<a href="https://github.com/OVERxPOWERED"><img src="assets/btn-github.svg" width="100%" alt="GitHub: OVERxPOWERED"/></a>
<a href="https://www.linkedin.com/in/burhanuddin-bohra-629abb370/"><img src="assets/btn-linkedin.svg" width="100%" alt="LinkedIn: Burhanuddin Bohra"/></a>
<a href="mailto:6burhanuddin6@gmail.com"><img src="assets/btn-email.svg" width="100%" alt="Email: 6burhanuddin6@gmail.com"/></a>
<img src="assets/about.svg" width="100%" alt="About"/>
<img src="assets/arsenal.svg" width="100%" alt="Arsenal"/>
<img src="assets/work-title.svg" width="100%" alt="Selected work"/>
<a href="https://github.com/OVERxPOWERED/op-caelestia-shell"><img src="assets/work-1.svg" width="100%" alt="op-caelestia-shell"/></a>
<a href="https://github.com/OVERxPOWERED/PocketFix"><img src="assets/work-2.svg" width="100%" alt="PocketFix"/></a>
<a href="https://github.com/OVERxPOWERED/Marg"><img src="assets/work-3.svg" width="100%" alt="Marg"/></a>
<a href="https://github.com/OVERxPOWERED/QuizSolver"><img src="assets/work-4.svg" width="100%" alt="QuizSolver"/></a>
<img src="assets/oss-title.svg" width="100%" alt="Open source"/>
<a href="https://github.com/NetPranav/Cero-Terminal"><img src="assets/oss-1.svg" width="100%" alt="Cero-Terminal"/></a>
<a href="https://github.com/NetPranav/WebGen"><img src="assets/oss-2.svg" width="100%" alt="WebGen, originally LazyLayouts"/></a>
<img src="assets/stats.svg" width="100%" alt="Live GitHub stats"/>
<img src="assets/footer.svg" width="100%" alt="Explore, build, learn, automate, repeat"/>
</p>
"""

if __name__ == "__main__":
    hero(); buttons(); about(); arsenal(); work_title(); work(); oss_title(); oss(); stats(); footer()
    open(os.path.join(OUT, "README.md"), "w").write(README)

#!/usr/bin/env python3
"""
build_sections.py
Builds the About and Arsenal rows below the header (assets/section-*.svg),
reusing the frame/text helpers and fonts from build_header.py.
"""
import base64, io, os
from PIL import Image
from build_header import FG, LN, SRC, box, hline, svg, spin_star, twinkle, vline, write

def art(n, region=None, q=78):
    im = Image.open(os.path.join(SRC, f"art-{n}.jpg")).convert("L")
    if region: im = im.crop(region)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def strip(idx, label, right):
    return (f'{box(40, 24, 80, 58)}<text x="80" y="59" font-size="17" text-anchor="middle">{idx}</text>'
            f'{box(120, 24, 890, 58)}<text x="165" y="59" font-size="17" letter-spacing="3">{label}</text>{hline(165 + len(label) * 20.5, 985, 53)}'
            f'{box(1022, 24, 953, 58)}{right}')

def tag(x, y, text):
    w = len(text) * 8.6 + 20
    return f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" fill="#0a0a0a" stroke="{LN}" stroke-width="1"/><text x="{x+10}" y="{y+17}" font-size="12.5" letter-spacing="1">{text}</text>'

def pan(values, dur, key="0;0.5;1"):
    return (f'<animateTransform attributeName="transform" type="translate" values="{values}" keyTimes="{key}" calcMode="spline" '
            f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="{dur}s" repeatCount="indefinite"/>')

# ------------------------------------------------------------------ About
def about():
    Y = 100; H = 320
    defs = (f'<clipPath id="p1"><rect x="41" y="{Y+1}" width="598" height="{H-2}"/></clipPath>'
            f'<clipPath id="p3"><rect x="1361" y="{Y+1}" width="598" height="{H-2}"/></clipPath>')
    chart = art(7, (0, 230, 736, 960))      # constellation chart, compass star near the middle
    nebula = art(8, None, 70)
    right = ('<circle cx="1300" cy="53" r="5" fill="#fff"><animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite"/></circle>'
             '<text x="1322" y="59" font-size="17" letter-spacing="3">STATUS: ONLINE &amp; SHIPPING</text>')
    # panel 1: star chart, slow drift + a ring around the compass star
    p1 = (f'<g clip-path="url(#p1)"><g>{pan("0 0;0 -70;0 0", 40)}'
          f'<image href="{chart}" x="41" y="{Y-110}" width="598" height="{round(730*598/736)}"/></g>'
          f'<g transform="translate(340 {Y+150})"><circle r="46" fill="none" stroke="#fff" stroke-width="1" stroke-dasharray="3 7" opacity="0.7">'
          f'<animateTransform attributeName="transform" type="rotate" values="0;360" dur="30s" repeatCount="indefinite"/></circle></g></g>')
    # panel 3: nebula fly-through
    scale = 598 / 736; ih = 1308 * scale
    p3 = (f'<g clip-path="url(#p3)"><g>{pan(f"0 0;0 -{ih - H:.0f};0 0", 90)}'
          f'<image href="{nebula}" x="1361" y="{Y+1}" width="598" height="{ih:.0f}"/></g></g>')
    lines = ["I build scalable web applications and modern", "desktop experiences. Fast, reliable, precise.", "",
             "Daily driver: Arch Linux + Wayland + Zsh.", "Somewhere between products, open source,", "automations, drones, gaming and UI-UX design."]
    txt = "".join(f'<text x="692" y="{Y+82+i*25}" font-size="17.5" opacity="0.93">{l}</text>' for i, l in enumerate(lines))
    rows = [("STATUS", "ONLINE &amp; SHIPPING DAILY"), ("WORKSTATION", "LINUX + WAYLAND + ZSH"), ("OPEN TO", "COLLABORATIONS &amp; ROLES")]
    tbl = "".join(f'{hline(662, 1338, Y+H-92+i*30, 0.5)}<text x="692" y="{Y+H-72+i*30}" font-size="13.5" letter-spacing="2" opacity="0.6">{k}</text>'
                  f'<text x="880" y="{Y+H-72+i*30}" font-size="14.5" letter-spacing="1">{v}</text>' for i, (k, v) in enumerate(rows))
    body = f'''{strip("02", "ABOUT", right)}
{p1}{box(40, Y, 600, H)}{tag(54, Y+H-38, "FIG. 02 / STAR CHART")}
{box(660, Y, 680, H)}<text x="692" y="{Y+40}" font-size="13.5" letter-spacing="3" opacity="0.6">FULL-STACK WEB &amp; SOFTWARE DEVELOPER</text>{hline(692, 1308, Y+54, 0.5)}{txt}{tbl}{spin_star(1308, Y+36, 9, 10)}
{p3}{box(1360, Y, 600, H)}{tag(1374, Y+H-38, "FIG. 03 / NEBULA")}'''
    write("section-about.svg", svg(2000, Y + H + 20, body, defs))

# ------------------------------------------------------------------ Arsenal
def arsenal():
    Y = 100; H = 290; W = 628; gap = 18
    cols = [("FRONTEND &amp; UI", ["Next.js (App Router, RSC)", "React + TypeScript", "Tailwind CSS + Three.js", "HTML5 + CSS3 + JavaScript", "Responsive + motion design"], 900),
            ("BACKEND &amp; DATA", ["Node.js + Express.js", "Python + Django", "PostgreSQL (schema + queries)", "RESTful API architecture", "Postman API testing"], 1250),
            ("SYSTEMS &amp; WORKFLOW", ["Linux + Unix systems", "Wayland + Zsh", "C++ + QML", "Git + GitHub", "Docker + Vercel"], 1560)]
    defs = "".join(f'<clipPath id="b{k}"><rect x="{41 + k*(W+gap)}" y="{Y+1}" width="{W-2}" height="68"/></clipPath>' for k in range(3))
    right = '<text x="1498" y="59" font-size="17" letter-spacing="3" text-anchor="middle">WEB + SYSTEMS + AUTOMATION</text>'
    body = strip("03", "ARSENAL", right)
    for k, (title, items, ry) in enumerate(cols):
        x = 40 + k * (W + gap)
        band = art(11, (0, ry, 760, ry + 68), 74)
        body += (f'{box(x, Y, W, H)}<g clip-path="url(#b{k})"><g>{pan("0 0;-140 0;0 0", 40 + k*7)}'
                 f'<image href="{band}" x="{x+1}" y="{Y+1}" width="760" height="68"/></g></g>{hline(x, x+W, Y+69)}'
                 f'<text x="{x+26}" y="{Y+104}" font-size="15" letter-spacing="3.5">{k+1:02d} / {title}</text>{hline(x+26, x+W-26, Y+120, 0.5)}')
        body += "".join(f'<text x="{x+26}" y="{Y+154+i*29}" font-size="17.5" opacity="0.9">+ {t}</text>' for i, t in enumerate(items))
        body += twinkle(x + W - 32, Y + 104, 8, 3.2 + k * 0.7, k * 0.8)
    write("section-arsenal.svg", svg(2000, Y + H + 20, body, defs))

# ------------------------------------------------------------------ Footer
def footer():
    from build_header import TODAY
    words = ["EXPLORE", "BUILD", "LEARN", "AUTOMATE", "REPEAT"]; x = 165; t = ""
    for i, w in enumerate(words):
        t += (f'<text x="{x:.0f}" y="59" font-size="17" letter-spacing="1.5" opacity="0.55">{w}<animate attributeName="opacity" values="0.55;1;1;0.55;0.55" '
              f'keyTimes="0;{i/5+0.03:.3f};{i/5+0.15:.3f};{i/5+0.2:.3f};1" dur="10s" repeatCount="indefinite"/></text>')
        x += len(w) * 11.7
        if i < 4: t += f'<text x="{x+12:.0f}" y="59" font-size="17">+</text>'; x += 38
    body = (f'{box(40, 24, 80, 58)}<text x="80" y="59" font-size="17" text-anchor="middle">07</text>'
            f'{box(120, 24, 890, 58)}{t}{box(1022, 24, 953, 58)}{vline(1912, 24, 82)}'
            f'<text x="1050" y="59" font-size="15" letter-spacing="2" opacity="0.7">BURHANUDDIN BOHRA / OPEN SOURCE / SYNCED {TODAY.isoformat()} UTC</text>'
            f'{spin_star(1943, 53, 15)}')
    write("section-footer.svg", svg(2000, 110, body))

if __name__ == "__main__":
    about(); arsenal(); footer()

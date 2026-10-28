#!/usr/bin/env python3
"""
build_minimal.py
Minimal variant: one quiet header and a small activity strip as SVG, everything
else is plain Markdown so it stays readable on any screen.
Writes variants/minimal/{README.md,assets/*.svg}.
"""
import json, os
from build_header import DAY, FG, LN, MONTH, SRC, TODAY, hline, spin_star, svg
from build_asym import crop_lv, label, shiny
import build_header

OUT = os.path.join(build_header.ROOT, "variants", "minimal")
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
def write(name, s): open(os.path.join(OUT, "assets", name), "w").write(s)
S = json.load(open(os.path.join(SRC, "stats.json")))

def header():
    name = crop_lv((58, 100, 1028, 278)); bohra = crop_lv((58, 288, 548, 432))
    d1, b1 = shiny("n", name, 80, 150, 1000, 183.5, 0.92, 0, dur=9)
    d2, b2 = shiny("b", bohra, 330, 345, 560, 165, 0.95, 1.4, blend=True, dur=9)
    body = f'''{label(80, 80, "BURHANUDDIN BOHRA", 14, 6, 0.8)}{label(1920, 80, f"{DAY} / {MONTH}", 14, 6, 0.8, "end")}{hline(80, 1920, 100, 0.3)}
{b1}{b2}
<text x="1260" y="240" font-size="30" letter-spacing="1.5">FULL-STACK WEB &amp;</text><text x="1260" y="282" font-size="30" letter-spacing="1.5">SOFTWARE DEVELOPER</text>
{hline(1260, 1294, 306)}
<text x="1260" y="344" font-size="19" opacity="0.85">Building scalable web applications</text><text x="1260" y="372" font-size="19" opacity="0.85">and modern desktop experiences.</text>
<rect x="1620" y="358" width="9" height="16" fill="#fff"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
{hline(80, 1920, 540, 0.3)}{label(80, 530, "EXPLORING + BUILDING + LEARNING + REPEATING", 13, 5, 0.6)}{spin_star(1900, 520, 11, 16)}'''
    write("header.svg", svg(2000, 580, body, d1 + d2))

def activity():
    days = S["days"]; weeks = [days[i:i + 7] for i in range(0, len(days), 7)][-53:]
    nz = sorted(d for d in days if d > 0); q = [nz[int(len(nz) * p)] for p in (0.25, 0.5, 0.75)]
    lvl = lambda c: 0 if c == 0 else 1 + sum(c > t for t in q)
    op = [0.09, 0.3, 0.52, 0.76, 1]; cs, hx, hy = 20, 860, 70
    cells = "".join(f'<rect x="{hx+wi*cs}" y="{hy+di*cs}" width="16" height="16" fill="#fff" opacity="{op[lvl(c)]}"/>' for wi, w in enumerate(weeks) for di, c in enumerate(w))
    mask = "".join(f'<rect x="{hx+wi*cs}" y="{hy+di*cs}" width="16" height="16" fill="#fff"/>' for wi, w in enumerate(weeks) for di, _ in enumerate(w))
    defs = (f'<mask id="hm" maskUnits="userSpaceOnUse" x="{hx}" y="{hy}" width="1080" height="150">{mask}</mask>'
            '<linearGradient id="sw" gradientUnits="userSpaceOnUse" x1="-140" x2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" values="{hx} 0;{hx+1300} 0;{hx+1300} 0" keyTimes="0;0.5;1" dur="8s" repeatCount="indefinite"/></linearGradient>')
    nums = [(f'{S["contributions"]:,}', "CONTRIBUTIONS / 12 MO"), (str(S["commits"]), "COMMITS"), (str(S["prs"]), "PULL REQUESTS")]
    n = "".join(f'<text x="{80+i*250}" y="150" font-size="{64 if i == 0 else 44}" letter-spacing="-1">{v}</text>{label(80+i*250, 184, l, 11.5, 3, 0.6)}' for i, (v, l) in enumerate(nums))
    body = (f'{label(80, 50, f"ACTIVITY / SYNCED {TODAY.isoformat()} UTC", 12.5, 4, 0.7)}{n}{cells}'
            f'<rect x="{hx}" y="{hy}" width="1080" height="150" fill="url(#sw)" mask="url(#hm)"/>{hline(80, 1920, 250, 0.3)}')
    write("activity.svg", svg(2000, 270, body, defs))

README = f"""<img src="assets/header.svg" width="100%" alt="Burhanuddin Bohra: Full-Stack Web & Software Developer"/>

<p align="center">
<a href="https://github.com/OVERxPOWERED">GitHub</a> &nbsp;/&nbsp;
<a href="https://www.linkedin.com/in/burhanuddin-bohra-629abb370/">LinkedIn</a> &nbsp;/&nbsp;
<a href="mailto:6burhanuddin6@gmail.com">6burhanuddin6@gmail.com</a>
</p>

I build scalable web applications and modern desktop experiences: fast, reliable, precise.
Daily driver is Arch Linux with Wayland and Zsh. I spend my time between products, open source, automations, drones, gaming and UI/UX design.

### Selected work

- **[op-caelestia-shell](https://github.com/OVERxPOWERED/op-caelestia-shell)** &mdash; Fluid, morphing Wayland desktop shell with zero-latency interaction.<br/>
  `QML` `C++` `GLSL` `Wayland`
- **[PocketFix](https://github.com/OVERxPOWERED/PocketFix)** &mdash; Production-ready full-stack task and workflow app.<br/>
  `Next.js` `TypeScript` `PostgreSQL`
- **[Marg](https://github.com/OVERxPOWERED/Marg)** &mdash; Freight dispatch, real-time tracking and route management.<br/>
  `Next.js` `TypeScript` `Python`
- **[QuizSolver](https://github.com/OVERxPOWERED/QuizSolver)** &mdash; Parses and evaluates structured assessments with automation.<br/>
  `Python`

### Stack

`Next.js` `React` `TypeScript` `Tailwind CSS` `Three.js` &nbsp;/&nbsp; `Node.js` `Express` `Python` `Django` `PostgreSQL` &nbsp;/&nbsp; `Linux` `Wayland` `Zsh` `C++` `QML` `Git` `Docker`

<img src="assets/activity.svg" width="100%" alt="GitHub activity over the last 12 months"/>

<p align="center"><sub>EXPLORE &middot; BUILD &middot; LEARN &middot; AUTOMATE &middot; REPEAT</sub></p>
"""

if __name__ == "__main__":
    header(); activity()
    open(os.path.join(OUT, "README.md"), "w").write(README)

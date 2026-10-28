#!/usr/bin/env python3
"""
build_asym.py
Asymmetric variant of the profile: same content and fonts, deliberately unbalanced
composition. Writes variants/asymmetric/{README.md,assets/*.svg}; the structured
version in the repo root is not touched.
"""
import json, math, os, random
from PIL import Image
from build_header import BG, FG, LN, REF, SRC, TODAY, crop, hline, svg, twinkle, spin_star, vline
import base64, io
from build_sections import art
import build_header

OUT = os.path.join(build_header.ROOT, "variants", "asymmetric")
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
def write(name, s): open(os.path.join(OUT, "assets", name), "w").write(s)
STATS = json.load(open(os.path.join(SRC, "stats.json")))

def crop_lv(box, floor=34, q=84):
    """Crop from the reference with the black point lifted to 0 so blend modes see true black."""
    im = REF.crop(box).point(lambda v: max(0, round((v - floor) * 255 / (255 - floor))))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def rot(a, cx, cy, inner): return f'<g transform="rotate({a} {cx} {cy})">{inner}</g>'
def frame(x, y, w, h, dash="", op=1, sw=1.5): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{LN}" stroke-width="{sw}" opacity="{op}" {dash}/>'
def ghost(x, y, w, h): return frame(x + 12, y + 10, w, h, 'stroke-dasharray="5 6"', 0.45, 1)   # misregistered second frame
def cross(x, y, r=9): return f'<path d="M{x-r} {y}H{x+r}M{x} {y-r}V{y+r}" stroke="{LN}" stroke-width="1.2" fill="none"/>'
def label(x, y, t, size=12.5, ls=3, op=0.65, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" letter-spacing="{ls}" opacity="{op}" text-anchor="{anchor}" {extra}>{t}</text>'
def outline(x, y, t, size, sw=1.3, ls=0, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" letter-spacing="{ls}" style="fill:none;stroke:{FG};stroke-width:{sw}" {extra}>{t}</text>'
def tag(x, y, t):
    w = len(t) * 8.6 + 20
    return f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" fill="#0a0a0a" stroke="{LN}"/><text x="{x+10}" y="{y+17}" font-size="12.5" letter-spacing="1">{t}</text>'
def pan(vals, dur):
    return (f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="0;0.5;1" calcMode="spline" '
            f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="{dur}s" repeatCount="indefinite"/>')

class Tile:
    """Clipped, slowly panning art panel with an optional rotation and a misregistered frame."""
    n = 0
    def __init__(self, uri, iw, ih, x, y, w, h, rotate=0, axis="y", dur=60, travel=0.7, ghosted=True, fit="cover"):
        Tile.n += 1; self.id = f"t{Tile.n}"
        s = max(w / iw, h / ih); sw_, sh_ = iw * s, ih * s
        if axis == "y": shift = (sh_ - h) * travel; vals = f"0 0;0 -{shift:.0f};0 0"
        else: shift = (sw_ - w) * travel; vals = f"0 0;-{shift:.0f} 0;0 0"
        inner = (f'<g clip-path="url(#{self.id})"><g>{pan(vals, dur)}<image href="{uri}" x="{x}" y="{y}" width="{sw_:.0f}" height="{sh_:.0f}"/></g></g>'
                 f'{frame(x, y, w, h)}' + (ghost(x, y, w, h) if ghosted else ""))
        self.defs = f'<clipPath id="{self.id}"><rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}"/></clipPath>'
        self.svg = rot(rotate, x + w / 2, y + h / 2, inner) if rotate else inner

def img_size(n): return Image.open(os.path.join(SRC, f"art-{n}.jpg")).size

def tile_art(n, *a, **k):
    iw, ih = img_size(n); return Tile(art(n, None, 70), iw, ih, *a, **k)

def shiny(mid, uri, x, y, w, h, op=0.9, delay=0, blend=False, dur=8):
    st = ' style="mix-blend-mode:screen"' if blend else ""
    defs = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}"><image href="{uri}" x="{x}" y="{y}" width="{w}" height="{h}"/></mask>'
            f'<linearGradient id="{mid}g" gradientUnits="userSpaceOnUse" x1="-260" x2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" values="{x} 0;{x+w+300} 0;{x+w+300} 0" keyTimes="0;0.5;1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></linearGradient>')
    body = (f'<image href="{uri}" x="{x}" y="{y}" width="{w}" height="{h}" opacity="{op}"{st}/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{mid}g)" mask="url(#{mid})"{st}/>')
    return defs, body

def barcode(x, y, w, h, seed=3):
    random.seed(seed); out = ""; cx = x
    while cx < x + w:
        bw = random.choice([1.5, 2, 3, 4]); out += f'<rect x="{cx}" y="{y}" width="{bw}" height="{h}" fill="#fff"><animate attributeName="opacity" values="1;0.35;1" dur="{random.uniform(1.8,3.4):.1f}s" begin="{random.uniform(0,2):.1f}s" repeatCount="indefinite"/></rect>'
        cx += bw + random.choice([2, 3, 4])
    return out

# =========================================================================== hero
def hero():
    H = 700
    name = crop_lv((58, 100, 1028, 278)); bohra = crop_lv((58, 288, 548, 432)); planet = crop((1052, 106, 1966, 546), 80)
    d1, b1 = shiny("sn", name, -20, 78, 1100, 202, 0.9, 0)
    d2, b2 = shiny("sb", bohra, 630, 300, 720, 212, 0.95, 1.2, blend=True)
    pt = Tile(planet, 914, 440, 1190, 36, 510, 530, axis="x", dur=90, travel=0.8)
    et = tile_art(12, 1745, 210, 215, 400, rotate=2.4, axis="x", dur=50, travel=0.6)
    rt = tile_art(6, 52, 500, 190, 150, rotate=-2.2, axis="y", dur=40)
    words = ["EXPLORING", "BUILDING", "LEARNING", "REPEATING"]; cx = 112; strip = ""
    for i, w in enumerate(words):
        strip += (f'<text x="{cx:.0f}" y="43" font-size="15" letter-spacing="1.2" opacity="0.55">{w}<animate attributeName="opacity" values="0.55;1;1;0.55;0.55" keyTimes="0;{i/4+0.03:.3f};{i/4+0.2:.3f};{i/4+0.25:.3f};1" dur="8s" repeatCount="indefinite"/></text>')
        cx += len(w) * 10.2 + 12
        if i < 3: strip += f'<text x="{cx-3:.0f}" y="43" font-size="15">+</text>'; cx += 22
    defs = d1 + d2 + pt.defs + et.defs + rt.defs
    body = f'''
<g transform="translate(26 668) rotate(-90)">{label(0, 0, "ARCH LINUX / WAYLAND / OPEN SOURCE", 11, 4, 0.5)}</g>
{b1}
{pt.svg}{tag(1204, 540, "FIG. A / ORBIT")}
{b2}
{et.svg}{tag(1752, 612, "FIG. B")}
{rt.svg}
<rect x="40" y="16" width="52" height="40" fill="none" stroke="{LN}" stroke-width="1.5"/><text x="66" y="42" font-size="15" text-anchor="middle">01</text>
<rect x="92" y="16" width="620" height="40" fill="none" stroke="{LN}" stroke-width="1.5"/>{strip}
{frame(1790, 10, 64, 66)}<text x="1822" y="38" font-size="16" text-anchor="middle">{build_header.DAY}</text>{hline(1810, 1834, 44)}<text x="1822" y="64" font-size="16" text-anchor="middle">{build_header.MONTH}</text>
{spin_star(1900, 44, 14, 14)}
{vline(272, 470, 650)}
<text x="298" y="496" font-size="30" letter-spacing="1">FULL-STACK WEB &amp;</text><text x="298" y="534" font-size="30" letter-spacing="1">SOFTWARE DEVELOPER</text>
{hline(298, 330, 556)}
<text x="298" y="590" font-size="17" opacity="0.9">Building scalable web applications</text><text x="298" y="614" font-size="17" opacity="0.9">and modern desktop experiences.</text>
<rect x="602" y="600" width="10" height="17" fill="#fff"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
{hline(52, 1090, 672, 0.5)}<circle cx="52" cy="672" r="3.5" fill="#fff"/><circle cx="1090" cy="672" r="3.5" fill="none" stroke="#fff"/>
{label(520, 664, "PRODUCTS / OPEN SOURCE / AUTOMATIONS / DRONES / GAMING / UI-UX / DESIGN", 12, 3, 0.55)}
<g transform="translate(1330 650)">{barcode(0, 0, 96, 22)}</g>{label(1330, 642, "REF 01 / OVRXPWRD", 10.5, 3, 0.45)}
{cross(1150, 30)}{cross(1712, 600)}{cross(590, 40)}{cross(1990-20, 400, 7)}
{twinkle(1060, 300, 11, 3.6, 0.4)}{twinkle(1665, 90, 8, 4.2, 1.1)}'''
    write("hero.svg", svg(2000, H, body, defs))

# =========================================================================== contact
GH = build_header.GH
def contact():
    H = 150
    def pill(name, w, y, icon, text, a):
        body = (f'{hline(0, w, y, 1)}{hline(0, w, y+64, 1)}{vline(0.75, y, y+64)}'
                f'<g transform="translate(26 {y+14})">{icon}</g><text x="78" y="{y+39}" font-size="17.5">{text}</text>'
                f'{label(w-18, y+82, a, 11, 3, 0.45, "end")}')
        write(name, svg(w, H, body))
    gh = f'<path transform="scale(2.1)" d="{GH}" fill="#fff"/>'
    li = f'<rect width="34" height="34" rx="5" fill="#fff"/><text x="17" y="26" font-size="22" text-anchor="middle" style="fill:#0a0a0a;font-weight:700">in</text>'
    em = f'<rect width="36" height="28" y="3" rx="4" fill="#fff"/><path d="M3 8 L18 19 L33 8" fill="none" stroke="#0a0a0a" stroke-width="2.6" stroke-linejoin="round"/>'
    pill("contact-b.svg", 300, 62, gh, "OVERxPOWERED", "A / CODE")
    pill("contact-c.svg", 340, 22, li, "Burhanuddin Bohra", "B / NETWORK")
    pill("contact-d.svg", 440, 82, em, "6burhanuddin6@gmail.com", "C / MAIL")
    write("contact-a.svg", svg(440, H, f'{label(40, 44, "[ 01 ] REACH ME", 13, 4, 0.7)}<text x="40" y="104" font-size="40" letter-spacing="-1">Say hello.</text>{hline(40, 330, 128, 0.5)}'))
    write("contact-e.svg", svg(520, H, f'{hline(0, 380, 100, 0.5)}<circle cx="380" cy="100" r="3.5" fill="none" stroke="#fff"/>{label(30, 90, "OPEN TO COLLABORATIONS &amp; ROLES", 12.5, 3.5, 0.75)}{twinkle(470, 44, 12, 3.8)}'))

# =========================================================================== about
def about():
    H = 560
    q = ["Building scalable web", "products with speed and", "precision, paired with", "ergonomic desktop", "environments."]
    ind = [0, 70, 20, 120, 40]
    qt = "".join(f'<text x="{90+ind[i]}" y="{150+i*50}" font-size="38" letter-spacing="-0.5">{l}</text>' for i, l in enumerate(q))
    tile1 = tile_art(7, 1290, 50, 330, 470, rotate=1.6, axis="y", dur=60, travel=0.5)
    tile2 = tile_art(8, 1650, 250, 250, 190, rotate=-2.4, axis="y", dur=70, travel=0.9, ghosted=False)
    facts = [("DAILY DRIVER", "ARCH LINUX + WAYLAND + ZSH"), ("ORBITING", "PRODUCTS / OSS / DRONES / GAMING / UI-UX"), ("STATUS", "ONLINE &amp; SHIPPING DAILY")]
    ft = "".join(f'{label(90, 420+i*34, k, 11.5, 3, 0.55)}<text x="300" y="{420+i*34}" font-size="14.5" letter-spacing="0.5">{v}</text>' for i, (k, v) in enumerate(facts))
    defs = tile1.defs + tile2.defs
    body = f'''{outline(1000, 520, "02", 280, 1.2, 0, 'opacity="0.35"')}
{label(90, 70, "[ 02 ] ABOUT", 13, 4, 0.75)}{hline(280, 560, 66, 0.5)}
{qt}{ft}{hline(90, 760, 396, 0.4)}
{tile1.svg}{tag(1304, 470, "FIG. 02 / STAR CHART")}{tile2.svg}
<g transform="rotate(-8 1500 505)"><rect x="1420" y="486" width="210" height="36" fill="#0a0a0a" stroke="#fff" stroke-width="2"/><text x="1525" y="510" font-size="14" letter-spacing="2.5" text-anchor="middle">ONLINE &amp; SHIPPING</text></g>
{cross(1640, 60)}{cross(1960, 520, 7)}{twinkle(1250, 90, 10, 3.2)}'''
    write("about.svg", svg(2000, H, body, defs))

# =========================================================================== arsenal
def arsenal():
    H = 640
    words = [
        (56, 222, "NEXT.JS", 128, 0), (640, 222, "REACT", 84, 1), (60, 284, "TYPESCRIPT + TAILWIND", 42, 0), (60, 324, "THREE.JS / HTML / CSS / MOTION", 22, 0),
        (930, 360, "NODE.JS", 56, 0), (930, 442, "POSTGRESQL", 84, 1), (1480, 442, "DJANGO", 44, 0), (930, 478, "EXPRESS + PYTHON + REST + POSTMAN", 21, 0),
        (240, 510, "ARCH LINUX", 96, 0), (240, 562, "WAYLAND", 44, 1), (240, 598, "ZSH / C++ / QML / GIT / DOCKER / VERCEL", 21, 0)]
    t = "".join(outline(x, y, w, s, 1.3) if o else f'<text x="{x}" y="{y}" font-size="{s}" letter-spacing="-1">{w}</text>' for x, y, w, s, o in words)
    band = tile_art(11, 1790, 30, 150, 440, rotate=3, axis="y", dur=70, travel=0.8, ghosted=False)
    labels = label(60, 72, "[ 03 ] ARSENAL", 13, 4, 0.75) + label(60, 112, "01 / FRONTEND &amp; UI", 12, 3.5, 0.55) + label(930, 300, "02 / BACKEND &amp; DATA", 12, 3.5, 0.55) + label(240, 424, "03 / SYSTEMS &amp; WORKFLOW", 12, 3.5, 0.55)
    body = f'''{labels}{hline(260, 560, 68, 0.5)}{hline(930, 1400, 312, 0.4)}{hline(240, 700, 436, 0.4)}
{t}{band.svg}{tag(1704, 520, "FIG. 04")}
{cross(900, 120)}{cross(1700, 560, 7)}{twinkle(1500, 150, 10, 3.4)}'''
    write("arsenal.svg", svg(2000, H, body, band.defs))

# =========================================================================== work
PROJ = [("op-caelestia-shell", "WAYLAND DESKTOP SHELL", ["Fluid, morphing desktop shell for", "Wayland. Zero-latency interaction,", "dynamic animation, ergonomic workspace."], ["QML", "C++", "GLSL", "WAYLAND"], 15),
        ("PocketFix", "TASK &amp; WORKFLOW APP", ["Full-stack app for reliable", "task coordination."], ["NEXT.JS", "POSTGRESQL"], 10),
        ("Marg", "LOGISTICS &amp; DISPATCH", ["Freight dispatch, real-time tracking", "and route management."], ["NEXT.JS", "TYPESCRIPT", "PYTHON"], 13),
        ("QuizSolver", "ASSESSMENT AUTOMATION", ["Parses and evaluates", "structured assessments."], ["PYTHON"], 17)]
# (svg width, card x, card y, card w, card h, art height, art on top, rotation, name size)
LAYOUT = [(760, 40, 30, 690, 610, 330, True, 0, 34), (380, 8, 170, 350, 400, 150, True, 1.2, 28), (540, 24, 70, 480, 540, 210, False, -0.8, 30), (320, 10, 250, 300, 390, 170, True, 1.6, 26)]
def chips(x, y, labels, maxw):
    out = ""
    for l in labels:
        w = len(l) * 8.4 + 20
        if x + w > maxw: x = 0; y += 32
        out += f'{frame(x, y, round(w), 24, "", 1, 1.2)}<text x="{x+10}" y="{y+17}" font-size="12.5" letter-spacing="1">{l}</text>'; x += w + 8
    return out
def work():
    H = 680
    for k, (name, sub, desc, tech, n) in enumerate(PROJ):
        W, cx, cy, cw, ch, ah, top, r, ns = LAYOUT[k]
        iw, ih = img_size(n); ay = cy if top else cy + ch - ah
        t = Tile(art(n, None, 70), iw, ih, cx, ay, cw, ah, axis="y", dur=44 + k * 8, travel=0.7, ghosted=False)
        ty = (cy + ah) if top else cy
        text = (f'<text x="{cx+24}" y="{ty+54}" font-size="{ns}">{name}</text>' + label(cx + 24, ty + 78, sub, 11.5, 2.5, 0.6) +
                "".join(f'<text x="{cx+24}" y="{ty+112+i*22}" font-size="14.5" opacity="0.88">{l}</text>' for i, l in enumerate(desc)) +
                f'<g transform="translate({cx+24} {ty+ch-ah-64})">{chips(0, 0, tech, cw-48)}</g>')
        inner = (f'{frame(cx, cy, cw, ch)}{ghost(cx, cy, cw, ch)}{t.svg}{hline(cx, cx+cw, cy+ah if top else cy+ch-ah)}{text}'
                 f'{tag(cx+12, (ay+12), f"{k+1:02d} / PROJECT")}{label(cx+cw-22, cy+ch-20 if top else cy+ch-ah-18, "OPEN REPO -&gt;", 13, 3, 0.85, "end")}')
        body = (rot(r, cx + cw / 2, cy + ch / 2, inner) if r else inner)
        if k == 0: body += outline(cx + 400, cy + ch + 60, "01", 130, 1.1, 0, 'opacity="0.0"')
        write(f"work-{k+1}.svg", svg(W, H, body, t.defs))
    write("work-title.svg", svg(2000, 140, f'{label(60, 60, "[ 04 ] SELECTED WORK", 13, 4, 0.75)}{outline(900, 120, "WORK", 120, 1.2, 10, 'opacity="0.4"')}{hline(330, 860, 56, 0.5)}{cross(1700, 70)}{label(1960, 60, "4 FILES / PRODUCTS + OSS", 12, 3, 0.5, "end")}'))

# =========================================================================== stats
def stats():
    s = STATS; H = 660
    days = s["days"]; weeks = [days[i:i + 7] for i in range(0, len(days), 7)][-53:]
    nz = sorted(d for d in days if d > 0); q = [nz[int(len(nz) * p)] for p in (0.25, 0.5, 0.75)]
    lvl = lambda c: 0 if c == 0 else 1 + sum(c > t for t in q)
    op = [0.09, 0.3, 0.52, 0.76, 1]; cs = 20; hx, hy = 830, 90
    cells = "".join(f'<rect x="{hx+wi*cs}" y="{hy+di*cs}" width="16" height="16" fill="#fff" opacity="{op[lvl(c)]}"/>' for wi, w in enumerate(weeks) for di, c in enumerate(w))
    mask = "".join(f'<rect x="{hx+wi*cs}" y="{hy+di*cs}" width="16" height="16" fill="#fff"/>' for wi, w in enumerate(weeks) for di, _ in enumerate(w))
    defs = (f'<mask id="hm" maskUnits="userSpaceOnUse" x="{hx}" y="{hy}" width="1080" height="150">{mask}</mask>'
            '<linearGradient id="sw" gradientUnits="userSpaceOnUse" x1="-140" x2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" values="{hx} 0;{hx+1300} 0;{hx+1300} 0" keyTimes="0;0.5;1" dur="8s" repeatCount="indefinite"/></linearGradient>')
    tot = sum(p for _, p in s["langs"]); x = 60; seg = ""; leg = ""
    for i, (n, p) in enumerate(s["langs"]):
        w = 820 * p / tot
        seg += f'<rect x="{x:.0f}" y="470" width="{max(w-3,2):.0f}" height="26" fill="#fff" opacity="{[1,0.7,0.5,0.35,0.22][i]}"><animate attributeName="width" values="0;{max(w-3,2):.0f};{max(w-3,2):.0f}" keyTimes="0;0.2;1" dur="8s" begin="{i*0.2}s" repeatCount="indefinite"/></rect>'
        leg += label(60, 534 + i * 22, f"{n.upper()}", 12.5, 2.5, 0.8) + label(300, 534 + i * 22, f"{p}%", 12.5, 1, 0.55)
        x += w
    wk = [sum(w) for w in weeks]; mx = max(wk) or 1; wbars = ""
    for i, c in enumerate(wk):
        h = max(3, round(c / mx * 200))
        wbars += (f'<rect x="{hx+i*cs}" y="{600-h}" width="14" height="{h}" fill="#fff" opacity="0.75"><animate attributeName="height" values="0;{h};{h}" keyTimes="0;0.25;1" dur="9s" begin="{i*0.03:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y" values="600;{600-h};{600-h}" keyTimes="0;0.25;1" dur="9s" begin="{i*0.03:.2f}s" repeatCount="indefinite"/></rect>')
    wbars += label(hx, 628, "WEEKLY ACTIVITY", 12, 3.5, 0.6) + hline(hx, hx + 1060, 606, 0.4)
    body = f'''{label(60, 70, "[ 05 ] LIVE STATS", 13, 4, 0.75)}{hline(300, 560, 66, 0.5)}{label(1960, 70, f"SYNCED DAILY / {TODAY.isoformat()} UTC", 12, 3, 0.6, "end")}
<text x="44" y="300" font-size="250" letter-spacing="-14">{s["contributions"]:,}</text>
{label(60, 364, "CONTRIBUTIONS / LAST 12 MONTHS", 13, 3.5, 0.7)}
<text x="60" y="424" font-size="26">{s["commits"]}<tspan font-size="12.5" opacity="0.6" letter-spacing="2.5"> COMMITS</tspan>   {s["prs"]}<tspan font-size="12.5" opacity="0.6" letter-spacing="2.5"> PRS</tspan>   {s["streak"]}D<tspan font-size="12.5" opacity="0.6" letter-spacing="2.5"> STREAK</tspan></text>
{seg}{leg}
{cells}<rect x="{hx}" y="{hy}" width="1080" height="150" fill="url(#sw)" mask="url(#hm)"/>
{frame(hx-14, hy-14, 1050, 178, 'stroke-dasharray="5 6"', 0.4, 1)}{label(hx, hy+190, "CONTRIBUTION MAP", 12, 3.5, 0.6)}
{wbars}{cross(1130, 640, 7)}{twinkle(1850, 330, 12, 3.7)}'''
    write("stats.svg", svg(2000, H, body, defs))

# =========================================================================== footer
def footer():
    words = [(70, 110, "EXPLORE", 64, 0), (400, 160, "BUILD", 64, 1), (260, 230, "LEARN", 64, 0), (820, 130, "AUTOMATE", 64, 1), (1220, 190, "REPEAT", 120, 0)]
    t = "".join(outline(x, y, w, s, 1.3) if o else f'<text x="{x}" y="{y}" font-size="{s}" letter-spacing="2">{w}</text>' for x, y, w, s, o in words)
    body = f'{t}{hline(60, 1100, 270, 0.4)}{label(1960, 262, "BOHRA GAZETTE / SAME UNIVERSE, DIFFERENT IDEAS", 12, 3.5, 0.55, "end")}{spin_star(1900, 120, 18, 16)}{cross(1100, 270, 7)}'
    write("footer.svg", svg(2000, 300, body))

README = """<p>
<img src="assets/hero.svg" width="100%" alt="Burhanuddin Bohra: Full-Stack Web & Software Developer"/>
<img src="assets/contact-a.svg" width="22%" alt="Say hello"/><a href="https://github.com/OVERxPOWERED"><img src="assets/contact-b.svg" width="15%" alt="GitHub: OVERxPOWERED"/></a><a href="https://www.linkedin.com/in/burhanuddin-bohra-629abb370/"><img src="assets/contact-c.svg" width="17%" alt="LinkedIn: Burhanuddin Bohra"/></a><a href="mailto:6burhanuddin6@gmail.com"><img src="assets/contact-d.svg" width="22%" alt="Email: 6burhanuddin6@gmail.com"/></a><img src="assets/contact-e.svg" width="24%" alt="Open to collaborations and roles"/>
<img src="assets/about.svg" width="100%" alt="About"/>
<img src="assets/arsenal.svg" width="100%" alt="Arsenal"/>
<img src="assets/work-title.svg" width="100%" alt="Selected work"/>
<a href="https://github.com/OVERxPOWERED/op-caelestia-shell"><img src="assets/work-1.svg" width="38%" alt="op-caelestia-shell"/></a><a href="https://github.com/OVERxPOWERED/PocketFix"><img src="assets/work-2.svg" width="19%" alt="PocketFix"/></a><a href="https://github.com/OVERxPOWERED/Marg"><img src="assets/work-3.svg" width="27%" alt="Marg"/></a><a href="https://github.com/OVERxPOWERED/QuizSolver"><img src="assets/work-4.svg" width="16%" alt="QuizSolver"/></a>
<img src="assets/stats.svg" width="100%" alt="Live GitHub stats"/>
<img src="assets/footer.svg" width="100%" alt="Explore, build, learn, automate, repeat"/>
</p>
"""

if __name__ == "__main__":
    hero(); contact(); about(); arsenal(); work(); stats(); footer()
    open(os.path.join(OUT, "README.md"), "w").write(README)

#!/usr/bin/env python3
"""
build_header.py
Builds the profile header as stacked SVG rows in assets/ from the reference
artwork in assets/src/. GitHub renders SMIL animation inside <img> but does not
make links inside an SVG clickable, so the contact bar is split into one SVG
per link and the README wraps each in <a>.
"""
import base64, datetime, io, math, os, random, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "src")
OUT = os.path.join(ROOT, "assets")
BG, FG, LN = "#0a0a0a", "#ECECEC", "#CFCFCF"
MONO = "'HM',ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace"
FONT = base64.b64encode(open(os.path.join(SRC, "mono-regular.woff2"), "rb").read()).decode()
REF = Image.open(os.path.join(SRC, "reference.png")).convert("L")
# the reference has a baked-in "20 06" in the planet panel: paint over it with neighbouring sky, the live date is drawn as text
REF.paste(REF.crop((1886, 203, 1913, 247)), (1915, 203))
# HEADER_DATE=YYYY-MM-DD overrides today (the daily workflow runs in UTC)
TODAY = datetime.date.fromisoformat(os.environ["HEADER_DATE"]) if os.environ.get("HEADER_DATE") else datetime.date.today()
DAY, MONTH = f"{TODAY.day:02d}", f"{TODAY.month:02d}"

STAR = "M0,-{o} C{i},-{i} {i},-{i} {o},0 C{i},{i} {i},{i} 0,{o} C-{i},{i} -{i},{i} -{o},0 C-{i},-{i} -{i},-{i} 0,-{o}Z"
def star_d(r): return STAR.format(o=r, i=round(r * 0.13, 2))

def crop(box, q=82):
    buf = io.BytesIO()
    REF.crop(box).save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# Desktop SVGs are 2000 units wide but shown ~850px wide on GitHub, so text is multiplied by TEXT_K
# (phone SVGs are 800 wide and already sized for their screen; cards that set final sizes pass scale=False).
TEXT_K = 1.25
def scale_text(body, k=TEXT_K):
    return re.sub(r'(font-size|letter-spacing)="([\d.]+)"', lambda m: f'{m[1]}="{float(m[2]) * k:.1f}"', body)

def svg(w, h, body, defs="", scale=True):
    if scale and w == 2000: body = scale_text(body)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><style>@font-face{{font-family:'HM';src:url(data:font/woff2;base64,{FONT}) format('woff2');}}
text{{font-family:{MONO};fill:{FG};}}</style>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.9 -0.35"/></filter>
{defs}</defs>
<rect width="{w}" height="{h}" fill="{BG}"/>
{body}
<rect width="{w}" height="{h}" filter="url(#grain)" opacity="0.07"/>
</svg>'''

def write(name, s):
    open(os.path.join(OUT, name), "w").write(s)

def box(x, y, w, h, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{LN}" stroke-width="1.5" {extra}/>'

def vline(x, y1, y2): return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{LN}" stroke-width="1.5"/>'
def hline(x1, x2, y, o=1): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{LN}" stroke-width="1.5" opacity="{o}"/>'

def twinkle(cx, cy, r, dur, begin=0):
    return (f'<g transform="translate({cx} {cy})"><path d="{star_d(r)}" fill="#fff">'
            f'<animate attributeName="opacity" values="0.25;1;0.25" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="scale" values="0.7;1.15;0.7" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path></g>')

def spin_star(cx, cy, r, dur=14):
    return (f'<g transform="translate({cx} {cy})"><path d="{star_d(r)}" fill="#fff">'
            f'<animateTransform attributeName="transform" type="rotate" values="0;360" dur="{dur}s" repeatCount="indefinite"/></path></g>')

# ------------------------------------------------------------------ row 1: top strip
def row1():
    words = [("EXPLORING", 165), ("BUILDING", 352), ("LEARNING", 525), ("REPEATING", 700)]
    seps = [308, 482, 655]
    t = ""
    for k, (w, x) in enumerate(words):
        t += (f'<text x="{x}" y="59" font-size="17" letter-spacing="1.5" opacity="0.55">{w}'
              f'<animate attributeName="opacity" values="0.55;1;1;0.55;0.55" keyTimes="0;{k/4+0.03:.3f};{k/4+0.2:.3f};{k/4+0.25:.3f};1" dur="8s" repeatCount="indefinite"/></text>')
    for x in seps:
        t += f'<text x="{x}" y="59" font-size="17">+</text>'
    random.seed(11); bars = ""; x = 1040
    while x < 1128:
        bw = random.choice([1.5, 2, 3, 4]); gap = random.choice([2, 3, 4])
        d = round(random.uniform(1.6, 3.2), 1)
        bars += f'<rect x="{x}" y="38" width="{bw}" height="32" fill="#fff"><animate attributeName="opacity" values="1;0.35;1" dur="{d}s" begin="{round(random.uniform(0,2),1)}s" repeatCount="indefinite"/></rect>'
        x += bw + gap
    body = f'''{box(40, 24, 80, 58)}<text x="80" y="59" font-size="17" text-anchor="middle">01</text>
{box(120, 24, 890, 58)}{t}{hline(840, 985, 53)}
{box(1022, 24, 953, 58)}{vline(1145, 24, 82)}{vline(1458, 24, 82)}{vline(1850, 24, 82)}{vline(1912, 24, 82)}
{bars}
<text x="1470" y="48" font-size="14" letter-spacing="0">A CURIOUS MIND</text>
<text x="1470" y="70" font-size="14" letter-spacing="0">TURNING IDEAS INTO REAL THINGS.</text>
<text x="1881" y="49" font-size="16" text-anchor="middle">{DAY}</text>{hline(1869, 1893, 55)}
<text x="1881" y="72" font-size="16" text-anchor="middle">{MONTH}</text>
{spin_star(1943, 53, 15)}'''
    write("header-1.svg", svg(2000, 100, body))

# ------------------------------------------------------------------ row 2: name + planet
def row2():
    W = 2000; H = 380
    name = crop((58, 100, 1028, 278)); bohra = crop((58, 288, 548, 432))
    planet = crop((1052, 106, 1966, 546), 80)
    defs = f'''
<mask id="mn" maskUnits="userSpaceOnUse" x="58" y="8" width="970" height="178"><image href="{name}" x="58" y="8" width="970" height="178"/></mask>
<mask id="mb" maskUnits="userSpaceOnUse" x="58" y="198" width="490" height="144"><image href="{bohra}" x="58" y="198" width="490" height="144"/></mask>
<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-260" y1="0" x2="0" y2="0">
<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;1400 0;1400 0" keyTimes="0;0.55;1" dur="7s" repeatCount="indefinite"/></linearGradient>
<clipPath id="pc"><rect x="1049" y="11" width="920" height="354"/></clipPath>'''
    pan = (f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -84;0 0" keyTimes="0;0.5;1" '
           f'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="44s" repeatCount="indefinite"/>')
    stars = "".join(twinkle(x, y, r, d, b) for x, y, r, d, b in
                    [(1690, 42, 9, 3.4, 0.2), (1815, 86, 7, 4.1, 1.1), (1905, 40, 6, 3.0, 2.0), (1600, 28, 5, 4.6, 0.7)])
    body = f'''
<image href="{name}" x="58" y="8" width="970" height="178" opacity="0.9"/>
<rect x="58" y="8" width="970" height="178" fill="url(#shine)" mask="url(#mn)"/>
<image href="{bohra}" x="58" y="198" width="490" height="144" opacity="0.9"/>
<rect x="58" y="198" width="490" height="144" fill="url(#shine)" mask="url(#mb)"/>
{box(560, 200, 80, 128)}{spin_star(600, 264, 21, 12)}{vline(655, 203, 330)}
<text x="680" y="237" font-size="22" letter-spacing="1.2">FULL-STACK WEB &amp;</text>
<text x="680" y="265" font-size="22" letter-spacing="1.2">SOFTWARE DEVELOPER</text>
{hline(680, 694, 283)}
<text x="680" y="307" font-size="17" opacity="0.92">Building scalable web applications</text>
<text x="680" y="331" font-size="17" opacity="0.92">and modern desktop experiences.</text>
<rect x="1004" y="318" width="10" height="17" fill="#fff"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
<g clip-path="url(#pc)"><g>{pan}<image href="{planet}" x="1050" y="12" width="918" height="440"/>
<text x="1927" y="126" font-size="17" text-anchor="middle" opacity="0.92">{DAY}</text><text x="1927" y="148" font-size="17" text-anchor="middle" opacity="0.92">{MONTH}</text></g></g>
{box(1048, 10, 922, 356)}
{stars}'''
    write("header-2.svg", svg(W, H, body, defs))

# ------------------------------------------------------------------ row 3: contact bar (one svg per link)
GH = "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"

def pill(name, w, icon, label, left_edge=False, right_edge=False):
    x0 = 40 if left_edge else 0
    x1 = w - 40 if right_edge else w
    lines = hline(x0, x1, 10) + hline(x0, x1, 70)
    if left_edge: lines += vline(x0, 10, 70)
    lines += vline(x1 if right_edge else w - 0.75, 10, 70)
    arrow = (f'<text x="{x1-26}" y="46" font-size="17" text-anchor="end" opacity="0.55">'
             f'↗<animate attributeName="opacity" values="0.3;0.9;0.3" dur="3s" repeatCount="indefinite"/></text>').replace("↗", "&#8599;")
    ix = x0 + 28
    body = f'{lines}<g transform="translate({ix} 24)">{icon}</g><text x="{ix+52}" y="46" font-size="18">{label}</text>'
    write(name, svg(w, 80, body))

def row3():
    gh = f'<path transform="scale(2.4)" d="{GH}" fill="#fff"/>'
    li = '<rect width="38" height="38" rx="5" fill="#fff"/><text x="19" y="29" font-size="24" text-anchor="middle" style="fill:#0a0a0a;font-weight:700">in</text>'
    em = '<rect width="40" height="32" y="3" rx="4" fill="#fff"/><path d="M3 8 L20 21 L37 8" fill="none" stroke="#0a0a0a" stroke-width="3" stroke-linejoin="round"/>'
    pill("header-3a.svg", 340, gh, "OVERxPOWERED", left_edge=True)
    pill("header-3b.svg", 340, li, "Burhanuddin Bohra")
    pill("header-3c.svg", 440, em, "6burhanuddin6@gmail.com")
    cats = "PRODUCTS / OPEN SOURCE / AUTOMATIONS / DRONES / GAMING / UI-UX / DESIGN"
    defs = '''<linearGradient id="cs" gradientUnits="userSpaceOnUse" x1="-200" x2="0"><stop offset="0" stop-color="#8a8a8a"/><stop offset="0.5" stop-color="#fff"/><stop offset="1" stop-color="#8a8a8a"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;1300 0" dur="6s" repeatCount="indefinite"/></linearGradient>'''
    body = f'{hline(0, 840, 10)}{hline(0, 840, 70)}<text x="28" y="46" font-size="17" letter-spacing="1.2" style="fill:url(#cs)">{cats}</text>{vline(840, 10, 70)}'
    write("header-3d.svg", svg(880, 80, body, defs))

# ------------------------------------------------------------------ row 4: bottom panels
def globe(cx, cy, r):
    n = 12; dur = 3.2; g = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LN}" stroke-width="1.5"/>'
    for lat in (-60, -30, 0, 30, 60):
        a = math.radians(lat); rx = r * math.cos(a)
        g += f'<ellipse cx="{cx}" cy="{cy + r*math.sin(a):.1f}" rx="{rx:.1f}" ry="{rx*0.2:.1f}" fill="none" stroke="{LN}" stroke-width="1.2" opacity="0.9"/>'
    for k in range(6):
        vals = ";".join(f"{r*abs(math.cos(math.radians(30*k + 30*j/n))):.2f}" for j in range(n + 1))
        g += (f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="none" stroke="{LN}" stroke-width="1.2" opacity="0.85">'
              f'<animate attributeName="rx" values="{vals}" dur="{dur}s" repeatCount="indefinite"/></ellipse>')
    return g

def brackets(x, y, w, h, s=14):
    p = (f"M{x} {y+s} V{y} H{x+s} M{x+w-s} {y} H{x+w} V{y+s} M{x} {y+h-s} V{y+h} H{x+s} M{x+w-s} {y+h} H{x+w} V{y+h-s}")
    return f'<path d="{p}" fill="none" stroke="{LN}" stroke-width="1.5"/>'

def row4():
    galaxy = crop((52, 580, 484, 716), 82); rocks = crop((884, 582, 1778, 714), 80)
    defs = '<clipPath id="g"><rect x="40" y="8" width="448" height="144"/></clipPath><clipPath id="r"><rect x="880" y="8" width="905" height="144"/></clipPath>'
    lines1 = ["SAME UNIVERSE.", "DIFFERENT IDEAS.", "//", "TURNING CURIOSITY", "INTO REAL THINGS."]
    t1 = "".join(f'<text x="680" y="{37+i*20}" font-size="14.5">{l}</text>' for i, l in enumerate(lines1))
    lines2 = ["EXPLORE", "BUILD", "LEARN", "AUTOMATE", "REPEAT"]
    t2 = "".join(f'<text x="1819" y="{42+i*21}" font-size="14.5">{l}</text>' for i, l in enumerate(lines2))
    body = f'''
{box(40, 8, 448, 144)}<g clip-path="url(#g)"><g transform="translate(264 80)"><g>
<image href="{galaxy}" x="-220" y="-70" width="440" height="140"/>
<animateTransform attributeName="transform" type="scale" values="1;1.07;1" dur="16s" repeatCount="indefinite"/></g></g></g>
{box(502, 8, 138, 144)}{brackets(512, 18, 118, 124)}{globe(571, 80, 52)}
{box(662, 8, 203, 144)}{t1}{hline(680, 846, 136)}{twinkle(844, 136, 9, 3.6)}
{box(880, 8, 905, 144)}<g clip-path="url(#r)"><g>
<animateTransform attributeName="transform" type="translate" values="0 0;-78 0;0 0" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="36s" repeatCount="indefinite"/>
<image href="{rocks}" x="882" y="6" width="984" height="146"/></g></g>
{box(1798, 8, 174, 144)}{t2}{hline(1819, 1852, 138)}{twinkle(1930, 62, 14, 3.9, 0.6)}'''
    write("header-4.svg", svg(2000, 160, body, defs))

if __name__ == "__main__":
    row1(); row2(); row3(); row4()

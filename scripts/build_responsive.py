#!/usr/bin/env python3
"""
build_responsive.py
Writes the root README.md so one page serves two layouts, using <picture> with a
width media query (GitHub keeps <source media>, as for dark/light logos):

  desktop (> 767px): the main HUD layout in assets/
  phone  (<= 767px): the single-column layout in variants/phone/assets/

Every desktop piece swaps to assets/blank.svg on phones. Every phone piece is a
1px assets/dot.svg on desktop (no width attribute) and swaps to the real phone SVG
on phones, where max-width:100% fits its natural 800px width to the screen. Phone
pieces share a line with desktop pieces whose widths leave a few px of slack, so
they add no extra lines on desktop.
"""
import os
from build_header import ROOT

MQ = "(max-width: 767px)"
P = "variants/phone/assets/"
GH, LI, EM = "https://github.com/OVERxPOWERED", "https://www.linkedin.com/in/burhanuddin-bohra-629abb370/", "mailto:6burhanuddin6@gmail.com"
REPO = "https://github.com/OVERxPOWERED/"

def pic(default, hidden=None, phone=None, width=None, alt="", href=None):
    """One slot. hidden: swap to blank on phones. phone: swap to this phone SVG on phones."""
    src = hidden or phone
    source = f'<source media="{MQ}" srcset="{src}">' if src else ""
    w = f' width="{round(width, 2):g}%"' if width else ""
    img = f'<picture>{source}<img src="{default}"{w} alt="{alt}"/></picture>'
    return f'<a href="{href}">{img}</a>' if href else img

def desk(svg, w=100, alt="", href=None, phone=None):
    """A desktop piece. With phone= it becomes that phone SVG on phones, otherwise it blanks out."""
    return pic(f"assets/{svg}", hidden=None if phone else "assets/blank.svg", phone=P + phone if phone else None, width=w, alt=alt, href=href)

def phone_only(svg, alt="", href=None):
    return pic("assets/dot.svg", phone=P + svg, alt=alt, href=href)

K = 0.992   # shrink multi-piece lines a little so the 1px phone slots always fit beside them
lines = [
    [desk("header-1.svg", alt="Burhanuddin Bohra: Full-Stack Web & Software Developer", phone="hero.svg")],
    [desk("header-2.svg", alt="")],
    [desk("header-3a.svg", 17 * K, "GitHub: OVERxPOWERED", GH), desk("header-3b.svg", 17 * K, "LinkedIn: Burhanuddin Bohra", LI),
     desk("header-3c.svg", 22 * K, "Email: 6burhanuddin6@gmail.com", EM), desk("header-3d.svg", 44 * K, "Products / Open Source / Automations / Drones / Gaming / UI-UX / Design"),
     phone_only("btn-github.svg", "GitHub: OVERxPOWERED", GH), phone_only("btn-linkedin.svg", "LinkedIn: Burhanuddin Bohra", LI), phone_only("btn-email.svg", "Email: 6burhanuddin6@gmail.com", EM)],
    [desk("header-4.svg", alt="Same universe. Different ideas. Explore, build, learn, automate, repeat.")],
    [desk("section-about.svg", alt="02 About", phone="about.svg")],
    [desk("section-arsenal.svg", alt="03 Arsenal: frontend, backend and systems tools", phone="arsenal.svg")],
    [desk("section-work.svg", alt="04 Selected work", phone="work-title.svg")],
    [desk(f"work-{i+1}.svg", w * K, n, REPO + n) for i, (n, w) in enumerate([("op-caelestia-shell", 25.85), ("PocketFix", 24.15), ("Marg", 24.15), ("QuizSolver", 25.85)])]
    + [phone_only(f"work-{i+1}.svg", n, REPO + n) for i, n in enumerate(["op-caelestia-shell", "PocketFix", "Marg", "QuizSolver"])],
    [desk("section-oss.svg", alt="05 Open source", phone="oss-title.svg")],
    [desk("oss-1.svg", 50 * K, "Cero-Terminal", "https://github.com/NetPranav/Cero-Terminal"), desk("oss-2.svg", 50 * K, "WebGen, originally LazyLayouts", "https://github.com/NetPranav/WebGen"),
     phone_only("oss-1.svg", "Cero-Terminal", "https://github.com/NetPranav/Cero-Terminal"), phone_only("oss-2.svg", "WebGen, originally LazyLayouts", "https://github.com/NetPranav/WebGen")],
    [desk("section-stats.svg", alt="06 Live GitHub stats", phone="stats.svg")],
    [desk("section-footer.svg", alt="Explore, build, learn, automate, repeat", phone="footer.svg")],
]

def svg_file(name, w, h, body=""):
    open(os.path.join(ROOT, "assets", name), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>')

if __name__ == "__main__":
    svg_file("blank.svg", 1000, 1)      # hides a desktop piece on phones (about 0px tall at any width)
    svg_file("dot.svg", 1, 1)           # 1px placeholder for a phone piece on desktop
    body = "<p>\n" + "\n".join("".join(l) for l in lines) + "\n</p>\n"
    open(os.path.join(ROOT, "README.md"), "w").write(body)

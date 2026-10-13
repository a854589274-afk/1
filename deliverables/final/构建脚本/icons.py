"""Flat-vector icon set (512x512, transparent background, no text/letters/numbers/logos).
Palette: navy #1F3A5F, teal #148F8A, orange #E8833A (small accents), light greys."""
import math, os, sys

NAVY = "#1F3A5F"; TEAL = "#148F8A"; TEAL2 = "#3FC1B8"; ORANGE = "#E8833A"
L1 = "#E9EFF5"; L2 = "#D5DFE9"; L3 = "#C9D5E1"; BLOOD = "#C94A3F"; BACK = "#E3ECF3"; WHITE = "#FFFFFF"
STRAW = "#F3C98F"


def svg(body, backdrop=True):
    bd = f'<circle cx="256" cy="256" r="236" fill="{BACK}"/>' if backdrop else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">'
            f'<defs><filter id="s" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="8" '
            f'stdDeviation="9" flood-color="#1F3A5F" flood-opacity="0.18"/></filter></defs>{bd}{body}</svg>')


def rr(x, y, w, h, r, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'


def tube(x, y, w, h, cap=NAVY, layers=((0.55, BLOOD, 0.75),), body=WHITE):
    """layers: (start_fraction_from_top, color, opacity) painted to the bottom."""
    s = [rr(x, y, w, h, w / 2, body, f'stroke="{NAVY}" stroke-width="8"')]
    for frac, col, op in layers:
        yy = y + h * frac
        s.append(f'<path d="M{x+4} {yy} H{x+w-4} V{y+h-w/2} A{w/2-4} {w/2-4} 0 0 1 {x+4} {y+h-w/2} Z" '
                 f'fill="{col}" fill-opacity="{op}"/>')
    s.append(rr(x - 8, y - 34, w + 16, 40, 10, cap))
    return "".join(s)


def screen(x, y, w, h):
    pts = []
    for k in range(7):
        px = x + 12 + k * (w - 24) / 6
        py = y + h * 0.62 - math.sin(k * 1.0) * h * 0.2 - k * h * 0.03
        pts.append(f"{px:.1f},{py:.1f}")
    return (rr(x, y, w, h, 10, TEAL) +
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="{WHITE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')


def carousel(cx, cy, r):
    s = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{L2}"/>', f'<circle cx="{cx}" cy="{cy}" r="{r*0.7}" fill="{L3}"/>']
    for k in range(8):
        a = k * math.pi / 4
        s.append(f'<circle cx="{cx+r*0.85*math.cos(a):.1f}" cy="{cy+r*0.85*math.sin(a):.1f}" r="{r*0.13:.1f}" fill="{NAVY}" fill-opacity="0.8"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.24}" fill="{TEAL}"/>')
    return "".join(s)


def analyzer(cx, by, w, h, kind="a"):
    """front view, base centre (cx, by)."""
    x = cx - w / 2; y = by - h
    s = [f'<g filter="url(#s)">', rr(x, y, w, h, 18, L1)]
    if kind == "a":       # screen top, carousel bottom
        s.append(rr(x, y, w, h * 0.16, 18, L2))
        s.append(screen(x + w * 0.12, y + h * 0.24, w * 0.76, h * 0.26))
        s.append(carousel(cx, y + h * 0.72, min(w, h) * 0.16))
        s.append(f'<circle cx="{x+w-22}" cy="{y+h*0.08}" r="8" fill="{ORANGE}"/>')
    elif kind == "b":     # carousel left, screen right, tube rack
        s.append(carousel(x + w * 0.3, y + h * 0.38, min(w, h) * 0.2))
        s.append(screen(x + w * 0.58, y + h * 0.16, w * 0.32, h * 0.32))
        for k in range(6):
            tx = x + w * 0.12 + k * w * 0.13
            s.append(rr(tx, y + h * 0.7, w * 0.07, h * 0.2, 6, WHITE))
            s.append(rr(tx - 2, y + h * 0.66, w * 0.07 + 4, h * 0.07, 4, TEAL if k == 2 else NAVY))
    s.append("</g>")
    return "".join(s)


def person(cx, cy, scale=1.0, coat=WHITE, shirt=TEAL, stetho=False, glasses=False):
    s = 1.0 * scale
    g = [f'<g transform="translate({cx},{cy}) scale({s})">']
    g.append(f'<path d="M-120 170 Q-120 40 0 40 Q120 40 120 170 Z" fill="{coat}" stroke="{NAVY}" stroke-width="8"/>')
    g.append(f'<path d="M-34 44 L0 110 L34 44 Z" fill="{shirt}"/>')
    g.append(f'<circle cx="0" cy="-30" r="62" fill="#F2D2B6"/>')
    g.append(f'<path d="M-62 -36 Q-60 -100 0 -98 Q62 -100 62 -36 Q40 -66 0 -64 Q-40 -66 -62 -36 Z" fill="{NAVY}"/>')
    if glasses:
        g.append(f'<rect x="-46" y="-40" width="38" height="24" rx="8" fill="none" stroke="{NAVY}" stroke-width="6"/>')
        g.append(f'<rect x="8" y="-40" width="38" height="24" rx="8" fill="none" stroke="{NAVY}" stroke-width="6"/>')
        g.append(f'<line x1="-8" y1="-30" x2="8" y2="-30" stroke="{NAVY}" stroke-width="5"/>')
    if stetho:
        g.append(f'<path d="M-40 60 Q-60 130 -10 140 Q30 142 34 112" fill="none" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>')
        g.append(f'<circle cx="36" cy="104" r="14" fill="{TEAL}"/>')
    g.append("</g>")
    return "".join(g)


def bubble(x, y, w, h, fill=WHITE, tail="left"):
    tx = x + 40 if tail == "left" else x + w - 40
    return (f'<g filter="url(#s)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h*0.35}" fill="{fill}"/>'
            f'<path d="M{tx-18} {y+h-4} L{tx-34 if tail=="left" else tx+34} {y+h+40} L{tx+20} {y+h-4} Z" fill="{fill}"/></g>')


def building(x, by, w, h, roof=NAVY, sign=True):
    y = by - h
    s = [f'<g filter="url(#s)">', rr(x, y, w, h, 12, L1),
         f'<path d="M{x-12} {y+16} L{x+w/2} {y-38} L{x+w+12} {y+16} Z" fill="{roof}"/>']
    cols, rows = 3, 2
    for i in range(cols):
        for j in range(rows):
            wx = x + w * 0.12 + i * w * 0.29; wy = y + h * 0.22 + j * h * 0.26
            s.append(rr(wx, wy, w * 0.18, h * 0.16, 5, TEAL if (i + j) % 2 == 0 else TEAL2, 'fill-opacity="0.85"'))
    s.append(rr(x + w * 0.4, by - h * 0.26, w * 0.2, h * 0.26, 6, NAVY))
    if sign:
        # flask emblem (generic, not a logo)
        fx, fy = x + w / 2, y - 4
        s.append(f'<circle cx="{fx}" cy="{fy+30}" r="0" fill="none"/>')
    s.append("</g>")
    return "".join(s)


def flask(cx, cy, s=1.0, fill=TEAL):
    return (f'<g transform="translate({cx},{cy}) scale({s})"><path d="M-14 -40 H14 V-6 L42 40 Q46 50 36 50 H-36 Q-46 50 -42 40 L-14 -6 Z" '
            f'fill="{WHITE}" stroke="{NAVY}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M-30 26 H30 L38 40 Q40 46 34 46 H-34 Q-40 46 -38 40 Z" fill="{fill}"/>'
            f'<rect x="-20" y="-50" width="40" height="12" rx="5" fill="{NAVY}"/></g>')


def arrow_double(x1, x2, y, color=NAVY, w=12):
    return (f'<line x1="{x1+26}" y1="{y}" x2="{x2-26}" y2="{y}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x1} {y} L{x1+34} {y-24} L{x1+34} {y+24} Z" fill="{color}"/>'
            f'<path d="M{x2} {y} L{x2-34} {y-24} L{x2-34} {y+24} Z" fill="{color}"/>')


def cycle_arrow(cx, cy, r, color=TEAL, w=16, start=200, end=500):
    a0, a1 = math.radians(start), math.radians(end)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    large = 1 if (end - start) % 360 > 180 else 0
    tip_a = a1 + math.pi / 2
    hx, hy = x1 + 26 * math.cos(tip_a), y1 + 26 * math.sin(tip_a)
    lx, ly = x1 + 22 * math.cos(a1), y1 + 22 * math.sin(a1)
    rx_, ry_ = x1 - 22 * math.cos(a1), y1 - 22 * math.sin(a1)
    return (f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{lx:.1f} {ly:.1f} L{hx:.1f} {hy:.1f} L{rx_:.1f} {ry_:.1f} Z" fill="{color}"/>')


def check(cx, cy, s=1.0, color=TEAL):
    return (f'<circle cx="{cx}" cy="{cy}" r="{38*s}" fill="{color}"/>'
            f'<path d="M{cx-17*s} {cy+1*s} L{cx-4*s} {cy+14*s} L{cx+19*s} {cy-12*s}" fill="none" stroke="{WHITE}" stroke-width="{9*s}" stroke-linecap="round" stroke-linejoin="round"/>')


def gear(cx, cy, r, fill=NAVY, teeth=8):
    pts = []
    for k in range(teeth * 2):
        a = k * math.pi / teeth
        rr_ = r if k % 2 == 0 else r * 0.8
        for d in (-0.16, 0.16):
            pts.append(f"{cx+rr_*math.cos(a+d):.1f},{cy+rr_*math.sin(a+d):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/><circle cx="{cx}" cy="{cy}" r="{r*0.34}" fill="{BACK}"/>'


def bottle(x, by, w, h, cap=NAVY, liquid=TEAL, label=True):
    y = by - h
    s = [f'<g filter="url(#s)">', rr(x, y + h * 0.18, w, h * 0.82, 22, WHITE, f'stroke="{NAVY}" stroke-width="8"'),
         rr(x + w * 0.28, y + h * 0.04, w * 0.44, h * 0.18, 8, WHITE, f'stroke="{NAVY}" stroke-width="8"'),
         rr(x + w * 0.22, y - h * 0.06, w * 0.56, h * 0.13, 8, cap),
         f'<path d="M{x+6} {y+h*0.52} H{x+w-6} V{by-22} Q{x+w-6} {by-6} {x+w-22} {by-6} H{x+22} Q{x+6} {by-6} {x+6} {by-22} Z" fill="{liquid}" fill-opacity="0.85"/>']
    if label:
        s.append(rr(x + w * 0.16, y + h * 0.3, w * 0.68, h * 0.14, 6, L2))
    s.append("</g>")
    return "".join(s)


def vial(x, by, w, h, cap=NAVY, level=0.5, liquid=TEAL, op=0.85):
    y = by - h
    lv = y + h * (1 - level)
    return (f'<g filter="url(#s)">' + rr(x, y, w, h, 14, WHITE, f'stroke="{NAVY}" stroke-width="7"') +
            f'<path d="M{x+5} {lv} H{x+w-5} V{by-16} Q{x+w-5} {by-5} {x+w-16} {by-5} H{x+16} Q{x+5} {by-5} {x+5} {by-16} Z" fill="{liquid}" fill-opacity="{op}"/>' +
            rr(x - 6, y - 26, w + 12, 32, 8, cap) + '</g>')


def card(x, y, w, h):
    return f'<g filter="url(#s)">' + rr(x, y, w, h, 24, WHITE) + '</g>'


# ------------------------------------------------------------------ icons
ICONS = {}


def icon(name):
    def deco(f):
        ICONS[name] = f
        return f
    return deco


@icon("toc_scales")
def _():
    b = [f'<g filter="url(#s)">', rr(244, 130, 24, 250, 10, NAVY), rr(170, 372, 172, 34, 14, NAVY),
         rr(110, 150, 292, 22, 11, NAVY), f'<circle cx="256" cy="142" r="22" fill="{ORANGE}"/>']
    for cx in (140, 372):
        b.append(f'<line x1="{cx}" y1="166" x2="{cx-52}" y2="282" stroke="{NAVY}" stroke-width="6"/>')
        b.append(f'<line x1="{cx}" y1="166" x2="{cx+52}" y2="282" stroke="{NAVY}" stroke-width="6"/>')
        b.append(f'<path d="M{cx-74} 280 H{cx+74} Q{cx+64} 336 {cx} 336 Q{cx-64} 336 {cx-74} 280 Z" fill="{TEAL}"/>')
    b.append("</g>")
    return "".join(b)


@icon("toc_tubes")
def _():
    return (f'<g filter="url(#s)">{tube(150, 150, 64, 230, cap=NAVY, layers=((0.45, BLOOD, 0.7),))}'
            f'{tube(298, 150, 64, 230, cap=TEAL, layers=((0.45, BLOOD, 0.7),))}</g>'
            + arrow_double(206, 306, 300, color=ORANGE, w=12))


@icon("toc_building")
def _():
    return building(126, 400, 260, 210) + flask(256, 132, 0.95)


# 4.1 verification conditions
@icon("c41_a_serum_plasma")
def _():
    return (f'<g filter="url(#s)">{tube(150, 140, 70, 250, cap=ORANGE, layers=((0.42, STRAW, 0.95), (0.62, BLOOD, 0.75)))}'
            f'{tube(292, 140, 70, 250, cap=TEAL, layers=((0.42, STRAW, 0.95), (0.6, WHITE, 0.0), (0.62, BLOOD, 0.75)))}</g>'
            f'<rect x="296" y="290" width="62" height="10" fill="{L3}"/>')


@icon("c41_b_two_brands")
def _():
    return analyzer(160, 380, 170, 230, "a") + analyzer(350, 380, 190, 170, "b")


@icon("c41_c_identical")
def _():
    return analyzer(160, 380, 160, 220, "a") + analyzer(352, 380, 160, 220, "a")


@icon("c41_d_modules")
def _():
    s = ['<g filter="url(#s)">']
    for k, x in enumerate((96, 206, 316)):
        s.append(rr(x, 150, 100, 200, 14, L1))
        s.append(carousel(x + 50, 210, 30))
        s.append(rr(x + 16, 262, 68, 18, 5, L3))
        s.append(f'<circle cx="{x+50}" cy="318" r="10" fill="{TEAL if k != 1 else ORANGE}"/>')
    s.append(rr(80, 350, 352, 50, 12, L2))
    for k in range(12):
        s.append(rr(100 + k * 26, 358, 14, 32, 5, WHITE))
        s.append(rr(98 + k * 26, 352, 18, 10, 3, NAVY))
    s.append(screen(210, 92, 92, 46))
    s.append("</g>")
    return "".join(s)


@icon("c41_e_sites")
def _():
    s = []
    pos = [(256, 200), (140, 380), (372, 380)]
    for (x1, y1), (x2, y2) in ((pos[0], pos[1]), (pos[1], pos[2]), (pos[2], pos[0])):
        s.append(f'<line x1="{x1}" y1="{y1-40}" x2="{x2}" y2="{y2-40}" stroke="{TEAL2}" stroke-width="8" stroke-dasharray="4 16" stroke-linecap="round"/>')
    for (x, by), sc in zip(pos, (1.0, 0.85, 0.85)):
        w, h = 120 * sc, 100 * sc
        s.append(building(x - w / 2, by, w, h))
    for (x, by) in pos:
        s.append(f'<circle cx="{x}" cy="{by-40}" r="0"/>')
    return "".join(s)


# 4.2 eight situations
@icon("t42_qc_drift")
def _():
    s = [card(96, 120, 320, 272)]
    for yy, dash in ((180, "10 10"), (256, ""), (332, "10 10")):
        s.append(f'<line x1="124" y1="{yy}" x2="388" y2="{yy}" stroke="{L3 if dash else NAVY}" stroke-width="5" stroke-dasharray="{dash}"/>')
    ys = [262, 248, 266, 240, 228, 214, 200, 188]
    pts = [(140 + i * 34, y) for i, y in enumerate(ys)]
    s.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{TEAL}" stroke-width="6"/>')
    for i, (x, y) in enumerate(pts):
        s.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{ORANGE if i >= 5 else TEAL}"/>')
    return "".join(s)


@icon("t42_eqa_corrected")
def _():
    s = [card(120, 110, 220, 290), rr(190, 92, 80, 40, 12, NAVY)]
    for k in range(4):
        s.append(rr(156, 170 + k * 46, 150, 14, 7, L3))
    s.append(f'<circle cx="368" cy="330" r="74" fill="{WHITE}" filter="url(#s)"/>')
    s.append(cycle_arrow(368, 330, 44, TEAL, 12, 210, 480))
    return "".join(s)


@icon("t42_reagent_lot")
def _():
    return (bottle(110, 390, 120, 220, cap=NAVY, liquid=TEAL) + bottle(282, 390, 120, 220, cap=ORANGE, liquid=TEAL2)
            + f'<path d="M210 150 Q256 108 302 150" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>'
            + f'<path d="M302 150 L276 146 L292 126 Z" fill="{NAVY}"/>'
            + f'<path d="M302 424 Q256 462 210 424" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>'
            + f'<path d="M210 424 L236 428 L220 448 Z" fill="{NAVY}"/>')


@icon("t42_repair")
def _():
    return (gear(220, 280, 120, NAVY) +
            f'<g transform="rotate(-40 300 240)"><rect x="284" y="150" width="34" height="210" rx="16" fill="{TEAL}"/>'
            f'<path d="M262 120 a40 40 0 1 0 78 0 l-18 0 l0 30 l-42 0 l0 -30 z" fill="{TEAL}"/></g>'
            + f'<circle cx="220" cy="280" r="20" fill="{ORANGE}"/>')


@icon("t42_software")
def _():
    s = ['<g filter="url(#s)">', rr(96, 120, 320, 220, 20, NAVY), rr(116, 140, 280, 180, 10, WHITE),
         rr(226, 340, 60, 40, 4, NAVY), rr(176, 376, 160, 22, 10, NAVY), '</g>']
    s.append(rr(136, 160, 110, 14, 7, L3)); s.append(rr(136, 188, 80, 14, 7, L3)); s.append(rr(136, 216, 100, 14, 7, L3))
    s.append(f'<circle cx="320" cy="236" r="58" fill="{BACK}"/>')
    s.append(cycle_arrow(320, 236, 40, TEAL, 12, 200, 470))
    s.append(f'<circle cx="320" cy="236" r="10" fill="{ORANGE}"/>')
    return "".join(s)


@icon("t42_clinician")
def _():
    s = [person(210, 300, 0.95, coat=WHITE, shirt=TEAL, stetho=True)]
    s.append(bubble(290, 96, 170, 96, tail="left"))
    for k in range(3):
        s.append(f'<circle cx="{332+k*44}" cy="144" r="12" fill="{NAVY}"/>')
    return "".join(s)


@icon("t42_patient")
def _():
    s = [person(210, 300, 0.95, coat=TEAL2, shirt=NAVY)]
    s.append(bubble(290, 96, 170, 96, tail="left"))
    s.append(f'<polyline points="318,150 346,124 374,166 402,124 430,150" fill="none" stroke="{ORANGE}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(s)


@icon("t42_frequency")
def _():
    s = [card(100, 130, 312, 270), rr(100, 130, 312, 64, 24, NAVY), rr(100, 164, 312, 30, 0, NAVY)]
    s.append(rr(160, 104, 22, 54, 10, TEAL)); s.append(rr(330, 104, 22, 54, 10, TEAL))
    for i in range(5):
        for j in range(3):
            cx, cy = 140 + i * 58, 236 + j * 56
            on = (i + j * 5) % 2 == 0
            s.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{TEAL if on else L2}"/>')
    s.append(f'<circle cx="400" cy="380" r="62" fill="{WHITE}" filter="url(#s)"/>')
    s.append(cycle_arrow(400, 380, 36, ORANGE, 11, 200, 470))
    return "".join(s)


# 5+6 preparation
@icon("p6_technician")
def _():
    return person(236, 290, 1.05, coat=WHITE, shirt=TEAL, glasses=True) + \
        f'<g transform="rotate(25 380 250)"><rect x="370" y="150" width="22" height="160" rx="10" fill="{NAVY}"/><path d="M372 310 L390 310 L384 352 L378 352 Z" fill="{TEAL}"/><rect x="362" y="136" width="38" height="24" rx="8" fill="{ORANGE}"/></g>'


@icon("p6_analyzer")
def _():
    return analyzer(256, 400, 240, 270, "a")


@icon("p6_reagents")
def _():
    return bottle(96, 400, 140, 250, cap=NAVY, liquid=TEAL) + bottle(266, 400, 120, 190, cap=ORANGE, liquid=TEAL2)


@icon("p6_tubes")
def _():
    s = ['<g filter="url(#s)">']
    for k, cap in enumerate((NAVY, TEAL, NAVY, ORANGE)):
        s.append(tube(128 + k * 70, 150, 50, 200, cap=cap, layers=((0.4, BLOOD, 0.72),)))
    s.append(rr(100, 300, 312, 40, 10, L3))
    s.append(rr(100, 360, 312, 30, 10, NAVY))
    s.append("</g>")
    return "".join(s)


@icon("p6_controls")
def _():
    return (vial(120, 390, 76, 170, cap=NAVY, level=0.35, liquid=TEAL, op=0.45) +
            vial(218, 390, 76, 170, cap=TEAL, level=0.55, liquid=TEAL, op=0.7) +
            vial(316, 390, 76, 170, cap=ORANGE, level=0.75, liquid=TEAL, op=0.95) +
            rr(100, 392, 312, 26, 10, L3))


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, f in ICONS.items():
        open(os.path.join(out, name + ".svg"), "w").write(svg(f()))
    print(len(ICONS), "icons")

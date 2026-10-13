import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from icons import *

def scene_mutual():
    W, H = 1600, 900
    b = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><filter id="s" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#1F3A5F" flood-opacity="0.18"/></filter></defs>']
    b.append(f'<ellipse cx="800" cy="760" rx="720" ry="70" fill="{BACK}"/>')
    # path
    b.append(f'<path d="M300 760 Q800 700 1300 760" fill="none" stroke="{L3}" stroke-width="14" stroke-dasharray="2 30" stroke-linecap="round"/>')
    # hospital left (tall)
    b.append(building(110, 760, 360, 420, roof=NAVY))
    b.append(flask(290, 300, 1.3))
    # hospital right (wide, teal roof)
    b.append(building(1130, 760, 400, 330, roof=TEAL))
    b.append(flask(1330, 395, 1.3, fill=ORANGE))
    # patient (front) holding report
    b.append(person(800, 520, 1.25, coat=TEAL2, shirt=NAVY))
    b.append('<g filter="url(#s)">' + rr(740, 560, 120, 150, 10, WHITE, f'stroke="{NAVY}" stroke-width="6"'))
    for k in range(4):
        b.append(rr(760, 588 + k * 26, 80 - (k % 2) * 24, 10, 5, L3))
    b.append('</g>')
    b.append(check(848, 690, 0.8, TEAL))
    # legs
    b.append(rr(760, 728, 30, 40, 10, NAVY)); b.append(rr(810, 728, 30, 40, 10, NAVY))
    # acceptance arcs + badges
    b.append(f'<path d="M740 560 Q560 380 420 300" fill="none" stroke="{TEAL}" stroke-width="7" stroke-dasharray="14 16" stroke-linecap="round"/>')
    b.append(f'<path d="M860 560 Q1040 400 1200 360" fill="none" stroke="{TEAL}" stroke-width="7" stroke-dasharray="14 16" stroke-linecap="round"/>')
    b.append(f'<circle cx="420" cy="290" r="56" fill="{WHITE}" filter="url(#s)"/>' + check(420, 290, 1.1, TEAL))
    b.append(f'<circle cx="1200" cy="352" r="56" fill="{WHITE}" filter="url(#s)"/>' + check(1200, 352, 1.1, TEAL))
    b.append('</svg>')
    return "".join(b)

def scene_divider():
    W, H = 1920, 1080
    b = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><radialGradient id="g" cx="75%" cy="45%" r="60%"><stop offset="0%" stop-color="#27486F"/><stop offset="100%" stop-color="#1F3A5F"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#g)"/>']
    for cx, cy, r, col, op in [(1420, 470, 330, TEAL, .32), (1640, 620, 250, "#FFFFFF", .07), (1260, 690, 210, TEAL2, .22),
                               (1560, 300, 150, ORANGE, .22), (1740, 860, 120, TEAL, .25), (1180, 300, 90, "#FFFFFF", .08)]:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" fill-opacity="{op}"/>')
    # measurement arc with ticks
    cx, cy, R = 1420, 470, 420
    for k in range(0, 61):
        a = math.radians(200 + k * 2.3)
        L = 34 if k % 10 == 0 else (22 if k % 5 == 0 else 12)
        x1, y1 = cx + R * math.cos(a), cy + R * math.sin(a)
        x2, y2 = cx + (R - L) * math.cos(a), cy + (R - L) * math.sin(a)
        b.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#FFFFFF" stroke-opacity="{0.55 if k%10==0 else 0.3}" stroke-width="{4 if k%10==0 else 2.5}" stroke-linecap="round"/>')
    b.append(f'<path d="M{cx+R*math.cos(math.radians(200)):.1f} {cy+R*math.sin(math.radians(200)):.1f} A{R} {R} 0 0 1 {cx+R*math.cos(math.radians(338)):.1f} {cy+R*math.sin(math.radians(338)):.1f}" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="3"/>')
    # needle
    a = math.radians(300)
    b.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+(R-60)*math.cos(a):.1f}" y2="{cy+(R-60)*math.sin(a):.1f}" stroke="{ORANGE}" stroke-width="7" stroke-linecap="round"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="18" fill="{ORANGE}"/>')
    # horizontal ruler bottom right
    for k in range(0, 41):
        x = 1060 + k * 20; L = 30 if k % 10 == 0 else (18 if k % 5 == 0 else 10)
        b.append(f'<line x1="{x}" y1="980" x2="{x}" y2="{980-L}" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2.5"/>')
    b.append('</svg>')
    return "".join(b)

if __name__ == "__main__":
    out = sys.argv[1]
    open(os.path.join(out, "scene_mutual.svg"), "w").write(scene_mutual())
    open(os.path.join(out, "divider_bg.svg"), "w").write(scene_divider())

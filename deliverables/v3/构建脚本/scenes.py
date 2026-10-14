# -*- coding: utf-8 -*-
"""逐图场景定义。文件名＝终稿页码_序号。尺寸：主视觉16:9、对比主图16:4、示例图2:3或1:1、角图16:10、图标组按格等分。"""
import json, os, subprocess, sys, math
from art import S, NAVY, TEAL, ORANGE, GREEN, RED

HERE = os.path.dirname(os.path.abspath(__file__))
SIZES = {'16:9': (1600, 900), '16:4': (1600, 400), '2:3': (600, 900), '1:1': (800, 800), '16:10': (800, 500)}
CELL = 360
REG = {}      # name -> (ratio, fn, transparent, prompt_en, n_icons, grid)

def reg(name, ratio, prompt, transparent=False, n=1, grid=None):
    def deco(fn):
        REG[name] = (ratio, fn, transparent, prompt, n, grid)
        return fn
    return deco

# ---------- 主视觉 ----------
@reg('01_1', '16:9', 'two high-end clinical chemistry analyzers standing side by side facing the viewer, perfectly symmetrical, a single soft teal beam of light joining them at the center')
def s01():
    s = S(1600, 900, 'navy'); s.floor(720)
    s.add('<ellipse cx="1260" cy="440" rx="360" ry="260" fill="#2E5482" opacity="0.35" filter="url(#glow2)"/>')
    s.analyzer(960, 420, 250, 300, 'nav'); s.analyzer(1310, 420, 250, 300, 'tea')
    s.glow_line(1210, 545, 1310, 545, 5)
    s.glow_dot(1260, 545, 9)
    return s

@reg('18_1', '16:9', 'front view of concentric precision measurement rings and a straight scale, perfectly centered, navy background, teal light lines')
def s18():
    s = S(1600, 900, 'navy')
    cx, cy = 1150, 450
    for i, r in enumerate([330, 260, 190, 120]):
        s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#3C6390" stroke-width="{10-i*2}" opacity="0.8"/>')
        for k in range(36 if i == 0 else 0):
            a = k * math.pi / 18
            s.add(f'<line x1="{cx+(r-14)*math.cos(a):.1f}" y1="{cy+(r-14)*math.sin(a):.1f}" x2="{cx+(r+14)*math.cos(a):.1f}" y2="{cy+(r+14)*math.sin(a):.1f}" stroke="#5E86B3" stroke-width="3"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="190" fill="none" stroke="#7FF0E8" stroke-width="3" opacity="0.9"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="190" fill="none" stroke="#7FF0E8" stroke-width="16" opacity="0.25" filter="url(#glow)"/>')
    s.glow_line(cx - 380, cy, cx + 380, cy, 4)
    for k in range(-8, 9):
        h = 26 if k % 4 == 0 else 14
        s.add(f'<line x1="{cx+k*45}" y1="{cy-h}" x2="{cx+k*45}" y2="{cy+h}" stroke="#7FF0E8" stroke-width="3" opacity="0.8"/>')
    s.glow_dot(cx, cy, 10)
    return s

@reg('40_1', '16:9', 'three identical pillars of light standing in a row, front view, softly lit analyzers in the background, symmetrical and calm')
def s40():
    s = S(1600, 900, 'navy'); s.floor(700)
    for i, x in enumerate([820, 1060, 1300]):
        s.add(f'<g opacity="0.35">'); s.analyzer(x - 110 + 0, 470, 220, 230, 'nav'); s.add('</g>')
    for x in [930, 1170, 1410]:
        s.add(f'<rect x="{x-45}" y="120" width="90" height="580" rx="45" fill="#7FF0E8" opacity="0.25" filter="url(#glow2)"/>')
        s.add(f'<rect x="{x-22}" y="140" width="44" height="560" rx="22" fill="url(#beamV)"/>')
        s.add(f'<rect x="{x-6}" y="150" width="12" height="550" rx="6" fill="#FFFFFF" opacity="0.8"/>')
        s.add(f'<ellipse cx="{x}" cy="700" rx="90" ry="14" fill="#7FF0E8" opacity="0.5" filter="url(#glow)"/>')
    return s

# ---------- 图标组 ----------
def icons(n, cols=None, rows=1):
    cols = cols or n
    return S(cols * CELL, rows * CELL, transparent=True)

def cell(i, cols):
    return (i % cols) * CELL, (i // cols) * CELL

def ic_balance(s, ox, oy):
    cx = ox + 180
    s.shadow(cx, oy + 300, 160, 0.2)
    s.rr(cx - 60, oy + 285, 120, 18, 8, 'url(#nav)')
    s.rr(cx - 9, oy + 90, 18, 200, 8, 'url(#cerS)', '#B8C3CF', 1)
    s.rr(cx - 130, oy + 95, 260, 12, 6, 'url(#nav)')
    s.add(f'<circle cx="{cx}" cy="{oy+92}" r="16" fill="url(#ora)"/>')
    for dx in (-110, 110):
        s.add(f'<line x1="{cx+dx}" y1="{oy+105}" x2="{cx+dx-40}" y2="{oy+200}" stroke="#8C99A8" stroke-width="3"/><line x1="{cx+dx}" y1="{oy+105}" x2="{cx+dx+40}" y2="{oy+200}" stroke="#8C99A8" stroke-width="3"/>')
        s.add(f'<path d="M{cx+dx-55},{oy+200} h110 a55,22 0 0 1 -110,0z" fill="url(#tea)"/>')

def ic_tubes2(s, ox, oy):
    s.tube(ox + 120, oy + 60, 46, 240, 'nav', '#E9C46A', 0.6)
    s.tube(ox + 194, oy + 60, 46, 240, 'tea', '#E9C46A', 0.6)

def ic_building(s, ox, oy, accent='nav', w=230, h=210):
    s.building(ox + 180 - w / 2, oy + 300 - h, w, h, accent, floors=4, cols=5)

def ic_analyzer(s, ox, oy, accent='nav', w=230, h=230):
    s.analyzer(ox + 180 - w / 2, oy + 300 - h, w, h, accent)

@reg('02_1', 'icons', 'balance scale; two test tubes side by side; laboratory building front elevation', True, 3)
def s02():
    s = icons(3); ic_balance(s, 0, 0); ic_tubes2(s, CELL, 0); ic_building(s, 2 * CELL, 0); return s

@reg('22_1', 'icons', 'serum tube and plasma tube; two different-design analyzers; two identical analyzers; one analyzer with several modules; three laboratory buildings in a row', True, 5)
def s22():
    s = icons(5)
    s.tube(110, 60, 46, 240, 'red', '#F2D27A', 0.62); s.tube(204, 60, 46, 240, 'tea', '#EAD9A8', 0.62)
    ox = CELL
    s.analyzer(ox + 30, 150, 140, 150, 'nav'); s.analyzer(ox + 190, 110, 140, 190, 'tea', tray=False)
    ox = 2 * CELL
    s.analyzer(ox + 30, 140, 140, 160, 'nav'); s.analyzer(ox + 190, 140, 140, 160, 'nav')
    ox = 3 * CELL
    s.shadow(ox + 180, 300, 320)
    for i in range(3):
        s.analyzer(ox + 30 + i * 100, 150, 100, 150, ['nav', 'tea', 'nav'][i], tray=(i == 1))
    ox = 4 * CELL
    for i, (w, h) in enumerate([(95, 130), (120, 180), (95, 130)]):
        x = ox + [30, 120, 245][i]
        s.building(x, 300 - h, w, h, 'tea' if i == 1 else 'nav', floors=3, cols=3)
    return s

@reg('22_2', '1:1', 'front view of an arterial blood-gas syringe and a serum tube with a vertical glass divider between them')
def s22b():
    s = S(800, 800); s.floor(640)
    # 注射器（水平放置于左侧台面上，正视）
    x0, y0 = 120, 380
    s.shadow(250, 640, 300)
    s.rr(x0 + 20, 300, 60, 340, 14, 'url(#gls)', '#AFC0CC', 1.5)
    s.rr(x0 + 26, 470, 48, 164, 10, '#B23A2E', op=0.85)
    s.rr(x0 + 10, 280, 80, 22, 6, 'url(#nav)')
    s.rr(x0 + 42, 180, 16, 110, 6, 'url(#cerS)', '#B8C3CF', 1)
    s.rr(x0 - 5, 165, 110, 18, 6, 'url(#nav)')
    s.rr(x0 + 47, 640, 6, 0, 1, '#888')
    s.rr(x0 + 140 + 30, 300, 60, 340, 14, 'url(#gls)', '#AFC0CC', 1.5)
    s.rr(x0 + 176, 470, 48, 164, 10, '#B23A2E', op=0.85)
    s.rr(x0 + 160, 280, 80, 22, 6, 'url(#tea)')
    # 玻璃隔板
    s.rr(392, 150, 16, 490, 6, 'url(#gls)', '#AFC2D0', 1.5)
    s.add('<rect x="396" y="160" width="4" height="470" rx="2" fill="#FFFFFF" opacity="0.8"/>')
    s.tube(540, 220, 70, 420, 'red', '#F2D27A', 0.55)
    return s

@reg('23_1', 'icons', 'a new analyzer being unboxed; a circular calendar cycle; a reagent bottle being exchanged', True, 3)
def s23a():
    s = icons(3)
    s.analyzer(80, 120, 200, 180, 'tea')
    s.rr(50, 230, 260, 70, 6, '#D9B98C', '#B8976A', 1.5)
    s.rr(50, 230, 260, 14, 4, '#C9A877')
    ox = CELL
    cx, cy = ox + 180, 180
    s.shadow(cx, 310, 200, 0.2)
    s.add(f'<circle cx="{cx}" cy="{cy}" r="110" fill="url(#cer)" stroke="#C9D1DA" stroke-width="2"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="88" fill="none" stroke="url(#tea)" stroke-width="18" stroke-dasharray="460 93" transform="rotate(-80 {cx} {cy})"/>')
    s.add(f'<path d="M{cx+45},{cy-95} l40,-8 l-14,38 z" fill="url(#tea)"/>')
    for k in range(12):
        a = k * math.pi / 6
        s.add(f'<circle cx="{cx+60*math.cos(a):.1f}" cy="{cy+60*math.sin(a):.1f}" r="5" fill="#5B6B7F"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="14" fill="url(#ora)"/>')
    ox = 2 * CELL
    for i, (cap, lq) in enumerate([('grey', '#9FB1C2'), ('tea', '#7FD3CC')]):
        x = ox + 70 + i * 130
        s.shadow(x + 45, 300, 110, 0.2)
        s.rr(x, 130, 90, 170, 16, 'url(#gls)', '#AFC0CC', 1.5)
        s.rr(x + 8, 190, 74, 104, 12, lq, op=0.85)
        s.rr(x + 25, 100, 40, 34, 6, f'url(#{cap})')
    s.add(f'<path d="M{ox+165},{150} h30 l-10,-10 M{ox+195},{150} l-10,10" stroke="{ORANGE}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return s

@reg('23_2', 'icons', 'a drifting curve; a failed assessment sheet shape; reagent lot exchange; wrench repair; software update gear; physician raising a hand; patient at a counter; a faster clock', True, 8, (4, 2))
def s23b():
    s = icons(8, 4, 2)
    def panel(ox, oy):
        s.shadow(ox + 180, oy + 300, 240, 0.18)
        s.rr(ox + 50, oy + 70, 260, 230, 18, 'url(#cer)', '#C9D1DA', 1.5)
    # 1 漂移曲线
    ox, oy = cell(0, 4); panel(ox, oy)
    s.add(f'<line x1="{ox+75}" y1="{oy+185}" x2="{ox+285}" y2="{oy+185}" stroke="#9FB1C2" stroke-width="3" stroke-dasharray="8 6"/>')
    pts = ' '.join(f'{ox+75+i*14},{oy+185 - (i*4 if i>6 else 0) + (8 if i%2 else -8)}' for i in range(16))
    s.add(f'<polyline points="{pts}" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linejoin="round"/>')
    # 2 不合格评估单
    ox, oy = cell(1, 4)
    s.doc(ox + 95, oy + 50, 170, 250, 'solid', 6, 'nav')
    cx, cy, r = ox + 230, oy + 250, 34
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#red)"/><path d="M{cx-13},{cy-13} L{cx+13},{cy+13} M{cx+13},{cy-13} L{cx-13},{cy+13}" stroke="#fff" stroke-width="7" stroke-linecap="round"/>')
    # 3 试剂批号更换
    ox, oy = cell(2, 4)
    for i, cap in enumerate(['nav', 'tea']):
        x = ox + 70 + i * 130
        s.shadow(x + 45, oy + 300, 110, 0.2)
        s.rr(x, oy + 130, 90, 170, 16, 'url(#gls)', '#AFC0CC', 1.5)
        s.rr(x + 8, oy + 190, 74, 104, 12, '#7FD3CC' if i else '#9FB1C2', op=0.85)
        s.rr(x + 25, oy + 100, 40, 34, 6, f'url(#{cap})')
        s.rr(x + 15, oy + 150, 60, 26, 4, '#FFFFFF', '#C9D1DA', 1)
    s.add(f'<path d="M{ox+165},{oy+80} q15,-25 30,0" stroke="{ORANGE}" stroke-width="5" fill="none"/>')
    # 4 扳手维修
    ox, oy = cell(3, 4); ic_analyzer(s, ox, oy, 'nav', 200, 190)
    s.add(f'<g transform="translate({ox+250},{oy+90})"><rect x="-12" y="0" width="24" height="120" rx="10" fill="url(#ora)"/><circle cx="0" cy="0" r="30" fill="url(#ora)"/><rect x="-11" y="-34" width="22" height="34" fill="#F7F9FB"/></g>')
    # 5 软件更新齿轮
    ox, oy = cell(4, 4); panel(ox, oy)
    s.rr(ox + 80, oy + 95, 200, 120, 10, 'url(#scr)')
    s.gear(ox + 180, oy + 155, 42, 'tea', 8)
    s.rr(ox + 90, oy + 245, 180, 16, 8, '#DDE3EA'); s.rr(ox + 90, oy + 245, 120, 16, 8, 'url(#tea)')
    # 6 医生举手
    ox, oy = cell(5, 4)
    s.person(ox + 180, oy + 310, 260, '#FFFFFF', 'tea')
    s.add(f'<path d="M{ox+215},{oy+145} L{ox+250},{oy+70}" stroke="#FFFFFF" stroke-width="22" stroke-linecap="round"/><path d="M{ox+215},{oy+145} L{ox+250},{oy+70}" stroke="#C9D1DA" stroke-width="1"/><circle cx="{ox+252}" cy="{oy+62}" r="13" fill="#EED6C2"/>')
    # 7 患者在柜台前
    ox, oy = cell(6, 4)
    s.person(ox + 120, oy + 310, 230, '#9FB7D3', 'nav')
    s.shadow(ox + 250, oy + 305, 150, 0.2)
    s.rr(ox + 180, oy + 190, 150, 115, 8, 'url(#cer)', '#C9D1DA', 1.5)
    s.rr(ox + 170, oy + 180, 170, 16, 6, 'url(#tea)')
    # 8 更快的时钟
    ox, oy = cell(7, 4)
    cx, cy = ox + 180, oy + 180
    s.shadow(cx, oy + 305, 200, 0.2)
    s.add(f'<circle cx="{cx}" cy="{cy}" r="110" fill="url(#cer)" stroke="url(#nav)" stroke-width="14"/>')
    for k in range(12):
        a = k * math.pi / 6
        s.add(f'<line x1="{cx+80*math.cos(a):.1f}" y1="{cy+80*math.sin(a):.1f}" x2="{cx+92*math.cos(a):.1f}" y2="{cy+92*math.sin(a):.1f}" stroke="#5B6B7F" stroke-width="4"/>')
    s.add(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-70}" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/><line x1="{cx}" y1="{cy}" x2="{cx+50}" y2="{cy+20}" stroke="{ORANGE}" stroke-width="7" stroke-linecap="round"/>')
    s.add(f'<path d="M{cx-150},{cy-30} h40 M{cx-160},{cy} h50 M{cx-150},{cy+30} h40" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')
    return s

@reg('26_1', 'icons', 'lab technician standing upright; analyzer; reagent bottles; patient blood tubes; quality-control vials', True, 5)
def s26():
    s = icons(5)
    s.person(180, 320, 280, '#FFFFFF', 'tea')
    ic_analyzer(s, CELL, 0, 'nav', 240, 220)
    ox = 2 * CELL
    for i, cap in enumerate(['nav', 'tea', 'nav']):
        x = ox + 45 + i * 95
        s.shadow(x + 40, 300, 100, 0.2)
        s.rr(x, 140, 80, 160, 14, 'url(#gls)', '#AFC0CC', 1.5)
        s.rr(x + 7, 190, 66, 104, 10, ['#9FB1C2', '#7FD3CC', '#B9C7DA'][i], op=0.85)
        s.rr(x + 22, 112, 36, 30, 6, f'url(#{cap})')
    ox = 3 * CELL
    for i in range(3):
        s.tube(ox + 85 + i * 70, 70, 44, 230, ['red', 'nav', 'tea'][i], '#A93226', 0.65)
    ox = 4 * CELL
    for i, lq in enumerate(['#F6E7B5', '#E9C46A', '#C98A2B']):
        s.vial(ox + 70 + i * 80, 140, 60, 160, 'tea', lq)
    return s

@reg('26_2', '1:1', 'front view of a brightly lit patient blood tube beside a dimmer proficiency-testing vial')
def s26b():
    s = S(800, 800); s.floor(640)
    s.tube(250, 170, 90, 470, 'red', '#A93226', 0.62, glow='#7FF0E8')
    s.add('<g opacity="0.55">'); s.vial(470, 330, 130, 310, 'grey', '#C9B98F'); s.add('</g>')
    return s

# ---------- 示例图 / 对比图 / 角图 ----------
@reg('03_1', '1:1', 'front view of two hospital buildings of equal height linked by a straight glowing bridge, one report document centered on the bridge')
def s03():
    s = S(800, 800); s.floor(620)
    s.building(70, 250, 230, 370, 'nav', 6, 4); s.building(500, 250, 230, 370, 'tea', 6, 4)
    s.rr(300, 395, 200, 26, 6, 'url(#gls)', '#AFC2D0', 1.5)
    s.glow_line(300, 408, 500, 408, 4)
    s.doc(355, 290, 90, 105, 'solid', 5, 'tea')
    return s

@reg('04_1', '2:3', 'front view of a straight staircase of glass steps rising toward a hospital entrance, symmetrical')
def s04():
    s = S(600, 900); s.floor(800)
    s.building(100, 120, 400, 330, 'nav', 4, 5)
    for i in range(7):
        w = 250 + i * 50
        s.rr(300 - w / 2, 450 + i * 50, w, 50, 6, 'url(#gls)', '#AFC2D0', 1.5)
        s.add(f'<rect x="{300-w/2+8}" y="{452+i*50}" width="{w-16}" height="4" rx="2" fill="#7FF0E8" opacity="0.8"/>')
    return s

@reg('05_1', '2:3', 'front view of a translucent ice block standing upright with a straight crack, warm teal light emerging from inside, symmetrical')
def s05():
    s = S(600, 900); s.floor(760)
    s.shadow(300, 760, 360)
    s.add('<rect x="270" y="200" width="60" height="540" fill="#7FF0E8" opacity="0.6" filter="url(#glow2)"/>')
    s.rr(120, 220, 360, 540, 26, 'url(#gls)', '#9FCFD6', 2)
    s.add('<rect x="140" y="240" width="40" height="500" rx="20" fill="#FFFFFF" opacity="0.6"/>')
    s.add('<path d="M300,230 L288,330 L312,420 L292,520 L310,620 L300,750" fill="none" stroke="#7FF0E8" stroke-width="7"/>')
    s.add('<path d="M300,230 L288,330 L312,420 L292,520 L310,620 L300,750" fill="none" stroke="#FFFFFF" stroke-width="2"/>')
    return s

@reg('06_1', '1:1', 'two document sheets side by side, front view: left translucent with dashed outline as a draft, right solid and complete with a check-mark shape as final, symmetrical')
def s06():
    s = S(800, 800); s.floor(650)
    s.doc(90, 190, 270, 360, 'draft', 8, 'nav'); s.doc(440, 190, 270, 360, 'solid', 8, 'tea', check=True)
    return s

@reg('07_1', '16:10', 'front view of a hardbound regulation book standing upright with six bookmark ribbons of different lengths')
def s07():
    s = S(800, 500); s.floor(440)
    s.book(270, 70, 260, 370, 'nav', ribbons=[50, 80, 120, 60, 95, 40])
    return s

@reg('08_1', '2:3', 'front view of an open SOP binder on a stand beside a precision analyzer, symmetrical')
def s08():
    s = S(600, 900); s.floor(760)
    s.analyzer(90, 480, 420, 280, 'nav')
    s.shadow(300, 470, 300, 0.2)
    s.rr(270, 400, 60, 70, 6, 'url(#cerS)', '#B8C3CF', 1)
    s.add('<path d="M120,170 L300,200 L300,420 L120,390 Z" fill="#FFFFFF" stroke="#C9D1DA" stroke-width="1.5"/>')
    s.add('<path d="M480,170 L300,200 L300,420 L480,390 Z" fill="#FFFFFF" stroke="#C9D1DA" stroke-width="1.5"/>')
    for i in range(7):
        s.add(f'<line x1="{145}" y1="{215+i*24}" x2="{275}" y2="{237+i*24}" stroke="#C5CDD6" stroke-width="7" stroke-linecap="round"/>')
        s.add(f'<line x1="{325}" y1="{237+i*24}" x2="{455}" y2="{215+i*24}" stroke="#C5CDD6" stroke-width="7" stroke-linecap="round"/>')
    s.add('<rect x="292" y="190" width="16" height="235" rx="6" fill="url(#nav)"/>')
    s.add('<path d="M400,180 h22 v70 l-11,-10 l-11,10 z" fill="url(#ora)"/>')
    return s

@reg('09_1', '16:10', 'front view of a calibration weight set and a pipette on a calibration stand')
def s09():
    s = S(800, 500); s.floor(420)
    s.shadow(300, 420, 360)
    s.rr(110, 395, 380, 26, 8, 'url(#nav)')
    for x, w, h in [(140, 70, 110), (230, 90, 150), (340, 70, 110), (430, 40, 70)]:
        s.rr(x, 395 - h, w, h - 20, w * 0.18, 'url(#cerS)', '#B8C3CF', 1.2)
        s.rr(x + w * 0.3, 395 - h - 22, w * 0.4, 26, 8, 'url(#cerS)', '#B8C3CF', 1.2)
    s.shadow(620, 420, 120)
    s.rr(560, 395, 120, 24, 8, 'url(#tea)')
    s.rr(612, 70, 16, 330, 6, 'url(#cerS)', '#B8C3CF', 1)
    s.rr(585, 90, 70, 150, 26, 'url(#cer)', '#B8C3CF', 1.5)
    s.rr(605, 60, 30, 34, 8, 'url(#ora)')
    s.add('<path d="M605,240 L635,240 L622,330 L618,330 Z" fill="url(#gls)" stroke="#AFC0CC" stroke-width="1.2"/>')
    return s

@reg('10_1', '16:10', 'front view of a rack holding quality-control vials of three concentration levels, light to dark liquid')
def s10():
    s = S(800, 500); s.floor(420)
    s.rack(140, 360, 520, 60)
    for i, lq in enumerate(['#F6E7B5', '#F6E7B5', '#E9C46A', '#E9C46A', '#C98A2B', '#C98A2B']):
        s.vial(175 + i * 78, 175, 58, 200, ['tea', 'tea', 'nav', 'nav', 'ora', 'ora'][i], lq)
    return s

@reg('11_1', '16:10', 'front view of a central laboratory building linked by straight light lines to six smaller laboratory buildings arranged symmetrically')
def s11():
    s = S(800, 500); s.floor(430)
    xs = [40, 145, 250, 470, 575, 680]
    for x in xs:
        s.glow_line(400, 330, x + 40, 390, 2)
    for x in xs:
        s.building(x, 340, 80, 90, 'tea', 2, 3, door=False)
    s.building(310, 170, 180, 260, 'nav', 5, 4)
    return s

@reg('12_1', '2:3', 'front view of two laboratories of equal size with identical sample tubes on a shared bench between them')
def s12():
    s = S(600, 900); s.floor(760)
    s.building(40, 250, 210, 330, 'nav', 5, 3); s.building(350, 250, 210, 330, 'tea', 5, 3)
    s.shadow(300, 760, 480)
    s.rr(70, 640, 460, 26, 6, 'url(#cerS)', '#B8C3CF', 1.2)
    s.rr(100, 666, 20, 94, 4, '#8C99A8'); s.rr(480, 666, 20, 94, 4, '#8C99A8')
    for i in range(6):
        s.tube(140 + i * 58, 500, 34, 140, 'nav' if i < 3 else 'tea', '#E9C46A', 0.55)
    return s

@reg('13_1', '16:10', 'two transparent document sheets placed side by side, front view, the differing regions softly glowing orange, symmetrical')
def s13():
    s = S(800, 500); s.floor(450)
    s.doc(150, 60, 220, 370, 'solid', 10, 'nav', glow_rows=[2, 6])
    s.doc(430, 60, 220, 370, 'solid', 10, 'tea', glow_rows=[2, 6])
    return s

@reg('14_1', '16:10', 'two document sheets side by side, front view: left faded grey as old version, right bright as new version, a straight horizontal arrow of light from left to right')
def s14():
    s = S(800, 500); s.floor(450)
    s.doc(110, 70, 220, 360, 'faded', 10, 'nav'); s.doc(470, 70, 220, 360, 'solid', 10, 'tea')
    s.glow_line(345, 250, 455, 250, 5)
    s.add('<path d="M452,232 L474,250 L452,268 Z" fill="#7FF0E8"/>')
    return s

@reg('15_1', '2:3', 'front view of a symmetrical five-tier frosted glass pyramid, each tier softly lit')
def s15():
    s = S(600, 900); s.floor(770)
    s.shadow(300, 770, 520)
    cols = ['#5B6B7F', '#148F8A', '#1F3A5F', '#1F3A5F', '#E8833A']
    for i in range(5):
        top = 170 + i * 120; wt = 70 + i * 100; wb = wt + 100
        s.add(f'<path d="M{300-wt/2},{top} L{300+wt/2},{top} L{300+wb/2},{top+110} L{300-wb/2},{top+110} Z" fill="{cols[i]}" opacity="0.30"/>')
        s.add(f'<path d="M{300-wt/2},{top} L{300+wt/2},{top} L{300+wb/2},{top+110} L{300-wb/2},{top+110} Z" fill="url(#glsN)" stroke="#FFFFFF" stroke-width="2"/>')
        s.add(f'<rect x="{300-wt/2+6}" y="{top+4}" width="{wt-12}" height="5" rx="2" fill="#FFFFFF" opacity="0.9"/>')
    return s

@reg('16_1', '16:4', 'two upright document stacks of different heights side by side, front view, a magnifying glass centered between them')
def s16():
    s = S(1600, 400); s.floor(370)
    for i in range(6):
        s.rr(470 - i * 2, 330 - i * 32, 240 + i * 4, 28, 4, '#FFFFFF' if i % 2 else '#F2F4F7', '#C2CBD5', 1.2)
    s.rr(466, 330 - 6 * 32, 248, 28, 4, 'url(#nav)')
    for i in range(3):
        s.rr(890 - i * 2, 330 - i * 32, 240 + i * 4, 28, 4, '#FFFFFF' if i % 2 else '#F2F4F7', '#C2CBD5', 1.2)
    s.rr(886, 330 - 3 * 32, 248, 28, 4, 'url(#tea)')
    s.magnifier(800, 170, 60)
    return s

@reg('17_1', '16:10', 'two puzzle pieces side by side, front view, one navy and one teal, a narrow orange gap between them')
def s17():
    s = S(800, 500); s.floor(430)
    s.shadow(400, 430, 520)
    s.add('<path d="M150,140 h200 v80 a35,35 0 0 1 0,70 v80 h-200 Z" fill="url(#nav)"/>')
    s.add('<path d="M650,140 h-250 v80 a35,35 0 0 1 0,70 v80 h250 Z" fill="url(#tea)" transform="translate(30,0)"/>')
    s.add('<rect x="383" y="140" width="10" height="230" fill="#E8833A" opacity="0.6" filter="url(#sh2)"/>')
    return s

@reg('19_1', '2:3', 'front view of a urine specimen cup with a stylized protein molecule above it and a vertical measuring scale beside it')
def s19():
    s = S(600, 900); s.floor(780)
    s.shadow(260, 780, 300)
    s.add('<path d="M140,480 L380,480 L360,780 L160,780 Z" fill="url(#gls)" stroke="#AFC0CC" stroke-width="2"/>')
    s.add('<path d="M152,600 L368,600 L360,770 L160,770 Z" fill="#F2D27A" opacity="0.85"/>')
    s.rr(125, 440, 270, 48, 12, 'url(#tea)')
    import random; random.seed(3)
    pts = [(260 + 80 * math.cos(k * 0.9) + random.randint(-15, 15), 250 + 70 * math.sin(k * 1.3) + random.randint(-12, 12)) for k in range(9)]
    for a, b in zip(pts, pts[1:]):
        s.add(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#9FB1C2" stroke-width="6"/>')
    for i, (x, y) in enumerate(pts):
        s.add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{18 if i%3 else 24}" fill="url(#{"ora" if i==4 else ("nav" if i%2 else "tea")})"/>')
    s.shadow(490, 780, 70)
    s.rr(465, 260, 50, 520, 10, 'url(#gls)', '#AFC0CC', 1.5)
    for k in range(13):
        s.add(f'<line x1="{465}" y1="{290+k*38}" x2="{465+(26 if k%2==0 else 16)}" y2="{290+k*38}" stroke="{NAVY}" stroke-width="3"/>')
    return s

@reg('20_1', '2:3', 'front view of a vertical glass ruler with three glowing markers near its base and a soft fog layer at the bottom')
def s20():
    s = S(600, 900); s.floor(800)
    s.shadow(300, 800, 160)
    s.rr(240, 100, 120, 700, 18, 'url(#gls)', '#AFC0CC', 2)
    for k in range(28):
        s.add(f'<line x1="240" y1="{130+k*24}" x2="{240+(44 if k%5==0 else 24)}" y2="{130+k*24}" stroke="{NAVY}" stroke-width="3"/>')
    for y, c in [(745, '#7FF0E8'), (680, '#7FF0E8'), (640, '#F3A266')]:
        s.glow_dot(330, y, 9, c)
    s.add('<ellipse cx="300" cy="790" rx="300" ry="70" fill="#FFFFFF" opacity="0.85" filter="url(#glow2)"/>')
    return s

@reg('chain', '16:10', 'front view of a vertical chain of linked rings descending from a reference crystal at top to a sample tube at bottom, centered')
def s21():
    s = S(800, 500); s.floor(470)
    s.add('<polygon points="400,20 440,60 400,110 360,60" fill="url(#tea)"/><polygon points="400,20 440,60 400,60" fill="#FFFFFF" opacity="0.35"/>')
    s.add('<polygon points="400,20 440,60 400,110 360,60" fill="#7FF0E8" opacity="0.4" filter="url(#glow)"/>')
    for i in range(5):
        y = 125 + i * 48
        if i % 2 == 0:
            s.add(f'<ellipse cx="400" cy="{y}" rx="20" ry="30" fill="none" stroke="url(#nav)" stroke-width="9"/>')
        else:
            s.add(f'<ellipse cx="400" cy="{y}" rx="8" ry="30" fill="none" stroke="#8FA6C0" stroke-width="9"/>')
    s.tube(385, 365, 30, 105, 'tea', '#E9C46A', 0.6)
    return s

@reg('24_1', '2:3', 'front view of a laboratory scientist and a physician standing side by side before a large screen of abstract curves, stylized figures, symmetrical')
def s24():
    s = S(600, 900); s.floor(800)
    s.shadow(300, 520, 460, 0.18)
    s.rr(60, 160, 480, 330, 16, 'url(#scr)')
    s.bell(110, 230, 380, 210, 0.8, '#4FC9C1', 0.25)
    s.bell(110, 270, 380, 170, 1.3, '#F3A266', 0.15)
    s.person(200, 820, 300, '#FFFFFF', 'tea'); s.person(400, 820, 300, '#FFFFFF', 'nav')
    return s

@reg('25_1', '1:1', 'front view of an upright procedure manual with colored tabs beside a checklist clipboard')
def s25():
    s = S(800, 800); s.floor(660)
    s.book(140, 180, 240, 480, 'nav')
    for i, c in enumerate(['tea', 'ora', 'tea', 'nav']):
        s.rr(380, 230 + i * 80, 30, 56, 6, f'url(#{c})')
    s.shadow(570, 660, 260)
    s.rr(450, 220, 240, 440, 16, 'url(#cer)', '#B8C3CF', 1.5)
    s.rr(520, 200, 100, 40, 10, 'url(#nav)')
    for i in range(6):
        y = 290 + i * 58
        s.rr(480, y, 26, 26, 5, 'url(#tea)')
        s.add(f'<path d="M486,{y+13} l6,7 l10,-12" stroke="#fff" stroke-width="4" fill="none"/>')
        s.rr(520, y + 8, 140 if i % 2 else 110, 10, 5, '#C5CDD6')
    return s

@reg('27_1', '16:10', 'symmetrical split composition, front view: left, one reference analyzer on a raised pedestal with three analyzers in a row facing the viewer; right, five analyzers in a straight row with a glowing horizontal line at mean height')
def s27():
    s = S(800, 500); s.floor(430)
    s.rr(60, 300, 180, 130, 10, 'url(#cerS)', '#B8C3CF', 1.2)
    s.analyzer(90, 170, 120, 130, 'ora')
    for x in [45, 140, 235]:
        pass
    for i, x in enumerate([40, 150, 260]):
        pass
    s.add('<line x1="400" y1="40" x2="400" y2="470" stroke="#C9D1DA" stroke-width="2"/>')
    for i in range(3):
        s.analyzer(255 + 0 * i, 0, 0, 0) if False else None
    for i, x in enumerate([258, 0, 0][:1]):
        s.analyzer(262, 340, 80, 90, 'nav')
    s.analyzer(30 + 0, 340, 0.1, 0.1) if False else None
    for i in range(5):
        h = [95, 110, 100, 120, 98][i]
        s.analyzer(420 + i * 74, 430 - h, 64, h, 'tea' if i % 2 else 'nav')
    s.glow_line(412, 340, 790, 340, 3)
    return s

@reg('28_1', '2:3', 'front view of a rack of five sample tubes, four glowing green and one glowing red')
def s28():
    s = S(600, 900); s.floor(700)
    s.rack(70, 640, 460, 60)
    for i in range(5):
        g = '#4CC07C' if i != 3 else '#E05A4B'
        s.tube(98 + i * 86, 330, 54, 330, 'nav', '#A93226', 0.6, glow=g)
    return s

@reg('29_1', '2:3', 'front view of five glass columns of slightly different heights, the tallest and shortest lit orange, a thin horizontal plane at mean height')
def s29():
    s = S(600, 900); s.floor(760)
    hs = [430, 470, 380, 520, 450]
    for i, h in enumerate(hs):
        col = 'ora' if h in (max(hs), min(hs)) else 'gls'
        s.column(70 + i * 96, 760, 74, h, col)
    m = sum(hs) / 5
    s.add(f'<rect x="40" y="{760-m-4}" width="520" height="8" rx="4" fill="#7FF0E8" opacity="0.5" filter="url(#sh2)"/>')
    s.add(f'<rect x="40" y="{760-m-2}" width="520" height="4" rx="2" fill="#148F8A"/>')
    return s

@reg('30_1', '1:1', 'two square glass panels side by side, front view, left with tightly clustered points, right with loosely scattered points')
def s30():
    s = S(800, 800); s.floor(600)
    import random; random.seed(7)
    for k, (x0, spread, col) in enumerate([(70, 22, '#148F8A'), (430, 85, '#E8833A')]):
        s.panel(x0, 240, 300, 300)
        for _ in range(26):
            px = x0 + 150 + random.gauss(0, spread); py = 390 + random.gauss(0, spread)
            px = min(max(px, x0 + 20), x0 + 280); py = min(max(py, 260), 520)
            s.add(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="{col}" opacity="0.85"/>')
    return s

@reg('31_1', '16:4', 'front view of a straight path splitting symmetrically into two branches: left branch ends at a calibration dial, right branch ends at a consultation room door')
def s31():
    s = S(1600, 400); s.floor(330)
    s.add('<path d="M760,400 L840,400 L840,330 L1160,330 L1160,300 L1100,300 L800,300 L500,300 L440,300 L440,330 L760,330 Z" fill="url(#gls)" stroke="#AFC2D0" stroke-width="1.5"/>')
    s.glow_line(800, 395, 800, 315, 3); s.glow_line(470, 315, 1130, 315, 3)
    cx, cy = 440, 170
    s.shadow(cx, 300, 200)
    s.add(f'<circle cx="{cx}" cy="{cy}" r="105" fill="url(#cer)" stroke="url(#nav)" stroke-width="12"/>')
    for k in range(11):
        a = math.pi * (0.8 + k * 0.14)
        s.add(f'<line x1="{cx+70*math.cos(a):.0f}" y1="{cy+70*math.sin(a):.0f}" x2="{cx+86*math.cos(a):.0f}" y2="{cy+86*math.sin(a):.0f}" stroke="#5B6B7F" stroke-width="4"/>')
    s.add(f'<line x1="{cx}" y1="{cy}" x2="{cx+55}" y2="{cy-45}" stroke="{GREEN}" stroke-width="8" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="12" fill="url(#nav)"/>')
    s.shadow(1160, 300, 220)
    s.rr(1060, 40, 200, 262, 8, 'url(#cer)', '#B8C3CF', 1.5)
    s.rr(1085, 62, 150, 240, 6, 'url(#ora)')
    s.rr(1095, 74, 130, 110, 4, '#FFFFFF', op=0.18)
    s.add('<circle cx="1210" cy="190" r="9" fill="#FFFFFF"/>')
    return s

@reg('32_1', '2:3', 'front view of two bell curves of different spread on an upright glass panel, a magnifier centered above')
def s32():
    s = S(600, 900); s.floor(780)
    s.panel(60, 330, 480, 440)
    s.bell(90, 420, 420, 300, 0.7, '#148F8A', 0.25)
    s.bell(90, 560, 420, 160, 1.5, '#E8833A', 0.2)
    s.magnifier(300, 160, 75)
    return s

@reg('33_1', '2:3', 'front view of a precision balance with two level pans, one holding a teal-capped tube and one a navy-capped tube, symmetrical')
def s33():
    s = S(600, 900); s.floor(760)
    s.shadow(300, 760, 360)
    s.rr(200, 735, 200, 28, 10, 'url(#nav)')
    s.rr(288, 300, 24, 440, 10, 'url(#cerS)', '#B8C3CF', 1)
    s.rr(80, 300, 440, 18, 9, 'url(#nav)')
    s.add('<circle cx="300" cy="300" r="22" fill="url(#ora)"/>')
    for cx, cap in [(130, 'tea'), (470, 'nav')]:
        s.add(f'<line x1="{cx}" y1="318" x2="{cx-60}" y2="520" stroke="#8C99A8" stroke-width="3"/><line x1="{cx}" y1="318" x2="{cx+60}" y2="520" stroke="#8C99A8" stroke-width="3"/>')
        s.tube(cx - 18, 400, 36, 120, cap, '#A93226', 0.6)
        s.add(f'<path d="M{cx-80},520 h160 a80,28 0 0 1 -160,0z" fill="url(#cerS)" stroke="#B8C3CF" stroke-width="1.5"/>')
    return s

@reg('34_1', '1:1', 'front view of two identical clinical chemistry analyzers side by side, one with navy accent and one with teal accent')
def s34():
    s = S(800, 800); s.floor(600)
    s.analyzer(60, 300, 320, 300, 'nav'); s.analyzer(420, 300, 320, 300, 'tea')
    return s

@reg('35_1', '1:1', 'front view of a horizontal center line with a glowing symmetrical band above and below it')
def s35():
    s = S(800, 800)
    s.panel(80, 180, 640, 440)
    s.add('<rect x="110" y="330" width="580" height="140" fill="#7FF0E8" opacity="0.30" filter="url(#glow)"/>')
    s.rr(110, 330, 580, 140, 10, '#148F8A', op=0.18)
    s.add('<line x1="110" y1="330" x2="690" y2="330" stroke="#148F8A" stroke-width="3" stroke-dasharray="12 8"/><line x1="110" y1="470" x2="690" y2="470" stroke="#148F8A" stroke-width="3" stroke-dasharray="12 8"/>')
    s.glow_line(110, 400, 690, 400, 4, '#F3A266')
    return s

@reg('36_1', '1:1', 'front view of three identical cuvettes in a row, each receiving one drop')
def s36():
    s = S(800, 800); s.floor(640)
    for i in range(3):
        x = 150 + i * 190
        s.shadow(x + 60, 640, 150, 0.22)
        s.rr(x, 360, 120, 280, 8, 'url(#gls)', '#AFC0CC', 1.5)
        s.rr(x + 8, 500, 104, 132, 6, '#E9C46A', op=0.85)
        s.add(f'<path d="M{x+60},230 q-22,36 0,52 q22,-16 0,-52z" fill="url(#tea)"/>')
        s.rr(x + 14, 370, 14, 250, 6, '#FFFFFF', op=0.6)
    return s

@reg('37_1', '1:1', 'front view of two target dots almost perfectly overlapping at the center of a target')
def s37():
    s = S(800, 800); s.floor(700)
    s.target(400, 380, 280)
    s.add('<circle cx="392" cy="384" r="26" fill="#1F3A5F" opacity="0.9"/><circle cx="408" cy="376" r="26" fill="#E8833A" opacity="0.85"/>')
    s.add('<circle cx="400" cy="380" r="60" fill="#7FF0E8" opacity="0.25" filter="url(#glow)"/>')
    return s

@reg('38_1', '16:10', 'front elevation of a hospital laboratory complex: central lab in the middle, emergency lab and outpatient lab on either side, symmetrical')
def s38():
    s = S(800, 500); s.floor(440)
    s.building(60, 240, 190, 200, 'tea', 3, 4); s.building(550, 240, 190, 200, 'tea', 3, 4)
    s.building(275, 120, 250, 320, 'nav', 5, 5)
    return s

@reg('39_1', '16:4', 'two upright documents side by side, front view: left a full checklist, right a checklist with some empty boxes softly glowing orange')
def s39():
    s = S(1600, 400); s.floor(370)
    s.doc(470, 30, 250, 330, 'solid', 8, 'nav', boxes=[True] * 8)
    s.doc(880, 30, 250, 330, 'solid', 8, 'tea', boxes=[True, False, True, False, False, True, False, True])
    return s

@reg('21_1', '2:3', 'front view of a single sample tube on a stand under a magnifier, faint glow at the bottom of the liquid')
def s21b():
    s = S(600, 900); s.floor(780)
    s.shadow(300, 780, 260)
    s.rr(200, 740, 200, 40, 10, 'url(#nav)')
    s.tube(260, 380, 80, 360, 'tea', '#F2D27A', 0.5, glow=None)
    s.add('<ellipse cx="300" cy="715" rx="38" ry="14" fill="#7FF0E8" opacity="0.7" filter="url(#glow)"/>')
    s.magnifier(300, 200, 95)
    return s


@reg('407_hero', '16:9', 'front view of three identical analyzers standing in a straight row, a single glowing teal horizontal line passing through all three at the same height, navy background, symmetrical')
def s407h():
    s = S(1600, 900, 'navy'); s.floor(720)
    s.add('<ellipse cx="1180" cy="460" rx="420" ry="260" fill="#2E5482" opacity="0.35" filter="url(#glow2)"/>')
    s.glow_line(820, 520, 1560, 520, 4)
    for x in (850, 1085, 1320):
        s.analyzer(x, 380, 215, 340, 'nav' if x != 1085 else 'tea')
    for x in (1065, 1300):
        s.glow_dot(x + 2, 520, 8)
    return s

@reg('407_scope', '16:10', 'front elevation of one hospital laboratory building with a row of identical analyzers on a bench in front of it, symmetrical')
def s407a():
    s = S(800, 500); s.floor(440)
    s.building(250, 70, 300, 250, 'nav', 4, 5)
    s.shadow(400, 440, 600)
    s.rr(110, 330, 580, 18, 6, 'url(#cerS)', '#B8C3CF', 1.2)
    for i, x in enumerate((130, 270, 410, 550)):
        s.analyzer(x, 350, 120, 90, 'tea' if i % 2 else 'nav', tray=False)
    return s

@reg('407_sample', '16:10', 'front view of a rack of patient serum tubes at two concentration levels, light and darker serum, with one proficiency-testing vial set slightly apart, symmetrical')
def s407b():
    s = S(800, 500); s.floor(440)
    s.rack(130, 390, 540, 50)
    for i in range(6):
        s.tube(165 + i * 85, 170, 46, 230, 'nav' if i < 3 else 'tea', '#F6E7B5' if i < 3 else '#D9A441', 0.6)
    return s

@reg('407_rbc', '16:10', 'front view of four hematology analyzers in a straight row, the second one softly dimmed with a thin orange outline, symmetrical')
def s407c():
    s = S(800, 500); s.floor(430)
    for i, x in enumerate((40, 230, 420, 610)):
        if i == 1:
            s.add(f'<rect x="{x-8}" y="{222}" width="166" height="216" rx="12" fill="none" stroke="#E8833A" stroke-width="4"/>')
            s.add('<g opacity="0.45">'); s.analyzer(x, 230, 150, 200, 'nav'); s.add('</g>')
        else:
            s.analyzer(x, 230, 150, 200, 'tea' if i == 0 else 'nav')
    return s


@reg('407_hero_w', '16:9', 'front view of three identical analyzers standing in a straight row, a single teal horizontal line passing through all three at the same height, clean white background, symmetrical')
def s407hw():
    s = S(1600, 900); s.floor(720)
    s.add('<line x1="820" y1="520" x2="1560" y2="520" stroke="#148F8A" stroke-width="16" opacity="0.18" filter="url(#glow)"/>')
    s.add('<line x1="820" y1="520" x2="1560" y2="520" stroke="#148F8A" stroke-width="4"/>')
    for x in (850, 1085, 1320):
        s.analyzer(x, 380, 215, 340, 'nav' if x != 1085 else 'tea')
    for x in (1065, 1300):
        s.add(f'<circle cx="{x+2}" cy="520" r="9" fill="#148F8A"/><circle cx="{x+2}" cy="520" r="4" fill="#FFFFFF"/>')
    return s

@reg('18_1w', '16:9', 'front view of concentric precision measurement rings and a straight scale, perfectly centered, clean white background, navy and teal lines')
def s18w():
    s = S(1600, 900)
    cx, cy = 1150, 450
    for i, r in enumerate([330, 260, 190, 120]):
        s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#B9C7DA" stroke-width="{10-i*2}"/>')
    for k in range(36):
        a = k * math.pi / 18
        s.add(f'<line x1="{cx+316*math.cos(a):.1f}" y1="{cy+316*math.sin(a):.1f}" x2="{cx+344*math.cos(a):.1f}" y2="{cy+344*math.sin(a):.1f}" stroke="#5B7FA8" stroke-width="3"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="190" fill="none" stroke="#148F8A" stroke-width="4"/>')
    s.add(f'<line x1="{cx-380}" y1="{cy}" x2="{cx+380}" y2="{cy}" stroke="#1F3A5F" stroke-width="4"/>')
    for k in range(-8, 9):
        h = 26 if k % 4 == 0 else 14
        s.add(f'<line x1="{cx+k*45}" y1="{cy-h}" x2="{cx+k*45}" y2="{cy+h}" stroke="#1F3A5F" stroke-width="3"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="12" fill="#E8833A"/><circle cx="{cx}" cy="{cy}" r="5" fill="#FFFFFF"/>')
    return s

@reg('40_1r', '16:9', 'three identical pillars of light standing in a row at the far right, front view, softly lit analyzers behind them, navy background, symmetrical and calm')
def s40r():
    s = S(1600, 900, 'navy'); s.floor(700)
    for x in (1365, 1475):
        s.add('<g opacity="0.35">'); s.analyzer(x - 55, 560, 110, 140, 'nav'); s.add('</g>')
    for x in (1370, 1460, 1550):
        s.add(f'<rect x="{x-30}" y="120" width="60" height="580" rx="30" fill="#7FF0E8" opacity="0.22" filter="url(#glow2)"/>')
        s.add(f'<rect x="{x-14}" y="140" width="28" height="560" rx="14" fill="url(#beamV)"/>')
        s.add(f'<rect x="{x-4}" y="150" width="8" height="550" rx="4" fill="#FFFFFF" opacity="0.8"/>')
    return s

# ---------- 角图版本：把 2:3 / 1:1 示例图嵌入 16:10 画布（背景与地面线无缝延展） ----------
import re as _re
def _cornerize(name):
    ratio, fn, tr, prompt, n, grid = REG[name]
    def make():
        inner = fn()
        fy = None
        for e in inner.el:
            m = _re.search(r'<rect x="0" y="([0-9.]+)" width="[0-9.]+" height="[0-9.]+" fill="#E1E6EC"', e)
            if m: fy = float(m.group(1)) / inner.h; break
        s = S(800, 500)
        if fy: s.floor(500 * fy)
        w = inner.w * 500 / inner.h
        body = inner.svg().replace('<svg xmlns="http://www.w3.org/2000/svg"', f'<svg x="{(800-w)/2}" y="0"', 1)
        body = _re.sub(r'width="%d" height="%d" viewBox' % (inner.w, inner.h), f'width="{w}" height="500" viewBox', body, 1)
        s.add(body)
        return s
    REG[name + 'c'] = ('16:10', make, False, prompt + ' (corner crop 16:10)', 1, None)

for _n in [k for k, v in list(REG.items()) if v[0] in ('2:3', '1:1')]:
    _cornerize(_n)

@reg('31_1c', '16:10', 'front view of a straight path splitting symmetrically into two branches (corner crop)')
def s31c():
    s = S(800, 500); s.floor(430)
    s.add('<path d="M370,500 L430,500 L430,430 L660,430 L660,400 L140,400 L140,430 L370,430 Z" fill="url(#gls)" stroke="#AFC2D0" stroke-width="1.5"/>')
    s.glow_line(400, 495, 400, 415, 3); s.glow_line(160, 415, 640, 415, 3)
    cx, cy = 170, 260
    s.shadow(cx, 400, 180)
    s.add(f'<circle cx="{cx}" cy="{cy}" r="95" fill="url(#cer)" stroke="url(#nav)" stroke-width="11"/>')
    for k in range(11):
        a = math.pi * (0.8 + k * 0.14)
        s.add(f'<line x1="{cx+62*math.cos(a):.0f}" y1="{cy+62*math.sin(a):.0f}" x2="{cx+78*math.cos(a):.0f}" y2="{cy+78*math.sin(a):.0f}" stroke="#5B6B7F" stroke-width="4"/>')
    s.add(f'<line x1="{cx}" y1="{cy}" x2="{cx+50}" y2="{cy-40}" stroke="{GREEN}" stroke-width="8" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="11" fill="url(#nav)"/>')
    s.shadow(640, 400, 200)
    s.rr(550, 130, 180, 272, 8, 'url(#cer)', '#B8C3CF', 1.5)
    s.rr(572, 150, 136, 252, 6, 'url(#ora)')
    s.add('<circle cx="690" cy="280" r="8" fill="#FFFFFF"/>')
    return s

# ---------- 渲染 ----------
def render(names=None, outdir=None, svgdir=None):
    outdir = outdir or os.path.join(HERE, '..', '插图')
    svgdir = svgdir or os.path.join(HERE, '..', '插图', 'SVG源文件')
    os.makedirs(outdir, exist_ok=True); os.makedirs(svgdir, exist_ok=True)
    jobs = []
    for name, (ratio, fn, tr, prompt, n, grid) in REG.items():
        if names and name not in names: continue
        s = fn()
        p = os.path.join(svgdir, name + '.svg'); s.save(p)
        jobs.append([p, os.path.join(outdir, name + '.png'), s.w, s.h, tr])
    jf = os.path.join(svgdir, '_jobs.json'); json.dump(jobs, open(jf, 'w'))
    subprocess.run(['node', os.path.join(HERE, 'render.js'), jf], check=True)
    # 图标组：按格等分裁切
    from PIL import Image
    for name, (ratio, fn, tr, prompt, n, grid) in REG.items():
        if (names and name not in names) or ratio != 'icons': continue
        im = Image.open(os.path.join(outdir, name + '.png'))
        cols, rows = grid or (n, 1)
        cw, ch = im.width // cols, im.height // rows
        for k in range(n):
            c, r = k % cols, k // cols
            im.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch)).save(os.path.join(outdir, f'{name}-{k+1}.png'))
    os.remove(jf)

if __name__ == '__main__':
    render(sys.argv[1:] or None)

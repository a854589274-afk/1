# -*- coding: utf-8 -*-
"""插图引擎：统一正视正交、居中对称、顶光柔和阴影、哑光陶瓷与磨砂玻璃材质。
全部为代码绘制的 SVG，经 Chromium 渲染为 PNG；画面不含任何文字、字母、数字、标志。"""
import math

NAVY, NAVY2, TEAL, TEAL2, ORANGE = '#1F3A5F', '#2E5482', '#148F8A', '#22AFA8', '#E8833A'
GREEN, RED = '#2E9E5B', '#C0392B'

DEFS = '''
<defs>
 <linearGradient id="bgW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E9EDF2"/></linearGradient>
 <radialGradient id="bgN" cx="0.5" cy="0.45" r="0.75"><stop offset="0" stop-color="#2A4A73"/><stop offset="0.6" stop-color="#1F3A5F"/><stop offset="1" stop-color="#132740"/></radialGradient>
 <linearGradient id="cer" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#F1F3F6"/><stop offset="1" stop-color="#D9DFE6"/></linearGradient>
 <linearGradient id="cerS" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E3E8EE"/><stop offset="0.5" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DCE2E9"/></linearGradient>
 <linearGradient id="nav" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#34598A"/><stop offset="1" stop-color="#1A3354"/></linearGradient>
 <linearGradient id="tea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2BB9B1"/><stop offset="1" stop-color="#11807B"/></linearGradient>
 <linearGradient id="ora" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3A266"/><stop offset="1" stop-color="#D9702A"/></linearGradient>
 <linearGradient id="grn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4CC07C"/><stop offset="1" stop-color="#25854C"/></linearGradient>
 <linearGradient id="red" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E05A4B"/><stop offset="1" stop-color="#A93226"/></linearGradient>
 <linearGradient id="gls" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/><stop offset="1" stop-color="#D6EEEC" stop-opacity="0.45"/></linearGradient>
 <linearGradient id="glsN" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.30"/><stop offset="1" stop-color="#9FD9D5" stop-opacity="0.12"/></linearGradient>
 <linearGradient id="scr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22405F"/><stop offset="1" stop-color="#0F2236"/></linearGradient>
 <linearGradient id="grey" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E4E7EB"/><stop offset="1" stop-color="#C3C9D1"/></linearGradient>
 <linearGradient id="beamV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FF0E8" stop-opacity="0"/><stop offset="0.5" stop-color="#7FF0E8" stop-opacity="0.9"/><stop offset="1" stop-color="#7FF0E8" stop-opacity="0"/></linearGradient>
 <linearGradient id="beamH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3FD3CB" stop-opacity="0.15"/><stop offset="0.5" stop-color="#7FF0E8" stop-opacity="1"/><stop offset="1" stop-color="#3FD3CB" stop-opacity="0.15"/></linearGradient>
 <filter id="sh" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
 <filter id="sh2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
 <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
 <filter id="glow2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
</defs>'''


class S:
    def __init__(self, w, h, bg='white', transparent=False):
        self.w, self.h, self.el = w, h, []
        if not transparent:
            if bg == 'navy':
                self.el.append(f'<rect width="{w}" height="{h}" fill="url(#bgN)"/>')
            else:
                self.el.append(f'<rect width="{w}" height="{h}" fill="url(#bgW)"/>')
        self.dark = bg == 'navy'

    def add(self, s):
        self.el.append(s); return self

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
                + DEFS + ''.join(self.el) + '</svg>')

    # ---- 通用 ----
    def shadow(self, cx, y, w, op=0.28, hh=None):
        hh = hh or max(8, w * 0.07)
        self.add(f'<ellipse cx="{cx}" cy="{y}" rx="{w/2}" ry="{hh}" fill="#0B1B2E" opacity="{op}" filter="url(#sh)"/>')

    def floor(self, y, op=0.6):
        if self.dark:
            self.add(f'<rect x="0" y="{y}" width="{self.w}" height="{self.h-y}" fill="#0F2035" opacity="{op}"/>')
            self.add(f'<rect x="0" y="{y}" width="{self.w}" height="2" fill="#3C6390" opacity="0.5"/>')
        else:
            self.add(f'<rect x="0" y="{y}" width="{self.w}" height="{self.h-y}" fill="#E1E6EC" opacity="{op}"/>')

    def rr(self, x, y, w, h, r, fill, stroke=None, sw=1.5, op=1, extra=''):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st} opacity="{op}" {extra}/>')

    def glow_line(self, x1, y1, x2, y2, w=6, col='#7FF0E8'):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w*4}" opacity="0.35" filter="url(#glow)" stroke-linecap="round"/>')
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFFFFF" stroke-width="{max(1,w/3)}" stroke-linecap="round" opacity="0.9"/>')

    def glow_dot(self, cx, cy, r, col='#7FF0E8'):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r*2.5}" fill="{col}" opacity="0.35" filter="url(#glow)"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/><circle cx="{cx}" cy="{cy}" r="{r*0.45}" fill="#FFFFFF"/>')

    # ---- 物件 ----
    def analyzer(self, x, y, w, h, accent='nav', tray=True):
        """临床化学分析仪（无品牌）：陶瓷机身、深色屏、样本盘、色带。"""
        self.shadow(x + w / 2, y + h, w * 1.05)
        self.rr(x, y + h * 0.18, w, h * 0.82, w * 0.04, 'url(#cer)', '#C9D1DA', 1.2)
        self.rr(x + w * 0.03, y, w * 0.94, h * 0.24, w * 0.035, 'url(#cerS)', '#C9D1DA', 1.2)
        self.rr(x + w * 0.10, y + h * 0.05, w * 0.80, h * 0.10, h * 0.02, 'url(#glsN)' if self.dark else 'url(#gls)', '#B8C6D2', 1)
        self.rr(x + w * 0.08, y + h * 0.30, w * 0.36, h * 0.22, w * 0.02, 'url(#scr)')
        for i in range(3):
            self.rr(x + w * 0.11, y + h * (0.34 + i * 0.055), w * (0.20 - i * 0.04), h * 0.02, 2, '#4FC9C1' if i == 0 else '#5D7EA6', op=0.85)
        self.rr(x + w * 0.52, y + h * 0.30, w * 0.40, h * 0.22, w * 0.02, '#E6EBF0', '#C9D1DA', 1)
        if tray:
            n = 6
            for i in range(n):
                tx = x + w * 0.55 + i * w * 0.36 / n
                self.rr(tx, y + h * 0.33, w * 0.035, h * 0.16, w * 0.012, '#FFFFFF', '#AAB6C3', 1)
                self.rr(tx, y + h * 0.33, w * 0.035, h * 0.035, w * 0.01, 'url(#tea)' if i % 2 == 0 else 'url(#nav)')
        self.rr(x, y + h * 0.60, w, h * 0.05, 0, f'url(#{accent})')
        for i in range(4):
            self.rr(x + w * (0.10 + i * 0.21), y + h * 0.72, w * 0.17, h * 0.20, w * 0.015, 'url(#cerS)', '#CFD6DE', 1)
        self.rr(x + w * 0.06, y + h - 4, w * 0.08, 8, 3, '#8C99A8'); self.rr(x + w * 0.86, y + h - 4, w * 0.08, 8, 3, '#8C99A8')

    def tube(self, x, y, w, h, cap='nav', liquid='#E9C46A', level=0.55, glow=None, glass=True):
        self.shadow(x + w / 2, y + h, w * 1.3, 0.22)
        if glow:
            self.add(f'<rect x="{x-w*0.4}" y="{y}" width="{w*1.8}" height="{h}" rx="{w}" fill="{glow}" opacity="0.45" filter="url(#glow)"/>')
        self.rr(x, y + h * 0.12, w, h * 0.88, w / 2, 'url(#gls)', '#AFC0CC', 1.2)
        lh = (h * 0.88 - w * 0.2) * level
        self.rr(x + w * 0.1, y + h - lh - w * 0.1, w * 0.8, lh, w * 0.4, liquid, op=0.9)
        self.rr(x + w * 0.18, y + h * 0.2, w * 0.12, h * 0.6, w * 0.06, '#FFFFFF', op=0.7)
        self.rr(x - w * 0.08, y, w * 1.16, h * 0.16, w * 0.12, f'url(#{cap})')

    def vial(self, x, y, w, h, cap='tea', liquid='#E9C46A', glow=None):
        self.shadow(x + w / 2, y + h, w * 1.3, 0.22)
        if glow:
            self.add(f'<rect x="{x-w*0.3}" y="{y}" width="{w*1.6}" height="{h}" rx="{w*0.4}" fill="{glow}" opacity="0.5" filter="url(#glow)"/>')
        self.rr(x, y + h * 0.28, w, h * 0.72, w * 0.18, 'url(#gls)', '#AFC0CC', 1.2)
        self.rr(x + w * 0.08, y + h * 0.55, w * 0.84, h * 0.41, w * 0.12, liquid, op=0.9)
        self.rr(x + w * 0.2, y + h * 0.16, w * 0.6, h * 0.14, 3, '#C9D1DA')
        self.rr(x + w * 0.1, y, w * 0.8, h * 0.18, w * 0.08, f'url(#{cap})')
        self.rr(x + w * 0.16, y + h * 0.34, w * 0.1, h * 0.5, 3, '#FFFFFF', op=0.7)

    def rack(self, x, y, w, h):
        self.shadow(x + w / 2, y + h, w * 1.02)
        self.rr(x, y, w, h, h * 0.15, 'url(#cer)', '#C2CBD5', 1.2)
        self.rr(x, y, w, h * 0.22, h * 0.1, 'url(#nav)')

    def building(self, x, y, w, h, accent='nav', floors=5, cols=6, door=True):
        self.shadow(x + w / 2, y + h, w * 1.08)
        self.rr(x, y, w, h, w * 0.02, 'url(#cer)', '#C2CBD5', 1.2)
        self.rr(x - w * 0.02, y - h * 0.04, w * 1.04, h * 0.06, 3, f'url(#{accent})')
        mw, mh = w * 0.08, h * 0.06
        gx = (w - 2 * mw) / cols; gy = (h * 0.72 - mh) / floors
        for f in range(floors):
            for c in range(cols):
                if door and f == floors - 1 and cols // 2 - 1 <= c <= cols // 2:
                    continue
                self.rr(x + mw + c * gx + gx * 0.15, y + mh + h * 0.04 + f * gy + gy * 0.15, gx * 0.7, gy * 0.62, 2,
                        'url(#glsN)' if self.dark else 'url(#scr)', op=0.88 if not self.dark else 1)
                if not self.dark:
                    self.rr(x + mw + c * gx + gx * 0.18, y + mh + h * 0.04 + f * gy + gy * 0.18, gx * 0.2, gy * 0.56, 1, '#6E8FB5', op=0.5)
        if door:
            dw = w * 0.22
            self.rr(x + w / 2 - dw / 2, y + h * 0.80, dw, h * 0.20, 3, 'url(#gls)', '#9FB1C2', 1)
            self.add(f'<line x1="{x+w/2}" y1="{y+h*0.80}" x2="{x+w/2}" y2="{y+h}" stroke="#9FB1C2" stroke-width="1.5"/>')
            self.rr(x + w / 2 - dw * 0.7, y + h * 0.76, dw * 1.4, h * 0.035, 2, f'url(#{accent})')

    def doc(self, x, y, w, h, style='solid', lines=9, accent='nav', glow_rows=None, check=False, boxes=None):
        """文件纸：抽象灰条代表文字（无任何字符）。style: solid / draft / faded / bright"""
        self.shadow(x + w / 2, y + h, w * 0.95, 0.22)
        if style == 'draft':
            self.rr(x, y, w, h, w * 0.03, '#FFFFFF', '#9FB1C2', 2, op=0.55, extra='stroke-dasharray="10 8"')
        elif style == 'faded':
            self.rr(x, y, w, h, w * 0.03, 'url(#grey)', '#B8C0CA', 1.2, op=0.8)
        else:
            self.rr(x, y, w, h, w * 0.03, '#FFFFFF', '#C9D1DA', 1.2)
        top = y + h * 0.10
        self.rr(x + w * 0.12, top, w * 0.45, h * 0.035, 3, f'url(#{accent})' if style != 'faded' else '#AEB6C0',
                op=0.5 if style == 'draft' else 1)
        for i in range(lines):
            yy = top + h * 0.09 + i * h * 0.075
            if yy > y + h * 0.9: break
            ww = w * (0.76 if i % 3 != 2 else 0.5)
            col = '#C5CDD6' if style != 'faded' else '#B4BBC4'
            if glow_rows and i in glow_rows:
                self.add(f'<rect x="{x+w*0.08}" y="{yy-h*0.02}" width="{w*0.84}" height="{h*0.06}" rx="6" fill="{ORANGE}" opacity="0.45" filter="url(#sh2)"/>')
                col = ORANGE
            if boxes is not None:
                bx = x + w * 0.12
                filled = boxes[i] if i < len(boxes) else True
                if filled:
                    self.rr(bx, yy - h * 0.012, h * 0.04, h * 0.04, 3, 'url(#tea)')
                else:
                    self.add(f'<rect x="{bx-h*0.015}" y="{yy-h*0.027}" width="{h*0.07}" height="{h*0.07}" rx="5" fill="{ORANGE}" opacity="0.55" filter="url(#sh2)"/>')
                    self.rr(bx, yy - h * 0.012, h * 0.04, h * 0.04, 3, '#FFFFFF', ORANGE, 2)
                self.rr(bx + h * 0.07, yy, ww - h * 0.07, h * 0.018, 3, col, op=0.5 if style == 'draft' else 1)
            else:
                self.rr(x + w * 0.12, yy, ww, h * 0.018, 3, col, op=0.5 if style == 'draft' else 1)
        if check:
            cx, cy, r = x + w * 0.72, y + h * 0.80, w * 0.13
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#grn)"/>')
            self.add(f'<path d="M{cx-r*0.45},{cy} L{cx-r*0.1},{cy+r*0.35} L{cx+r*0.5},{cy-r*0.35}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.22}" stroke-linecap="round" stroke-linejoin="round"/>')

    def book(self, x, y, w, h, color='nav', ribbons=None):
        self.shadow(x + w / 2, y + h, w * 1.1)
        if ribbons:
            n = len(ribbons)
            for i, L in enumerate(ribbons):
                rx = x + w * 0.18 + i * w * 0.64 / max(1, n - 1) - w * 0.025
                col = ['url(#tea)', 'url(#nav)', 'url(#ora)', 'url(#tea)', 'url(#nav)', 'url(#tea)'][i % 6]
                if i == 2: col = 'url(#ora)'
                self.add(f'<path d="M{rx},{y-2} h{w*0.05} v{h*0.05+L} l{-w*0.025},{-w*0.03} l{-w*0.025},{w*0.03} z" fill="{col}"/>')
        self.rr(x, y, w, h, w * 0.04, f'url(#{color})')
        self.rr(x + w * 0.06, y + h * 0.02, w * 0.03, h * 0.96, 2, '#FFFFFF', op=0.18)
        self.rr(x + w * 0.2, y + h * 0.18, w * 0.6, h * 0.22, w * 0.03, '#FFFFFF', op=0.12)
        self.rr(x + w * 0.2, y + h * 0.82, w * 0.6, h * 0.012, 2, '#FFFFFF', op=0.35)

    def person(self, cx, base, h, coat='#FFFFFF', accent='nav'):
        """风格化人物：正面站立，无五官。"""
        self.shadow(cx, base, h * 0.35, 0.25)
        hw = h * 0.13
        body_w = h * 0.30
        self.rr(cx - body_w * 0.32, base - h * 0.30, body_w * 0.26, h * 0.30, body_w * 0.1, '#3B4C63')
        self.rr(cx + body_w * 0.06, base - h * 0.30, body_w * 0.26, h * 0.30, body_w * 0.1, '#3B4C63')
        self.add(f'<path d="M{cx-body_w/2},{base-h*0.25} Q{cx-body_w/2},{base-h*0.72} {cx},{base-h*0.74} Q{cx+body_w/2},{base-h*0.72} {cx+body_w/2},{base-h*0.25} Z" fill="{coat}" stroke="#C9D1DA" stroke-width="1.2"/>')
        self.add(f'<path d="M{cx-body_w*0.12},{base-h*0.73} L{cx},{base-h*0.58} L{cx+body_w*0.12},{base-h*0.73}" fill="url(#{accent})"/>')
        self.rr(cx - h * 0.035, base - h * 0.80, h * 0.07, h * 0.08, 4, '#E8CDB5')
        self.add(f'<circle cx="{cx}" cy="{base-h*0.87}" r="{hw*0.62}" fill="#EED6C2"/>')
        self.add(f'<path d="M{cx-hw*0.64},{base-h*0.87} A{hw*0.64},{hw*0.64} 0 0 1 {cx+hw*0.64},{base-h*0.87} Q{cx},{base-h*0.95} {cx-hw*0.64},{base-h*0.87} Z" fill="#2B3A4E"/>')

    def panel(self, x, y, w, h, dark_ok=True):
        self.shadow(x + w / 2, y + h, w)
        self.rr(x, y, w, h, 14, 'url(#gls)' if not self.dark else 'url(#glsN)', '#AFC2D0', 1.5)

    def bell(self, x, y, w, h, sd, col=TEAL, fill_op=0.25):
        pts = []
        for i in range(101):
            t = -3 + 6 * i / 100
            v = math.exp(-t * t / (2 * sd * sd))
            pts.append((x + w * i / 100, y + h - v * h))
        d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
        self.add(f'<path d="{d} L{x+w},{y+h} L{x},{y+h} Z" fill="{col}" opacity="{fill_op}"/>')
        self.add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4"/>')

    def magnifier(self, cx, cy, r):
        self.shadow(cx, cy + r * 2.4, r * 1.4, 0.2)
        self.rr(cx - r * 0.13, cy + r * 0.95, r * 0.26, r * 1.25, r * 0.1, 'url(#nav)')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gls)" stroke="url(#cerS)" stroke-width="{r*0.18}"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r*1.09}" fill="none" stroke="#B8C3CF" stroke-width="1.5"/>')
        self.add(f'<path d="M{cx-r*0.55},{cy-r*0.2} A{r*0.6},{r*0.6} 0 0 1 {cx-r*0.1},{cy-r*0.62}" fill="none" stroke="#FFFFFF" stroke-width="{r*0.1}" stroke-linecap="round" opacity="0.9"/>')

    def target(self, cx, cy, r):
        self.shadow(cx, cy + r * 1.15, r * 1.6, 0.2)
        for i, c in enumerate(['url(#cer)', 'url(#nav)', 'url(#cer)', 'url(#tea)', 'url(#cer)']):
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{r*(1-i*0.19)}" fill="{c}" stroke="#C9D1DA" stroke-width="1"/>')

    def column(self, x, base, w, h, col='gls'):
        self.shadow(x + w / 2, base, w * 1.3, 0.2)
        self.rr(x, base - h, w, h, w * 0.12, f'url(#{col})', '#AFC2D0', 1.2)
        self.rr(x + w * 0.14, base - h + w * 0.15, w * 0.12, h - w * 0.3, w * 0.06, '#FFFFFF', op=0.6)

    def gear(self, cx, cy, r, col='nav', teeth=8):
        pts = []
        for i in range(teeth * 2):
            a = math.pi * i / teeth
            rr = r if i % 2 == 0 else r * 0.80
            for da in (-0.17, 0.17):
                pts.append((cx + rr * math.cos(a + da * (math.pi / teeth) * 2), cy + rr * math.sin(a + da * (math.pi / teeth) * 2)))
        d = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts) + 'Z'
        self.add(f'<path d="{d}" fill="url(#{col})"/><circle cx="{cx}" cy="{cy}" r="{r*0.35}" fill="#FFFFFF"/>')

    def save(self, path):
        open(path, 'w').write(self.svg())

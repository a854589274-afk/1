# -*- coding: utf-8 -*-
"""版式系统与文字工具：网格、文字测量、条文框、徽章、图框、替换引擎。
标注版与清洁版共用：几何尺寸一律按标注版（文字更多）测量，两版版面完全一致。"""
import copy, re, unicodedata
from pptx import Presentation
from pptx.util import Emu, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import ImageFont

EMU = 914400
SW, SH = 13.333, 7.5
ML, MR, MT, MB = 0.6, 0.6, 0.45, 0.45
GUT = 0.25
COLW = (SW - ML - MR - 11 * GUT) / 12

def span(n):          # n 栏宽度
    return n * COLW + (n - 1) * GUT
def colx(i):          # 第 i 栏（0 起）左边
    return ML + i * (COLW + GUT)

# 固定区域
Y_CHAP, H_CHAP = 0.45, 0.26
Y_TITLE, H_TITLE = 0.74, 0.56
CT = 1.70                     # 内容区顶
Y_BADGE, H_BADGE = 6.40, 0.28  # 来源徽章（右下，页脚上方）
CB_R = Y_BADGE - GUT           # 右侧栏（与徽章同列）内容底
CB_L = 6.62                    # 左侧栏内容底（徽章不在其下方）
Y_FOOT, H_FOOT = 6.82, 0.23
CORNER_W, CORNER_H = 1.6, 1.0

C = dict(NAVY='1F3A5F', TEAL='148F8A', SLATE='5B6B7F', ORANGE='E8833A', RED='C0392B',
         GREEN='2E9E5B', BOX='F3F5F7', TEXT='222222', GRAY='6B7280', LGRAY='D5DAE0',
         WHITE='FFFFFF', DEL='9CA3AF')
SRC = {'GL': C['NAVY'], 'WS': C['TEAL'], 'REG': C['SLATE'], 'ORANGE': C['ORANGE'],
       'RED': C['RED'], 'GREEN': C['GREEN']}
RADIUS = 0.08
FONT_EA, FONT_LAT = '微软雅黑', 'Arial'
PITCH = 1.2        # 行距（倍字号，固定磅值）
PAD = 0.15          # 条文框内边距
QGUT = 0.30         # 条文框左侧大引号占位

# ---------------- 文字测量 ----------------
_lat = {}
def _latfont(sz, bold=False):
    k = (round(sz * 4), bold)
    if k not in _lat:
        f = '/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf' % ('Bold' if bold else 'Regular')
        _lat[k] = ImageFont.truetype(f, 400)
    return _lat[k]

def is_wide(ch):
    return unicodedata.east_asian_width(ch) in ('W', 'F', 'A') and ord(ch) > 0x2000 or ord(ch) >= 0x2E80

def char_w(ch, sz, bold=False):
    """返回字符宽度（磅）。中文/全角按 1em（微软雅黑），西文按 Arial（Liberation Sans 同度量）。"""
    if ch in '　':
        return sz
    if is_wide(ch):
        return sz * 1.0
    if ch == ' ':
        return sz * 0.5
    try:
        return _latfont(sz, bold).getlength(ch) / 400 * sz
    except Exception:
        return sz * 0.6

_NOSTART = set('，。、；：？！）》」』】〕”’,.;:!?)%]')
def wrap_lines(segs, width_pt, sz, safety=0.965):
    """segs: [(text, size, bold)] -> 行数。按中文逐字、西文按词断行，含避头标点。"""
    W = width_pt * safety
    toks = []
    for t, s, b in segs:
        for m in re.finditer(r'[A-Za-z0-9\.\-\+/%_=×μ~]+ ?|.', t, re.S):
            tok = m.group(0)
            toks.append((tok, sum(char_w(c, s, b) for c in tok)))
    lines, cur = 1, 0.0
    for i, (tok, w) in enumerate(toks):
        if tok == '\n':
            lines += 1; cur = 0; continue
        if cur + w > W and cur > 0:
            if tok[0] in _NOSTART:           # 避头：把前一个字带下来
                lines += 1; cur = w + sz
            else:
                lines += 1; cur = w
            while cur > W:                   # 超长西文串强制断
                lines += 1; cur -= W
        else:
            cur += w
    wrap_lines.last = cur
    return lines

def para_segs(para, sz):
    out = []
    for s in para:
        if s.get('kind') == 'del_hidden':
            continue
        size = s.get('size') or sz
        if s.get('base'):
            size = size * 0.7
        out.append((s['t'], size, bool(s.get('bold'))))
    return out

def para_height_pt(para, width_pt, sz, pitch=PITCH):
    segs = para_segs(para, sz)
    if not any(t.strip() for t, _, _ in segs):
        wrap_lines.last = 0
        return sz * pitch
    mx = max([s for _, s, _ in segs] + [sz])
    return wrap_lines(segs, width_pt, mx) * mx * pitch

def text_height_in(paras, width_in, sz, gap_pt=4, pitch=PITCH):
    """paras: list of paragraph(list of segs) or ('size', para) 元组；返回英寸。"""
    h = 0
    for i, p in enumerate(paras):
        psz, ind = sz, 0
        if isinstance(p, dict):
            psz = p.get('size', sz); ind = p.get('indent', 0); p = p['segs']
        h += para_height_pt(p, (width_in - ind) * 72, psz, pitch)
        if i:
            h += gap_pt
    return h / 72

# ---------------- 段落/替换引擎 ----------------
def seg(t, **kw):
    d = dict(t=t); d.update(kw); return d

def P(*items, **kw):
    """快速构造段落：字符串或 seg。"""
    out = []
    for it in items:
        out.append(seg(it, **kw) if isinstance(it, str) else it)
    return out

def ptext(para, mode='clean'):
    """段落在某版本中显示的文字。"""
    o = ''
    for s in para:
        k = s.get('kind', 'orig')
        if k == 'rep':
            o += (s['old'] + s['t']) if mode == 'annot' else s['t']
        elif k == 'tag':
            o += s['t'] if mode == 'annot' else ''
        else:
            o += s['t']
    return o

def orig_text(para):
    """段落的原文（替换前）文字。"""
    o = ''
    for s in para:
        k = s.get('kind', 'orig')
        if k == 'rep':
            o += s['old']
        elif k in ('tag',):
            pass
        elif k == 'add':
            pass
        else:
            o += s['t']
    return o

def _split_at(para, idx):
    """在原文字符位置 idx 处切分段落中的 orig 段。"""
    out, pos = [], 0
    for s in para:
        k = s.get('kind', 'orig')
        L = len(s['t']) if k == 'orig' else (len(s['old']) if k == 'rep' else 0)
        if k == 'orig' and pos < idx < pos + L:
            a, b = dict(s), dict(s)
            a['t'] = s['t'][:idx - pos]; b['t'] = s['t'][idx - pos:]
            out += [a, b]
        else:
            out.append(s)
        pos += L
    return out

REPLOG = []   # (slide_label, code, old, new, basis)

def replace(para, old, new, basis, code, label=''):
    """把原文 old 替换为 new；标注版显示 灰删除线old + 橙下划线new + 依据标签。"""
    ot = orig_text(para)
    i = ot.find(old)
    assert i >= 0, (code, old, ot)
    para = _split_at(_split_at(para, i), i + len(old))
    out, pos, done = [], 0, False
    for s in para:
        k = s.get('kind', 'orig')
        L = len(s['t']) if k == 'orig' else (len(s['old']) if k == 'rep' else 0)
        if k == 'orig' and i <= pos < i + len(old):
            if not done:
                fmt = {kk: vv for kk, vv in s.items() if kk in ('color', 'bold', 'size')}
                out.append(dict(kind='rep', old=old, t=new, **fmt))
                out.append(dict(kind='tag', t='依据：' + basis))
                done = True
        else:
            out.append(s)
        pos += L
    REPLOG.append((label, code, old, new, basis))
    return out

def insert(para, before, text, basis, code, label=''):
    """在原文 before 之前插入 text（old 为空的替换）。"""
    ot = orig_text(para)
    i = ot.find(before)
    assert i >= 0, (code, before, ot)
    para = _split_at(para, i)
    out, pos, done = [], 0, False
    for s in para:
        k = s.get('kind', 'orig')
        L = len(s['t']) if k == 'orig' else (len(s['old']) if k == 'rep' else 0)
        if not done and k == 'orig' and pos == i:
            fmt = {kk: vv for kk, vv in s.items() if kk in ('color', 'bold', 'size')}
            out.append(dict(kind='rep', old='', t=text, **fmt))
            out.append(dict(kind='tag', t='依据：' + basis))
            done = True
        out.append(s)
        pos += L
    assert done, code
    REPLOG.append((label, code, '', text, basis))
    return out

def cut(para, a=None, b=None):
    """按原文子串切段：返回从子串 a 起（含）到子串 b 前（不含）的段落片段。"""
    ot = orig_text(para)
    i = 0 if a is None else ot.find(a)
    j = len(ot) if b is None else ot.find(b, i + 1)
    assert i >= 0 and j >= 0, (a, b, ot[:40])
    p = _split_at(_split_at(para, i), j)
    out, pos = [], 0
    for s in p:
        k = s.get('kind', 'orig')
        L = len(s['t']) if k == 'orig' else (len(s['old']) if k == 'rep' else 0)
        if i <= pos < j or (L == 0 and i <= pos < j):
            out.append(s)
        pos += L
    return out

def mode_segs(para, mode):
    """把段落转成某版本的渲染 run 列表。"""
    out = []
    for s in para:
        k = s.get('kind', 'orig')
        base = {kk: vv for kk, vv in s.items() if kk not in ('kind', 't', 'old')}
        if k == 'rep':
            if mode == 'annot':
                if s['old']:   # 标注版：被替换原文 灰色删除线（按说明性文字 12pt 显示）
                    out.append(dict(base, t=s['old'], color=C['DEL'], strike=True, size=12))
                out.append(dict(base, t=s['t'], color=C['ORANGE'], ul=True))
            else:
                out.append(dict(base, t=s['t']))
        elif k == 'tag':
            if mode == 'annot':
                out.append(dict(t='［' + s['t'] + '］', color=C['ORANGE'], size=12, bold=False))
        else:
            out.append(dict(base, t=s['t']))
    return out

def meas_para(para):
    """测量用：按标注版（最长）展开。"""
    return [dict(t=x['t'], size=x.get('size'), bold=x.get('bold'), base=x.get('base'))
            for x in mode_segs(para, 'annot')]

# ---------------- 低层形状 ----------------
def _rgb(h):
    return RGBColor.from_string(h)

def set_run_font(r, size=None, color=None, bold=None, strike=False, ul=False, base=None, ea=FONT_EA, lat=FONT_LAT):
    rPr = r._r.get_or_add_rPr()
    if size: rPr.set('sz', str(int(round(size * 100))))
    if bold is not None: rPr.set('b', '1' if bold else '0')
    if strike: rPr.set('strike', 'sngStrike')
    if ul: rPr.set('u', 'sng')
    if base: rPr.set('baseline', str(base))
    for ch in list(rPr):
        if ch.tag in (qn('a:latin'), qn('a:ea'), qn('a:cs'), qn('a:solidFill')):
            rPr.remove(ch)
    if color:
        sf = etree.SubElement(rPr, qn('a:solidFill'))
        etree.SubElement(sf, qn('a:srgbClr')).set('val', color)
    if ul and color:
        uf = etree.SubElement(rPr, qn('a:uFill'))
        sf2 = etree.SubElement(uf, qn('a:solidFill'))
        etree.SubElement(sf2, qn('a:srgbClr')).set('val', color)
    etree.SubElement(rPr, qn('a:latin')).set('typeface', lat)
    etree.SubElement(rPr, qn('a:ea')).set('typeface', ea)
    etree.SubElement(rPr, qn('a:cs')).set('typeface', lat)

def _pitch(p, sz, pitch=PITCH, after=0, before=0, align='l'):
    pPr = p._p.get_or_add_pPr()
    pPr.set('algn', align)
    for t in ('a:lnSpc', 'a:spcBef', 'a:spcAft'):
        for e in pPr.findall(qn(t)): pPr.remove(e)
    ln = etree.SubElement(pPr, qn('a:lnSpc')); etree.SubElement(ln, qn('a:spcPts')).set('val', str(int(sz * pitch * 100)))
    sb = etree.SubElement(pPr, qn('a:spcBef')); etree.SubElement(sb, qn('a:spcPts')).set('val', str(int(before * 100)))
    sa = etree.SubElement(pPr, qn('a:spcAft')); etree.SubElement(sa, qn('a:spcPts')).set('val', str(int(after * 100)))
    # 顺序：lnSpc, spcBef, spcAft 必须在 buNone 之前
    bu = etree.SubElement(pPr, qn('a:buNone'))

def textbox(shapes, x, y, w, h, paras, sz, mode='clean', color=C['TEXT'], align='l', anchor='t',
            bold=False, gap=4, pitch=PITCH, ins=(0, 0, 0, 0), name=None, ea=FONT_EA, force=False):
    """paras: list of 段落（seg 列表）或 dict(segs=..., size=..., align=...)。"""
    tb = shapes.add_textbox(Emu(int(x * EMU)), Emu(int(y * EMU)), Emu(int(w * EMU)), Emu(int(h * EMU)))
    if name: tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    bp = tf._txBody.find(qn('a:bodyPr'))
    bp.set('lIns', str(int(ins[0] * EMU))); bp.set('tIns', str(int(ins[1] * EMU)))
    bp.set('rIns', str(int(ins[2] * EMU))); bp.set('bIns', str(int(ins[3] * EMU)))
    bp.set('anchor', {'t': 't', 'm': 'ctr', 'b': 'b'}[anchor])
    for e in list(bp): bp.remove(e)
    etree.SubElement(bp, qn('a:noAutofit'))
    first = True
    for pp in paras:
        psz, palign, ind, pfont = sz, align, 0, None
        if isinstance(pp, dict):
            psz = pp.get('size', sz); palign = pp.get('align', align); ind = pp.get('indent', 0); pfont = pp.get('font'); pp = pp['segs']
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        _pitch(p, psz, pitch, after=0, before=0 if first else gap, align=palign)
        if ind:
            p._p.get_or_add_pPr().set('marL', str(int(ind * EMU)))
        first = False
        for s in mode_segs(pp, mode):
            if not s['t']: continue
            r = p.add_run(); r.text = s['t']
            set_run_font(r, size=s.get('size') or psz, color=color if force else (s.get('color') or color),
                         bold=s.get('bold') if s.get('bold') is not None else bold,
                         strike=s.get('strike'), ul=s.get('ul'), base=s.get('base'), ea=pfont or ea,
                         **({'lat': pfont} if pfont else {}))
    return tb

def rrect(shapes, x, y, w, h, fill=None, line=None, lw=0.75, radius=RADIUS, name=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = shapes.add_shape(shape, Emu(int(x * EMU)), Emu(int(y * EMU)), Emu(int(w * EMU)), Emu(int(h * EMU)))
    if name: s.name = name
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = min(0.5, radius / min(w, h))
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = _rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = _rgb(line); s.line.width = Pt(lw)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    tf = s.text_frame
    return s

def group(shapes, name):
    g = shapes.add_group_shape()
    g.name = name
    return g

# ---------------- 组件 ----------------
def cite_w(cite):
    return sum(char_w(c, 12) for c in cite) * 1.06 / 72 + 0.2

def quote_box_h(paras, w, sz, cite=True, quote=True, gap=4, citetext=None):
    inner = w - 2 * PAD - (QGUT if quote else 0)
    mp = [dict(segs=meas_para(p['segs'] if isinstance(p, dict) else p),
               size=(p.get('size', sz) if isinstance(p, dict) else sz),
               indent=(p.get('indent', 0) if isinstance(p, dict) else 0)) for p in paras]
    th = text_height_in(mp, inner, sz, gap)
    inline = False
    if cite and citetext:
        free = inner * 0.965 - wrap_lines.last / 72          # 最后一行剩余宽度
        inline = free > cite_w(citetext) + 0.25
    quote_box_h.inline = inline
    clines = 1
    if cite and citetext and not inline:
        clines = max(1, -(-int(cite_w(citetext) * 100) // int((w - 2 * PAD) * 100)))
    quote_box_h.clines = clines
    return 2 * PAD + th + (0.24 * clines if cite and not inline else 0)

def quote_box(shapes, x, y, w, paras, sz, src='GL', cite=None, mode='clean', h=None, quote=True,
              gap=4, label=None, fill=C['BOX'], tags=None):
    """条文框：浅灰底，四边来源色 0.75pt，圆角 0.08"，左上大引号，右下引用行。"""
    need = quote_box_h(paras, w, sz, cite is not None, quote, gap, cite)
    inline = quote_box_h.inline
    clines = quote_box_h.clines
    h = max(h or 0, need)
    col = SRC.get(src, src)
    g = group(shapes, 'QBOX')
    rrect(g.shapes, x, y, w, h, fill=fill, line=col, lw=0.75)
    tx = x + PAD + (QGUT if quote else 0)
    if quote:
        textbox(g.shapes, x + PAD - 0.04, y + PAD - 0.10, QGUT, 0.42, [P('“')], 24, color=col, bold=True, pitch=1.0)
    th = h - 2 * PAD - (0.24 * clines if cite and not inline else 0)
    if tags:                                   # 框头右侧标签（同组内）
        tx2 = x + w - PAD
        for t, tcol in reversed(tags):
            tw = badge_w(t)
            tx2 -= tw
            badge(g.shapes, tx2, y + PAD, t, tcol, w=tw, h=0.28)
            tx2 -= 0.08
    textbox(g.shapes, tx, y + PAD, w - 2 * PAD - (QGUT if quote else 0), th + 0.01, paras, sz, mode=mode, gap=gap)
    if cite:
        cw = min(w - 2 * PAD, cite_w(cite) + 0.1)
        cy = y + h - PAD - (sz * PITCH / 72 + 0.22) / 2 - 0.01 if inline else y + h - PAD - 0.24 * clines + 0.02
        textbox(g.shapes, x + w - PAD - cw, cy, cw, 0.24 * clines - 0.02, [P(cite)], 12, color=col, align='r', pitch=1.2, name='CITE')
    return h

def badge(shapes, x, y, text, col, w=None, h=0.30, sz=12, fill=True, name='BADGE'):
    """统一徽章：圆角小块，来源色底白字（fill）或白底来源色字边框。"""
    if w is None:
        w = badge_w(text, sz)
    s = rrect(shapes, x, y, w, h, fill=col if fill else C['WHITE'], line=col, lw=0.75, radius=RADIUS, name=name)
    tf = s.text_frame
    bp = tf._txBody.find(qn('a:bodyPr'))
    for k in ('lIns', 'rIns'): bp.set(k, str(int(0.06 * EMU)))
    for k in ('tIns', 'bIns'): bp.set(k, '0')
    bp.set('anchor', 'ctr'); bp.set('wrap', 'none')
    p = tf.paragraphs[0]; _pitch(p, sz, 1.0, align='ctr')
    r = p.add_run(); r.text = text
    set_run_font(r, size=sz, color=C['WHITE'] if fill else col, bold=True)
    return w

def badge_w(text, sz=12):
    return sum(char_w(c, sz, True) for c in text) * 1.04 / 72 + 0.30

def picture(shapes, path_or_stream, x, y, w=None, h=None, rounded=True, crop=None, name='PIC'):
    pic = shapes.add_picture(path_or_stream, Emu(int(x * EMU)), Emu(int(y * EMU)),
                             Emu(int(w * EMU)) if w else None, Emu(int(h * EMU)) if h else None)
    pic.name = name
    if crop:
        pic.crop_left, pic.crop_top, pic.crop_right, pic.crop_bottom = crop
    if rounded:
        sp = pic._element.spPr
        pg = sp.find(qn('a:prstGeom'))
        pg.set('prst', 'roundRect')
        av = pg.find(qn('a:avLst'))
        if av is None: av = etree.SubElement(pg, qn('a:avLst'))
        for e in list(av): av.remove(e)
        ww, hh = pic.width / EMU, pic.height / EMU
        gd = etree.SubElement(av, qn('a:gd')); gd.set('name', 'adj'); gd.set('fmla', 'val %d' % int(min(50000, RADIUS / min(ww, hh) * 100000)))
    return pic

def framed_pic(shapes, img, x, y, w, h, line=C['LGRAY'], name='PICFRAME'):
    """原截图/原扫描图统一图框：等比缩放后居中放入 w×h 区域，圆角细边。"""
    from PIL import Image
    if isinstance(img, (bytes, bytearray)):
        import io; im = Image.open(io.BytesIO(img)); src = io.BytesIO(img)
    else:
        im = Image.open(img); src = img
    iw, ih = im.size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    px, py = x + (w - pw) / 2, y + (h - ph) / 2
    pic = picture(shapes, src, px, py, pw, ph, name=name)
    pic.line.color.rgb = _rgb(line); pic.line.width = Pt(0.75)
    return (px, py, pw, ph)

def caption(shapes, x, y, w, text, align='l', color=C['GRAY'], sz=12):
    textbox(shapes, x, y, w, 0.24, [P(text)], sz, color=color, align=align, pitch=1.2)
    return 0.24

def bignum(shapes, x, y, w, num, label, cite=None, h=None, col=C['ORANGE'], src='WS', nsz=34):
    """大数字卡：数字 32–40pt 橙色，下方标签 14pt。"""
    lab_h = text_height_in([P(label)], w - 2 * PAD, 14)
    hh = PAD + nsz * 1.15 / 72 + 0.05 + lab_h + (0.26 if cite else 0) + PAD
    h = max(h or 0, hh)
    g = group(shapes, 'BIGNUM')
    rrect(g.shapes, x, y, w, h, fill=C['WHITE'], line=C['LGRAY'])
    textbox(g.shapes, x + PAD, y + PAD, w - 2 * PAD, nsz * 1.15 / 72 + 0.02, [P(num)], nsz, color=col, bold=True, pitch=1.1)
    textbox(g.shapes, x + PAD, y + PAD + nsz * 1.15 / 72 + 0.05, w - 2 * PAD, lab_h + 0.01, [P(label)], 14, color=C['TEXT'])
    if cite:
        textbox(g.shapes, x + PAD, y + h - PAD - 0.22, w - 2 * PAD, 0.22, [P(cite)], 12, color=SRC.get(src, src), align='r', pitch=1.2)
    return h

# ---------------- 页面框架 ----------------
CHAPTERS = {1: '① 为什么要比', 2: '② 怎么比', 3: '③ 我科怎么做'}

def frame(slide, title_paras, chap, page, src_text=None, src_key='GL', corner=None, mode='clean',
          title_w=None, dark=False):
    sh = slide.shapes
    fg = C['WHITE'] if dark else C['NAVY']
    textbox(sh, ML, Y_CHAP, 4, H_CHAP, [P(CHAPTERS[chap])], 12, color=C['WHITE'] if dark else C['TEAL'], bold=True, pitch=1.2, name='CHAPTER')
    tw = title_w or (SW - ML - MR - (CORNER_W + GUT if corner else 0))
    textbox(sh, ML, Y_TITLE, tw, H_TITLE, title_paras, 28, mode=mode, color=fg, bold=True, pitch=1.15, name='TITLE')
    if corner:
        picture(sh, corner, SW - MR - CORNER_W, MT, CORNER_W, CORNER_H, name='NEWIMG_CORNER')
    footer(slide, page, dark)
    if src_text:
        w = badge_w(src_text)
        badge(sh, SW - MR - w, Y_BADGE, src_text, SRC.get(src_key, src_key), w=w, h=H_BADGE, fill=False, name='SRCBADGE')

def footer(slide, page, dark=False):
    sh = slide.shapes
    col = 'C9D3DF' if dark else C['GRAY']
    textbox(sh, ML, Y_FOOT, 4, H_FOOT, [P('第940医院检验科')], 12, color=col, pitch=1.1, name='FOOTER')
    textbox(sh, SW - MR - 1, Y_FOOT, 1, H_FOOT, [P(str(page))], 12, color=col, align='r', pitch=1.1, name='FOOTER')


def cut_i(para, i, j):
    """按原文字符下标切段 [i, j)。"""
    p = _split_at(_split_at(para, i), j)
    out, pos = [], 0
    for s in p:
        k = s.get('kind', 'orig')
        L = len(s['t']) if k == 'orig' else (len(s['old']) if k == 'rep' else 0)
        if i <= pos < j:
            out.append(s)
        pos += L
    return out


def split_head(para, head):
    ot = orig_text(para)
    assert ot.startswith(head), (head, ot[:20])
    return cut_i(para, 0, len(head)), cut_i(para, len(head), len(ot))


def excise(para, sub):
    """从段落中取出子串 sub（作为标签单独显示），返回 (剩余段落, 子串段落)。"""
    ot = orig_text(para)
    i = ot.find(sub)
    assert i >= 0, (sub, ot[:30])
    return cut_i(para, 0, i) + cut_i(para, i + len(sub), len(ot)), cut_i(para, i, i + len(sub))

# -*- coding: utf-8 -*-
"""页面级组件：条文框堆叠、示例图、卡片、中缝徽章、时间轴等。所有组件记录越界量用于自动定字号。"""
from lib import *
from core import img, clear_slide


class Ctx:
    def __init__(self, deck):
        self.deck = deck
        self.mode = deck.mode
        self.over = 0.0
        self.page = 0
        self.notes = {}

    def chk(self, bottom, limit):
        if bottom - limit > self.over:
            import inspect
            st = inspect.stack()
            self.over_src = ' < '.join(f'{f.function}:{f.lineno}' for f in st[1:4])
        self.over = max(self.over, bottom - limit)

    def L(self, **kw):
        d = self.notes.setdefault(self.page, dict(template='', added=[], pending=[], orig='', size='', images=[]))
        for k, v in kw.items():
            if isinstance(d.get(k), list):
                d[k] += v if isinstance(v, list) else [v]
            else:
                d[k] = v


def fit(ctx, sl, fn, sizes, variants=None):
    """依次尝试字号（原字号优先，逐级下调，不低于14pt）；给出 variants 时，同一字号下先试标准版式、再试宽版式。
    返回采用的字号（及版式变体存入 ctx.variant）。"""
    combos = [(sz, v) for sz in sizes for v in (variants or [None])]
    for idx, (sz, v) in enumerate(combos):
        clear_slide(sl)
        ctx.over = 0.0
        ctx.variant = v
        ctx.notes.setdefault(ctx.page, dict(template='', added=[], pending=[], orig='', size='', images=[]))['images'] = []
        mark = len(REPLOG)
        fn(sz, v) if variants else fn(sz)
        if ctx.over <= 0.005:
            return sz
        if idx < len(combos) - 1:
            del REPLOG[mark:]
    print(f'  !! 第{ctx.page}页 14pt 仍越界 {ctx.over:.2f} 英寸 @ {ctx.over_src}')
    ctx.L(pending='【版式】自动定字号到下限仍越界 %.2f 英寸' % ctx.over)
    return sz


def bold_head(para, head):
    """把段落开头的 head 设为加粗（框头）。"""
    from lib import _split_at, orig_text
    ot = orig_text(para)
    assert ot.startswith(head), (head, ot[:20])
    p = _split_at(para, len(head))
    out, pos = [], 0
    for s in p:
        k = s.get('kind', 'orig')
        L = len(s['t']) if k == 'orig' else (len(s['old']) if k == 'rep' else 0)
        if pos < len(head):
            s = dict(s, bold=True)
        out.append(s); pos += L
    return out


def _lim(x, w, limit):
    import lib
    return min(limit, CB_R) if x + w > lib.BADGE_X - 0.02 else limit


def qb(ctx, sl, x, y, w, paras, sz, src='GL', cite=None, h=None, limit=CB_L, quote=True, gap=4, fill=C['BOX'], tags=None, icon=None):
    limit = _lim(x, w, limit)
    hh = quote_box(sl.shapes, x, y, w, paras, sz, src=src, cite=cite, mode=ctx.mode, h=h, quote=quote, gap=gap, fill=fill, tags=tags, icon=icon)
    ctx.chk(y + hh, limit)
    return hh


def qbh(paras, w, sz, cite=True, quote=True, gap=4):
    return quote_box_h(paras, w, sz, cite, quote, gap)


def stack(ctx, sl, x, y, w, items, limit=CB_L, gap=GUT, equal=False):
    """items: [dict(paras, sz, src, cite)] 纵向堆叠，返回底边 y。"""
    for it in items:
        h = qb(ctx, sl, x, y, w, it['paras'], it['sz'], it.get('src', 'GL'), it.get('cite'), it.get('h'), limit)
        y += h + gap
    return y - gap


def ex_image(ctx, sl, name, x, y, w, h, cap=None, limit=CB_R, capw=None):
    """新生成示例图：圆角图框 + 下方 12pt 灰色说明。"""
    picture(sl.shapes, img(name), x, y, w, h, name='NEWIMG')
    ctx.L(images=name)
    yb = y + h
    if cap:
        caption(sl.shapes, x, yb + 0.06, capw or max(w, sum(char_w(c, 12) for c in cap) / 72 + 0.1), cap)
        yb += 0.30
    ctx.chk(yb, limit)
    return yb


def mid_badge(sl, cx, cy, sym, col, w=0.46, h=0.30):
    badge(sl.shapes, cx - w / 2, cy - h / 2, sym, col, w=w, h=h, sz=14)


def text(ctx, sl, x, y, w, paras, sz, color=C['TEXT'], bold=False, align='l', limit=CB_L, pitch=PITCH, gap=4, force=False):
    limit = _lim(x, w, limit)
    mp = [dict(segs=meas_para(p['segs'] if isinstance(p, dict) else p), size=(p.get('size', sz) if isinstance(p, dict) else sz)) for p in paras]
    h = text_height_in(mp, w, sz, gap, pitch) + 0.02
    textbox(sl.shapes, x, y, w, h, paras, sz, mode=ctx.mode, color=color, bold=bold, align=align, pitch=pitch, gap=gap, force=force)
    ctx.chk(y + h, limit)
    return h


def card(ctx, sl, x, y, w, h, icon, paras, sz, color=C['TEXT'], line=C['LGRAY'], icon_h=1.0, limit=CB_L, bold=False, fill=C['WHITE'], cite=None):
    """T7 卡片：顶部图标（来自同一张图标组图的等分裁切），下方原文。"""
    limit = _lim(x, w, limit)
    g = group(sl.shapes, 'CARD')
    if cite:
        textbox(g.shapes, x + w - PAD - cite_w(cite), y + h - 0.30, cite_w(cite), 0.22, [P(cite)], 12, color=line, align='r', pitch=1.2, name='CITE')
    rrect(g.shapes, x, y, w, h, fill=fill, line=line)
    if icon:
        picture(g.shapes, img(icon), x + (w - icon_h) / 2, y + PAD, icon_h, icon_h, rounded=False, name='NEWIMG_ICON')
        ctx.L(images=icon)
    ty = y + PAD + (icon_h + 0.08 if icon else 0)
    mp = [dict(segs=meas_para(p), size=sz) for p in paras]
    th = text_height_in(mp, w - 2 * PAD, sz) + 0.02
    textbox(g.shapes, x + PAD, ty, w - 2 * PAD, th, paras, sz, mode=ctx.mode, color=color, bold=bold)
    need = ty + th + PAD - y
    ctx.chk(y + max(h, need), limit)
    ctx.chk(y + need, y + h)
    return need


def card_h(paras, w, sz, icon_h=1.0, icon=True):
    mp = [dict(segs=meas_para(p), size=sz) for p in paras]
    return PAD + (icon_h + 0.08 if icon else 0) + text_height_in(mp, w - 2 * PAD, sz) + 0.02 + PAD


def flow_box(ctx, sl, x, y, w, h, paras, sz, col=C['NAVY'], fill=C['WHITE'], color=C['TEXT'], bold=False, align='l'):
    g = group(sl.shapes, 'FLOW')
    rrect(g.shapes, x, y, w, h, fill=fill, line=col, lw=1.0)
    mp = [dict(segs=meas_para(p), size=sz) for p in paras]
    th = text_height_in(mp, w - 2 * 0.1, sz) + 0.02
    textbox(g.shapes, x + 0.1, y + (h - th) / 2, w - 0.2, th, paras, sz, mode=ctx.mode, color=color, bold=bold, align=align)
    ctx.chk(th + 0.1, h)
    return h


def arrow(sl, x1, y1, x2, y2, col=C['GRAY'], w=1.5):
    from pptx.enum.shapes import MSO_CONNECTOR
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(int(x1 * EMU)), Emu(int(y1 * EMU)), Emu(int(x2 * EMU)), Emu(int(y2 * EMU)))
    c.line.color.rgb = RGBColor.from_string(col); c.line.width = Pt(w)
    ln = c.line._get_or_add_ln()
    te = etree.SubElement(ln, qn('a:tailEnd')); te.set('type', 'triangle'); te.set('w', 'med'); te.set('len', 'med')
    c.name = 'ARROW'
    return c


def line(sl, x1, y1, x2, y2, col=C['LGRAY'], w=1.5, dash=False):
    from pptx.enum.shapes import MSO_CONNECTOR
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(int(x1 * EMU)), Emu(int(y1 * EMU)), Emu(int(x2 * EMU)), Emu(int(y2 * EMU)))
    c.line.color.rgb = RGBColor.from_string(col); c.line.width = Pt(w)
    if dash:
        from pptx.enum.dml import MSO_LINE
        c.line.dash_style = MSO_LINE.DASH
    c.name = 'LINE'
    return c


def dot(sl, cx, cy, r, col):
    s = rrect(sl.shapes, cx - r, cy - r, 2 * r, 2 * r, fill=col, shape=MSO_SHAPE.OVAL, name='DOT')
    return s


def head_badges(ctx, sl, x, y, items, gap=0.12, limit=CB_L):
    """一行徽章：items=[(text,color,fill)]，返回宽度。"""
    xx = x
    for t, col, fill in items:
        w = badge_w(t)
        badge(sl.shapes, xx, y, t, col, w=w, fill=fill)
        xx += w + gap
    ctx.chk(y + 0.30, limit)
    return xx - x - gap


# ---------------- 通用块排版（列优先，按阅读顺序） ----------------
class QB:
    def __init__(self, paras, src='GL', cite=None, tags=None, quote=True, fill=C['BOX'], minh=0):
        self.paras, self.src, self.cite, self.tags, self.quote, self.fill, self.minh = paras, src, cite, tags, quote, fill, minh
    def h(self, w, sz):
        return max(self.minh, quote_box_h(self.paras, w, sz, self.cite is not None, self.quote, 4, self.cite))
    def draw(self, ctx, sl, x, y, w, sz, limit):
        return qb(ctx, sl, x, y, w, self.paras, sz, self.src, self.cite, limit=limit, tags=self.tags, quote=self.quote, fill=self.fill, h=self.minh or None)

class OPic:
    """原图：等比缩放，宽不超过栏宽，高不超过 maxh。"""
    def __init__(self, D, on, sid, maxh=2.5, cap=None, minw=0):
        self.inf = D.pic(on, sid); self.maxh, self.cap = maxh, cap
    def size(self, w):
        _, _, _, pw, ph = self.inf
        s = min(w / pw, self.maxh / ph)
        return pw * s, ph * s
    def h(self, w, sz):
        return self.size(w)[1] + (0.30 if self.cap else 0)
    def draw(self, ctx, sl, x, y, w, sz, limit):
        import io
        pw, ph = self.size(w)
        p = picture(sl.shapes, io.BytesIO(self.inf[1]), x, y, pw, ph, crop=self.inf[2], name='ORIGPIC')
        p.line.color.rgb = RGBColor.from_string(C['LGRAY']); p.line.width = Pt(0.75)
        if self.cap: caption(sl.shapes, x, y + ph + 0.06, w, self.cap)
        ctx.chk(y + self.h(w, sz), limit)
        return self.h(w, sz)

class NImg:
    def __init__(self, name, ratio, cap=None, maxh=9):
        self.name, self.ratio, self.cap, self.maxh = name, ratio, cap, maxh
    def size(self, w):
        h = min(w / self.ratio, self.maxh); return h * self.ratio, h
    def h(self, w, sz):
        return self.size(w)[1] + (0.30 if self.cap else 0)
    def draw(self, ctx, sl, x, y, w, sz, limit):
        iw, ih = self.size(w)
        return ex_image(ctx, sl, self.name, x, y, iw, ih, self.cap, limit=limit, capw=w) - y

class TX:
    def __init__(self, paras, size=None, color=C['TEXT'], bold=False):
        self.paras, self.size, self.color, self.bold = paras, size, color, bold
    def h(self, w, sz):
        s = self.size or sz
        return text_height_in([dict(segs=meas_para(p), size=s) for p in self.paras], w, s) + 0.02
    def draw(self, ctx, sl, x, y, w, sz, limit):
        return text(ctx, sl, x, y, w, self.paras, self.size or sz, color=self.color, bold=self.bold, limit=limit)

class FN:
    """自定义块：hfn(w,sz)->h；dfn(ctx,sl,x,y,w,sz,limit)->h"""
    def __init__(self, hfn, dfn):
        self.hfn, self.dfn = hfn, dfn
    def h(self, w, sz): return self.hfn(w, sz)
    def draw(self, ctx, sl, x, y, w, sz, limit): return self.dfn(ctx, sl, x, y, w, sz, limit)


def pack(ctx, sl, blocks, x, w, ncols, sz, top=CT, right_edge=True, breaks=None, gap=GUT, widths=None):
    """把 blocks 按阅读顺序列优先排入 ncols 列；breaks 可指定强制换列的块序号。返回各列底边。"""
    ws = widths or [(w - (ncols - 1) * GUT) / ncols] * ncols
    xs = [x + sum(ws[:i]) + i * GUT for i in range(ncols)]
    if breaks is None and ncols > 1:          # 枚举所有连续分组，取最大越界最小者
        import itertools
        n = len(blocks)
        lims = [_lim(xs[c], ws[c], CB_R if (right_edge and c == ncols - 1) else CB_L) for c in range(ncols)]
        hc = [[b.h(ws[c], sz) for b in blocks] for c in range(ncols)]
        best = None
        for cuts in itertools.combinations(range(1, n), ncols - 1):
            bounds = (0,) + cuts + (n,)
            worst = 0
            for c in range(ncols):
                seg_ = range(bounds[c], bounds[c + 1])
                hh = sum(hc[c][i] for i in seg_) + GUT * (len(seg_) - 1)
                worst = max(worst, top + hh - lims[c])
            if best is None or worst < best[0]:
                best = (worst, set(cuts))
        if best: breaks = best[1]
    hs = [b.h(ws[0], sz) for b in blocks]
    total = sum(hs) + gap * (len(blocks) - 1)
    target = total / ncols
    ci, y = 0, top
    bottoms = [top] * ncols
    for i, b in enumerate(blocks):
        hb = b.h(ws[ci], sz)
        must = breaks is not None and i in breaks
        auto = breaks is None and ci < ncols - 1 and y > top and (y - top + hb / 2 > target)
        if (must or auto) and ci < ncols - 1:
            ci += 1; y = top
        lim = _lim(xs[ci], ws[ci], CB_R if (right_edge and ci == ncols - 1) else CB_L)
        hh = b.draw(ctx, sl, xs[ci], y, ws[ci], sz, lim)
        y += hh + gap
        bottoms[ci] = y - gap
    return bottoms


def layout_page(ctx, sl, blocks, sz, v, side=None, corner=None, breaks=None):
    """v: 'L8x1' 左8栏单列+右4栏 side 块；'L8x2'；'FWx2' 通栏两列+角图；'FWx3'。"""
    reg, n = v.split('x'); n = int(n)
    if reg == 'L8':
        pack(ctx, sl, blocks, X0, span(8), n, sz, right_edge=False, breaks=breaks)
        if side:
            yy = CT
            for b in side:
                yy += b.draw(ctx, sl, colx(8), yy, span(4), sz, CB_R) + GUT
    elif reg == 'L9':
        pack(ctx, sl, blocks, X0, span(9), n, sz, right_edge=False, breaks=breaks)
        if side:
            yy = CT
            for b in side:
                yy += b.draw(ctx, sl, colx(9), yy, span(3), sz, CB_R) + GUT
    else:
        pack(ctx, sl, blocks, X0, SW - ML - MR, n, sz, breaks=breaks)

X0 = ML

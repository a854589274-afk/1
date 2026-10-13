# -*- coding: utf-8 -*-
"""第1–17页（第一章：为什么要比）。"""
from lib import *
from kit import *
from core import img

X0, FW = ML, SW - ML - MR
L8x, L8w, R4x, R4w = colx(0), span(8), colx(8), span(4)
L7w, R5x, R5w = span(7), colx(7), span(5)
WHITE = C['WHITE']
SIZES = lambda top: [s for s in (40, 36, 32, 28, 24, 22, 20, 19, 18, 17, 16, 15, 14) if s <= top]


def pic_box(pinfo, maxw, maxh):
    _, blob, crop, w, h = pinfo
    s = min(maxw / w, maxh / h)
    return w * s, h * s


def orig_pic(ctx, sl, pinfo, x, y, w, h, limit=CB_L):
    import io
    _, blob, crop, pw, ph = pinfo
    p = picture(sl.shapes, io.BytesIO(blob), x, y, w, h, crop=crop, name='ORIGPIC')
    p.line.color.rgb = RGBColor.from_string(C['LGRAY']); p.line.width = Pt(0.75)
    ctx.chk(y + h, limit)


# ---------------------------------------------------------------- 1
def p01(D, ctx):
    sl = D.orig(1); ctx.page = ctx.pg
    def draw(sz):
        picture(sl.shapes, img('01_1'), 0, 0, SW, SH, rounded=False, name='NEWIMG_HERO')
        textbox(sl.shapes, ML, Y_CHAP, 4, H_CHAP, [P(CHAPTERS[1])], 12, color='9FE3DE', bold=True, pitch=1.2, name='CHAPTER')
        t = D.T(1, 2, 0)
        y = 1.75
        y += text(ctx, sl, ML, y, L7w, [cut(t, None, '结果'), cut(t, '结果')], sz, color=WHITE, bold=True, pitch=1.15, force=True) + 0.25
        y += text(ctx, sl, ML, y, L7w, [P('WS/T 407-2012 & CNAS-GL047:2021 解读与我科应用')], 20, color='9FE3DE') + 0.40
        y += text(ctx, sl, ML, y, L7w, D.T(1, 3), 28, color=WHITE, bold=True, force=True) + 0.25
        text(ctx, sl, ML, y, L7w, [P('第940医院检验科　·　2026年　月　日')], 16, color='C9D3DF')
        footer(sl, ctx.page, dark=True)
    sz = fit(ctx, sl, draw, [48])
    ctx.L(template='T1 主视觉页', orig='原P1', size=f'主标题{sz}pt（原48pt）', images='01_1',
          added=['主视觉新图 01_1', '副标题「WS/T 407-2012 & CNAS-GL047:2021 解读与我科应用」', '科室与日期行（日期留空待填）'],
          pending=['讲课日期【待填】'])


# ---------------------------------------------------------------- 2
def p02(D, ctx):
    sl = D.orig(2); ctx.page = ctx.pg
    def draw(sz):
        frame(sl, [P('本讲要回答的三个问题')], 1, ctx.page, '来源：原PPT', 'REG', mode=ctx.mode)
        top = [P('本讲依据：', bold=True), P('WS/T 407-2012《医疗机构内定量检验结果的可比性验证指南》'),
               P('CNAS-GL047:2021《医学实验室定量检验程序结果可比性验证指南》')]
        h = qb(ctx, sl, X0, CT, FW, top, 18, 'GL', '—— 本讲依据文件')
        y = CT + h + GUT
        cw = (FW - 2 * GUT) / 3
        qs = [D.T(2, 3, 0), D.T(2, 3, 1), P('我科怎么做？', color=C['RED'])]
        ch = max(card_h([q], cw, sz, 1.1) for q in qs)
        for i, q in enumerate(qs):
            card(ctx, sl, X0 + i * (cw + GUT), y, cw, ch, f'02_1-{i+1}', [q], sz, bold=True, icon_h=1.1, limit=CB_R)
    sz = fit(ctx, sl, draw, SIZES(40))
    ctx.L(template='T7 卡片网格页', orig='原P2', size=f'问题{sz}pt（原40pt）',
          added=['标题「本讲要回答的三个问题」', '顶部条文框：本讲依据两份文件全称', '第三问卡「我科怎么做？」', '图标组 02_1（天平/试管/实验楼）'])


# ---------------------------------------------------------------- 3
def p03(D, ctx):
    sl = D.orig(3); ctx.page = ctx.pg
    def draw(sz):
        frame(sl, D.T(3, 13), 1, ctx.page, '来源：国卫医发〔2022〕6号', 'REG', mode=ctx.mode)
        a, b = D.pic(3, 9), D.pic(3, 23)
        ph = (L7w - GUT) / (a[3] / a[4] + b[3] / b[4])          # 两张原截图等高并排
        wa, wb = ph * a[3] / a[4], ph * b[3] / b[4]
        orig_pic(ctx, sl, a, X0, CT, wa, ph); orig_pic(ctx, sl, b, X0 + wa + GUT, CT, wb, ph)
        y2 = CT + ph + GUT
        cw = wb
        lh = text_height_in([D.T(3, 11)[0]], cw - 2 * PAD, 14) * 5 + 0.1
        g = group(sl.shapes, 'CARD')
        rrect(g.shapes, X0 + wa + GUT, y2, cw, lh + 2 * PAD, fill=WHITE, line=C['SLATE'])
        textbox(g.shapes, X0 + wa + GUT + PAD, y2 + PAD, cw - 2 * PAD, lh, D.T(3, 11), 14, mode=ctx.mode, gap=0)
        ctx.chk(y2 + lh + 2 * PAD, CB_L)
        side = min(CB_L - y2 - 0.30, wa)
        ex_image(ctx, sl, '03_1', X0, y2, side, side, '示例图：院际结果互认', limit=CB_L)
        # 右 5 栏：第一章条文框 + 章节条 + 徽章
        paras = [dict(segs=bold_head(D.T(3, 19, 0), D.T(3, 19, 0)[0]['t'][:3]), size=sz), D.T(3, 15, 0), D.T(3, 17, 0)]
        h = qb(ctx, sl, R5x, CT, R5w, paras, sz, 'REG', '——《医疗机构检查检验结果互认管理办法》第一章', limit=CB_R)
        y = CT + h + GUT
        chs = D.T(3, 21) + D.T(3, 24)
        bw = (R5w - GUT) / 2
        bh = max(text_height_in([c], bw - 0.3, sz) for c in chs) + 0.12
        for i, c in enumerate(chs):
            cx, cy = R5x + (i // 3) * (bw + GUT), y + (i % 3) * (bh + 0.08)
            g = group(sl.shapes, 'CHAPTERBAR')
            rrect(g.shapes, cx, cy, bw, bh, fill=C['BOX'], line=C['SLATE'])
            textbox(g.shapes, cx + 0.15, cy + 0.06, bw - 0.3, bh - 0.12, [c], sz, mode=ctx.mode)
        bx = title_end(D.T(3, 13))
        head_badges(ctx, sl, bx, Y_TITLE + 0.13, [(D.T(3, 26, 0)[0]['t'] + D.T(3, 26, 0)[1]['t'] + D.T(3, 26, 0)[2]['t'] + D.T(3, 26, 0)[3]['t'], C['SLATE'], True),
                                      ('2022-03-01施行', C['ORANGE'], True)], limit=CB_R)
        ctx.chk(y + 3 * bh + 2 * 0.08, CB_R)
    sz = fit(ctx, sl, draw, SIZES(14))
    ctx.L(template='T5 数据页', orig='原P3', size=f'正文{sz}pt（原14pt；章节与落款原12pt→14pt）',
          added=['第一章两段放入条文框', '第二至七章做成章节条（两列×三行）', '落款四部门与日期放入卡片', '徽章「7章39条」（原文）「2022-03-01施行」', '示例图 03_1'],
          pending=[])


# ---------------------------------------------------------------- 4 / 5 （原P4 拆为两页）
P4_NODES = [  # (年份, 头段索引, 内容段索引, 引用)
    ('2006', 0, 1, '—— 卫办医发〔2006〕32号'),
    ('2009', 2, 3, '—— 国发〔2009〕12号'),
    ('2010', 4, 5, '—— 国办函〔2010〕67号'),
    ('2010', 6, 7, '—— 原PPT所列：卫办医改发〔2010〕108号'),
    ('2012', 8, 9, '—— 国发〔2012〕57号'),
    ('2013', 10, 11, '—— 国发〔2013〕40号'),
    ('2016', None, 12, '—— 原PPT'),
    ('2021', None, 13, '—— 原PPT'),
]

def _timeline(D, ctx, sl, nodes, sz, v):
    """std：左8栏纵向时间轴；wide：通栏两列时间轴（示例图移至角图位），用于保住原字号。"""
    ps = D.T(4, 2)
    items = []
    for yr, hi, ci, cite in nodes:
        paras = ([dict(segs=[dict(s, bold=True) for s in ps[hi]], size=sz)] if hi is not None else []) + [ps[ci]]
        items.append((yr, paras, cite))
    if v == 'std':
        cols = [(X0, L8w, items)]
    else:
        half = (FW - GUT) / 2
        k = (len(items) + 1) // 2
        cols = [(X0, half, items[:k]), (X0 + half + GUT, half, items[k:])]
    tops = []
    for cx, cw, its in cols:
        lx = cx + 0.55
        bx, bw = cx + 0.85, cw - 0.85
        y = CT
        for yr, paras, cite in its:
            h = qb(ctx, sl, bx, y, bw, paras, sz, 'REG', cite)
            tops.append((y, h, yr, bx, bw))
            y += h + GUT
        line(sl, lx, CT + 0.27, lx, y - GUT - 0.2, C['LGRAY'], 2)
        for (ty, h, yr, _, _) in tops[-len(its):]:
            dot(sl, lx, ty + 0.27, 0.08, C['NAVY'] if yr != '2021' else C['ORANGE'])
            textbox(sl.shapes, cx, ty + 0.12, 0.45, 0.3, [P(yr)], 14, color=C['NAVY'], bold=True, pitch=1.1)
    return tops


def p04(D, ctx):
    sl = D.orig(4); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, D.T(4, 3), 1, ctx.page, '来源：原PPT所列文件', 'REG', mode=ctx.mode, corner=img('04_1c') if v == 'wide' else None)
        _timeline(D, ctx, sl, P4_NODES[:4], sz, v)
        if v == 'std':
            h = CB_R - CT - 0.30; w = h * 2 / 3
            ex_image(ctx, sl, '04_1', R4x, CT, w, h, '示例图：逐级推进的互认')
        else:
            ctx.L(images='04_1c')
    sz = fit(ctx, sl, draw, SIZES(20), ('std', 'wide'))
    ctx.L(template='T2 条文页（纵向时间轴）' + ('；宽版：为保字号，时间轴改为通栏两列，示例图移至标题行角图位' if ctx.variant == 'wide' else ''),
          orig='原P4（上半：2006–2010）', size=f'正文{sz}pt（原20pt）',
          added=['每个文号一个节点，节点内容放入条文框，引用写对应文号', '新图 04_1'],
          pending=['卫办医发〔2006〕32号的标题与成文日期', '「卫办医改发」还是「卫办医政发」〔2010〕108号'])


def p05(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, [P('检查结果互认历程（续）')], 1, ctx.page, '来源：原PPT所列文件', 'REG', mode=ctx.mode, corner=img('05_1c') if v == 'wide' else None)
        tops = _timeline(D, ctx, sl, P4_NODES[4:], sz, v)
        ty, h, _, bx, bw = tops[-1]
        bwid = badge_w('↻ 正式稿见下页')
        if v == 'std':
            badge(sl.shapes, R4x, ty + 0.12, '↻ 正式稿见下页', C['ORANGE'], w=bwid)
            hh = ty - GUT - CT - 0.30; w = hh * 2 / 3
            ex_image(ctx, sl, '05_1', R4x, CT, w, hh, '示例图：2016年互认“破冰”')
        else:
            badge(sl.shapes, bx + bw - bwid, ty + h + 0.12, '↻ 正式稿见下页', C['ORANGE'], w=bwid)
            ctx.chk(ty + h + 0.42, CB_R)
            ctx.L(images='05_1c')
    sz = fit(ctx, sl, draw, SIZES(20), ('std', 'wide'))
    ctx.L(template='T2 条文页（纵向时间轴）' + ('；宽版：通栏两列，示例图移至角图位' if ctx.variant == 'wide' else ''),
          orig='原P4（下半：2012–2021）——原P4文字20pt，单页放不下，拆为两页', size=f'正文{sz}pt（原20pt）',
          added=['标题「检查结果互认历程（续）」', '徽章「↻ 正式稿见下页」', '新图 05_1'],
          pending=['2016年京津冀「27项·132家」仅核到媒体报道层（健康界2016-09-05），三地原始通知未核'])


# ---------------------------------------------------------------- 6 新：互认最新进展
def p06(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    def draw(sz):
        frame(sl, [P('互认最新进展（2022–2026）')], 1, ctx.page, '来源：国家政策文件与行业标准', 'REG', mode=ctx.mode)
        nodes = [
            ('2022-03-01', [P('《医疗机构检查检验结果互认管理办法》施行（国卫医发〔2022〕6号）；第十三条规定互认标志统一为HR')], C['SLATE']),
            ('2024-11', [P('七部门《关于进一步推进医疗机构检查检验结果互认的指导意见》（国卫医政发〔2024〕37号）：2025年底地市域互认项目>200项，2027年底省域>300项')], C['SLATE']),
            ('2026-11-01', [P('WS/T 885—2026 实施；4.2.3 要求', P('“实验室内部比对”', color=C['ORANGE'], bold=True)[0], '遵循 WS/T 407 等标准')], C['ORANGE']),
        ]
        cw = (FW - 2 * GUT) / 3
        ly = CT + 0.15
        line(sl, X0, ly, X0 + FW, ly, C['LGRAY'], 2.5)
        hmax = max(text_height_in([n[1][0]], cw - 0.3, sz) for n in nodes) + 0.3 + 0.38
        for i, (d, ps, col) in enumerate(nodes):
            x = X0 + i * (cw + GUT)
            dot(sl, x + 0.15, ly, 0.09, col)
            g = group(sl.shapes, 'TLNODE')
            rrect(g.shapes, x, ly + 0.25, cw, hmax, fill=C['BOX'] if col != C['ORANGE'] else 'FDF1E8', line=col, lw=1.0 if col == C['ORANGE'] else 0.75)
            textbox(g.shapes, x + 0.15, ly + 0.25 + 0.12, cw - 0.3, 0.3, [P(d)], 16, color=col, bold=True, pitch=1.1)
            textbox(g.shapes, x + 0.15, ly + 0.25 + 0.5, cw - 0.3, hmax - 0.6, ps, sz, mode=ctx.mode)
        y = ly + 0.25 + hmax + 0.4
        paras = [P('互认的技术前提＝院内结果可比', bold=True, color=C['NAVY']),
                 P('“……发挥相关质控组织、专业机构等作用，明确不同仪器设备、试剂和检测方法的参考范围和结果判读标准”')]
        h = qb(ctx, sl, X0, y, L8w, paras, sz, 'REG', '—— 国卫医政发〔2024〕37号')
        yb = y + h + GUT
        w1 = badge_w('2021 征求意见稿'); badge(sl.shapes, X0, yb, '2021 征求意见稿', C['SLATE'], w=w1, fill=False)
        mid_badge(sl, X0 + w1 + 0.37, yb + 0.15, '≠', C['ORANGE'])
        badge(sl.shapes, X0 + w1 + 0.62, yb, '2022 正式稿', C['NAVY'], w=badge_w('2022 正式稿'))
        ctx.chk(yb + 0.3, CB_L)
        side = min(R4w, CB_R - y - 0.30)
        ex_image(ctx, sl, '06_1', R4x, y, side, side, '示例图：征求意见稿与正式稿')
    sz = fit(ctx, sl, draw, SIZES(18))
    ctx.L(template='T4 流程页（横向时间轴）', orig='新增页', size=f'正文{sz}pt',
          added=['三节点时间轴（2026节点橙色高亮）', '条文框「互认的技术前提＝院内结果可比」+ 2024意见原文一句', '对照徽章「2021 征求意见稿 ≠ 2022 正式稿」', '示例图 06_1'],
          pending=['2024节点按核到的成文日期写「2024-11」（你给的「2024-11-27」是新闻发布会日期，见日志§2）'])


# ---------------------------------------------------------------- 7 原P5
def p07(D, ctx):
    sl = D.orig(5); ctx.page = ctx.pg
    def draw(sz):
        frame(sl, D.T(5, 4), 1, ctx.page, '来源：卫医发〔2006〕73号', 'REG', corner=img('07_1'), mode=ctx.mode)
        ctx.L(images='07_1')
        a = D.pic(5, 2)
        ph = 2.2; pw = ph * a[3] / a[4]
        orig_pic(ctx, sl, a, X0, CT, pw, ph)
        # 环形图 + 六章
        from chart import doughnut
        cx = X0 + pw + GUT
        doughnut(sl, cx, CT, 1.45, [5, 16, 11, 11, 9, 4], hi=2)
        lx = cx + 1.45 + 0.15
        text(ctx, sl, lx, CT, X0 + L7w - lx, D.T(5, 6), 14, gap=2, pitch=1.2)
        y = CT + ph + GUT
        ctx.p7y = y + qb(ctx, sl, X0, y, L7w, D.T(5, 3), sz, 'REG', '—— 原PPT')
        # 右5栏：10 条要点编号卡（两列）
        items = D.T(5, 9)
        nums = ['1', '2', '3', '4', '', '', '', '', '', '']
        cw = (R5w - 0.12) / 2
        hs = [text_height_in([it], cw - 0.2 - 0.3, 14) for it in items]
        y = CT
        for r in range(5):
            rh = max(hs[r], hs[r + 5]) + 0.14
            for c in range(2):
                k = r + 5 * c
                x = R5x + c * (cw + 0.12)
                g = group(sl.shapes, 'NUMCARD')
                rrect(g.shapes, x, y, cw, rh, fill=WHITE, line=C['LGRAY'])
                if nums[k]:
                    textbox(g.shapes, x + 0.08, y + 0.07, 0.3, 0.26, [P(nums[k] + '.')], 14, color=C['ORANGE'], bold=True, pitch=1.2)
                textbox(g.shapes, x + 0.38, y + 0.07, cw - 0.46, rh - 0.14, [items[k]], 14, mode=ctx.mode, pitch=1.2)
            y += rh + 0.08
            ctx.chk(y - 0.08, CB_R)
        t = '↻ 2020年国卫办医函〔2020〕560号修订第二十八条'
        badge(sl.shapes, X0, ctx.p7y + GUT, t, C['SLATE'], w=badge_w(t))
        ctx.chk(ctx.p7y + GUT + 0.3, CB_L)
    sz = fit(ctx, sl, draw, SIZES(20))
    ctx.L(template='T5 数据页', orig='原P5', size=f'说明段{sz}pt（原20pt）；章节与要点14pt（原18/14pt）',
          added=['原生环形图（5/16/11/11/9/4，第三章高亮）', '10条要点做成编号卡片两列（第1–4条原为自动编号，补显示编号）', '徽章「↻ 2020年国卫办医函〔2020〕560号修订第二十八条」', '角图 07_1'],
          pending=['「2000年1月31日卫生厅医政司批准立项」一句出处未核（上轮建议删除，本轮按规则保留原文）', '国卫办医函〔2020〕560号我未能独立核到原件'])


# ---------------------------------------------------------------- 8–12 原P6–P10（《办法》条文页）
def law_page(D, ctx, page, on, title_id, arts, pics, newimg, warn, extra=None, sizes=None, picnote=None):
    """arts: [(段落列表, 条号, 标签子串列表, 各段字号)]；pics: 原图 shape id。
    版式变体：std（8/4栏）→ wide（9/3栏）→ cols2（通栏两列，新图在角图位）；同字号下依次尝试，均放不下再降字号。"""
    sl = D.orig(on); ctx.page = page

    def mk_boxes(sz):
        out = []
        for paras, head, tags, sizes_ in arts:
            ps = list(paras)
            tagp = []
            for t in tags:                       # 括号标注移到框头右侧橙色标签
                for k in range(len(ps)):
                    if t in orig_text(ps[k]):
                        ps[k], tp = excise(ps[k], t)
                        tagp.append(ptext(tp))
                        break
            hd, rest = split_head(ps[0], head)
            body = [dict(segs=[dict(s, bold=True, color=C['NAVY']) for s in hd], size=sz)]
            if orig_text(rest).strip():
                body.append(dict(segs=rest, size=sz))
            for k, p in enumerate(ps[1:], 1):
                body.append(dict(segs=p, size=min(sz, sizes_[k]) if sizes_ else sz))
            out.append((body, '—— 原PPT引《医疗机构临床实验室管理办法》' + head, [(t, C['ORANGE']) for t in tagp]))
        return out

    def pics_block(x, y, w, maxh, row=False):
        infos = [D.pic(on, p) for p in pics]
        n = len(infos)
        if n == 4:
            if row:
                cw = (w - 3 * 0.12) / 4; chh = cw * 0.66
                cells = [(x + i * (cw + 0.12), y) for i in range(4)]
                hh = chh
            else:
                cw = (w - 0.12) / 2; chh = cw * 0.62
                cells = [(x + (i % 2) * (cw + 0.12), y + (i // 2) * (chh + 0.12)) for i in range(4)]
                hh = 2 * chh + 0.12
            for (cx, cy), inf in zip(cells, infos):
                w_, h_ = pic_box(inf, cw, chh)
                orig_pic(ctx, sl, inf, cx, cy, w_, h_, limit=CB_L)
        else:
            w_, h_ = pic_box(infos[0], w, maxh)
            orig_pic(ctx, sl, infos[0], x, y, w_, h_, limit=CB_L)
            hh = h_
        yb = y + hh
        if picnote:
            caption(sl.shapes, x, yb + 0.06, w, picnote[0]); yb += 0.30
        if extra:
            extra(sl, x, yb + 0.10, w); yb += 0.40
        return yb

    def warn_title():
        x0 = title_end(D.T(on, title_id))
        x1 = SW - MR - CORNER_W - GUT
        g = group(sl.shapes, 'WARN')
        rrect(g.shapes, x0, Y_TITLE - 0.02, x1 - x0, 0.62, fill=C['RED'], line=C['RED'])
        textbox(g.shapes, x0 + 0.1, Y_TITLE + 0.04, x1 - x0 - 0.2, 0.5, [P(warn)], 12, color=C['WHITE'], bold=True, pitch=1.2)
        ctx.chk(text_height_in([P(warn)], x1 - x0 - 0.2, 12, pitch=1.2) + 0.04, 0.52)

    def draw(sz, v):
        boxes = mk_boxes(sz)
        warn_title()
        corner = True
        cimg = None if (not v.startswith('cols2') and not pics) else img(newimg + ('' if pics else 'c'))
        frame(sl, D.T(on, title_id), 1, page, '来源：原PPT', 'REG', mode=ctx.mode, corner=cimg)
        if cimg: ctx.L(images=newimg + ('' if pics else 'c'))
        if v in ('std', 'wide'):
            tw, sx = (L8w, R4x) if v == 'std' else (span(9), colx(9))
            sw = SW - MR - sx
            y = CT
            for body, cite, tags in boxes:
                y += qb(ctx, sl, X0, y, tw, body, sz, 'REG', cite, tags=tags) + GUT
            y -= GUT
            if pics:
                yb = pics_block(sx, CT, sw, CB_R - CT - 0.8)
                ctx.chk(yb, CB_R)
            else:
                hh = min(CB_R - CT - 0.30, sw * 1.5); ww = hh * 2 / 3
                ex_image(ctx, sl, newimg, sx, CT, ww, hh, '示例图', capw=sw)
        else:   # cols2：两列（左列可加宽），按阅读顺序先填左列
            r = {'cols2': 0.5, 'cols2a': 0.58, 'cols2b': 0.64}[v]
            cw0 = (FW - GUT) * r; cw1 = FW - GUT - cw0
            cols = [[X0, CT], [X0 + cw0 + GUT, CT]]
            hs = [qbh(b, cw0, sz) for b, _, _ in boxes]
            # 第一个框放左列，其余放右列（若第一个框之后左列仍可放下第二个框则继续放左列）
            ci = 0
            for k, (body, cite, tags) in enumerate(boxes):
                if ci == 0 and k > 0 and cols[0][1] + hs[k] > CB_L:
                    ci = 1
                x, y = cols[ci]
                cols[ci][1] += qb(ctx, sl, x, y, cw0 if ci == 0 else cw1, body, sz, 'REG', cite, tags=tags,
                                  limit=CB_L if ci == 0 else CB_R) + GUT
            x, y = cols[1]
            if pics:
                y = pics_block(x, y, cw1, 2.0, row=True) + GUT
            ctx.chk(y - GUT, CB_R)
    sz = fit(ctx, sl, draw, sizes or SIZES(18), ('std', 'wide', 'cols2', 'cols2a', 'cols2b'))
    return sz


def _law_log(ctx, on, sz, orig_sz, added, pending=None):
    ctx.L(template='T2 条文页' + {'std': '', 'wide': '（宽版9/3栏：为保字号）', 'cols2': '（通栏两列版：为保字号，新图移至角图位）', 'cols2a': '（通栏两列版：为保字号，新图移至角图位）', 'cols2b': '（通栏两列版：为保字号，新图移至角图位）'}[ctx.variant], orig=f'原P{on}',
          size=f'正文{sz}pt（原{orig_sz}）', added=added,
          pending=(pending or []) + ['（一）（二）……细化款项非国家《办法》原文，出处【待核】（交GPT检索，见指令第三部分）'])


WARN = '! （一）（二）……细化款项非国家《办法》原文，出处【待核】；见第13页'

def p08(D, ctx):
    a = D.T(6, 3); b = D.T(6, 5)
    sz = law_page(D, ctx, 8, 6, 8, [(a, '第二十二条', ['（记录控制）', '（SOP）'], None), (b, '第二十三条', ['(注册证有效）'], None)],
                  [], '08_1', WARN)
    _law_log(ctx, 6, sz, '18pt', ['每条放入条文框，条号作框头加粗', '括号标注（记录控制）（SOP）(注册证有效）改为框头右侧橙色标签（括号文字保留）', '红色徽章：细化款项出处待核', '示例图 08_1'])


def p09(D, ctx):
    a = D.T(7, 3); b = D.T(7, 5)
    sz = law_page(D, ctx, 9, 7, 9, [(a, '第二十四条', [], None), (b, '第二十五条', [], None)], [8], '09_1', WARN,
                  picnote=('示例图：精密度 ≠ 正确度',))
    _law_log(ctx, 7, sz, '18pt', ['每条放入条文框', '原靶心图放右栏，图下说明「示例图：精密度 ≠ 正确度」', '红色徽章', '角图 09_1'])


def p10(D, ctx):
    a = D.T(8, 3); b = D.T(8, 5)
    sz = law_page(D, ctx, 10, 8, 6, [(a, '第二十六条', [], [18, 16, 16, 16, 16, 16, 16, 16]), (b, '第二十七条', [], None)],
                  [9, 11, 13, 15], '10_1', WARN)
    _law_log(ctx, 8, sz, '18pt；款项16pt', ['每条放入条文框', '四张原质控图右栏2×2等大排列', '红色徽章', '角图 10_1'],
             ['第二十七条所引计划号 20032302-T-361 对应 GB/T 20468-2006，已于2026-01-28废止（上轮已核，书目层）；页面按原文保留，未加注'])


def p11(D, ctx):
    a = D.T(9, 3); b = D.T(9, 5)
    def extra(sl, x, y, w):
        badge(sl.shapes, x, y, '● 图中中心：' + D.T(9, 12, 0)[0]['t'], C['SLATE'], fill=False)
    sz = law_page(D, ctx, 11, 9, 6, [(a, '第二十八条', ['（实验室间比对、能力验证）'], None), (b, '第二十九条', [], None)], [9],
                  '11_1', '! 第二十八条“全省……”非国家《办法》原文，出处【待核】；见第13页', extra=extra)
    _law_log(ctx, 9, sz, '18pt', ['每条放入条文框', '（实验室间比对、能力验证）改为橙色标签', '原网络图右栏；原图上叠放的椭圆标签「临床检验中心」移到图下（避免压图）', '红色徽章', '角图 11_1'])


def p12(D, ctx):
    a = D.T(10, 3); b = D.T(10, 5)
    sz = law_page(D, ctx, 12, 10, 6, [(a, '第三十条', [], None), ([b[0]], '第三十一条', [], None), ([b[1]], '第三十二条', [], None)],
                  [], '12_1', '! “每年比对不少于2次”“1/2PT”非国家《办法》原文，出处【待核】；见第13页')
    _law_log(ctx, 10, sz, '18pt', ['第三十、三十一、三十二条各放一个条文框', '红色徽章', '示例图 12_1'],
             ['第三十一条所引计划号 20032301-T-361 对应 GB/T 20470-2006，已于2026-01-28废止（上轮已核，书目层）'])


# ---------------------------------------------------------------- 13 新：国家原文对照
def p13(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    O = C['ORANGE']
    rows = [
        ('第二十二条',
         P('……加强临床实验室质量控制和管理', P('工作，', color=O)[0], '制定并严格执行……'),
         P('医疗机构应当加强临床实验室质量控制和管理', P('。医疗机构临床实验室应当', color=O)[0], '制定并严格执行临床检验项目标准操作规程和检验仪器的标准操作、维护规程。')),
        ('第二十八条',
         P(P('全省三级以上医疗机构', color=O)[0], '……必须参加由', P('省卫生厅临床检验中心', color=O)[0], '组织的室间质量评价活动'),
         P('医疗机构临床实验室应当参加', P('室间质量评价机构', color=O)[0], '组织的临床检验室间质量评价。')),
        ('第二十九条（末句）',
         P('（原PPT未收录）', color=C['GRAY']),
         P('医疗机构应当对床旁临床检验项目与临床实验室相同临床检验项目常规临床检验方法进行比对。')),
        ('第三十条',
         P('（一）', P('每年比对不少于2次，比对样本不少于5个', color=O)[0], '……（三）……相对偏差不能大于', P('1/2PT', color=O)[0], '可接受范围'),
         P('医疗机构临床实验室应当将尚未开展室间质量评价的临床检验项目与其他临床实验室的同类项目进行比对，或者用其他方法验证其结果的可靠性。临床检验项目比对有困难时，医疗机构临床实验室应当对方法学进行评价，包括准确性、精密度、特异性、线性范围、稳定性、抗干扰性、参考范围等，并有质量保证措施。')),
        ('第三十二条',
         P('质量管理记录保存期限', P('在2年以上', color=O)[0]),
         P('质量管理记录保存期限', P('至少为2年', color=O)[0], '。')),
    ]
    def draw(sz):
        frame(sl, [P('《医疗机构临床实验室管理办法》国家原文对照')], 1, ctx.page, '来源：卫医发〔2006〕73号（2020年修订）', 'REG', corner=img('13_1'), mode=ctx.mode)
        ctx.L(images='13_1')
        widths = [1.05, 4.3, 0.45, FW - 1.05 - 4.3 - 0.45]
        heads = [[P('条款')], [P('原PPT表述（出处待核）')], [P('')], [P('国家原文（卫医发〔2006〕73号，2020年修订）')]]
        body = []
        for head, lt, rt in rows:
            hc = [P(head, bold=True, color=C['NAVY'])] + ([P('↑ 新增', bold=True, color=C['ORANGE'])] if '二十九' in head else [])
            body.append([hc, [lt], [P('≠')], [rt]])
        native_table(ctx, sl, X0, CT, widths, heads, body, sz, [C['SLATE'], C['RED'], C['ORANGE'], C['SLATE']],
                     mid_col=2, limit=CB_R)
    sz = fit(ctx, sl, draw, SIZES(16))
    ctx.L(template='T3 对照页（表格化：左右两栏＋中缝≠列）', orig='新增页', size=f'正文{sz}pt',
          added=['新图 13_1（角图位）', '左栏只摘原PPT中有差异的短句（加省略号），右栏为国家原文；差异处橙色', '中缝列逐行「≠」；第二十九条末句加「↑ 新增」', '版式说明：五行条文按T3卡片排列需约7.5英寸高，改为原生表格（左右对照＋中缝列），对比主图移至角图位'],
          pending=['右栏国家原文取自地方卫健委转载的2020修订版全文与NCCL刊载2006原文（上轮内容已核）；国家卫健委官网原件我未能直接打开'])


# ---------------------------------------------------------------- 14 原P11：CL02 2012→2023
def p14(D, ctx):
    sl = D.orig(11); ctx.page = ctx.pg
    def draw(sz):
        frame(sl, D.T(11, 4)[:1], 1, ctx.page, '来源：CNAS-CL02', 'GL', mode=ctx.mode)
        rw = 2.95
        lw = FW - 0.5 - rw
        xr = X0 + lw + 0.5
        y0 = CT
        T12, T23 = [('2012版', C['SLATE'])], [('2023版', C['NAVY'])]
        # 上排：原封面 | 副标题与5.6 | 5.6.3 条文框
        b563 = [dict(segs=[dict(s, bold=True) for s in D.T(11, 8, 0)], size=sz), D.T(11, 16, 0)]
        b564 = [dict(segs=[dict(s, bold=True) for s in D.T(11, 12, 0)], size=sz), D.T(11, 14, 0), D.T(11, 6, 0), D.T(11, 9, 0), D.T(11, 9, 1)]
        h564 = qbh(b564, lw, sz)
        rowh = CB_L - y0 - GUT - h564
        a = D.pic(11, 5)
        pw = min(1.15, rowh * a[3] / a[4]); ph14 = pw * a[4] / a[3]
        best = None
        for tw in [1.9 + 0.1 * i for i in range(16)]:
            bw = lw - pw - tw - 2 * GUT
            ht = text_height_in([dict(segs=meas_para(p), size=sz) for p in D.T(11, 4)[1:] + D.T(11, 3)], tw, sz, 3)
            hb = qbh(b563, bw, sz)
            m = max(ht, hb)
            if best is None or m < best[0]: best = (m, tw)
        tw = best[1]
        bw = lw - pw - tw - 2 * GUT
        orig_pic(ctx, sl, a, X0, y0, pw, ph14)
        text(ctx, sl, X0 + pw + GUT, y0, tw, D.T(11, 4)[1:] + D.T(11, 3), sz, gap=3, limit=y0 + rowh)
        qb(ctx, sl, X0 + pw + tw + 2 * GUT, y0, bw, b563, sz, 'GL', '—— CNAS-CL02:2012', limit=y0 + rowh, tags=T12)
        qb(ctx, sl, X0, y0 + rowh + GUT, lw, b564, sz, 'GL', '—— CNAS-CL02:2012', tags=T12)
        if rowh < 1.2: ctx.chk(1.2 - rowh, 0)
        note = [P('CNAS-CL02:2012 已于 2023-12-01 废止；现行 CNAS-CL02:2023（2023-12-01 实施），对应条款 7.3.7.4', P('【条文待核】', color=C['RED'], bold=True)[0])]
        h3 = qb(ctx, sl, xr, y0, rw, [P('2023版', bold=True, color=C['NAVY'])] + note, sz, 'GL', '—— CNAS 认可规范文件清单', limit=CB_R)
        mid_badge(sl, xr - 0.25, y0 + h3 / 2, '↻', C['ORANGE'], w=0.4)
        bt = '↻ 5.6.4 → 7.3.7.4'
        badge(sl.shapes, xr, y0 + h3 + GUT, bt, C['ORANGE'], w=badge_w(bt))
        iy = y0 + h3 + GUT + 0.3 + GUT
        iw = min(rw, (CB_R - iy - 0.3) * 1.6)
        ex_image(ctx, sl, '14_1', xr, iy, iw, iw / 1.6, '示例图：旧版 → 新版', capw=rw)
    sz = fit(ctx, sl, draw, SIZES(18))
    ctx.L(template='T3 对照页（变体：2012版宽栏＋2023版窄栏；标题过长无角图，对比图16:10放右栏）', orig='原P11', size=f'正文{sz}pt（原18/14pt；副标题两行原28pt）',
          added=['左「2012版」：5.6.3、5.6.4各一条文框，引用「—— CNAS-CL02:2012」，原封面截图保留', '右「2023版」注释框（含【条文待核】）', '中缝「↻」与徽章「↻ 5.6.4 → 7.3.7.4」', '新图 14_1（角图位）'],
          pending=['CNAS-CL02:2023 第7.3.7.4条原文（CNAS官网仅公开封面与前言，受ISO版权保护）'])


# ---------------------------------------------------------------- 15 新：文件层级金字塔
def p15(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    tiers = [
        ('①', '部门规范性文件', '《医疗机构临床实验室管理办法》《医疗机构检查检验结果互认管理办法》', C['SLATE']),
        ('②', '行业标准', 'WS/T 407-2012、WS/T 885—2026', C['TEAL']),
        ('③', '认可准则', 'CNAS-CL02:2023 第7.3.7.4条', C['NAVY']),
        ('④', '认可指南', 'CNAS-GL047:2021', '2E5482'),
        ('⑤', '我科', 'LZJY-2-CX-38《比对管理程序》', C['ORANGE']),
    ]
    def draw(sz):
        frame(sl, [P('可比性验证的文件层级')], 1, ctx.page, '来源：各文件原文', 'REG', mode=ctx.mode)
        n = len(tiers); th = 0.78; gap = 0.12
        pw_top, pw_bot = 1.4, 4.0
        for i, (num, lvl, docs, col) in enumerate(tiers):
            y = CT + i * (th + gap)
            wt = pw_top + (pw_bot - pw_top) * i / n
            wb = pw_top + (pw_bot - pw_top) * (i + 1) / n
            cx = X0 + pw_bot / 2
            s = sl.shapes.add_shape(MSO_SHAPE.TRAPEZOID, Emu(int((cx - wb / 2) * EMU)), Emu(int(y * EMU)), Emu(int(wb * EMU)), Emu(int(th * EMU)))
            s.adjustments[0] = (wb - wt) / 2 / th
            s.fill.solid(); s.fill.fore_color.rgb = RGBColor.from_string(col); s.line.fill.background(); s.shadow.inherit = False
            s.name = 'PYRAMID'
            tf = s.text_frame; bp = tf._txBody.find(qn('a:bodyPr')); bp.set('anchor', 'ctr')
            p = tf.paragraphs[0]; from lib import _pitch; _pitch(p, 16, 1.1, align='ctr')
            r = p.add_run(); r.text = num + ' ' + lvl; set_run_font(r, size=16, color=C['WHITE'], bold=True)
            tx = X0 + pw_bot + GUT
            g = group(sl.shapes, 'TIERTEXT')
            rrect(g.shapes, tx, y, L8w - pw_bot - GUT, th, fill=C['BOX'], line=col)
            textbox(g.shapes, tx + PAD, y + 0.06, L8w - pw_bot - GUT - 2 * PAD, th - 0.12, [P(docs)], sz, anchor='m', pitch=1.2)
            ctx.chk(text_height_in([P(docs)], L8w - pw_bot - GUT - 2 * PAD, sz, pitch=1.2), th - 0.12)
        yb = CT + n * (th + gap) - gap + GUT
        text(ctx, sl, X0, yb, L8w, [P('①②面向所有医疗机构；③④面向申请或已获 CNAS 认可的实验室；⑤为我科执行文件', color=C['GRAY'])], 14)
        hh = CB_R - CT - 0.30; ww = hh * 2 / 3
        ex_image(ctx, sl, '15_1', R4x, CT, ww, hh, '示例图：五级文件层级', capw=R4w)
    sz = fit(ctx, sl, draw, SIZES(18))
    ctx.L(template='T2 条文页（左8栏为原生金字塔）', orig='新增页', size=f'正文{sz}pt',
          added=['原生五层金字塔（来源色：法规灰蓝/WS青绿/CNAS藏青/我科橙）', '适用对象说明行', '示例图 15_1'],
          pending=['CNAS-CL02-A001:2023 第7.3.7.4条（指名可参考 GL047 与 WS/T 407）未列入第③层，按你的方案处理；是否加入请你决定'])


# ---------------------------------------------------------------- 16 原P12：两份文件
def p16(D, ctx):
    sl = D.orig(12); ctx.page = ctx.pg
    def draw(sz):
        frame(sl, [P('两份文件：CNAS-GL047 与 WS/T 407')], 1, ctx.page, '来源：CNAS-GL047:2021；WS/T 407-2012', 'GL', mode=ctx.mode)
        iw = span(4); ih = iw / 4
        picture(sl.shapes, img('16_1'), colx(4), CT, iw, ih, name='NEWIMG'); ctx.L(images='16_1')
        top = CT + ih + GUT
        mw, ag = 2.3, 0.5
        cw = (FW - mw - 2 * ag) / 2
        xl, xm, xr = X0, X0 + cw + ag, X0 + cw + ag + mw + ag
        # 左：GL047 封面 + 前言条文框
        bh = qbh([D.T(12, 3, 0)], cw, sz)
        a = D.pic(12, 5)
        ph = CB_L - top - bh - GUT - 0.42; pw = ph * a[3] / a[4]
        orig_pic(ctx, sl, a, xl, top, pw, ph)
        bt = '该条款在CL02:2023中对应7.3.7.4'
        badge(sl.shapes, xl + pw + 0.15, top, bt, C['ORANGE'], w=min(cw - pw - 0.15, badge_w(bt)))
        ctx.chk(badge_w(bt), cw - pw - 0.15)
        qb(ctx, sl, xl, top + ph + GUT, cw, [D.T(12, 3, 0)], sz, 'GL', '—— CNAS-GL047 前言')
        # 中：范围红框
        h = qb(ctx, sl, xm, top, mw, D.T(12, 8), sz, 'GL', '—— CNAS-GL047 范围', quote=False, fill='FFF7F7')
        for x0, x1 in ((xl + cw + 0.06, xm - 0.06), (xr - 0.06, xm + mw + 0.06)):
            ay = top + h / 2
            arrow(sl, x0, ay, x1, ay, C['ORANGE'], 3)
        # 右：WS/T 407 封面与标题
        th = text(ctx, sl, xr, top, cw, D.T(12, 10), 14, bold=True)
        gpics = [D.pic(12, 14), D.pic(12, 12)]
        avail = CB_R - top - th - 0.15
        tot_h = sum(p[4] for p in gpics); sc = min(avail / tot_h, cw / max(p[3] for p in gpics))
        yy = top + th + 0.15
        for p in gpics:
            orig_pic(ctx, sl, p, xr, yy, p[3] * sc, p[4] * sc, limit=CB_R); yy += p[4] * sc
    sz = fit(ctx, sl, draw, SIZES(18))
    ctx.L(template='T3 对照页（中缝加宽至2.3英寸放GL047范围原文）', orig='原P12', size=f'正文{sz}pt（原16/18pt）',
          added=['标题「两份文件：CNAS-GL047 与 WS/T 407」', '对比主图 16_1', '左：GL047封面＋前言条文框', '中：范围原文＋（周期性），两侧橙色箭头水平对称指向中缝', '右：WS/T 407封面（原组合图拆为上下两图等比保留）', '徽章「该条款在CL02:2023中对应7.3.7.4」'],
          pending=[])


# ---------------------------------------------------------------- 17 新：两份文件对照表
def p17(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    rows = [
        ('性质', '卫生行业推荐性标准，2012-12-25发布，2013-08-01实施', 'CNAS认可指南，2021-04-25发布实施，解释认可准则的可比性条款', '≠'),
        ('适用', '同一医疗机构内；最多10个检测系统；重复不超过5次', '相同或不同地点的多个检验程序', '≠'),
        ('前提', '各系统已按EP9-A2/EP15-A2完成性能评价；最大CV/最小CV<2倍', '关键性能指标经验证满足要求', '='),
        ('样本', '宜首选临床标本，用其他物质须验证互通性；至少2个浓度（正常+异常），取质控总均值±20%', '应使用患者样本（抗凝剂相同）；覆盖临床适宜区间，重点关注医学决定水平；不少于5例', '≠'),
        ('方法', '合并CV→查表A.1定重复次数→相对极差R', '检测系统≤4个用参比系统比对法；>4个用均值法；7.2.3可参考WS/T 407', '≠'),
        ('判定', 'R ≤ 分析质量要求（按7级优选顺序确定）', '参比法：5份中≥4份符合，或扩样后≥90%符合；均值法：R符合判断标准', '≠'),
        ('不通过', '剔除偏差大的系统，与规范操作系统比对；必要时校准转换；不可比时采用不同参考区间并在报告单标示', '具有计量学可比性的可用修正值/修正因子；否则避免向临床发出具有不同临床意义的结果，与用户沟通并记录', '≠'),
        ('时机', '8种情形（见WS/T 407第5章）', '启用前、常规定期评审、任一要素变更时', '≠'),
    ]
    def draw(sz):
        frame(sl, [P('两份文件对照：WS/T 407-2012 与 CNAS-GL047:2021')], 1, ctx.page, '来源：WS/T 407-2012；CNAS-GL047:2021', 'GL', corner=img('17_1'), mode=ctx.mode)
        ctx.L(images='17_1')
        w0, wb = 0.95, 0.6
        wc = (FW - w0 - wb) / 2
        widths = [w0, wc, wc, wb]
        mar = 0.08
        pitch = 1.15
        hh = [max(text_height_in([P(c)], w - 2 * mar, sz, pitch=pitch) for c, w in zip(r[:3], widths)) + 2 * 0.05 for r in rows]
        head_h = sz * pitch / 72 + 0.12
        tot = head_h + sum(hh)
        ctx.chk(CT + tot, CB_R)
        gf = sl.shapes.add_table(len(rows) + 1, 4, Emu(int(X0 * EMU)), Emu(int(CT * EMU)), Emu(int(FW * EMU)), Emu(int(tot * EMU)))
        gf.name = 'TABLE'
        tb = gf.table
        tbl = gf._element.graphic.graphicData.tbl
        tbl.tblPr.set('firstRow', '1'); tbl.tblPr.set('bandRow', '0')
        sid = tbl.tblPr.find(qn('a:tableStyleId'))
        if sid is not None: sid.text = '{5940675A-B579-460E-94D1-54222C63F5DA}'   # 无样式、细网格
        for j, w in enumerate(widths): tb.columns[j].width = Emu(int(w * EMU))
        tb.rows[0].height = Emu(int(head_h * EMU))
        for i, h in enumerate(hh): tb.rows[i + 1].height = Emu(int(h * EMU))
        heads = ['维度', 'WS/T 407-2012', 'CNAS-GL047:2021', '']
        hcol = [C['SLATE'], C['TEAL'], C['NAVY'], C['SLATE']]
        def setcell(c, txt, size, color, bold=False, fill=None):
            c.margin_left = c.margin_right = Emu(int(mar * EMU)); c.margin_top = c.margin_bottom = Emu(int(0.05 * EMU))
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]; from lib import _pitch; _pitch(p, size, pitch, align='l')
            r = p.add_run(); r.text = txt; set_run_font(r, size=size, color=color, bold=bold)
            if fill: c.fill.solid(); c.fill.fore_color.rgb = RGBColor.from_string(fill)
            else: c.fill.solid(); c.fill.fore_color.rgb = RGBColor.from_string('FFFFFF')
        for j in range(4):
            setcell(tb.cell(0, j), heads[j], sz, C['WHITE'], True, hcol[j])
        for i, (d, a, b, s) in enumerate(rows, 1):
            setcell(tb.cell(i, 0), d, sz, C['NAVY'], True, C['BOX'])
            setcell(tb.cell(i, 1), a, sz, C['TEXT'])
            setcell(tb.cell(i, 2), b, sz, C['TEXT'])
            setcell(tb.cell(i, 3), s, sz, C['WHITE'], True, C['ORANGE'] if s == '≠' else C['GREEN'])
            tb.cell(i, 3).text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        # 「适用」「方法」两行橙色细框：直接设置这两行单元格的上下边框（及首尾列外框）
        for i, r in enumerate(rows, 1):
            if r[0] in ('适用', '方法'):
                for j in range(4):
                    tcPr = tb.cell(i, j)._tc.get_or_add_tcPr()
                    sides = ['a:lnT', 'a:lnB'] + (['a:lnL'] if j == 0 else []) + (['a:lnR'] if j == 3 else [])
                    for side in sides:
                        for e in tcPr.findall(qn(side)): tcPr.remove(e)
                        ln = etree.Element(qn(side)); ln.set('w', str(int(Pt(1.75)))); ln.set('cmpd', 'sng')
                        sf = etree.SubElement(ln, qn('a:solidFill')); etree.SubElement(sf, qn('a:srgbClr')).set('val', C['ORANGE'])
                        tcPr.insert(0, ln)
    sz = fit(ctx, sl, draw, SIZES(16))
    ctx.L(template='T6 表格页', orig='新增页（全片核心页）', size=f'表格{sz}pt',
          added=['原生表格（表头WS青绿/GL藏青），每行最右「≠/=」徽章格', '「适用」「方法」两行橙色细框', '角图 17_1'],
          pending=['表格内容按你给的文字照录。上轮审计指出的措辞问题（GL047"可以选用"非"用"、"90%以上"非"≥90%"、第8章为"或与用户讨论"、WS/T 407 6.9"和(或)医学决定水平"）未改动表格，见日志§2，由你决定是否改'])


def native_table(ctx, sl, x, y, widths, heads, body, sz, head_cols, mid_col=None, limit=CB_R, pitch=1.1, mar=0.08, first_fill=C['BOX']):
    """原生表格：heads/body 的每格是段落列表；按测量设定行高。"""
    from lib import _pitch
    def ch(cell, w):
        return text_height_in([dict(segs=meas_para(p), size=sz) for p in cell], w - 2 * mar, sz, 2, pitch)
    head_h = max(ch(c, w) for c, w in zip(heads, widths)) + 0.12
    hh = [max(ch(c, w) for c, w in zip(r, widths)) + 0.12 for r in body]
    tot = head_h + sum(hh)
    ctx.chk(y + tot, limit)
    gf = sl.shapes.add_table(len(body) + 1, len(widths), Emu(int(x * EMU)), Emu(int(y * EMU)), Emu(int(sum(widths) * EMU)), Emu(int(tot * EMU)))
    gf.name = 'TABLE'
    tb = gf.table
    tbl = gf._element.graphic.graphicData.tbl
    tbl.tblPr.set('firstRow', '1'); tbl.tblPr.set('bandRow', '0')
    sid = tbl.tblPr.find(qn('a:tableStyleId'))
    if sid is not None: sid.text = '{5940675A-B579-460E-94D1-54222C63F5DA}'
    for j, w in enumerate(widths): tb.columns[j].width = Emu(int(w * EMU))
    tb.rows[0].height = Emu(int(head_h * EMU))
    for i, h in enumerate(hh): tb.rows[i + 1].height = Emu(int(h * EMU))
    def setcell(c, paras, color, bold, fill, align='l'):
        c.margin_left = c.margin_right = Emu(int(mar * EMU)); c.margin_top = c.margin_bottom = Emu(int(0.06 * EMU))
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = c.text_frame; tf.word_wrap = True
        for k, para in enumerate(paras):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            _pitch(p, sz, pitch, before=0 if k == 0 else 2, align=align)
            for s in mode_segs(para, ctx.mode):
                if not s['t']: continue
                r = p.add_run(); r.text = s['t']
                set_run_font(r, size=s.get('size') or sz, color=s.get('color') or color, bold=s.get('bold') if s.get('bold') is not None else bold,
                             strike=s.get('strike'), ul=s.get('ul'), base=s.get('base'))
        c.fill.solid(); c.fill.fore_color.rgb = RGBColor.from_string(fill)
    for j, cell in enumerate(heads):
        setcell(tb.cell(0, j), cell, C['WHITE'], True, head_cols[j])
    for i, row in enumerate(body, 1):
        for j, cell in enumerate(row):
            if j == mid_col:
                setcell(tb.cell(i, j), cell, C['WHITE'], True, C['ORANGE'] if ptext(cell[0]) == '≠' else C['GREEN'], align='ctr')
            else:
                setcell(tb.cell(i, j), cell, C['TEXT'], False, first_fill if j == 0 else C['WHITE'])
    return tot, head_h, hh

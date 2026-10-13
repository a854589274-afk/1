# -*- coding: utf-8 -*-
"""第18–31页（第二章：怎么比——GL047 部分）。"""
from lib import *
from kit import *
from core import img
from pages_a import orig_pic, pic_box, native_table, SIZES, WHITE

X0, FW = ML, SW - ML - MR
L8x, L8w, R4x, R4w = colx(0), span(8), colx(8), span(4)
L7w, R5x, R5w = span(7), colx(7), span(5)
VAR = ('L8x1', 'L8x2', 'L9x1', 'FWx2', 'FWx3')
VLOG = {'L8x1': '', 'L8x2': '（左8栏内两列）', 'L9x1': '（宽版9/3栏：为保字号）', 'FWx2': '（通栏两列：为保字号，新图移至角图位）', 'FWx3': '（通栏三列：为保字号，新图移至角图位）'}


def H(para, color=C['NAVY']):
    """框头：整段加粗。"""
    return [dict(s, bold=True, color=color) for s in para]


def title2(D, a, b):
    """“总 则 · 4.1 验证条件”式标题：两段原文合为一行。"""
    return [D.T(*a, 0) + [seg(' · ', kind='add')] + D.T(*b, 0)]


def std_page(ctx, sl, page, title, blocks, sizes, side_img, corner_img, src, key, chap=2, variants=VAR, breaks=None, side_extra=None):
    def draw(sz, v):
        fw = v.startswith('FW')
        frame(sl, title, chap, page, src, key, mode=ctx.mode, corner=img(corner_img) if fw else None)
        side = None
        if not fw:
            sw = span(4) if v.startswith('L8') else span(3)
            side = (side_extra or []) + [NImg(side_img, 2 / 3, '示例图', maxh=CB_R - CT - 0.3 - sum(b.h(sw, sz) + GUT for b in (side_extra or [])))]
        layout_page(ctx, sl, blocks(sz), sz, v, side=side, breaks=breaks)
        if fw:
            for b in (side_extra or []):
                pass
            ctx.L(images=corner_img)
    sz = fit(ctx, sl, draw, sizes, variants)
    return sz


# ---------------------------------------------------------------- 18 原P13：GL047 分隔页
def p18(D, ctx):
    sl = D.orig(13); ctx.page = ctx.pg
    def draw(sz):
        picture(sl.shapes, img('18_1'), 0, 0, SW, SH, rounded=False, name='NEWIMG_HERO')
        textbox(sl.shapes, ML, Y_CHAP, 4, H_CHAP, [P(CHAPTERS[2])], 12, color='9FE3DE', bold=True, pitch=1.2, name='CHAPTER')
        y = 2.3
        t0 = D.T(13, 2)
        y += text(ctx, sl, ML, y, L7w, [cut(t0[0], None, '医学'), cut(t0[0], '医学'), t0[1]], sz, color=WHITE, bold=True, pitch=1.2, force=True) + 0.3
        text(ctx, sl, ML, y, L7w, [P('2021-04-25发布实施')], 20, color='9FE3DE')
        footer(sl, ctx.page, dark=True)
    sz = fit(ctx, sl, draw, [32])
    ctx.L(template='T1 主视觉页（分隔页）', orig='原P13', size=f'{sz}pt（原32pt）', added=['主视觉 18_1', '副标题「2021-04-25发布实施」'], images='18_1')


# ---------------------------------------------------------------- 19 原P14：术语
def p19(D, ctx):
    sl = D.orig(14); ctx.page = ctx.pg
    def blocks(sz):
        g = lambda p: dict(segs=p, size=sz)
        ana = replace(D.T(14, 5, 0), '如：在“24h 尿蛋白质质量”中', '注：在“24h 尿蛋白质质量”中', 'CNAS-GL047 3', 'B1', ctx.page)
        mea = D.T(14, 12, 0)
        mea = insert(mea, '在检验医学中', '注1：', 'CNAS-GL047 3', 'B2', ctx.page)
        mea = insert(mea, '被测量可以是生物活性', '注2：', 'CNAS-GL047 3', 'B2', ctx.page)
        pro = D.T(14, 16, 0)
        pro = insert(pro, '测量程序通常在文件中', '注1：', 'CNAS-GL047 3', 'B3', ctx.page)
        pro = insert(pro, '测量程序可以包括', '注2：', 'CNAS-GL047 3', 'B3', ctx.page)
        com = replace(D.T(14, 23, 0), '获得检验结果间的一致性', '获得的检测结果间的一致性', 'WS/T 407 3.1', 'B4', ctx.page)
        cg = '—— CNAS-GL047 第3章'
        J = lambda h, d, col=C['NAVY']: [H(h, col) + [seg('　', kind='add')] + d]
        decomp(ctx, sl)
        return [QB(J(D.T(14, 3, 0), ana), 'GL', cg), QB(J(D.T(14, 10, 0), mea), 'GL', cg), QB(J(D.T(14, 14, 0), pro), 'GL', cg),
                QB(J(D.T(14, 19, 0), D.T(14, 20, 0)), 'GL', cg), QB(J(D.T(14, 22, 0), com, C['TEAL']), 'WS', '—— WS/T 407 3.1')]
    def decomp(ctx, sl):
        x = title_end(D.T(14, 18))
        y = Y_TITLE + 0.08
        textbox(sl.shapes, x, y + 0.03, 2.6, 0.3, [P('“24h 尿蛋白质质量”拆解：')], 14, color=C['NAVY'], bold=True, pitch=1.2)
        x += 2.65
        for a, b_ in [('蛋白质', '分析物'), ('质量', '特性')]:
            badge(sl.shapes, x, y, a, C['ORANGE'], w=0.95, h=0.36, sz=14); x += 0.98
            textbox(sl.shapes, x, y + 0.03, 0.3, 0.3, [P('＝')], 14, pitch=1.2); x += 0.3
            badge(sl.shapes, x, y, b_, C['NAVY'], w=0.95, h=0.36, sz=14, fill=False); x += 1.15
        ctx.chk(x, SW - MR - CORNER_W - GUT + 0.2)
    sz = std_page(ctx, sl, 19, D.T(14, 18), blocks, SIZES(18), '19_1', '19_1c', '来源：GL047 第3章；WS/T 407 3.1', 'GL')
    ctx.L(template='T2 条文页' + VLOG[ctx.variant], orig='原P14', size=f'正文{sz}pt（原18pt）',
          added=['5个术语各一条文框（术语名作框头）', '「可比性」框用青绿边框、引用 WS/T 407 3.1', '“24h尿蛋白质质量”拆解小图（原生徽章）：第6格放不下，移至标题行', '术语名与定义同框首行（加粗术语名后接定义），节省一行', '新图 19_1（角图位）'])


# ---------------------------------------------------------------- 20/21 原P15（拆两页）
def p20(D, ctx):
    sl = D.orig(15); ctx.page = ctx.pg
    def blocks(sz):
        mi = D.T(15, 10, 0)
        mi = insert(mi, '体外诊断医疗器械性能特征', '注1：', 'CNAS-GL047 3', 'B5', ctx.page)
        mi = insert(mi, '测量区间的下限', '注2：', 'CNAS-GL047 3', 'B5', ctx.page)
        notebox(ctx, sl)
        return [QB([H(D.T(15, 8, 0)), mi], 'GL', '—— CNAS-GL047 第3章'),
                QB([D.T(15, 17, 0)], 'REG', '—— 原PPT补充'), QB([D.T(15, 19, 0)], 'REG', '—— 原PPT补充')]
    def notebox(ctx, sl):
        note = [P(P('【需主任确认是否上屏】', bold=True, color=C['ORANGE'])[0], 'LoD–LoQ（2.6–3.3 μg/L）之间的结果报告方式需补充；检出限与定量限的现行文件为 CLSI EP17-A2（2012）')]
        x0 = title_end(D.T(15, 22))
        x1 = SW - MR - CORNER_W - GUT
        gg = group(sl.shapes, 'NOTE')
        rrect(gg.shapes, x0, Y_TITLE - 0.06, x1 - x0, 0.72, fill='FDF1E8', line=C['ORANGE'])
        textbox(gg.shapes, x0 + 0.1, Y_TITLE - 0.02, x1 - x0 - 0.2, 0.66, note, 12, pitch=1.2, gap=0)
        ctx.chk(text_height_in(note, x1 - x0 - 0.2, 12, 0, 1.2), 0.66)
    sz = std_page(ctx, sl, ctx.page, D.T(15, 22), blocks, SIZES(16), '20_1', '20_1c', '来源：CNAS-GL047 第3章；原PPT补充', 'GL',
                  variants=('L8x1', 'L9x1', 'FWx2', 'FWx3'))
    ctx.L(template='T2 条文页' + VLOG[ctx.variant], orig='原P15（上半：测量区间、检出限、检测下限）——原P15约800字，14pt单页放不下，拆为两页', size=f'正文{sz}pt（原16/14pt）',
          added=['测量区间框（引用 GL047 第3章）', '检出限、检测下限两框（引用「原PPT补充」）', '注释框【需主任确认是否上屏】（放标题行右侧）', '新图 20_1'],
          pending=['注释框内「CLSI EP17-A2（2012）为现行版」：我未独立核实是否已有更新版次【待核】'])


def p21(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    def blocks(sz):
        afp = [D.T(15, 23, 0), dict(segs=[seg('—— ', color=C['SLATE'], kind='add')] + [dict(s, color=C['SLATE']) for s in D.T(15, 24, 0)], size=14, align='r')]
        def ah(w, sz): return 0.8
        def ad(ctx, sl, x, y, w, sz, limit):
            x0, x1 = x + 0.3, x + w - 0.6
            vmax = 4.0
            X = lambda v: x0 + (x1 - x0) * v / vmax
            ly = y + 0.32
            line(sl, x0, ly, x1, ly, C['SLATE'], 2)
            rrect(sl.shapes, X(2.6), ly - 0.07, X(3.3) - X(2.6), 0.14, fill=C['ORANGE'], line=None, radius=0.02, name='SEG')
            for v, lab in [(0.8, 'LoB 0.8'), (2.6, 'LoD 2.6'), (3.3, 'LoQ 3.3')]:
                line(sl, X(v), ly - 0.12, X(v), ly + 0.12, C['NAVY'], 2)
                textbox(sl.shapes, X(v) - 0.5 + (0.18 if v == 3.3 else -0.18 if v == 2.6 else 0), ly + 0.14, 1.0, 0.26, [P(lab)], 12, color=C['NAVY'], align='ctr', pitch=1.1)
            textbox(sl.shapes, x1 + 0.1, ly - 0.13, 0.6, 0.26, [P('μg/L')], 12, color=C['GRAY'], pitch=1.1)
            t = '? 原文未给报告方式'
            badge(sl.shapes, X(2.95) - badge_w(t) / 2, y, t, C['ORANGE'], w=badge_w(t), h=0.24)
            ctx.chk(y + 0.8, limit)
            return 0.8
        return [QB([D.T(15, 21, 0)], 'REG', '—— 原PPT补充'), QB(afp, 'REG', None), FN(ah, ad)]
    sz = std_page(ctx, sl, ctx.page, [P('术语和定义（续）')], blocks, SIZES(16), '21_1', '21_1c', '来源：原PPT补充；CLSI EP17-A', 'GL',
                  variants=('L8x1', 'L9x1', 'FWx2'))
    ctx.L(template='T2 条文页' + VLOG[ctx.variant], orig='原P15（下半：灵敏度、AFP示例、EP17-A）', size=f'正文{sz}pt（原16/14pt）',
          added=['标题「术语和定义（续）」', '灵敏度框（原PPT补充）', 'AFP示例框；EP17-A原文作为该框末行引用（14pt保持原字号）', '原生浓度轴（0.8/2.6/3.3 μg/L，2.6–3.3橙色「? 原文未给报告方式」）', '新图 21_1'],
          pending=['原文"1各单位"疑为"1个单位"（错别字，仅记录不改）'])


# ---------------------------------------------------------------- 21 原P16：计量学可比性
def p22(D, ctx):
    sl = D.orig(16); ctx.page = ctx.pg
    steps = ['SI单位', '一级参考测量程序/一级参考物质', '二级参考物质', '制造商工作校准品', '产品校准品', '患者样本结果']
    def ladder_h(w, sz):
        return len(steps) * 0.40 + (len(steps) - 1) * 0.10 + 0.25 + 0.30
    def ladder(ctx, sl, x, y, w, sz, limit):
        for i, s in enumerate(steps):
            ind = i * 0.12
            yy = y + i * 0.50
            col = C['NAVY'] if i < 5 else C['ORANGE']
            gg = group(sl.shapes, 'STEP')
            rrect(gg.shapes, x + ind, yy, w - ind, 0.40, fill=C['BOX'], line=col)
            textbox(gg.shapes, x + ind + 0.1, yy + 0.05, w - ind - 0.2, 0.3, [P(s)], 14 if len(s) < 14 else 13 if False else 14, pitch=1.15, anchor='m')
        bt = '溯源性（过程）≠ 计量学可比性（结果）'
        yb = y + len(steps) * 0.5 - 0.1 + 0.25
        badge(sl.shapes, x, yb, bt, C['ORANGE'], w=min(w, badge_w(bt)))
        ctx.chk(yb + 0.3, limit)
        return yb + 0.3 - y
    def draw(sz, v):
        frame(sl, D.T(16, 2), 2, ctx.page, '来源：GL047 第3章；GB/T 29791.1', 'GL', corner=img('chain'), mode=ctx.mode)
        ctx.L(images='chain')
        tw = L8w if v == 'L8' else span(9)
        h = qb(ctx, sl, X0, CT, tw, [H(D.T(16, 12, 0)), D.T(16, 14, 0), dict(segs=D.T(16, 9, 0), size=min(sz, 14))], sz, 'GL', '—— CNAS-GL047 第3章；GB/T 29791.1-2013 A.3.39')
        y = CT + h + GUT
        a = D.pic(16, 6)
        pw, ph = pic_box(a, tw, CB_L - y)
        orig_pic(ctx, sl, a, X0, y, pw, ph)
        if ph < 1.5: ctx.chk(1.5 - ph, 0)
        ladder(ctx, sl, colx(8) if v == 'L8' else colx(9), CT, R4w if v == 'L8' else span(3), sz, CB_R)
    sz = fit(ctx, sl, draw, SIZES(18), ('L8', 'L9'))
    ctx.L(template='T2 条文页（右4栏为原生溯源链阶梯）', orig='原P16', size=f'正文{sz}pt（原18/14pt）',
          added=['计量学可比性条文框（含GB/T 29791.1原出处行）', '原截图在条文框下方', '原生溯源链阶梯（6级，通用简化示意）', '对照徽章「溯源性（过程）≠ 计量学可比性（结果）」', '角图 21_1'],
          pending=['溯源链为通用简化示意，非GL047原文'])


# ---------------------------------------------------------------- 22 原P17：4.1 验证条件
def p23(D, ctx):
    sl = D.orig(17); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, title2(D, (17, 10), (17, 8)), 2, ctx.page, '来源：CNAS-GL047 4.1', 'GL', mode=ctx.mode)
        h = qb(ctx, sl, X0, CT, FW, [D.T(17, 12, 0)], sz, 'GL', '—— CNAS-GL047 4.1')
        y = CT + h + GUT
        ids = [14, 18, 20, 22, 24]
        n = 5; cw = (FW - 4 * GUT) / 5
        ih = 0.6 if v == 'a' else 0.45
        ch = max(card_h([D.T(17, i, 0)], cw, sz, ih) for i in ids)
        for k, i in enumerate(ids):
            card(ctx, sl, X0 + k * (cw + GUT), y, cw, ch, f'22_1-{k+1}', [D.T(17, i, 0)], sz, icon_h=ih, limit=CB_R)
        y += ch + GUT
        # a) 卡下方的红色「不宜比对」卡 + 小图
        rw = 2 * cw + GUT
        im = 0.8
        tp = [P('! 不宜比对', bold=True, color=C['RED']), dict(segs=D.T(17, 16, 0), size=max(14, min(sz, 14)))]
        th = text_height_in([dict(segs=meas_para(p['segs'] if isinstance(p, dict) else p), size=14) for p in tp], rw - 2 * PAD - im - 0.15, 14) + 2 * PAD
        rh = max(th, im + 2 * PAD)
        gg = group(sl.shapes, 'REDCARD')
        rrect(gg.shapes, X0, y, rw, rh, fill='FBEDEC', line=C['RED'])
        picture(gg.shapes, img('22_2'), X0 + PAD, y + PAD, im, im, name='NEWIMG')
        textbox(gg.shapes, X0 + PAD + im + 0.15, y + PAD, rw - 2 * PAD - im - 0.15, rh - 2 * PAD, tp, 14, mode=ctx.mode)
        ctx.chk(y + rh, CB_L)
    sz = fit(ctx, sl, draw, SIZES(18), ('a', 'b'))
    ctx.L(template='T7 卡片网格页', orig='原P17', size=f'正文{sz}pt（原18pt；注原11pt→14pt）', images=['22_1', '22_2'],
          added=['标题合并原两行「总 则」「4.1 验证条件」', '顶部通栏条文框：4.1引导段', '5张卡对应a)–e)，图标取自同一张图标组图等分裁切', 'a)卡下方红色卡「! 不宜比对」放原"注"＋小图22_2'],
          pending=['e)可补我科实例（如门诊/急诊/POCT），未添加'])


# ---------------------------------------------------------------- 23 原P18：4.2 验证时机
def p24(D, ctx):
    sl = D.orig(18); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, title2(D, (18, 5), (18, 4)), 2, ctx.page, '来源：CNAS-GL047 4.2；WS/T 407 第5章', 'GL', mode=ctx.mode)
        mg = 1.25
        lw = {'a': (FW - mg) / 2, 'b': 6.6, 'c': 7.0}[v]
        rw = FW - mg - lw
        xr = X0 + lw + mg
        ic = 0.62
        y = CT
        tops = []
        for k, sid in enumerate([7, 9, 11]):
            p = D.T(18, sid, 0)
            hd = p[0]['t'].split(' ')[0]
            h = qb(ctx, sl, X0 + ic + 0.18, y, lw - ic - 0.18, [p], sz, 'GL', '—— CNAS-GL047 ' + hd)
            picture(sl.shapes, img(f'23_1-{k+1}'), X0, y + 0.05, ic, ic, rounded=False, name='NEWIMG_ICON')
            tops.append(y); y += h + GUT
        ctx.L(images='23_1')
        mid_badge(sl, X0 + lw + mg / 2, CT + (y - GUT - CT) / 2, '≠ 侧重不同', C['ORANGE'], w=mg - 0.2)
        th = text(ctx, sl, xr, CT, rw, D.T(18, 19), 14, bold=True, limit=CB_R)
        a = D.pic(18, 17)
        gh = rw / 2           # 8图标 2×4 组图
        pw, ph = pic_box(a, rw, CB_R - CT - th - 0.15 - gh - GUT)
        orig_pic(ctx, sl, a, xr, CT + th + 0.15, pw, ph, limit=CB_R)
        gy = CT + th + 0.15 + ph + GUT
        picture(sl.shapes, img('23_2'), xr, gy, rw, gh, rounded=False, name='NEWIMG_ICONS')
        ctx.L(images='23_2')
        ctx.chk(gy + gh, CB_R)
        if ph < 1.6: ctx.chk(1.6 - ph, 0)
    sz = fit(ctx, sl, draw, SIZES(18), ('a', 'b', 'c'))
    ctx.L(template='T3 对照页（中缝加宽放「≠ 侧重不同」）', orig='原P18', size=f'正文{sz}pt（原18pt）',
          added=['左「GL047 4.2」三条文框纵向排列，左侧图标组 23_1（启用/周期/变更）', '右「WS/T 407 第5章」原截图保留，下方8种情形图标组 23_2（2×4）'])


# ---------------------------------------------------------------- 24 原P19：4.3 判断标准
def p25(D, ctx):
    sl = D.orig(19); ctx.page = ctx.pg
    def blocks(sz):
        p1 = replace(D.T(19, 2, 0), '另外如果基于检测系统不精密度建立的标准高于临床要求，可根据临床需求适当调整可接受标准',
                     '反之，如果基于检测系统不精密度建立的标准高于临床要求，实验室负责人可根据临床需要适当调整可接受标准', 'WS/T 407 6.7.1', 'B6', ctx.page)
        p2 = D.T(19, 2, 1)
        p2 = replace(p2, '③依据生物学变异确定的分析质量要求，允许差异为个体内生物学变异（CV)的1/3',
                     '③依据生物学变异确定的分析质量要求（注：对于精密度检测结果符合要求的检测系统，同一检测项目可比性结果的允许差异为个体内生物学变异（CV)的1/3）',
                     'WS/T 407 6.7.2 c)', 'A1', ctx.page)
        p2 = replace(p2, '按以下优先顺序', '按以下优选顺序', 'WS/T 407 6.7.2', 'B7', ctx.page)
        p2 = replace(p2, '医疗机构内医师的临床经验', '医疗机构内医生的临床经验', 'WS/T 407 6.7.2', 'B7', ctx.page)
        ot = orig_text(p2)
        idx = [ot.find(c) for c in '①②③④⑤⑥⑦'] + [len(ot)]
        parts = [dict(segs=cut_i(p2, 0, idx[0]), size=sz)]
        for k in range(7):
            parts.append(dict(segs=cut_i(p2, idx[k], idx[k + 1]), size=sz, indent=0.14 * k))
        return [QB([H(D.T(19, 13, 0)), D.T(19, 15, 0)], 'GL', '—— CNAS-GL047 4.3'),
                QB([p1], 'WS', '—— WS/T 407 6.7.1'),
                QB(parts, 'WS', '—— WS/T 407 6.7.2')]
    def draw(sz, v):
        frame(sl, title2(D, (19, 5), (19, 13)), 2, ctx.page, '来源：CNAS-GL047 4.3；WS/T 407 6.7', 'GL', mode=ctx.mode, corner=img('24_1c'))
        ctx.L(images='24_1c')
        a = D.pic(19, 4)
        bw_ = CORNER_H * a[3] / a[4]
        orig_pic(ctx, sl, a, SW - MR - CORNER_W - GUT - bw_, MT, bw_, CORNER_H, limit=9)
        bl = blocks(sz)
        if v == 'FWx2':
            pack(ctx, sl, bl, X0, FW, 2, sz)
        else:
            pack(ctx, sl, bl, X0, FW, 2, sz, widths=[(FW - GUT) * 0.45, (FW - GUT) * 0.55])
    sz = fit(ctx, sl, draw, SIZES(18), ('FWx2', 'FWx2b'))
    ctx.L(template='T2 条文页（通栏两列：为保字号，原封面与新图移至标题行）', orig='原P19', size=f'正文{sz}pt（原18/14pt）',
          added=['4.3原文条文框（藏青）', '（1）条文框（青绿，引用WS/T 407 6.7.1）', '（2）条文框（青绿，引用6.7.2），①–⑦逐级缩进成阶梯', '原书籍封面图保留（移至标题行，与新图并列）', '新图 24_1（角图位）'])


# ---------------------------------------------------------------- 25 原P20：5 验证方案
def p26(D, ctx):
    sl = D.orig(20); ctx.page = ctx.pg
    items = ['检测系统（分析仪器、试剂和校准品）', '样本类型和数量', '实验操作和质量控制过程', '数据处理方法和判断标准', '人员了解验证方案', '制定验证计划，组织实施并记录']
    def draw(sz, v):
        frame(sl, D.T(20, 3), 2, ctx.page, '来源：CNAS-GL047 5', 'GL', mode=ctx.mode)
        lw = {'a': L7w, 'b': span(6)}[v]
        rx = X0 + lw + GUT; rw = FW - lw - GUT
        cw = (lw - 2 * 0.12) / 3
        nums = '①②③④⑤⑥'
        hs = [text_height_in([P(t)], cw - 0.53, 14) + 0.14 for t in items]
        rows = [max(hs[0:3]), max(hs[3:6])]
        cards_h = sum(rows) + 0.08
        a, b_ = D.pic(20, 4), D.pic(20, 7)
        w = (lw - GUT) / 2
        ph = min(w * a[4] / a[3], w * b_[4] / b_[3], CB_L - CT - cards_h - GUT)
        for k, p in enumerate((a, b_)):
            pw_, ph_ = pic_box(p, w, ph)
            orig_pic(ctx, sl, p, X0 + k * (w + GUT) + (w - pw_) / 2, CT, pw_, ph_)
        y = CT + ph + GUT
        for r in range(2):
            for c in range(3):
                k = 3 * r + c
                x = X0 + c * (cw + 0.12)
                gg = group(sl.shapes, 'NUMCARD')
                rrect(gg.shapes, x, y, cw, rows[r], fill=WHITE, line=C['LGRAY'])
                textbox(gg.shapes, x + 0.08, y + 0.07, 0.4, 0.3, [P(nums[k])], 16, color=C['ORANGE'], bold=True, pitch=1.1)
                textbox(gg.shapes, x + 0.45, y + 0.07, cw - 0.53, rows[r] - 0.14, [P(items[k])], 14, pitch=PITCH)
            y += rows[r] + 0.08
        ctx.chk(y - 0.08, CB_L)
        h = qb(ctx, sl, rx, CT, rw, [D.T(20, 6, 0)], sz, 'GL', '—— CNAS-GL047 5', limit=CB_R)
        yy = CT + h + GUT
        side = min(rw, CB_R - yy - 0.30)
        if side < 1.0: ctx.chk(1.0 - side, 0)
        ex_image(ctx, sl, '25_1', rx, yy, side, side, '示例图：程序文件与核对清单', capw=rw)
    sz = fit(ctx, sl, draw, SIZES(18), ('a', 'b'))
    ctx.L(template='T5 数据页', orig='原P20', size=f'正文{sz}pt（原18pt）',
          added=['两张程序文件截图等宽并排', '第5条原文条文框（右5栏）', '①–⑥编号卡：从原文摘出的六项要素（新增文字，原文不动；为保字号放在左栏截图下方）', '示例图 25_1'])


# ---------------------------------------------------------------- 26 原P21：6 实验前准备
def p27(D, ctx):
    sl = D.orig(21); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, D.T(21, 4), 2, ctx.page, '来源：CNAS-GL047 6；WS/T 407 6.3.1', 'GL', mode=ctx.mode, corner=img('26_2c'))
        cg = '—— CNAS-GL047 6'
        cw = (FW - 2 * GUT) / 3
        ih = 0.5
        cards = [(8, 10), (12, 14), (16, 18)]
        ch = max(card_h([H(D.T(21, a, 0)), D.T(21, b, 0)], cw, sz, ih) for a, b in cards) + 0.22
        for k, (a, b) in enumerate(cards):
            x = X0 + k * (cw + GUT)
            card(ctx, sl, x, CT, cw, ch, f'26_1-{k+1}', [H(D.T(21, a, 0)), D.T(21, b, 0)], sz, icon_h=ih, line=C['NAVY'], cite=cg)
        y = CT + ch + GUT
        # 6.4 宽卡（左9栏）：原文（A2、A3替换）＋左右对照
        p = D.T(21, 22, 0)
        p = replace(p, '应首选患者样本', '应使用患者样本', 'CNAS-GL047 6.4', 'A2', ctx.page)
        p = replace(p, '也可用室间质评物或其他参考物质，应验证互通性。',
                    '宜使用临床标本作为首选比对物质；不得不使用其他物质（如室间质评物或其他参考物质）时，应验证比对物质的互通性。（WS/T 407 6.3.1）',
                    'WS/T 407 6.3.1', 'A3', ctx.page)
        ww = span(9)
        body = [H(D.T(21, 20, 0)), p]
        h = qb(ctx, sl, X0, y, ww, body, sz, 'GL', '—— CNAS-GL047 6.4', icon=(img('26_1-4'), 0.3))
        xr = colx(9); wr = span(3)
        c5 = [H(D.T(21, 24, 0)), D.T(21, 26, 0)]
        h5 = card_h(c5, wr, sz, 0.45) + 0.22
        card(ctx, sl, xr, y, wr, h5, '26_1-5', c5, sz, icon_h=0.45, line=C['NAVY'], limit=CB_R, cite=cg)
        # 6.4 对照条放标题行（卡内与卡下均放不下）
        x0 = title_end(D.T(21, 4))
        x1 = SW - MR - CORNER_W - GUT
        ws_t = 'WS/T 407：宜首选临床标本；不得不用其他物质时验证互通性'
        gl_t = 'GL047：应使用患者样本'
        gw = sum(char_w(c, 14, True) for c in gl_t) / 72 + 0.3
        ww2 = x1 - x0 - gw - 0.55
        th = max(text_height_in([P(ws_t)], ww2 - 0.2, 14, pitch=1.15), 0.25) + 0.12
        yt = Y_TITLE + 0.28 - th / 2
        for xx, wdt, t, col in [(x0, gw, gl_t, C['NAVY']), (x0 + gw + 0.55, ww2, ws_t, C['TEAL'])]:
            gg = group(sl.shapes, 'CMP')
            rrect(gg.shapes, xx, yt, wdt, th, fill=WHITE, line=col)
            textbox(gg.shapes, xx + 0.1, yt + 0.06, wdt - 0.2, th - 0.12, [P(t)], 14, color=col, bold=True, pitch=1.15, anchor='m')
        mid_badge(sl, x0 + gw + 0.275, yt + th / 2, '≠', C['ORANGE'])
        ctx.chk(yt + th, 1.45)
        ctx.chk(y + h5, CB_R)
    sz = fit(ctx, sl, draw, SIZES(18), ('a',))
    ctx.L(template='T7 卡片网格页（变体：6.1–6.3一排三卡；6.4宽卡＋6.5卡；小图26_2移至角图位）', orig='原P21', size=f'正文{sz}pt（原18pt）', images=['26_1', '26_2c'],
          added=['6.1–6.5放入卡片，引用「—— CNAS-GL047 6」', '6.4对照「GL047：应使用患者样本 ≠ WS/T 407：宜首选临床标本…」放在标题行（卡内放不下）', '图标组 26_1（5枚）', '小图 26_2（角图位）'],
          pending=['版式说明：6.4原文含A2/A3替换后约230字，五卡等宽一排无法容纳，改为上排三卡、下排宽卡＋窄卡；6.4对照条移到标题行'])


# ---------------------------------------------------------------- 27 原P22：7.1 验证方法
def p28(D, ctx):
    sl = D.orig(22); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, D.T(22, 4), 2, ctx.page, '来源：CNAS-GL047 7.1', 'GL', corner=img('27_1'), mode=ctx.mode)
        ctx.L(images='27_1')
        h = qb(ctx, sl, X0, CT, FW, [H(D.T(22, 8, 0)), D.T(22, 10, 0)], sz, 'GL', '—— CNAS-GL047 7.1')
        y = CT + h + GUT
        cw = (FW - 0.5) / 2
        p1 = replace(D.T(22, 10, 1), '计算每个检测系统与参比系统检测结果的偏差', '计算每个检测系统结果与参比系统检测结果的偏差', 'CNAS-GL047 7.1', 'B8', ctx.page)
        tree_h = 0.95
        hh = max(qbh([P('参比系统比对法（检测系统≤4）', bold=True), p1], cw, sz), qbh([P('均值法（>4）', bold=True), D.T(22, 10, 2)], cw, sz))
        qb(ctx, sl, X0, y, cw, [P('参比系统比对法（检测系统≤4）', bold=True, color=C['NAVY']), p1], sz, 'GL', '—— CNAS-GL047 7.1', h=hh)
        qb(ctx, sl, X0 + cw + 0.5, y, cw, [P('均值法（>4）', bold=True, color=C['NAVY']), D.T(22, 10, 2)], sz, 'GL', '—— CNAS-GL047 7.1', h=hh, limit=CB_R)
        mid_badge(sl, X0 + cw + 0.25, y + hh / 2, '≠', C['ORANGE'])
        y += hh + GUT
        # 原生决策树
        bw, bh = 2.1, 0.4
        flow_box(ctx, sl, X0, y + 0.24, bw, bh, [P('检测系统数量？')], 14, col=C['NAVY'], bold=True)
        flow_box(ctx, sl, X0 + bw + 0.5, y, 3.3, bh, [P('≤4 → 参比系统比对法（7.2.1）')], 14, col=C['NAVY'])
        flow_box(ctx, sl, X0 + bw + 0.5, y + bh + 0.08, 3.3, bh, [P('>4 → 均值法（7.2.2）')], 14, col=C['NAVY'])
        flow_box(ctx, sl, X0 + bw + 0.5 + 3.3 + 0.4, y + 0.24, 3.6, bh, [P('按CV定次数 → WS/T 407（7.2.3）')], 14, col=C['TEAL'])
        ctx.chk(y + 0.24 + bh, CB_R)
        arrow(sl, X0 + bw, y + 0.24 + bh / 2, X0 + bw + 0.5, y + bh / 2, C['GRAY'])
        arrow(sl, X0 + bw, y + 0.24 + bh / 2, X0 + bw + 0.5, y + bh + 0.08 + bh / 2, C['GRAY'])
        ctx.chk(y + 2 * bh + 0.08, CB_L)
    sz = fit(ctx, sl, draw, SIZES(18), ('a',))
    ctx.L(template='T3 对照页（对比主图移至角图位：标题行下需留给引导句与两栏）', orig='原P22', size=f'正文{sz}pt（原18pt）',
          added=['顶部条文框：7.1引导句', '左「参比系统比对法（≤4）」右「均值法（>4）」，中缝「≠」', '底部原生决策树', '新图 27_1（16:10角图）'])


# ---------------------------------------------------------------- 28 原P23：7.2.1 参比系统比对方案
def p29(D, ctx):
    sl = D.orig(23); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, title2(D, (23, 3), (23, 5)), 2, ctx.page, '来源：CNAS-GL047 7.2.1', 'GL', mode=ctx.mode)
        ps = D.T(23, 7)
        d1 = cut(ps[3], None, '若比对样本量')
        d2 = cut(ps[3], '若比对样本量')
        boxes = [('a)', ps[0]), ('b)', ps[1]), ('c)', ps[2]), ('d)', d1)]
        ag = 0.4
        bw = (FW - 3 * ag) / 4
        hh = max(text_height_in([P(l), dict(segs=meas_para(p), size=sz)], bw - 0.2, sz) for l, p in boxes) + 0.2
        for k, (lab, p) in enumerate(boxes):
            x = X0 + k * (bw + ag)
            flow_box(ctx, sl, x, CT, bw, hh, [P(lab, bold=True, color=C['ORANGE']), p], sz, col=C['NAVY'])
            if k < 3:
                arrow(sl, x + bw + 0.05, CT + hh / 2, x + bw + ag - 0.05, CT + hh / 2, C['NAVY'], 2)
        # c) 下点阵：4 绿 1 红
        cx = X0 + 2 * (bw + ag)
        for i in range(5):
            dot(sl, cx + 0.25 + i * 0.36, CT + hh + 0.25, 0.12, C['GREEN'] if i != 3 else C['RED'])
        textbox(sl.shapes, cx + 0.2 + 5 * 0.36, CT + hh + 0.12, 1.1, 0.28, [P('4/5 通过')], 14, color=C['GREEN'], bold=True, pitch=1.1)
        y = CT + hh + 0.6
        h = qb(ctx, sl, X0, y, L8w, [d2], sz, 'GL', '—— CNAS-GL047 7.2.1')
        y += h + GUT
        chain = ['扩样', '≥90%', '达到20份仍不符合', '分析其他因素']
        x = X0
        for k, t in enumerate(chain):
            w = sum(char_w(c, 14, True) for c in t) / 72 + 0.4
            flow_box(ctx, sl, x, y, w, 0.42, [P(t)], 14, col=C['ORANGE'] if k == 3 else C['NAVY'], bold=True)
            x += w
            if k < 3:
                arrow(sl, x + 0.05, y + 0.21, x + 0.35, y + 0.21, C['GRAY'], 2); x += 0.4
        ctx.chk(y + 0.42, CB_L)
        side = CB_R - (CT + hh + 0.6) - 0.3
        ex_image(ctx, sl, '28_1', R4x, CT + hh + 0.6, side * 2 / 3, side, '示例图：5份中4份通过', capw=R4w)
    sz = fit(ctx, sl, draw, SIZES(18), ('a',))
    ctx.L(template='T4 流程页', orig='原P23', size=f'正文{sz}pt（原18pt）',
          added=['上方通栏流程 a)→b)→c)→d)（原文无编号字母，补显示a)–d)）', 'c)框下「5份中4份通过」点阵（4绿1红）', 'd)后半句放入下方条文框并接箭头链「扩样 → ≥90% → 达到20份仍不符合 → 分析其他因素」', '示例图 28_1'],
          pending=['箭头链中"≥90%"为你的写法，GL047原文为"90%以上"'])


# ---------------------------------------------------------------- 29 原P24：7.2.2 均值法
def p30(D, ctx):
    sl = D.orig(24); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, title2(D, (24, 3), (24, 4)), 2, ctx.page, '来源：CNAS-GL047 7.2.2', 'GL', mode=ctx.mode, corner=img('29_1c'))
        ctx.L(images='29_1c')
        ps = [D.T(24, 8, 0)] + D.T(24, 12)
        body = []
        for k, p in enumerate(ps):
            t = orig_text(p)
            if k in (2, 6):        # 两个公式：单独居中成行，Cambria Math
                body.append(dict(segs=[dict(s) for s in p], size=sz + 2, align='ctr', font='Cambria Math'))
            else:
                body.append(dict(segs=p, size=sz))
        tw = L8w if v == 'a' else span(9)
        qb(ctx, sl, X0, CT, tw, body, sz, 'GL', '—— CNAS-GL047 7.2.2', gap=3)
        # 右栏：示意柱状图
        from chart import bars
        sx = X0 + tw + GUT; sw = FW - tw - GUT
        vals = [5.05, 5.20, 4.85, 5.45, 5.10]
        cols = ['1F3A5F', '1F3A5F', C['ORANGE'], C['ORANGE'], '1F3A5F']
        bars(sl, sx, CT, sw, 2.1, ['系统1', '系统2', '系统3', '系统4', '系统5'], vals, cols, ymax=6, number_format='0.00', label_size=12)
        m = sum(vals) / 5; R = (max(vals) - min(vals)) / m * 100
        text(ctx, sl, sx, CT + 2.15, sw, [P('示意数据', bold=True, color=C['RED']),
                                          P(f'X̄ = {m:.2f}'), P('Xmax = 5.45；Xmin = 4.85'), P(f'R = 0.60 / {m:.2f} = {R:.1f}%')], 14, limit=CB_R)
        ctx.chk(CT + 2.15 + 1.2, CB_R)
    sz = fit(ctx, sl, draw, SIZES(18), ('a', 'b'))
    ctx.L(template='T2 条文页', orig='原P24', size=f'正文{sz}pt（原18pt）',
          added=['a)–f)原文放入一个条文框，两个公式单独居中成行（Cambria Math，原字符不变；未用OMML对象）', '右栏原生柱状图（5台仪器，标「示意数据」，Xmax/Xmin橙色），R=11.7%已复算', '新图 29_1（角图位：右栏下方放不下）'])


# ---------------------------------------------------------------- 30 原P25：7.2.3
def p31(D, ctx):
    sl = D.orig(25); ctx.page = ctx.pg
    steps = [('长期CV', '≥6个月质控数据', 'CV'), ('最大/最小CV<2倍', '否则先确认性能', 'CVmax/CVmin<2'),
             ('确定浓度', '质控总均值±20%', 'm总×(1±20%)'), ('合并CV查表A.1', '定重复次数 n', '√(ΣCVi²/n)'),
             ('计算R', '极差÷总均值', '(Xmax−Xmin)/X̄'), ('R≤要求则通过', '否则剔除后再比', 'R≤要求')]
    def draw(sz, v):
        frame(sl, title2(D, (25, 4), (25, 3)), 2, ctx.page, '来源：GL047 7.2.3；WS/T 407 6.4–6.8', 'GL', mode=ctx.mode)
        ag = 0.3
        bw = (FW - 5 * ag) / 6
        bh = 1.6
        for k, (a, b, f) in enumerate(steps):
            x = X0 + k * (bw + ag)
            gg = group(sl.shapes, 'FLOW')
            col = C['TEAL'] if k < 5 else C['GREEN']
            rrect(gg.shapes, x, CT, bw, bh, fill=C['BOX'], line=col, lw=1.0)
            textbox(gg.shapes, x + 0.1, CT + 0.08, bw - 0.2, 0.3, [P('①②③④⑤⑥'[k])], 16, color=C['ORANGE'], bold=True, pitch=1.1)
            textbox(gg.shapes, x + 0.1, CT + 0.40, bw - 0.2, bh - 0.82, [P(a, bold=True), P(b, color=C['GRAY'])], 14, pitch=1.15, gap=0)
            badge(gg.shapes, x + 0.08, CT + bh - 0.36, f, col, w=bw - 0.16, h=0.28, sz=12)
            ctx.chk(text_height_in([P(a), P(b)], bw - 0.2, 14, 0, 1.15) + 0.40, bh - 0.40)
            if k < 5:
                arrow(sl, x + bw + 0.03, CT + bh / 2, x + bw + ag - 0.03, CT + bh / 2, C['TEAL'], 2)
        y = CT + bh + 0.4
        qb(ctx, sl, X0, y, L8w, [D.T(25, 6, 0)], sz, 'GL', '—— CNAS-GL047 7.2.3')
        side = min(R4w, CB_R - y - 0.3)
        ex_image(ctx, sl, '30_1', R4x, y, side, side, '示例图：不精密度小 vs 大', capw=R4w)
    sz = fit(ctx, sl, draw, SIZES(18), ('a',))
    ctx.L(template='T4 流程页', orig='原P25', size=f'正文{sz}pt（原18pt）',
          added=['上方原生WS/T 407六步流程，每步一个公式徽章（新增文字）', '7.2.3原文条文框', '示例图 30_1'])


# ---------------------------------------------------------------- 31 原P26：8 相关措施
def p32(D, ctx):
    sl = D.orig(26); ctx.page = ctx.pg
    def draw(sz, v):
        frame(sl, D.T(26, 3), 2, ctx.page, '来源：CNAS-GL047 8', 'GL', mode=ctx.mode, corner=img('31_1c') if v == 'c' else None)
        y = CT
        if v != 'c':
            iw = span(6) if v == 'a' else span(4); ih = iw / 4
            picture(sl.shapes, img('31_1'), X0 + (FW - iw) / 2, CT, iw, ih, name='NEWIMG')
            y += ih + GUT
        ctx.L(images='31_1' if v != 'c' else '31_1c')
        cw = (FW - 0.5) / 2
        lp = [P('具有计量学可比性', bold=True, color=C['GREEN']), D.T(26, 5, 0), P('→ 修正值/修正因子 + 记录', bold=True, color=C['GREEN'])]
        rp = [P('不具有计量学可比性', bold=True, color=C['ORANGE']), D.T(26, 5, 1), P('→ 避免发出不同临床意义的结果，或与用户讨论 → 记录', bold=True, color=C['ORANGE'])]
        hh = max(qbh(lp, cw, sz), qbh(rp, cw, sz))
        qb(ctx, sl, X0, y, cw, lp, sz, 'GL', '—— CNAS-GL047 8', h=hh)
        qb(ctx, sl, X0 + cw + 0.5, y, cw, rp, sz, 'GL', '—— CNAS-GL047 8', h=hh, limit=CB_R)
        mid_badge(sl, X0 + cw + 0.25, y + hh / 2, '≠', C['ORANGE'])
    sz = fit(ctx, sl, draw, SIZES(18), ('a', 'b', 'c'))
    ctx.L(template='T3 对照页', orig='原P26', size=f'正文{sz}pt（原18pt）',
          added=['左「具有计量学可比性」第一段＋绿色结尾行', '右「不具有计量学可比性」第二段＋橙色结尾行', '中缝「≠」', '对比主图 31_1'],
          pending=['橙色结尾行按GL047原文写成"避免发出……，或与用户讨论 → 记录"（你的方案写作"→ 与用户讨论"，原文是"或"）', 'GL047第8章原文"符合4.2规定的可比性验证条件"，按章节结构疑应为4.1（仅记录，不改）'])

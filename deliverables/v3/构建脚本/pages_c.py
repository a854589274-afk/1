# -*- coding: utf-8 -*-
"""第33–40页：WS/T 407 比对试验实施、ALT 示例、我科怎么做、小结。"""
from lib import *
from kit import *
from core import img
from pages_a import orig_pic, pic_box, native_table, SIZES, WHITE
from pages_b import H, VLOG, std_page

X0, FW = ML, SW - ML - MR
L7w, R5x, R5w = span(7), colx(7), span(5)


def step_boxes(D, ctx, ks):
    """原P27 七个步骤（含 A4–A6、B9–B11 替换）。"""
    ps = D.T(27, 3)
    pg = ctx.page
    out = {k: ps[k] for k in range(7)}
    p = ps[0]
    if 0 in ks:
      p = replace(p, '监测数据估计不精密度，尽可能使用6个月的数据', '检测数据估计不精密度，尽可能使用累计6个月的检测数据', 'WS/T 407 6.4.1', 'B9', pg)
      p = insert(p, '如大于2倍', '如小于2倍，可使用本指南规定的比对方案；', 'WS/T 407 6.4.2', 'B9', pg)
      p = replace(p, 'CLSIEP9-A2', 'CLSI EP9-A2', 'WS/T 407 6.4.2', 'B9', pg)
      p = replace(p, '确认检测系统的性能符合要求', '确认检测系统间的结果可比性', 'WS/T 407 6.4.2', 'A4', pg)
      out[0] = p
    if 2 in ks:
      out[2] = replace(ps[2], '使用计算合并CV值确定每台仪器', '使用计算合并CV值查找附录A的表A.1，以确定每台仪器', 'WS/T 407 6.6', 'B10', pg)
    if 4 in ks:
      p = ps[4]
      ot = orig_text(p)
      first = ot.find(']X100%')
      p = replace(p, ']X100%', ']×100%', 'WS/T 407 6.8.4', 'B11', pg)
      from lib import cut_i
      ot2 = orig_text(p); j = ot2.find(']X100%', first + 1)
      a, b = cut_i(p, 0, j), cut_i(p, j, len(ot2))
      p = a + replace(b, ']X100%', ']×100%', 'WS/T 407 6.8.4', 'B11', pg)
      out[4] = p
    if 6 in ks:
      p = ps[6]
      p = replace(p, '如比对偏差大于或等于分析质量要求', '如比对偏差大于分析质量要求', 'WS/T 407 6.8.5 b)', 'A5', pg)
      p = replace(p, '均值最大的两个系统间可比性不符合要求，剔除偏差较大检测系统的结果后再比',
                  '均值差异最大的两个检测系统间的可比性不符合要求，将两个检测系统的结果分别与规范操作检测系统的结果进行比较，剔除偏差较大检测系统的结果后再比',
                  'WS/T 407 6.8.5 b)', 'A6', pg)
      out[6] = p
    cites = {0: '—— WS/T 407 6.4', 1: '—— WS/T 407 6.5', 2: '—— WS/T 407 6.6', 3: '—— WS/T 407 6.8.2–6.8.3', 4: '—— WS/T 407 6.8.4', 5: '—— WS/T 407 6.8.5', 6: '—— WS/T 407 6.8.5'}
    return [QB([out[k]], 'WS', cites[k]) for k in ks]


def p33(D, ctx):
    sl = D.orig(27); ctx.page = ctx.pg
    def draw(sz, v):
        fw = v.startswith('FW')
        frame(sl, D.T(27, 2), 2, ctx.page, '来源：WS/T 407-2012 6.4–6.8', 'WS', mode=ctx.mode, corner=img('32_1c') if fw else None)
        bl = step_boxes(D, ctx, [0, 1, 2])
        if fw:
            pack(ctx, sl, bl, X0, FW, 2, sz); ctx.L(images='32_1c')
        else:
            pack(ctx, sl, bl, X0, span(9), 2 if v == 'L9x2' else 1, sz, right_edge=False)
            hh = CB_R - CT - 0.3; ww = min(span(3), hh * 2 / 3); hh = ww * 1.5
            ex_image(ctx, sl, '32_1', colx(9), CT, ww, hh, '示例图：不精密度比较', capw=span(3))
    sz = fit(ctx, sl, draw, SIZES(18), ('L9x1', 'L9x2', 'FWx2'))
    ctx.L(template='T2 条文页' + ('（通栏两列，新图移至角图位）' if ctx.variant == 'FWx2' else '（左9栏/右3栏）'), orig='原P27（步骤1–3）——原P27约860字（含替换），14pt单页放不下，拆为两页',
          size=f'正文{sz}pt（原18pt；方案允许14pt）', added=['步骤1–3各一编号条文框，引用WS/T 407对应条款', '新图 32_1'])


def p34(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    def draw(sz, v):
        fw = v.startswith('FW')
        frame(sl, [P('比对试验实施（续）')], 2, ctx.page, '来源：WS/T 407-2012 6.8', 'WS', mode=ctx.mode, corner=img('33_1c') if fw else None)
        bl = step_boxes(D, ctx, [3, 4, 5, 6])
        def vh(w, sz): return 0.42
        def vd(ctx, sl, x, y, w, sz, limit):
            a = '≤ 分析质量要求 → 通过'; b = '> 分析质量要求 → 不通过'
            wa = badge_w(a, 14); wb = badge_w(b, 14)
            badge(sl.shapes, x, y, a, C['GREEN'], w=wa, h=0.36, sz=14)
            mid_badge(sl, x + wa + 0.25, y + 0.18, '≠', C['ORANGE'])
            badge(sl.shapes, x + wa + 0.5, y, b, C['RED'], w=wb, h=0.36, sz=14)
            ctx.chk(y + 0.36, limit); ctx.chk(x + wa + 0.5 + wb, x + w)
            return 0.42
        bl.append(FN(vh, vd))
        if fw:
            pack(ctx, sl, bl, X0, FW, 2, sz); ctx.L(images='33_1c')
        else:
            pack(ctx, sl, bl, X0, span(9), 2 if v == 'L9x2' else 1, sz, right_edge=False)
            hh = CB_R - CT - 0.3; ww = min(span(3), hh * 2 / 3); hh = ww * 1.5
            ex_image(ctx, sl, '33_1', colx(9), CT, ww, hh, '示例图：判定', capw=span(3))
    sz = fit(ctx, sl, draw, SIZES(18), ('L9x1', 'L9x2', 'FWx2'))
    ctx.L(template='T2 条文页' + ('（通栏两列，新图移至角图位）' if ctx.variant == 'FWx2' else '（左9栏/右3栏）'), orig='原P27（步骤4–7）', size=f'正文{sz}pt（原18pt；方案允许14pt）',
          added=['标题「比对试验实施（续）」', '步骤4–7各一编号条文框', '第7步下方对照「≤ → 通过（绿）≠ > → 不通过（红）」', '新图 33_1'])


def alt_frame(ctx, sl, D, n, name):
    tw = sum(char_w(ch, 28, True) for ch in ptext(D.T(n, 2, 0))) * 1.03 / 72
    use = tw <= SW - ML - MR - CORNER_W - GUT
    frame(sl, D.T(n, 2), 2, ctx.page, '来源：WS/T 407-2012 附录B', 'WS', mode=ctx.mode, corner=img(name + 'c') if use else None)
    if use: ctx.L(images=name + 'c')
    return use


def p35(D, ctx):
    sl = D.orig(28); ctx.page = ctx.pg
    def draw(sz, v):
        cn = alt_frame(ctx, sl, D, 28, '34_1')
        t = replace(D.T(28, 4, 0), '结果见表', '结果见表B.1', 'WS/T 407 B.1.1', 'B12', ctx.page)
        y = CT
        y += text(ctx, sl, X0, y, L7w, [H(D.T(28, 3, 0)), t], sz) + 0.15
        a = D.pic(28, 6)
        pw, ph = pic_box(a, L7w, CB_L - y)
        orig_pic(ctx, sl, a, X0, y, pw, ph)
        yy = CT
        yy += bignum(sl.shapes, R5x, yy, R5w, '47.6 / 120.8 U/L', 'm总（浓度水平1 / 水平2）', nsz=32) + GUT
        yy += bignum(sl.shapes, R5x, yy, R5w, '2.39% / 2.10%', 'CV合并（浓度水平1 / 水平2）', cite='—— WS/T 407 B.1.1', nsz=32) + GUT
        side = min(R5w, CB_R - yy - 0.3)
        if side < 1.0 and not cn: ctx.chk(1.0 - side, 0)
        if not cn: ex_image(ctx, sl, '34_1', R5x, yy, side, side, '示例图：两台同型号分析仪', capw=R5w)
    sz = fit(ctx, sl, draw, SIZES(18), ('a',))
    ctx.L(template='T5 数据页', orig='原P28', size=f'正文{sz}pt（原18pt）',
          added=['扫描表与计算式保留（原图）', '大数字卡「m总 47.6 / 120.8 U/L」「CV合并 2.39% / 2.10%」（已复算）', '示例图 34_1'])


def p36(D, ctx):
    sl = D.orig(29); ctx.page = ctx.pg
    def draw(sz, v):
        cn = alt_frame(ctx, sl, D, 29, '35_1')
        y = CT
        y += text(ctx, sl, X0, y, L7w, [H(D.T(29, 3, 0))], sz) + 0.1
        a, b = D.pic(29, 7), D.pic(29, 10)
        h2 = text_height_in([D.T(29, 8, 0)], L7w, sz) + 0.1
        avail = CB_L - y - h2 - 0.25
        sc = min(L7w / a[3], L7w / b[3], avail / (a[4] + b[4]))
        orig_pic(ctx, sl, a, X0, y, a[3] * sc, a[4] * sc); y += a[4] * sc + 0.15
        t = replace(D.T(29, 8, 0), '3.比对试验的可接受标准', '3.比对试验的结果可接受标准', 'WS/T 407 B.1.3', 'B13', ctx.page)
        y += text(ctx, sl, X0, y, L7w, [H(t)], sz) + 0.1
        orig_pic(ctx, sl, b, X0, y, b[3] * sc, b[4] * sc)
        # 右：±20% 浓度带
        yy = CT
        for lvl, m, lo, hi in [('水平1', 47.6, 38.1, 57.1), ('水平2', 120.8, 96.6, 145.0)]:
            gg = group(sl.shapes, 'BAND')
            rrect(gg.shapes, R5x, yy, R5w, 0.74, fill=WHITE, line=C['LGRAY'])
            textbox(gg.shapes, R5x + 0.12, yy + 0.06, 1.0, 0.28, [P(lvl)], 14, color=C['NAVY'], bold=True, pitch=1.1)
            bx0, bx1 = R5x + 1.0, R5x + R5w - 0.2
            rrect(gg.shapes, bx0, yy + 0.16, bx1 - bx0, 0.2, fill='D6EEEC', line=C['TEAL'], radius=0.03)
            line(gg, (bx0 + bx1) / 2, yy + 0.1, (bx0 + bx1) / 2, yy + 0.42, C['ORANGE'], 2)
            textbox(gg.shapes, bx0 - 0.25, yy + 0.42, 0.9, 0.26, [P(f'{lo}')], 12, color=C['TEAL'], pitch=1.1, align='ctr')
            textbox(gg.shapes, (bx0 + bx1) / 2 - 0.5, yy + 0.42, 1.0, 0.26, [P(f'{m}')], 12, color=C['ORANGE'], pitch=1.1, align='ctr', bold=True)
            textbox(gg.shapes, bx1 - 0.85, yy + 0.42, 0.95, 0.26, [P(f'{hi} U/L')], 12, color=C['TEAL'], pitch=1.1, align='r')
            yy += 0.74 + 0.1
        yy += GUT - 0.1
        yy += bignum(sl.shapes, R5x, yy, R5w, '6% = CVI 18.0% × 1/3', '分析质量要求', cite='—— WS/T 407 B.1.2–B.1.3', nsz=32) + GUT
        side = min(R5w, CB_R - yy - 0.3)
        if side < 0.7 and not cn: ctx.chk(0.7 - side, 0)
        if not cn: ex_image(ctx, sl, '35_1', R5x, yy, side, side, '示例图：±20% 浓度带', capw=R5w)
    sz = fit(ctx, sl, draw, SIZES(18), ('a',))
    ctx.L(template='T5 数据页', orig='原P29', size=f'正文{sz}pt（原18pt）',
          added=['两张扫描图保留', '原生「±20%浓度带」（38.1–57.1、96.6–145.0 U/L，已复算）', '大数字卡「6% = CVI 18.0% × 1/3」', '示例图 35_1'],
          pending=['ALT个体内生物学变异18.0%为标准示例原值；现行生物学变异数据库数值可能不同（未核，不上页面）'])


def p37(D, ctx):
    sl = D.orig(30); ctx.page = ctx.pg
    def draw(sz, v):
        cn = alt_frame(ctx, sl, D, 30, '36_1')
        y = CT
        y += text(ctx, sl, X0, y, L7w, [H(D.T(30, 3, 0))], sz) + 0.12
        a, b = D.pic(30, 5), D.pic(30, 9)
        sc = min(L7w / a[3], L7w / b[3], (CB_L - y - 0.15) / (a[4] + b[4]))
        orig_pic(ctx, sl, a, X0, y, a[3] * sc, a[4] * sc); y += a[4] * sc + 0.15
        orig_pic(ctx, sl, b, X0, y, b[3] * sc, b[4] * sc)
        yy = CT
        yy += bignum(sl.shapes, R5x, yy, R5w, 'n = 3', '每份样本的重复检测次数', cite='—— WS/T 407 B.1.4', nsz=40) + 0.15
        note = '表中“2系统/3次/CV 1%”=2.67，与同行其他列不一致，按公式应为2.27；不影响本例结论'
        yy += text(ctx, sl, R5x, yy, R5w, [P(note, color=C['ORANGE'])], 12, limit=CB_R) + GUT
        side = min(R5w, CB_R - yy - 0.3)
        if side < 0.9 and not cn: ctx.chk(0.9 - side, 0)
        if not cn: ex_image(ctx, sl, '36_1', R5x, yy, side, side, '示例图：每份样本重复测定3次', capw=R5w)
    sz = fit(ctx, sl, draw, SIZES(18), ('a',))
    ctx.L(template='T5 数据页', orig='原P30', size=f'正文{sz}pt（原18pt）',
          added=['两张扫描图保留（表B.2中2.67照原样保留）', '大数字卡「n = 3」', '橙色小注：2.67按公式应为2.27（q₀.₉₅(2,4)/√3 = 2.267，本轮独立复算）', '示例图 36_1'])


def p38(D, ctx):
    sl = D.orig(31); ctx.page = ctx.pg
    def draw(sz, v):
        cn = alt_frame(ctx, sl, D, 31, '37_1')
        y = CT
        y += text(ctx, sl, X0, y, L7w, [H(D.T(31, 3, 0))], sz) + 0.1
        concl = replace(D.T(31, 10, 0), '均小于分析质量标准，两台生化机检测的ALT结果具有可比性',
                        '均小于分析质量要求，故认为A和B生化分析仪检测ALT的结果可比性是可接受的', 'WS/T 407 B.1.6', 'B14', ctx.page)
        hc = qbh([concl], L7w, sz)
        a, b = D.pic(31, 6), D.pic(31, 8)
        avail = CB_L - y - hc - 0.15 - 0.25
        sc = min(L7w / a[3], avail / (a[4] + b[4]))
        orig_pic(ctx, sl, a, X0, y, a[3] * sc, a[4] * sc); y += a[4] * sc + 0.15
        orig_pic(ctx, sl, b, X0, y, b[3] * sc, b[4] * sc); y += b[4] * sc + GUT
        qb(ctx, sl, X0, y, L7w, [concl], sz, 'WS', '—— WS/T 407 B.1.5–B.1.6')
        if sc * a[3] < 4.0: ctx.chk(4.0 - sc * a[3], 0)
        # 右：原生柱状图 + 6% 红色虚线
        from chart import bars
        ch_h = 2.0
        gf = bars(sl, R5x, CT, R5w, ch_h, ['水平1', '水平2'], [2.64, 1.92], [C['GREEN'], C['GREEN']], ymax=8, number_format='0.00"%"', label_size=12)
        pa = gf.chart._chartSpace.find('.//' + qn('c:plotArea'))
        lay = pa.find(qn('c:layout'))
        if lay is None:
            lay = etree.SubElement(pa, qn('c:layout')); pa.remove(lay); pa.insert(0, lay)
        ml = etree.SubElement(lay, qn('c:manualLayout'))
        for tag, val in [('layoutTarget', 'inner'), ('xMode', 'edge'), ('yMode', 'edge'), ('x', '0.14'), ('y', '0.08'), ('w', '0.82'), ('h', '0.76')]:
            etree.SubElement(ml, qn('c:' + tag)).set('val', val)
        yl = CT + ch_h * (0.08 + 0.76 * (1 - 6 / 8))
        line(sl, R5x + R5w * 0.14, yl, R5x + R5w * 0.96, yl, C['RED'], 2, dash=True)
        yy = CT + ch_h + 0.1
        textbox(sl.shapes, R5x, yy, R5w, 0.28, [P('红色虚线：分析质量要求 6%', color=C['RED'])], 12, pitch=1.2)
        yy += 0.38
        badge(sl.shapes, R5x, yy, '= 通过', C['GREEN'], w=1.1, h=0.36, sz=14)
        yy += 0.36 + GUT
        side = min(R5w, CB_R - yy - 0.3)
        if side < 0.9 and not cn: ctx.chk(0.9 - side, 0)
        if not cn: ex_image(ctx, sl, '37_1', R5x, yy, side, side, '示例图：两台仪器结果几乎重合', capw=R5w)
    sz = fit(ctx, sl, draw, SIZES(18), ('a',))
    ctx.L(template='T5 数据页', orig='原P31', size=f'正文{sz}pt（原18/16pt）',
          added=['两张扫描表保留', '结论原文放入条文框（B14替换）', '原生柱状图 R=2.64%、1.92%（绿），6%红色虚线，「= 通过」徽章', '示例图 37_1'],
          pending=['R值2.64%/1.92%为标准印刷值；按表B.3原始数据未取整计算为2.78%/1.98%（上轮复算，本轮未重读扫描表），结论不变'])


def p39(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    def draw(sz, v=None):
        frame(sl, [P('我科多系统项目清单与程序文件对照')], 3, ctx.page, '来源：GL047 5；LZJY-2-CX-38', 'ORANGE', corner=img('38_1'), mode=ctx.mode)
        ctx.L(images='38_1')
        lw = 6.4
        textbox(sl.shapes, X0, CT, lw, 0.3, [P('① 多系统项目清单', bold=True, color=C['NAVY'])], 16, pitch=1.15)
        heads = [[P(t)] for t in ['项目', '系统A', '系统B', '系统C', '适用方案', '上次比对日期', '结果']]
        rows = [[[P(n, bold=True)]] + [[P('【待填】', color=C['ORANGE'])] for _ in range(6)] for n in ['生化', '血细胞分析', '凝血', 'POCT血糖', '血气']]
        widths = [1.24, 0.86, 0.86, 0.86, 0.86, 0.86, 0.86]
        tot1, _, _ = native_table(ctx, sl, X0, CT + 0.4, widths, heads, rows, 14, [C['ORANGE']] * 7, limit=CB_L, mar=0.03)
        yl = CT + 0.4 + tot1 + 0.15
        yl += text(ctx, sl, X0, yl, lw, [P('适用方案：参比法（≤4个系统）/ 均值法（>4个）/ WS/T 407（需按CV定重复次数）', color=C['GRAY'])], 14) + GUT
        qb(ctx, sl, X0, yl, lw, [P('↻ 依据可补充：CNAS-CL02:2023、WS/T 885—2026')], 14, 'REG', None, quote=False, limit=CB_L)
        # 右：程序文件对照（= / ≠）
        rx = X0 + lw + 0.4; rw = FW - lw - 0.4
        textbox(sl.shapes, rx, CT, rw, 0.3, [P('② GL047第5条要求 ↔ 《比对管理程序》', bold=True, color=C['NAVY'])], 16, pitch=1.15)
        items = [('职责', '='), ('实施流程', '='), ('记录', '='), ('相关文件', '='),
                 ('样本类型与数量', '≠'), ('判断标准', '≠'), ('数据处理方法', '≠'), ('验证时机', '≠')]
        hd = [[P('GL047第5条要求')], [P('')], [P('LZJY-2-CX-38（第5/2版，2022-09-01实施）')]]
        body = [[[P(a)], [P(s)], [P('已有' if s == '=' else '未见（请主任确认）', color=C['TEXT'] if s == '=' else C['ORANGE'])]] for a, s in items]
        tot, _, _ = native_table(ctx, sl, rx, CT + 0.4, [1.45, 0.4, rw - 1.85], hd, body, 14, [C['NAVY'], C['SLATE'], C['ORANGE']], mid_col=1, limit=CB_R)
        y = CT + 0.4 + tot + 0.15
        text(ctx, sl, rx, y, rw, [P('“未见”项可能在专业组作业指导书中，请主任确认', color=C['GRAY'])], 14, limit=CB_R)
    sz = fit(ctx, sl, draw, [14], None)
    ctx.L(template='T6 表格页（变体：左清单表＋右对照表）', orig='新增页（合并你方案的第36页清单与第37页程序文件对照）', size='表格14pt',
          added=['左：多系统项目清单原生表格（生化/血细胞分析/凝血/POCT血糖/血气，全部【待填】）', '右：GL047第5条要求与LZJY-2-CX-38逐项对照（=/≠），措辞为清单而非"缺陷"', '底部「↻ 依据可补充」框', '角图 38_1'],
          pending=['全表待科室填写', '"≠"四项是否在专业组作业指导书中：请主任确认', '合并原因：原P15与原P27各需拆为两页以保住≥14pt字号，为守住≤40页，把两张新增"我科"页合并为一页'])


def p40(D, ctx):
    sl = D.new(); ctx.page = ctx.pg
    def draw(sz):
        picture(sl.shapes, img('40_1'), 0, 0, SW, SH, rounded=False, name='NEWIMG_HERO')
        textbox(sl.shapes, ML, Y_CHAP, 4, H_CHAP, [P(CHAPTERS[3])], 12, color='9FE3DE', bold=True, pitch=1.2, name='CHAPTER')
        textbox(sl.shapes, ML, Y_TITLE, 7, H_TITLE, [P('小结')], 28, color=WHITE, bold=True, pitch=1.15, name='TITLE')
        cards = [('什么时候比', '启用前／定期／要素变更'), ('怎么比', '≤4个系统用参比法，>4个用均值法，需按CV定重复次数时用WS/T 407'),
                 ('不过怎么办', '能修正就修正，不能修正就告知临床')]
        cw = (L7w - 2 * GUT) / 3
        ch = max(text_height_in([P(b)], cw - 2 * PAD, sz) for _, b in cards) + 0.45 + 2 * PAD
        for k, (a, b) in enumerate(cards):
            x = ML + k * (cw + GUT)
            gg = group(sl.shapes, 'CARD')
            rrect(gg.shapes, x, CT + 0.3, cw, ch, fill='22406A', line='3C6390')
            textbox(gg.shapes, x + PAD, CT + 0.3 + PAD, cw - 2 * PAD, 0.36, [P(a)], 18, color='9FE3DE', bold=True, pitch=1.1)
            textbox(gg.shapes, x + PAD, CT + 0.3 + PAD + 0.45, cw - 2 * PAD, ch - 0.45 - 2 * PAD, [P(b)], sz, color=WHITE, pitch=PITCH)
        ctx.chk(CT + 0.3 + ch, 5.2)
        textbox(sl.shapes, ML, 5.6, L7w, 0.8, [P('谢谢')], 40, color=WHITE, bold=True, pitch=1.1)
        footer(sl, ctx.page, dark=True)
    sz = fit(ctx, sl, draw, [18, 16, 14])
    ctx.L(template='T1 主视觉页（结束页）', orig='新增页', size=f'卡片{sz}pt', images='40_1',
          added=['三张小结卡（什么时候比／怎么比／不过怎么办）', '「谢谢」', '主视觉 40_1'])

# -*- coding: utf-8 -*-
"""第5轮修改（在第4轮44页版上操作）：
1) 每页左下角“第940医院检验科”换成院徽；删除左上角章节标签（为什么要比/怎么比/我科怎么做）；
2) 第14页：删除2012版全部内容，换为CNAS-CL02:2023相应内容（封面、前言节选、A001:2023 7.3.7.3/7.3.7.4原文）；
3) 第18、28页（两个分隔页）背景改为白色；
4) 第25页：补表A.1摘录（覆盖表B.2的全部单元格），橙框标出并用箭头连到表B.2；
5) 第44页：“怎么比”详细展开。其余页面不动。
用法：python3 v5_edits.py 输入44页.pptx 输出.pptx"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
from pptx.enum.shapes import MSO_CONNECTOR
from lib import *
from kit import *
from core import img, clear_slide
from pages_a import native_table, WHITE

HERE = os.path.dirname(os.path.abspath(__file__))
X0, FW = ML, SW - ML - MR
LOGO = img('logo_940')
COVER23 = os.path.join(HERE, '..', '插图', 'cl02_2023_cover.png')
LOGO_S = 0.34
LOGO_Y = 6.835


class _D:
    mode = 'clean'


def walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:
            yield from walk(sh.shapes)


def logo_and_chapter(prs):
    for sl in prs.slides:
        for sh in list(sl.shapes):
            if sh.name == 'CHAPTER':
                sh._element.getparent().remove(sh._element)
            elif sh.name == 'FOOTER' and sh.has_text_frame and sh.text_frame.text.strip() == '第940医院检验科':
                sh._element.getparent().remove(sh._element)
                p = sl.shapes.add_picture(LOGO, Emu(int(ML * EMU)), Emu(int(LOGO_Y * EMU)), Emu(int(LOGO_S * EMU)), Emu(int(LOGO_S * EMU)))
                p.name = 'LOGO'


def keep_footer(sl):
    """清空页面但保留页码与院徽。"""
    keep = [sh._element for sh in sl.shapes if sh.name in ('FOOTER', 'LOGO')]
    clear_slide(sl)
    for e in keep:
        sl.shapes._spTree.append(e)


# ---------------------------------------------------------------- 第14页
A001_733 = [
    P('应符合 ISO 15189，7.3.7.3 条款及下列要求：'),
    P('……'),
    P('3) 室间质量评价不可获得的检验（检查）项目，可参考 ', P('WS/T 415 通过与其他实验室比对', bold=True, color=C['ORANGE'])[0],
      '的方式确定检验结果的可接受性，并规定比对实验室的选择原则（如使用相同检测系统/检测方法的已获认可的实验室或其它同级别、高级别实验室）、比对样品数量、比对频次（宜参考 7.3.7.3 1）参加室间质量评价的频次要求）、判断标准等。'),
]
A001_734 = [
    P('应符合 ISO 15189，7.3.7.4 条款及下列要求：'),
    P('1) 实验室内部结果比对的程序文件应规定比对条件、样品类型及数量、比对方案、判断标准、频次及相关措施，',
      P('可参考 CNAS-GL047 以及相关国家/行业标准，如 WS/T 406、WS/T 407', bold=True, color=C['ORANGE'])[0], '。'),
    P('2) 应规定由多个人员进行的手工检验项目比对的方法和判断标准，例如：显微镜检查、培养结果判读、抑菌圈测量等，定期（至少每 6 个月 1 次，每次至少 5 份临床样品）进行检验人员的结果比对。'),
    P('3) 比对记录应由授权人员审核并签字，并至少保留 2 年。'),
]
PREFACE = [P('本准则等同采用ISO 15189:2022《医学实验室—质量和能力的要求》……'),
           P('本准则包含即时检验（POCT）的要求。'),
           P('本准则为第四版，取代CNAS-CL02:2012(第三版)。')]


def page14(sl, ctx):
    ctx.page = 14
    def draw(sz, v):
        clear_slide(sl)
        frame(sl, [P('《医学实验室质量和能力认可准则》CNAS-CL02：2023', color=C['RED'])], 1, 14, '来源：CNAS-CL02:2023；CNAS-CL02-A001:2023', 'GL',
              corner=img('14_1'), mode='clean')
        lw = {'a': 3.2, 'b': 3.0, 'c': 3.0}[v]
        ch = {'a': 1.8, 'b': 1.7, 'c': 1.7}[v]
        cw = ch * 910 / 1287
        p = picture(sl.shapes, COVER23, X0, CT, cw, ch, name='ORIGPIC')
        p.line.color.rgb = RGBColor.from_string(C['LGRAY']); p.line.width = Pt(0.75)
        text(ctx, sl, X0 + cw + 0.12, CT, lw - cw - 0.12, [P('2023-06-01'), P('发布'), P('2023-12-01'), P('实施'), P('代替2012版', color=C['ORANGE'], bold=True)], 14, limit=CT + ch, gap=2)
        y = CT + ch + GUT
        qb(ctx, sl, X0, y, lw, [P('前言（节选）', bold=True, color=C['NAVY'])] + PREFACE, sz, 'GL', '—— CNAS-CL02:2023 前言')
        rx = X0 + lw + GUT; rw = FW - lw - GUT
        w2 = (rw - GUT) * {'a': 0.5, 'b': 0.52, 'c': 0.47}.get(v, 0.47); w3 = rw - GUT - w2
        x3 = rx + w2 + GUT
        h2 = qb(ctx, sl, rx, CT, w2, [P('7.3.7.3 室间质量评价（节选）', bold=True, color=C['NAVY'])] + A001_733, sz, 'GL', '—— CNAS-CL02-A001:2023 7.3.7.3',
                tags=[('原5.6.3', C['ORANGE'])])
        text(ctx, sl, rx, CT + h2 + 0.12, w2, [P('注：CL02:2023第7.3.7.3、7.3.7.4条正文与ISO 15189:2022完全一致，受版权保护未公开【条文待核】；两框为CNAS应用要求CNAS-CL02-A001:2023原文。', color=C['GRAY'])], 12)
        qb(ctx, sl, x3, CT, w3, [P('7.3.7.4 检验结果可比性', bold=True, color=C['NAVY'])] + A001_734, sz, 'GL', '—— CNAS-CL02-A001:2023 7.3.7.4',
           tags=[('原5.6.4', C['ORANGE'])], limit=CB_R)
        ctx.L(images='14_1')
    sz = fit(ctx, sl, draw, [18, 17, 16, 15, 14], ('a', 'b', 'c'))
    return sz


# ---------------------------------------------------------------- 第18、28页：白底
RECOL = {'FFFFFF': C['NAVY'], '9FE3DE': C['TEAL'], 'C9D3DF': C['GRAY']}


def whiten(sl, new_img):
    for sh in list(sl.shapes):
        if sh.name == 'NEWIMG_HERO':
            el = sh._element
            p = sl.shapes.add_picture(new_img, 0, 0, Emu(int(SW * EMU)), Emu(int(SH * EMU)))
            p.name = 'NEWIMG_HERO'
            tree = sl.shapes._spTree
            tree.remove(p._element)
            el.addprevious(p._element)
            tree.remove(el)
    for sh in walk(sl.shapes):
        if sh.has_text_frame:
            for para in sh.text_frame.paragraphs:
                for r in para.runs:
                    rPr = r._r.find(qn('a:rPr'))
                    if rPr is None: continue
                    sf = rPr.find(qn('a:solidFill'))
                    if sf is not None and len(sf) and sf[0].get('val') in RECOL:
                        sf[0].set('val', RECOL[sf[0].get('val')])


# ---------------------------------------------------------------- 第25页：表A.1 → 表B.2
A1_ROWS = [  # (系统数, 次数, 1%..6%) —— 取自 WS/T 407 表A.1；"2/4/3%"按原版为5.19（OCR误作8.19）；2.67 照原表保留
    ('2', '2', '4.30', '8.60', '12.90', '17.20', '21.49', '25.79'),
    ('2', '3', '2.67', '4.53', '6.80', '9.07', '11.33', '13.60'),
    ('2', '4', '1.73', '3.46', '5.19', '6.92', '8.65', '10.38'),
    ('2', '5', '1.46', '2.92', '4.38', '5.83', '7.29', '8.75'),
    ('3', '1', '8.33', '16.66', '24.99', '33.32', '41.65', '49.98'),
]


def page25(sl, ctx):
    ctx.page = 25
    pics = [sh for sh in sl.shapes if sh.name == 'ORIGPIC']
    b2 = max(pics, key=lambda s: s.top)                     # 下方的表B.2 扫描图
    # 右栏现有元素：大数字卡、小注、示例图与说明
    big = [sh for sh in sl.shapes if sh.name == 'BIGNUM'][0]
    note = [sh for sh in sl.shapes if sh.has_text_frame and '2.67' in sh.text_frame.text][0]
    newimg = [sh for sh in sl.shapes if sh.name == 'NEWIMG'][0]
    capt = [sh for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.startswith('示例图')][0]
    rx = big.left / EMU; rw = big.width / EMU
    y = big.top / EMU + big.height / EMU + 0.15
    # 标题徽章
    t = '表A.1 临界值表（部分）· 橙框＝表B.2 全部数值'
    badge(sl.shapes, rx, y, t, C['ORANGE'], w=min(rw, badge_w(t))); y += 0.30 + 0.08
    heads = [[P('系统数')], [P('次数')]] + [[P(f'{c}%')] for c in range(1, 7)]
    body = [[[P(c)] for c in r] for r in A1_ROWS]
    body.append([[P('……')]] + [[P('')] for _ in range(7)])
    widths = [0.66, 0.5] + [(rw - 1.16) / 6] * 6
    tot, head_h, hh = native_table(ctx, sl, rx, y, widths, heads, body, 14, [C['TEAL']] * 8, limit=CB_R, mar=0.03, pitch=1.0)
    tb = [sh for sh in sl.shapes if sh.name == 'TABLE'][-1].table
    # 橙框：行1–4（2系统、2–5次）× 列2–5（1%–4%）＝表B.2 全部数值
    for i in range(1, 5):
        for j in range(2, 6):
            tcPr = tb.cell(i, j)._tc.get_or_add_tcPr()
            tc = tb.cell(i, j); tc.fill.solid(); tc.fill.fore_color.rgb = RGBColor.from_string('FDF1E8')
            want = {'a:lnL': j == 2, 'a:lnR': j == 5, 'a:lnT': i == 1, 'a:lnB': i == 4}
            for side in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
                for e in tcPr.findall(qn(side)): tcPr.remove(e)
            k = 0
            for side in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):          # 模式顺序：lnL, lnR, lnT, lnB, …, 填充
                if not want[side]: continue
                ln = etree.Element(qn(side)); ln.set('w', str(int(Pt(2.25)))); ln.set('cmpd', 'sng')
                sf = etree.SubElement(ln, qn('a:solidFill')); etree.SubElement(sf, qn('a:srgbClr')).set('val', C['ORANGE'])
                tcPr.insert(k, ln); k += 1
    ty0 = y + head_h; ty1 = ty0 + sum(hh[:4])
    ctx.chk(y + tot, CB_R)
    # 示例图与小注移到左栏表B.2下方
    ly = (b2.top + b2.height) / EMU + 0.15
    side = min(1.0, CB_L - ly)
    newimg.left, newimg.top, newimg.width, newimg.height = [Emu(int(v * EMU)) for v in (X0, ly, side, side)]
    tx = X0 + side + 0.15; tw = span(7) - side - 0.15
    capt.left, capt.top, capt.width = Emu(int(tx * EMU)), Emu(int(ly * EMU)), Emu(int(tw * EMU))
    note.left, note.top, note.width = Emu(int(tx * EMU)), Emu(int((ly + 0.3) * EMU)), Emu(int(tw * EMU))
    ctx.chk(ly + 0.3 + note.height / EMU, CB_L)
    # 表B.2 扫描图加橙色边框，箭头从表A.1橙框指向表B.2
    b2.line.color.rgb = RGBColor.from_string(C['ORANGE']); b2.line.width = Pt(2.25)
    bx1 = (b2.left + b2.width) / EMU; by = (b2.top + b2.height / 2) / EMU
    c = sl.shapes.add_connector(MSO_CONNECTOR.ELBOW, Emu(int(rx * EMU)), Emu(int(((ty0 + ty1) / 2) * EMU)), Emu(int((bx1 + 0.02) * EMU)), Emu(int(by * EMU)))
    c.line.color.rgb = RGBColor.from_string(C['ORANGE']); c.line.width = Pt(2.5)
    ln = c.line._get_or_add_ln()
    te = etree.SubElement(ln, qn('a:tailEnd')); te.set('type', 'triangle'); te.set('w', 'med'); te.set('len', 'med')
    c.name = 'ARROW'
    return (rx, ty0, ty1, bx1, by)


# ---------------------------------------------------------------- 第44页：小结（“怎么比”展开）
HOW = [
    ('选方案', '检测系统≤4个，用参比系统比对法；>4个，用均值法；需按不精密度确定样本浓度和重复检测次数时，参考WS/T 407。', 'GL047 7.1、7.2.3'),
    ('做准备', '人员熟悉检测系统；关键性能经验证；试剂和校准品不宜更换批号；同时做好室内质控。样本用患者样本（抗凝剂相同），覆盖临床适宜区间，重点关注医学决定水平，不少于5例。', 'GL047 6'),
    ('按WS/T 407定参数', '长期CV尽可能累计6个月；最大CV/最小CV<2倍；至少2个浓度水平，浓度取m总×(1±20%)；合并CV查表A.1定重复次数。', 'WS/T 407 6.3–6.6'),
    ('算偏差', '参比法：各系统与参比系统的偏差；均值法/WS/T 407：R=(Xmax−Xmin)/X̄×100%。', 'GL047 7.2；WS/T 407 6.8.4'),
    ('判结果', '参比法：5份中4份符合即通过（扩样后90%以上符合）；R≤分析质量要求即通过，要求按WS/T 407 6.7优选顺序确定（如CVI的1/3）。', 'GL047 7.2.1；WS/T 407 6.7'),
]


def page44(sl, ctx):
    ctx.page = 44
    import copy as _cp
    saved = [_cp.deepcopy(sh._element) for sh in sl.shapes if sh.name in ('FOOTER', 'LOGO')]
    def draw(sz, v):
        for e in saved:
            sl.shapes._spTree.append(_cp.deepcopy(e))
        picture(sl.shapes, img('40_1r'), 0, 0, SW, SH, rounded=False, name='NEWIMG_HERO')
        tree = sl.shapes._spTree
        hero = tree[-1]; tree.remove(hero); tree.insert(2, hero)          # 背景置底
        textbox(sl.shapes, ML, Y_TITLE, 4, H_TITLE, [P('小结')], 28, color=WHITE, bold=True, pitch=1.15, name='TITLE')
        top = CT
        wl, wm, wr = {'a': (2.5, 5.4, 2.0), 'b': (2.3, 5.8, 1.9), 'c': (2.0, 6.4, 1.75)}[v]
        xl = ML; xm = xl + wl + GUT; xr = xm + wm + GUT
        bottom = 6.08
        def card_box(x, w, head, paras):
            g = group(sl.shapes, 'CARD')
            rrect(g.shapes, x, top, w, bottom - top, fill='22406A', line='3C6390')
            textbox(g.shapes, x + PAD, top + PAD, w - 2 * PAD, 0.36, [P(head)], 18, color='9FE3DE', bold=True, pitch=1.1)
            th = text_height_in([dict(segs=p, size=sz) for p in paras], w - 2 * PAD, sz, 6) + 0.02
            textbox(g.shapes, x + PAD, top + PAD + 0.45, w - 2 * PAD, th, paras, sz, color=WHITE, gap=6)
            ctx.chk(top + PAD + 0.45 + th + PAD, bottom)
        card_box(xl, wl, '什么时候比', [P('启用前／定期／要素变更')])
        # “怎么比”：五步，每步一行标签 + 说明 + 依据
        paras = []
        for k, (h, t, c) in enumerate(HOW, 1):
            paras.append(P(P(f'{k} {h}：', bold=True, color='F3A266')[0], t, P(f'（{c}）', color='9FB7D3', size=12)[0]))
        card_box(xm, wm, '怎么比', paras)
        card_box(xr, wr, '不过怎么办', [P('能修正就修正，不能修正就告知临床')])
        textbox(sl.shapes, ML + LOGO_S + 0.25, 6.15, 3, 0.6, [P('谢谢')], 32, color=WHITE, bold=True, pitch=1.1)
    sz = fit(ctx, sl, draw, [18, 17, 16, 15, 14], ('a', 'b', 'c'))
    return sz


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    prs = Presentation(src)
    assert len(prs.slides) == 44
    ctx = Ctx(_D())
    S = list(prs.slides)
    logo_and_chapter(prs)
    sz14 = page14(S[13], ctx)
    whiten(S[17], img('407_hero_w'))
    whiten(S[27], img('18_1w'))
    page25(S[24], ctx)
    sz44 = page44(S[43], ctx)
    logo_and_chapter(prs)          # 第14、44页重建后再清一次章节标签/文字页脚
    prs.save(dst)
    print('p14', sz14, 'p44', sz44, 'over', ctx.notes)

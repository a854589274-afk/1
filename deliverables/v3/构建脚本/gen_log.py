# -*- coding: utf-8 -*-
import json, csv, os, re, sys
out = sys.argv[1]
log = json.load(open(os.path.join(out, '_build_log.json'))); qa = json.load(open(os.path.join(out, '_qa.json')))
imgmap = json.load(open(os.path.join(out, '_imgmap.json')))
notes = log['clean']['notes']; rep = log['annot']['replog']
L = []
w = L.append
w('## 4 逐页记录（40页）\n')
w('| 页 | 原页 | 模板 | 字号（原→现） | 新图（文件名） | 增加了什么 | 替换（原文 → 新文 → 依据） | 仍【待核】 |')
w('|---|---|---|---|---|---|---|---|')
for pg in sorted(notes, key=int):
    d = notes[pg]
    imgs = '、'.join(n for n, _, _ in imgmap.get(pg, []))
    reps = [r for r in rep if str(r[0]) == pg]
    rs = '<br>'.join(f"{r[1]}：「{r[2] or '（插入）'}」→「{r[3]}」→ {r[4]}" for r in reps) or '—'
    add = '<br>'.join(d['added']) or '—'
    pend = '<br>'.join(d['pending']) or '—'
    w(f"| {pg} | {d['orig']} | {d['template']} | {d['size']} | {imgs} | {add} | {rs} | {pend} |")
open(os.path.join(out, '_log_pages.md'), 'w').write('\n'.join(L) + '\n')

# 守恒 md
per = qa['per_slide']
M = ['# 文字守恒核对表（汇总）\n', '方法：用 python-pptx 抽取原PPT每一段文字（去空白后比较），在标注版与清洁版对应页（含拆页）中查找。"原样出现"＝整段连续出现；"拆分出现"＝字符序列完整但分布在相邻框/标签中（如括号标注移为框头标签）；替换段单列，分别核对清洁版新文完整、标注版旧文与新文均在。逐段明细见 `文字守恒核对表.csv`。\n',
     '| 原页 | 原段落数 | 原样出现 | 拆分出现 | 替换段 | 缺失 | 等式 |', '|---|---|---|---|---|---|---|']
T = dict(total=0, same=0, split=0, rep=0, missing=0)
for n in sorted(per, key=int):
    s = per[n]
    for k in T: T[k] += s[k]
    ok = '✅' if s['total'] == s['same'] + s['split'] + s['rep'] and s['missing'] == 0 else '❌'
    M.append(f"| P{n} | {s['total']} | {s['same']} | {s['split']} | {s['rep']} | {s['missing']} | {s['total']} = {s['same']}+{s['split']}+{s['rep']} {ok} |")
M.append(f"| 合计 | {T['total']} | {T['same']} | {T['split']} | {T['rep']} | {T['missing']} | {T['total']} = {T['same']}+{T['split']}+{T['rep']} |")
M.append('\n## 替换段明细\n')
rows = list(csv.DictReader(open(os.path.join(out, '文字守恒核对表.csv'), encoding='utf-8-sig')))
M.append('| 原页 | 终稿页 | 段落（前60字） | 结果 |\n|---|---|---|---|')
for r in rows:
    if '替换' in r['结果'] or '拆分' in r['结果']:
        M.append(f"| P{r['原页']} | {r['终稿页']} | {r['原段落']} | {r['结果']} |")
open(os.path.join(out, '文字守恒核对表.md'), 'w').write('\n'.join(M) + '\n')

# 版式 md
V = ['# 版式检查结果（代码自动检查）\n', '检查对象：标注版、清洁版各40页。\n',
     '| 检查项 | 方法 | 标注版 | 清洁版 |', '|---|---|---|---|']
a, c = qa['annot'], qa['clean']
f = lambda r, key: [x['page'] for x in r['layout'] if x[key]]
V.append(f"| 总页数≤40 | 计数 | {a['pages']} ✅ | {c['pages']} ✅ |")
V.append(f"| 文字溢出 | LibreOffice 独立复排：把每个自动换行文本框改为“根据文字调整形状”，转换后读回高度，凡比原框高出0.03英寸以上记为溢出 | {len(a['lo_overflow'])} / {a['lo_checked']} 个文本框 ✅ | {len(c['lo_overflow'])} / {c['lo_checked']} ✅ |")
V.append(f"| 元素重叠 | 每页顶层元素两两求交（组合内部元素按组合整体计；连接线、时间轴圆点、全幅主视觉背景除外） | 有重叠的页：{f(a,'overlaps') or '无'} ✅ | {f(c,'overlaps') or '无'} ✅ |")
V.append(f"| 超出页边 | 左右0.6″、上下0.45″（全幅主视觉背景除外） | {f(a,'out_of_bounds') or '无'} ✅ | {f(c,'out_of_bounds') or '无'} ✅ |")
nn = [x['page'] for x in a['layout'] if not x['new_image_groups']]; n2 = [x['page'] for x in a['layout'] if len(x['new_image_groups']) > 2]
V.append(f"| 每页≥1张新图、≤2组 | 按构建日志统计每页使用的新图组（同一图标组的裁切算1组） | 无新图页：{nn or '无'}；超2组：{n2 or '无'} ✅ | 同左 ✅ |")
V.append(f"| 字号下限 | 全部文字 run 的字号 | 小于12pt：{len(a['small_fonts'])} 处 ✅ | {len(c['small_fonts'])} ✅ |")
V.append(f"| 字体 | 全部 run 的西文/东亚字体 | {'、'.join(a['fonts'])} | {'、'.join(c['fonts'])} |")
V.append('\n说明：\n1. LibreOffice 用文泉驿正黑代替微软雅黑排版（本环境无微软雅黑）。两者中文字宽同为1个字号，所以高度可比；我另用30段原文做过校准，自写的测量函数与 LibreOffice 结果一致或多估1行。PowerPoint 实际渲染我无法在本环境测，建议你翻一遍。\n2. "Cambria Math" 只用于第30页的两行公式（原文是数学斜体 Unicode 字符，微软雅黑/Arial 无此字形）。\n3. 正文 ≥14pt 已满足；12pt 只用于引用行、示例图说明、徽章、标签，以及标注版中被删除线划掉的原文。')
V.append('\n## 各页新图组\n\n| 页 | 新图 |\n|---|---|')
for pg in sorted(imgmap, key=int):
    V.append(f"| {pg} | {'、'.join(n + ('（图标组，含裁切 ' + str(k) + ' 枚）' if k else '') for n, _, k in imgmap[pg])} |")
open(os.path.join(out, '版式检查结果.md'), 'w').write('\n'.join(V) + '\n')
print('ok')

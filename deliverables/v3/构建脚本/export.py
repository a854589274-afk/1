# -*- coding: utf-8 -*-
"""导出：按“页码_序号”命名插图；生成修改日志、文字守恒核对表（md）、版式检查结果。"""
import json, os, re, shutil, csv, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
out = sys.argv[1]
log = json.load(open(os.path.join(out, '_build_log.json'))); qa = json.load(open(os.path.join(out, '_qa.json')))
notes = log['annot']['notes']; replog = log['annot']['replog']
src = os.path.join(ROOT, '插图'); dst = os.path.join(out, '插图_按页码'); 
if os.path.exists(dst): shutil.rmtree(dst)
os.makedirs(dst)
imgmap = {}
for pg in sorted(notes, key=int):
    seen = []
    for im in notes[pg]['images']:
        base = re.sub(r'-\d+$', '', im)
        if base not in seen: seen.append(base)
    for k, base in enumerate(seen, 1):
        name = f'{int(pg):02d}_{k}'
        shutil.copy(os.path.join(src, base + '.png'), os.path.join(dst, name + '.png'))
        crops = sorted(f for f in os.listdir(src) if re.fullmatch(re.escape(base) + r'-\d+\.png', f))
        for c in crops:
            i = c[len(base) + 1:-4]
            shutil.copy(os.path.join(src, c), os.path.join(dst, f'{name}-{i}.png'))
        imgmap.setdefault(pg, []).append((name, base, len(crops)))
json.dump(imgmap, open(os.path.join(out, '_imgmap.json'), 'w'), ensure_ascii=False, indent=1)
# 生图提示词清单
sys.path.insert(0, HERE)
import scenes
PREFIX = ('Formal premium 3D studio render, front-facing straight-on orthographic view, perfectly level horizon, symmetrical centered composition, subject upright and not tilted, no isometric or diagonal angle, soft even studio lighting, matte ceramic and frosted glass materials, refined color grading, palette deep navy #1F3A5F and teal #148F8A with restrained warm orange #E8833A accents, clean seamless white-to-pale-gray background (deep navy background for hero slides), generous whitespace, serious medical-institution tone, uncluttered, absolutely no text, no letters, no numbers, no logos, no brand names, no flags, no emblems, no badges.')
with open(os.path.join(out, '插图提示词清单.md'), 'w') as f:
    f.write('# 插图提示词清单（可用于以AI生图替换；替换时保持文件名与画幅不变）\n\n')
    f.write('本次插图为代码绘制（SVG→PNG），本环境没有可调用的AI生图接口。下列提示词按你的统一前缀拼好，可直接投给生图模型；生成后按同名覆盖 插图_按页码/ 下的文件，再运行构建脚本即可。\n\n')
    f.write('| 文件 | 画幅 | 提示词主体（另加统一前缀） |\n|---|---|---|\n')
    for pg in sorted(imgmap, key=int):
        for name, base, nc in imgmap[pg]:
            r = scenes.REG.get(base)
            if not r: continue
            ratio, _, tr, prompt, n, grid = r
            if ratio == 'icons':
                g = grid or (n, 1)
                pre = f'a set of {n} icons in {"one straight row" if g[1]==1 else f"an exact {g[1]}x{g[0]} grid"}, identical size, same baseline, evenly spaced, front view, identical lighting, transparent background; '
                f.write(f'| {name}.png（裁切为 {name}-1…{n}） | 图标组 | {pre}{prompt} |\n')
            else:
                f.write(f'| {name}.png | {ratio} | {prompt} |\n')
    f.write(f'\n统一风格前缀：\n\n> {PREFIX}\n')
print('images', sum(len(v) for v in imgmap.values()))

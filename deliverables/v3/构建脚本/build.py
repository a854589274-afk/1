# -*- coding: utf-8 -*-
"""用法：python3 build.py 原PPT.pptx 输出目录   —— 同一份脚本生成标注版与清洁版。"""
import sys, os, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from core import Deck
from kit import Ctx

def pages():
    mods = [importlib.import_module(m) for m in ('pages_a', 'pages_b', 'pages_c') if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), m + '.py'))]
    fns = []
    for m in mods:
        fns += sorted([getattr(m, n) for n in dir(m) if n.startswith('p') and n[1:3].isdigit()], key=lambda f: f.__name__)
    return fns

def build(src, out, mode):
    lib.REPLOG.clear()
    D = Deck(src, mode)
    ctx = Ctx(D)
    for i, fn in enumerate(pages(), 1):
        ctx.pg = i
        fn(D, ctx)
    D.finish(out)
    return ctx

if __name__ == '__main__':
    src, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    res = {}
    for mode, name in (('annot', '标注版'), ('clean', '清洁版')):
        ctx = build(src, os.path.join(outdir, f'定量检验程序结果可比性验证_{name}.pptx'), mode)
        res[mode] = dict(notes=ctx.notes, replog=list(lib.REPLOG))
    json.dump(res, open(os.path.join(outdir, '_build_log.json'), 'w'), ensure_ascii=False, indent=1, default=str)
    print('pages', len(res['clean']['notes']))

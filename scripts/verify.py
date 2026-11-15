#!/usr/bin/env python3
"""ビルド結果(public)の検証。使い方: python3 -I scripts/verify.py <publicのパス> [baseurlのパス 例: /jair-mjir]
内部リンク・画像・CSS/JSが存在するか、content/ の全ページが出力されたか、未展開のテンプレート記法が残っていないかを確認する。"""
import re, sys, json
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent.parent
SITE = Path(sys.argv[1]).expanduser()
BASE = sys.argv[2].rstrip("/") if len(sys.argv) > 2 else ""
sources = sorted((HERE / "content/posts").glob("*.md")) + sorted((HERE / "content/pages").iterdir())
htmls = list(SITE.rglob("*.html"))
print(f"HTML {len(htmls)}  投稿ソース {len(list((HERE/'content/posts').glob('*.md')))}  ページソース {len(list((HERE/'content/pages').iterdir()))}")

miss = []
for f in sources:
    m = re.search(r'^url: (".*")\s*$', f.read_text(encoding="utf-8"), re.M)
    if not m:
        miss.append(f.name)
        continue
    url = json.loads(m.group(1))
    p = unquote(url).lstrip("/")
    cand = SITE / p
    if not (cand.is_file() or (cand / "index.html").is_file()):
        miss.append(url)
print("出力されていないページ:", len(miss), miss[:8])

bad, total = {}, 0
for f in htmls:
    h = f.read_text(encoding="utf-8", errors="replace")
    refs = []
    for m in re.finditer(r'(href|src|srcset)="([^"]*)"', h):
        if m.group(1) == "srcset":
            refs += [x.strip().split(" ")[0] for x in m.group(2).split(",") if x.strip()]
        else:
            refs.append(m.group(2))
    for u in refs:
        u = re.split(r"[#?]", u)[0]
        if not u or not u.startswith("/") or u.startswith("//"):
            continue
        total += 1
        if BASE and (u == BASE or u.startswith(BASE + "/")):
            u = u[len(BASE):] or "/"
        elif BASE:
            bad.setdefault(u, []).append(str(f.relative_to(SITE)))  # baseURL が付いていない
            continue
        p = SITE / unquote(u).lstrip("/")
        if not (p.is_file() or (p / "index.html").is_file()):
            bad.setdefault(u, []).append(str(f.relative_to(SITE)))
print(f"内部リンク/画像/CSS/JS {total}件 / 存在しない {len(bad)}種類")
for u, fs in sorted(bad.items())[:20]:
    print("  ", unquote(u), "←", unquote(fs[0]), f"(+{len(fs)-1})" if len(fs) > 1 else "")
left = [str(f.relative_to(SITE)) for f in htmls if re.search(r"so012964|\{\{|\{%|ZgotmplZ", f.read_text(encoding="utf-8", errors="replace"))]
print("参考サイトのURL/テンプレート記法の残り:", left[:5], len(left))

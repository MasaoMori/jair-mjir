#!/usr/bin/env python3
"""Jekyll版(jekyll-site)のコンテンツ・静的ファイルを Hugo 用に変換して取り込む。

使い方: python3 -I scripts/convert_from_jekyll.py <jekyll-siteのパス>   (jair-mjir直下で実行)

- _posts/*.md  -> content/posts/   (permalink -> url、date をISO形式、categories を配列に)
- pages/*      -> content/pages/   (permalink -> url)
- _data/*.yml  -> data/
- assets/, wp-content/ -> static/
- 本文中の {{ '/path' | relative_url }} は '/path' に直す(baseURL は表示側の partial で付ける)
- 本文中の {% include news-filter.html %} 等は Hugo のショートコードに置き換える
注意: 取り込み済みのサイトで再実行すると、content/ と data/ を作り直すので、その後に追加・編集した内容は消える。
そのため content/ がすでにある場合は --force を付けないと実行しない。
"""
import json, re, shutil, sys
from pathlib import Path

SRC = Path([a for a in sys.argv[1:] if not a.startswith("--")][0]).expanduser().resolve()
DST = Path(__file__).resolve().parent.parent

REL = re.compile(r"\{\{\s*'([^']*)'\s*\|\s*relative_url\s*\}\}")
INC_FILTER = re.compile(r"\{%\s*include\s+news-filter\.html\s*%\}")
INC_ROWS = re.compile(r"\{%\s*include\s+news-rows\.html\s+posts=site\.posts\s*%\}")


def split_fm(text):
    m = re.match(r"---\n(.*?)\n---\n?(.*)\Z", text, re.S)
    if not m:
        raise ValueError("front matter がありません")
    return m.group(1), m.group(2)


def parse_fm(block):
    out = {}
    for line in block.split("\n"):
        if not line.strip():
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        out[k.strip()] = json.loads(v) if v.startswith('"') else v
    return out


def y(v):
    return json.dumps(v, ensure_ascii=False)


def fix_markdown(body):
    """kramdown と goldmark(Hugo) の解釈の違いを吸収する(.md のみ)。
    - **太字** / ***太字+斜体*** / ~~取り消し線~~ : CommonMark では句読点・リンクの隣で効かず「**」が表示されるので、同じ行内なら HTML に直す。
    - 文章の直後の「-----」 : goldmark では直前の行が見出し(h2)になってしまうので、前に空行を入れて区切り線にする。
    コードブロック(```)の中は触らない。"""
    out, fence = [], False
    for line in body.split("\n"):
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
        elif not fence:
            if re.fullmatch(r"-{3,}\s*", line) and out and out[-1].strip():
                out.append("")
            line = re.sub(r"(?<!\\)\*\*\*(.+?)(?<!\\)\*\*\*", r"<strong><em>\1</em></strong>", line)
            line = re.sub(r"(?<!\\)\*\*(.+?)(?<!\\)\*\*", r"<strong>\1</strong>", line)
            line = re.sub(r"~~(.+?)~~", r"<del>\1</del>", line)
        out.append(line)
    return "\n".join(out)


def convert_body(body, is_md=False):
    if is_md:
        body = fix_markdown(body)
    body = REL.sub(lambda m: m.group(1), body)
    body = INC_FILTER.sub("{{< news-filter >}}", body)
    body = INC_ROWS.sub("{{< news-rows >}}", body)
    left = re.search(r".{0,40}(\{\{(?!<)|\{%).{0,40}", body)
    if left:
        raise ValueError("未変換の Liquid が残っています: " + left.group(0))
    return body


def convert(src_file, dst_file, is_post):
    fm_text, body = split_fm(src_file.read_text(encoding="utf-8"))
    fm = parse_fm(fm_text)
    lines = ["---"]
    lines.append(f"title: {y(fm.pop('title'))}")
    if is_post:
        d = fm.pop("date")  # 2012-08-13 17:43:59 +0900
        m = re.fullmatch(r"(\d{4}-\d\d-\d\d) (\d\d:\d\d:\d\d) ([+-])(\d\d)(\d\d)", d)
        lines.append(f"date: {m.group(1)}T{m.group(2)}{m.group(3)}{m.group(4)}:{m.group(5)}")
    lines.append(f"url: {y(fm.pop('permalink'))}")
    # layout は native(手書きHTMLページ)だけ残す。post / page は置き場所(posts / pages)で自動的に決まる。
    layout = fm.pop("layout")
    if layout == "native":
        lines.append(f"layout: {y(layout)}")
    # 投稿の nav_section は "news" 固定でテンプレート側が決めるので書かない。
    if is_post:
        fm.pop("nav_section", None)
    if "categories" in fm:
        cats = fm.pop("categories")
        lines.append(f"categories: {y(json.loads(cats) if isinstance(cats, str) else cats)}")
    for k, v in fm.items():
        lines.append(f"{k}: {y(v)}")
    lines.append("---")
    dst_file.write_text("\n".join(lines) + "\n" + convert_body(body, src_file.suffix == ".md"), encoding="utf-8")


def main():
    if (DST / "content").exists() and "--force" not in sys.argv:
        sys.exit("content/ がすでにあります。再実行すると追加・編集した内容が消えるので中止しました(上書きするなら --force)。")
    for d in ("content", "data"):
        shutil.rmtree(DST / d, ignore_errors=True)
    (DST / "content/posts").mkdir(parents=True)
    (DST / "content/pages").mkdir(parents=True)
    n = {"posts": 0, "pages": 0}
    for f in sorted((SRC / "_posts").glob("*.md")):
        convert(f, DST / "content/posts" / f.name, True)
        n["posts"] += 1
    for f in sorted((SRC / "pages").iterdir()):
        if f.name.startswith("."):
            continue
        convert(f, DST / "content/pages" / f.name, False)
        n["pages"] += 1
    shutil.copytree(SRC / "_data", DST / "data")
    for d in ("assets", "wp-content"):
        shutil.copytree(SRC / d, DST / "static" / d, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".DS_Store"))
    print("変換:", n)


main()

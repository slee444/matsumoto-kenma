#!/usr/bin/env python3
"""Add TOC and related articles to all 5 column pages."""

import re
from pathlib import Path

BASE = Path("/Users/slee/slee_workspace/matsumoto-kenma/column")

# All articles data (ordered: newest first)
ALL_ARTICLES = [
    {
        "slug": "metal-machining",
        "date": "2026.07.22",
        "category": "加工基礎知識",
        "title": "金属加工とは？種類・方法・素材の選び方を神奈川県川崎市の職人が解説",
    },
    {
        "slug": "flexible-polishing",
        "date": "2026.07.20",
        "category": "仕上げ技術",
        "title": "フレキ研磨とは？特徴・用途・他の研磨との違いを神奈川県川崎市の職人が解説",
    },
    {
        "slug": "hairline-finish",
        "date": "2026.07.20",
        "category": "仕上げ技術",
        "title": "ヘアライン仕上げとは？特徴・工程・バフ研磨との違いを神奈川県川崎市の職人が解説",
    },
    {
        "slug": "belt-polishing",
        "date": "2026.07.20",
        "category": "仕上げ技術",
        "title": "ベルト研磨とは？番手・工程・バフ研磨との違いを神奈川県川崎市の職人が解説",
    },
    {
        "slug": "buff-polishing-ra-value",
        "date": "2026.07.20",
        "category": "仕上げ技術",
        "title": "バフ研磨とは？種類・工程・Ra値の見方を神奈川県川崎市の職人が解説",
    },
]

# TOC items per article
TOC_ITEMS = {
    "belt-polishing": [
        ("what-is", "ベルト研磨とは"),
        ("grit", "研磨ベルトの番手と使い分け"),
        ("process", "ベルト研磨の工程"),
        ("ra-value", "Ra値との関係"),
        ("vs-buff", "バフ研磨との違いと使い分け"),
        ("materials", "ベルト研磨が適した素材と用途"),
        ("pros-cons", "ベルト研磨のメリット・デメリット"),
        ("about-us", "松本研磨工業のベルト研磨について"),
    ],
    "buff-polishing-ra-value": [
        ("what-is", "バフ研磨とは"),
        ("buff-types", "バフの種類と使い分け"),
        ("compound", "研磨剤（コンパウンド）の種類"),
        ("process", "バフ研磨の工程"),
        ("ra-value", "Ra値とは何か——仕上がりの「粗さ」を数値で見る"),
        ("materials", "バフ研磨が適した素材"),
        ("pros-cons", "バフ研磨のメリット・デメリット"),
        ("about-us", "松本研磨工業のバフ研磨について"),
    ],
    "hairline-finish": [
        ("what-is", "ヘアライン仕上げとは"),
        ("features", "ヘアライン仕上げの特徴"),
        ("process", "ヘアライン仕上げの工程"),
        ("grit", "番手と仕上がりの目安"),
        ("materials", "ヘアライン仕上げが適した素材"),
        ("vs-others", "バフ研磨・ベルト研磨との違いと使い分け"),
        ("pros-cons", "ヘアライン仕上げのメリット・デメリット"),
        ("about-us", "松本研磨工業のヘアライン仕上げについて"),
    ],
    "flexible-polishing": [
        ("what-is", "フレキ研磨とは"),
        ("tools", "フレキ研磨で使う主な工具"),
        ("process", "フレキ研磨の工程"),
        ("materials", "フレキ研磨が適した形状・素材"),
        ("vs-others", "バフ研磨・ベルト研磨との違いと使い分け"),
        ("pros-cons", "フレキ研磨のメリット・デメリット"),
        ("about-us", "松本研磨工業のフレキ研磨について"),
    ],
    "metal-machining": [
        ("what-is", "金属加工とは"),
        ("categories", "金属加工の5つの分類"),
        ("materials", "加工方法と素材の選び方"),
        ("surface-treatment", "表面処理としての研磨加工の重要性"),
        ("summary", "まとめ"),
    ],
}

# H2 text to ID mapping per article
H2_IDS = {
    "belt-polishing": {
        "ベルト研磨とは": "what-is",
        "研磨ベルトの番手と使い分け": "grit",
        "ベルト研磨の工程": "process",
        "Ra値との関係": "ra-value",
        "バフ研磨との違いと使い分け": "vs-buff",
        "ベルト研磨が適した素材と用途": "materials",
        "ベルト研磨のメリット・デメリット": "pros-cons",
        "松本研磨工業のベルト研磨について": "about-us",
    },
    "buff-polishing-ra-value": {
        "バフ研磨とは": "what-is",
        "バフの種類と使い分け": "buff-types",
        "研磨剤（コンパウンド）の種類": "compound",
        "バフ研磨の工程": "process",
        "Ra値とは何か——仕上がりの「粗さ」を数値で見る": "ra-value",
        "バフ研磨が適した素材": "materials",
        "バフ研磨のメリット・デメリット": "pros-cons",
        "松本研磨工業のバフ研磨について": "about-us",
    },
    "hairline-finish": {
        "ヘアライン仕上げとは": "what-is",
        "ヘアライン仕上げの特徴": "features",
        "ヘアライン仕上げの工程": "process",
        "番手と仕上がりの目安": "grit",
        "ヘアライン仕上げが適した素材": "materials",
        "バフ研磨・ベルト研磨との違いと使い分け": "vs-others",
        "ヘアライン仕上げのメリット・デメリット": "pros-cons",
        "松本研磨工業のヘアライン仕上げについて": "about-us",
    },
    "flexible-polishing": {
        "フレキ研磨とは": "what-is",
        "フレキ研磨で使う主な工具": "tools",
        "フレキ研磨の工程": "process",
        "フレキ研磨が適した形状・素材": "materials",
        "バフ研磨・ベルト研磨との違いと使い分け": "vs-others",
        "フレキ研磨のメリット・デメリット": "pros-cons",
        "松本研磨工業のフレキ研磨について": "about-us",
    },
    "metal-machining": {
        "金属加工とは": "what-is",
        "金属加工の5つの分類": "categories",
        "加工方法と素材の選び方": "materials",
        "表面処理としての研磨加工の重要性": "surface-treatment",
        "まとめ": "summary",
    },
}


def build_toc(slug):
    items = TOC_ITEMS[slug]
    li_items = "\n".join(
        f'    <li><a href="#{anchor}" class="hover:underline underline-offset-2">{text}</a></li>'
        for anchor, text in items
    )
    return f"""<nav aria-label="目次" class="bg-paper-2 border-l-[3px] border-accent px-5 py-4 mb-2">
  <p class="font-mono text-[10px] tracking-[.2em] text-muted mb-3">目次</p>
  <ol class="list-decimal pl-4 space-y-1.5 font-serif text-[14px] leading-[1.7] text-accent-ink marker:text-muted marker:font-mono marker:text-[11px]">
{li_items}
  </ol>
</nav>"""


def build_related(current_slug):
    related = [a for a in ALL_ARTICLES if a["slug"] != current_slug]
    items = []
    for a in related:
        href = f"../{a['slug']}/"
        item = f"""      <a href="{href}" class="block border-b border-line-light py-4 pl-0 hover:pl-2 transition-all group">
        <div class="font-mono text-[10px] tracking-[.16em] text-muted mb-1">{a['date']}　{a['category']}</div>
        <p class="font-serif text-[14px] font-medium leading-[1.6] group-hover:text-accent transition-colors">{a['title']}</p>
      </a>"""
        items.append(item)
    items_html = "\n".join(items)
    return f"""<aside class="border-t border-line-light pt-10 pb-2">
  <div class="wrap">
    <p class="font-mono text-[10px] tracking-[.2em] text-muted mb-4">関連記事</p>
    <div class="border-t border-line-light">
{items_html}
    </div>
  </div>
</aside>"""


def process_file(slug):
    path = BASE / slug / "index.html"
    content = path.read_text(encoding="utf-8")

    # 1. Add IDs to H2 tags
    h2_map = H2_IDS[slug]
    for text, id_ in h2_map.items():
        # Match <h2>text</h2> (no existing id)
        old = f'<h2>{text}</h2>'
        new = f'<h2 id="{id_}">{text}</h2>'
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"  WARNING: H2 not found for [{slug}]: {text!r}")

    # 2. Insert TOC: after first <p>...</p> inside <article>, before first <h2>
    # Find the first <p> after <article ...>
    article_match = re.search(r'<article[^>]*>', content)
    if not article_match:
        print(f"  ERROR: <article> not found in {slug}")
        return

    article_start = article_match.end()
    # Find first <p>...</p> after <article>
    first_p_match = re.search(r'<p>[^<]*(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*</p>', content[article_start:])
    if not first_p_match:
        print(f"  ERROR: first <p> not found after <article> in {slug}")
        return

    insert_pos = article_start + first_p_match.end()
    toc_html = "\n\n" + build_toc(slug) + "\n"
    content = content[:insert_pos] + toc_html + content[insert_pos:]

    # 3. Insert related articles before <div class="border-t border-line-light py-8">
    related_html = build_related(slug) + "\n\n"
    target = '<div class="border-t border-line-light py-8">'
    if target in content:
        content = content.replace(target, related_html + target, 1)
    else:
        print(f"  ERROR: insertion point not found in {slug}")
        return

    path.write_text(content, encoding="utf-8")
    print(f"  OK: {slug}")


slugs = ["belt-polishing", "buff-polishing-ra-value", "hairline-finish", "flexible-polishing", "metal-machining"]

for slug in slugs:
    print(f"Processing {slug}...")
    process_file(slug)

print("Done.")

#!/usr/bin/env python3
"""
Sync the 'コラム' preview section on the top page (index.html) with the
3 newest articles in column/index.html.

column/index.html already lists articles newest-first, so this script
just parses the first 3 <a class="article-row"> blocks from it and
rewrites the #column-preview section in index.html to match.

Run this after adding a new column article and updating column/index.html.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
COLUMN_INDEX = BASE / "column" / "index.html"
TOP_INDEX = BASE / "index.html"

ARTICLE_RE = re.compile(
    r'<a href="([^"]+)/" class="article-row[^"]*"[^>]*>\s*'
    r'<div class="font-mono[^"]*">([^<]+)</div>\s*'
    r'<p class="article-title[^"]*"[^>]*>([^<]+)</p>\s*'
    r'</a>'
)

column_html = COLUMN_INDEX.read_text(encoding="utf-8")
articles = ARTICLE_RE.findall(column_html)
if len(articles) < 3:
    raise SystemExit(f"expected >=3 articles, found {len(articles)}")

newest_three = articles[:3]

cards = []
for slug, date_category, title in newest_three:
    cards.append(
        '      <a href="column/{slug}/" class="group border-t-2 border-ink/15 pt-4 hover:border-accent transition-colors">\n'
        '        <div class="font-mono text-[10px] tracking-[.16em] text-muted mb-2">{date_category}</div>\n'
        '        <p class="font-serif text-[14px] font-medium leading-[1.6] group-hover:text-accent transition-colors">{title}</p>\n'
        '      </a>'.format(slug=slug, date_category=date_category, title=title)
    )
new_grid_inner = "\n".join(cards)

top_html = TOP_INDEX.read_text(encoding="utf-8")

section_re = re.compile(
    r'(<div class="grid grid-cols-1 sm:grid-cols-3 gap-5 md:gap-6">\n)'
    r'(.*?)'
    r'(\n    </div>\n  </div>\n</section>\n\n<!-- ===== FAQ ===== -->)',
    re.DOTALL
)

new_top_html, n = section_re.subn(
    lambda m: m.group(1) + new_grid_inner + m.group(3), top_html
)
if n != 1:
    raise SystemExit(f"expected 1 replacement in index.html, got {n}")

TOP_INDEX.write_text(new_top_html, encoding="utf-8")
print("Updated index.html column preview with:")
for slug, date_category, title in newest_three:
    print(f"  - {date_category}  {title}")

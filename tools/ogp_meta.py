"""OGP画像まわりのmetaタグを整える。

- /web-ai/ 配下（マツケンスタジオ）… images/ogp-studio.jpg
- それ以外（松本研磨工業）………… images/ogp.jpg
画像は tools/ogp-source.html を Playwright で 1200x630・2倍 で書き出して作る。

使い方: python3 tools/ogp_meta.py   （全ページに反映。何度実行しても同じ結果）
"""
import re, pathlib

BASE = 'https://matsumoto-kenma.co.jp'
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = {
    'kenma':  {'img': f'{BASE}/images/ogp.jpg',        'name': '株式会社松本研磨工業',
               'alt': '株式会社松本研磨工業｜神奈川県川崎市の金属研磨'},
    'studio': {'img': f'{BASE}/images/ogp-studio.jpg', 'name': 'マツケンスタジオ by 松本研磨工業',
               'alt': 'マツケンスタジオ by 松本研磨工業｜Web集客・AI活用支援'},
}

def _meta(attr, key, val):
    return f'<meta {attr}="{key}" content="{val}">'

def apply(html, site):
    s = SITES[site]
    # 既存の画像系タグ・site_name を消してから入れ直す
    html = re.sub(r'\n?[ \t]*<meta (?:property="og:(?:image[^"]*|site_name)"|name="twitter:(?:card|image[^"]*|title|description)")[^>]*>', '', html)
    get = lambda k: (re.search(rf'<meta property="og:{k}" content="([^"]*)">', html) or [None, ''])[1]
    title, desc = get('title'), get('description')
    if not title:
        return html
    tags = [
        _meta('property', 'og:site_name', s['name']),
        _meta('property', 'og:image', s['img']),
        _meta('property', 'og:image:width', '1200'),
        _meta('property', 'og:image:height', '630'),
        _meta('property', 'og:image:alt', s['alt']),
        _meta('name', 'twitter:card', 'summary_large_image'),
        _meta('name', 'twitter:title', title),
        _meta('name', 'twitter:description', desc),
        _meta('name', 'twitter:image', s['img']),
    ]
    anchor = re.search(r'<meta property="og:(?:locale|url)" content="[^"]*">', html)
    return html[:anchor.end()] + ''.join('\n' + t for t in tags) + html[anchor.end():]

def site_of(path):
    return 'studio' if 'web-ai' in path.relative_to(ROOT).parts else 'kenma'

if __name__ == '__main__':
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT).parts
        if rel[0] in ('node_modules', 'tools', 'skills', 'input', 'output', 'agents', 'memory'):
            continue
        src = p.read_text(encoding='utf-8')
        out = apply(src, site_of(p))
        if out != src:
            p.write_text(out, encoding='utf-8'); n += 1
    print(f'updated {n} files')

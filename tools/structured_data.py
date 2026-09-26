"""全ページの構造化データ（JSON-LD）を整える。

- 会社（LocalBusiness）・サイト（WebSite）・マツケンスタジオを @id でつなぎ、全ページに入れる
- ページの種類に合わせて WebPage / AboutPage / ContactPage / CollectionPage を入れる
- 研磨技術とWeb集客のサービスページには Service を入れる
- 画面に「よくある質問」があるのに FAQPage がないページには、画面の内容から作る
- コラム記事（BlogPosting）の著者・発行元を会社の @id につなぐ

このスクリプトが入れる部分は data-sd="managed" の付いた <script> にまとめ、何度実行しても同じ結果になる。
使い方: python3 tools/structured_data.py
"""
import re, json, html as H, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://matsumoto-kenma.co.jp'
ORG_ID, SITE_ID, STUDIO_ID = f'{BASE}/#organization', f'{BASE}/#website', f'{BASE}/web-ai/#studio'
SKIP = ('node_modules', 'tools', 'skills', 'input', 'output', 'agents', 'memory')

ORG = {
    '@type': 'LocalBusiness',
    '@id': ORG_ID,
    'name': '株式会社松本研磨工業',
    'alternateName': ['松本研磨工業', '松本研磨'],
    'url': f'{BASE}/',
    'logo': {'@type': 'ImageObject', 'url': f'{BASE}/images/logo.png', 'width': 512, 'height': 512},
    'image': f'{BASE}/images/ogp.jpg',
    'description': '神奈川県川崎市川崎区の金属研磨工場。1967年創業。ステンレス・アルミ・真鍮・鉄などのバフ研磨（鏡面仕上げ）、ベルト研磨、ヘアライン仕上げ、フレキ研磨を、試作の1個から小量産まで手作業で請け負っています。図面がなくても、現物や写真からお見積りできます。',
    'telephone': '+81-44-333-8412',
    'faxNumber': '+81-44-333-3843',
    'address': {'@type': 'PostalAddress', 'postalCode': '210-0851', 'addressRegion': '神奈川県',
                'addressLocality': '川崎市川崎区', 'streetAddress': '浜町3-9-22', 'addressCountry': 'JP'},
    'geo': {'@type': 'GeoCoordinates', 'latitude': 35.5257, 'longitude': 139.7194},
    'hasMap': 'https://maps.google.com/?q=神奈川県川崎市川崎区浜町3-9-22',
    'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification',
                                   'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                   'opens': '08:30', 'closes': '18:00'}],
    'foundingDate': '1967',
    'areaServed': [{'@type': 'Country', 'name': '日本'}, {'@type': 'City', 'name': '川崎市'},
                   {'@type': 'City', 'name': '横浜市'}, {'@type': 'AdministrativeArea', 'name': '東京都'}],
    'knowsAbout': ['金属研磨', 'バフ研磨', '鏡面仕上げ', 'ベルト研磨', 'ヘアライン仕上げ', 'フレキ研磨',
                   'ステンレス研磨', 'アルミ研磨', '真鍮研磨', '曲面研磨'],
    'sameAs': ['https://www.instagram.com/matsu_polish/', 'https://www.youtube.com/channel/UCIGiSzo9TyINLuygAsuP5ew/'],
    'department': {'@id': STUDIO_ID},
}
SITE = {'@type': 'WebSite', '@id': SITE_ID, 'url': f'{BASE}/', 'name': '株式会社松本研磨工業',
        'inLanguage': 'ja', 'publisher': {'@id': ORG_ID}}
STUDIO = {
    '@type': 'Organization',
    '@id': STUDIO_ID,
    'name': 'マツケンスタジオ',
    'alternateName': 'マツケンスタジオ by 松本研磨工業',
    'url': f'{BASE}/web-ai/',
    'image': f'{BASE}/images/ogp-studio.jpg',
    'description': '株式会社松本研磨工業が運営する、町工場発のWeb事業。製造業・建設業・工務店・運送業など、現場と技術のある中小企業のホームページ制作・リニューアル、検索対策、Web広告、AI活用をお手伝いします。',
    'parentOrganization': {'@id': ORG_ID},
    'sameAs': ['https://www.instagram.com/matsuken_studio/', 'https://page.line.me/115rhdee'],
    'areaServed': {'@type': 'Country', 'name': '日本'},
    'knowsAbout': ['ホームページ制作', 'ホームページリニューアル', 'Web集客', 'SEO', 'LLMO', 'サイト制作', 'LP制作', 'Web広告', 'CVR改善', 'BtoBマーケティング', 'AI活用'],
}

# Service を入れないページ（一覧・事例・問い合わせなど）
NOT_SERVICE = {'web-ai', 'case', 'column', 'contact'}


def url_of(rel):
    parts = rel.parts[:-1]
    return f'{BASE}/' + ''.join(p + '/' for p in parts)


def meta(s, name):
    m = re.search(rf'<meta (?:name|property)="{name}" content="([^"]*)"', s)
    return H.unescape(m[1]) if m else ''


def text(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def lastmods():
    sm = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    return dict(re.findall(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', sm))


def faq_from_page(s):
    """画面の .faq2 ブロック（研磨ページのQ&A）から質問と答えを取り出す"""
    items = []
    for blk in s.split('<div class="faq2">')[1:]:
        q = re.search(r'<div class="font-medium[^"]*">(.*?)</div>', blk, re.S)
        a = re.search(r'<p[^>]*>(.*?)</p>', blk, re.S)
        if q and a:
            items.append((text(q[1]), text(a[1])))
    return items


def column_items():
    out = []
    for p in sorted((ROOT / 'column').glob('*/index.html')):
        s = p.read_text(encoding='utf-8')
        m = re.search(r'"headline":\s*"([^"]+)"', s)
        if m:
            out.append((m[1], f'{BASE}/column/{p.parent.name}/'))
    return out


def graph_for(rel, s, mods):
    url = url_of(rel)
    parts = rel.parts[:-1]
    top = parts[0] if parts else ''
    studio = top == 'web-ai'
    title = re.search(r'<title>([^<]*)', s)[1]
    desc = meta(s, 'description')
    h1 = text(re.search(r'<h1\b[^>]*>(.*?)</h1>', s, re.S)[1])

    if parts in [('company',)]:
        ptype = 'AboutPage'
    elif parts in [('contact',), ('web-ai', 'contact')]:
        ptype = 'ContactPage'
    elif parts in [('column',), ('news',), ('web-ai', 'column'), ('polishing',)]:
        ptype = 'CollectionPage'
    else:
        ptype = 'WebPage'

    page = {'@type': ptype, '@id': url + '#webpage', 'url': url, 'name': H.unescape(title),
            'description': desc, 'inLanguage': 'ja', 'isPartOf': {'@id': SITE_ID},
            'about': {'@id': STUDIO_ID if studio else ORG_ID},
            'primaryImageOfPage': {'@type': 'ImageObject',
                                   'url': f'{BASE}/images/ogp-studio.jpg' if studio else f'{BASE}/images/ogp.jpg'}}
    if url in mods:
        page['dateModified'] = mods[url]
    nodes = [ORG, SITE] + ([STUDIO] if studio else []) + [page]

    # サービス
    if top == 'polishing' and len(parts) == 2:
        nodes.append({'@type': 'Service', '@id': url + '#service', 'name': h1, 'serviceType': h1,
                      'category': '金属研磨', 'description': desc, 'url': url, 'provider': {'@id': ORG_ID},
                      'areaServed': {'@type': 'Country', 'name': '日本'}})
        page['mainEntity'] = {'@id': url + '#service'}
    if studio and len(parts) >= 2 and parts[1] not in NOT_SERVICE:
        name = H.unescape(title).split('｜')[0]
        nodes.append({'@type': 'Service', '@id': url + '#service', 'name': name, 'serviceType': name,
                      'category': 'Web集客・AI活用支援', 'description': desc, 'url': url,
                      'provider': {'@id': STUDIO_ID}, 'areaServed': {'@type': 'Country', 'name': '日本'}})
        page['mainEntity'] = {'@id': url + '#service'}

    # 一覧ページ
    if parts == ('column',):
        items = column_items()
        page['mainEntity'] = {'@type': 'ItemList', 'numberOfItems': len(items), 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'url': u} for i, (n, u) in enumerate(items)]}
    if parts == ('polishing',):
        subs = [('バフ研磨', 'buff-polishing'), ('ベルト研磨', 'belt-polishing'),
                ('ヘアライン仕上げ', 'hairline-finish'), ('フレキ研磨', 'flexible-polishing')]
        page['mainEntity'] = {'@type': 'ItemList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'url': f'{BASE}/polishing/{u}/'}
            for i, (n, u) in enumerate(subs)]}
    return nodes


def managed_blocks(rel, s, mods):
    blocks = [{'@context': 'https://schema.org', '@graph': graph_for(rel, s, mods)}]
    parts = rel.parts[:-1]
    if 'BreadcrumbList' not in s and parts:
        crumbs = [('ホーム', f'{BASE}/')]
        if parts == ('column',):
            crumbs.append(('コラム', f'{BASE}/column/'))
        if len(crumbs) > 1:
            blocks.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(crumbs)]})
    if '"FAQPage"' not in s:
        faq = faq_from_page(s)
        if faq:
            blocks.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]})
    return blocks


def fix_existing(s):
    """前からある JSON-LD を整理する（会社情報の重複を消し、記事の発行元を会社につなぐ）"""
    def repl(m):
        try:
            j = json.loads(m[1])
        except ValueError:
            return m[0]
        t = j.get('@type')
        if t in ('LocalBusiness', 'Organization'):
            return ''  # 会社情報は managed の @graph に一本化
        if t == 'BlogPosting':
            j['author'] = {'@type': 'Organization', '@id': ORG_ID, 'name': '株式会社松本研磨工業', 'url': f'{BASE}/'}
            j['publisher'] = {'@id': ORG_ID}
            j['inLanguage'] = 'ja'
            return '<script type="application/ld+json">\n' + json.dumps(j, ensure_ascii=False, indent=2) + '\n</script>'
        return m[0]
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>\n?', repl, s, flags=re.S)
    return re.sub(r'<script type="application/ld\+json" data-sd="managed">.*?</script>\n?', '', s, flags=re.S)


def apply(rel, s, mods):
    s = fix_existing(s)
    lds = ''.join('<script type="application/ld+json" data-sd="managed">\n' +
                  json.dumps(b, ensure_ascii=False, indent=2) + '\n</script>\n'
                  for b in managed_blocks(rel, s, mods))
    return s.replace('</head>', lds + '</head>', 1)


if __name__ == '__main__':
    mods, n = lastmods(), 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP or rel.name != 'index.html':
            continue
        s = p.read_text(encoding='utf-8')
        if 'noindex' in s or 'http-equiv="refresh"' in s:
            continue
        out = apply(rel, s, mods)
        if out != s:
            p.write_text(out, encoding='utf-8'); n += 1
    print(f'updated {n} files')

"""AI検索（ChatGPT・Perplexity・Geminiなど）向けの案内ファイル llms.txt を作る。

各ページの <title> と description から一覧を作るので、ページを増やしたら実行し直す。
使い方: python3 tools/llms_txt.py
"""
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://matsumoto-kenma.co.jp'


def info(rel):
    s = (ROOT / rel / 'index.html').read_text(encoding='utf-8')
    t = html.unescape(re.search(r'<title>([^<]*)', s)[1]).split('｜')[0]
    d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s)[1])
    return f'- [{t}]({BASE}/{rel}{"/" if rel else ""}): {d}'


def section(title, rels):
    return f'\n## {title}\n\n' + '\n'.join(info(r) for r in rels) + '\n'


def subdirs(d, exclude=()):
    return sorted(f'{d}/{p.parent.name}' for p in (ROOT / d).glob('*/index.html')
                  if p.parent.name not in exclude and 'noindex' not in p.read_text(encoding='utf-8'))


out = f'''# 株式会社松本研磨工業

> 神奈川県川崎市川崎区の金属研磨工場（1967年創業）。ステンレス・アルミ・真鍮・鉄・銅・チタンなどの金属を、バフ研磨（鏡面仕上げ）・ベルト研磨・ヘアライン仕上げ・フレキ研磨で仕上げています。試作の1個から小量産まで対応し、図面がなくても現物や写真からお見積りできます。Web集客・AI活用支援の事業「マツケンスタジオ」も運営しています。

## 会社の基本情報

- 会社名: 株式会社松本研磨工業
- 所在地: 〒210-0851 神奈川県川崎市川崎区浜町3-9-22
- 電話: 044-333-8412（平日 8:30〜18:00、土日祝休み）
- 創業: 1967年（設立 1977年6月16日）
- 対応地域: 全国（川崎・横浜・東京を中心とした関東全域。遠方は宅配便・運送便で受付）
- 金属研磨のお問い合わせ: {BASE}/contact/
- Web集客・AI活用支援のお問い合わせ: {BASE}/web-ai/contact/
'''
out += section('金属研磨', ['', 'polishing'] + subdirs('polishing'))
out += section('会社情報・お知らせ', ['company', 'news'])
out += section('研磨・金属加工コラム', ['column'] + subdirs('column'))
out += section('Web集客・AI活用支援（マツケンスタジオ）', ['web-ai'] + subdirs('web-ai', exclude=('contact',)))
(ROOT / 'llms.txt').write_text(out, encoding='utf-8')
print(f'llms.txt: {out.count(chr(10))} lines')

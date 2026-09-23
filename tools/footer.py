"""全ページのフッターを共通の形に置きかえる。

- /web-ai/ 配下（マツケンスタジオ）は電話番号・研磨の問い合わせを出さず、専用フォームだけにする
- リンクの前につける相対パス（'' / '../' / '../../' / '/'）は、今のフッターの「#home」リンクから判定する

使い方: python3 tools/footer.py   （何度実行しても同じ結果）
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

IG = '<svg class="w-5 h-5 stroke-current fill-none stroke-[1.5]" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
YT = '<svg class="w-5 h-5 fill-current" viewBox="0 0 24 24" aria-hidden="true"><path d="M21.8 8s-.2-1.4-.8-2c-.8-.8-1.6-.8-2-.9C16.8 5 12 5 12 5s-4.8 0-7 .1c-.4.1-1.3.1-2 .9-.6.6-.8 2-.8 2S2 9.6 2 11.2v1.5c0 1.6.2 3.2.2 3.2s.2 1.4.8 2c.8.8 1.8.8 2.2.9C6.8 19 12 19 12 19s4.8 0 7-.2c.4-.1 1.3-.1 2-.9.6-.6.8-2 .8-2s.2-1.6.2-3.2v-1.5C22 9.6 21.8 8 21.8 8zM9.8 14.5V9.5l5.4 2.5-5.4 2.5z"/></svg>'

def _col(title, links, pre):
    items = ''.join(f'\n          <li><a href="{pre}{h}" class="ft-link">{t}</a></li>' for t, h in links)
    return f'''
      <nav aria-label="{title}">
        <h3 class="ft-head">{title}</h3>
        <ul class="space-y-3">{items}
        </ul>
      </nav>'''

def render(pre, studio=False):
    cols = [
        ('金属研磨', [('金属研磨技術の種類', 'polishing/'), ('バフ研磨', 'polishing/buff-polishing/'),
                     ('ベルト研磨', 'polishing/belt-polishing/'), ('ヘアライン仕上げ', 'polishing/hairline-finish/'),
                     ('フレキ研磨', 'polishing/flexible-polishing/'), ('加工実績', '#works')]),
        ('会社について', [('会社情報', 'company/'), ('アクセス', 'company/#access'), ('よくある質問', '#faq'),
                        ('お知らせ', 'news/'), ('コラム', 'column/')]),
        ('Web集客・AI活用支援', [('サービス一覧', 'web-ai/'), ('SEO・集客対策', 'web-ai/seo-consulting/'),
                              ('サイト制作・LP制作', 'web-ai/website/'), ('AI活用支援', 'web-ai/ai-katsuyo/'),
                              ('実績・事例', 'web-ai/case/')]),
    ]
    links = ''.join(_col(t, l, pre) for t, l in cols)
    if studio:
        contact = f'''
        <p class="text-[14px] leading-[1.9] text-paper/80 mb-5">マツケンスタジオへのご相談は、お問い合わせフォームで受け付けています。</p>
        <a href="{pre}web-ai/contact/" class="ft-btn">1分で問い合わせ</a>'''
        address = '〒210-0851 神奈川県川崎市川崎区浜町3-9-22'
    else:
        contact = f'''
        <a href="tel:0443338412" class="block text-[26px] md:text-[28px] font-bold tracking-[.02em] text-paper leading-none hover:underline underline-offset-4">044-333-8412</a>
        <p class="text-[13px] leading-[1.8] text-paper/70 mt-2 mb-5">平日 8:30〜18:00（土日祝休み）<br/>※営業・勧誘のお電話はお断りしています</p>
        <a href="{pre}contact/" class="ft-btn">お問い合わせフォーム</a>'''
        address = '〒210-0851 神奈川県川崎市川崎区浜町3-9-22<br/>電話 044-333-8412 ／ FAX 044-333-3843'
    return f'''<footer class="site-footer bg-navy text-paper pt-14 md:pt-20 pb-8">
  <div class="wrap">
    <div class="grid grid-cols-1 lg:grid-cols-[1.2fr_1fr] gap-10 lg:gap-16 pb-10 md:pb-14 border-b border-paper/15">
      <div>
        <a href="{pre}" class="inline-flex items-center gap-3">
          <span class="w-11 h-11 rounded-full grid place-items-center font-semibold text-xl bg-paper text-ink">松</span>
          <span class="text-[18px] md:text-[20px] font-bold tracking-[.04em] text-paper">株式会社松本研磨工業</span>
        </a>
        <p class="mt-5 text-[14px] leading-[1.9] text-paper/75">{address}</p>
        <div class="mt-6 flex gap-3">
          <a href="https://www.instagram.com/matsu_polish/" target="_blank" rel="noopener" class="ft-sns">{IG}<span>Instagram</span></a>
          <a href="https://www.youtube.com/channel/UCIGiSzo9TyINLuygAsuP5ew/" target="_blank" rel="noopener" class="ft-sns">{YT}<span>YouTube</span></a>
        </div>
      </div>
      <div class="lg:border-l lg:border-paper/15 lg:pl-16">
        <h3 class="ft-head">お問い合わせ</h3>{contact}
      </div>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-10 py-10 md:py-14 border-b border-paper/15">{links}
    </div>
    <div class="pt-6 flex flex-col sm:flex-row justify-between items-center gap-3 text-[13px] text-paper/60">
      <a href="{pre}privacy/" class="hover:text-paper hover:underline underline-offset-4">プライバシーポリシー</a>
      <div>© 2026 株式会社松本研磨工業</div>
    </div>
  </div>
</footer>'''

CSS = '''<style>/* site-footer */
.site-footer .ft-head{font-size:15px;font-weight:700;color:#F4F2ED;letter-spacing:.04em;padding-bottom:12px;margin-bottom:16px;border-bottom:1px solid rgba(244,242,237,.2)}
.site-footer .ft-link{font-size:15px;color:rgba(244,242,237,.82);line-height:1.6}
.site-footer .ft-link:hover{color:#F4F2ED;text-decoration:underline;text-underline-offset:4px}
.site-footer .ft-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-width:240px;padding:15px 24px;border-radius:4px;background:#F4F2ED;color:#0E0E10;font-size:15px;font-weight:700;transition:background .2s}
.site-footer .ft-btn::after{content:"→"}
.site-footer .ft-btn:hover{background:#fff}
.site-footer .ft-sns{display:inline-flex;align-items:center;gap:8px;padding:9px 14px;border:1px solid rgba(244,242,237,.3);border-radius:4px;font-size:13px;color:#F4F2ED}
.site-footer .ft-sns:hover{background:rgba(244,242,237,.1)}
.site-footer a:focus-visible{outline:2px solid #F4F2ED;outline-offset:3px}
</style>
'''

def apply(html, pre, studio=False):
    html = re.sub(r'<footer\b.*?</footer>', lambda m: render(pre, studio), html, count=1, flags=re.S)
    html = re.sub(r'<style>/\* site-footer \*/.*?</style>\n?', '', html, flags=re.S)
    return html.replace('</head>', CSS + '</head>', 1)

def prefix_of(html):
    ft = re.search(r'<footer\b.*?</footer>', html, flags=re.S)
    if not ft:
        return None
    m = re.search(r'href="([^"#]*)#home"', ft.group(0)) or re.search(r'<a href="([./]*)" class="inline-flex items-center gap-3">', ft.group(0))
    return m.group(1) if m else None

if __name__ == '__main__':
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if p.relative_to(ROOT).parts[0] in ('node_modules', 'tools', 'skills', 'input', 'output', 'agents', 'memory'):
            continue
        src = p.read_text(encoding='utf-8')
        pre = prefix_of(src)
        if pre is None:
            continue
        out = apply(src, pre, 'web-ai' in p.relative_to(ROOT).parts)
        if out != src:
            p.write_text(out, encoding='utf-8'); n += 1
    print(f'updated {n} files')

import ogp_meta
import footer
import os, re, json, glob

SERVICE_SHELL = 'polishing/buff-polishing/index.html'   # depth-2 shell (nav links already ../../)
BASE = 'https://matsumoto-kenma.co.jp'

CATEGORIES = [
    ('戦略・コンサルティング', [
        ('consulting', 'デジタルマーケティングコンサルティング', 'digitalmarketing-consulting',
         '集客の方法・予算の配分・優先順位が分からない状態から、何にどれだけ力を入れるべきかを一緒に整理します。'),
        ('btob-marketing', 'BtoBマーケティング支援', 'btob-marketing',
         '会社同士の取引が中心の方向けに、発注担当者に届く情報の出し方・見せ方を考えます。'),
    ]),
    ('集客・改善', [
        ('seo-consulting', 'SEOコンサルティング', 'seo-consulting',
         '検索結果に出てこない状態から、問い合わせにつながる言葉での上位表示を目指します。'),
        ('ad-consulting', 'Web広告コンサルティング', 'ad-consulting',
         '広告費を無駄にしないための出し方と効果の測り方を、商談までの長さも踏まえて考えます。'),
        ('cro-consulting', 'CVR改善／CROコンサルティング', 'cro-consulting',
         '見てもらえているのに問い合わせが来ないサイトの、つまずいている場所を見つけて直します。'),
        ('llmo-consulting', 'LLMOコンサルティング', 'llmo-consulting',
         'ChatGPTなどのAIに、自社のことを正しく紹介してもらうための書き方・作り方を考えます。'),
    ]),
    ('制作', [
        ('website', 'サイト制作', 'website',
         '表示の速さや見つけてもらいやすさまで考えた、問い合わせにつながる会社のサイトをつくります。'),
        ('lp', 'LP制作', 'lp',
         '一つの商品・サービスに絞って、問い合わせを集めるためのページをつくります。'),
        ('seo-writing', 'SEO/LLMO記事制作代行', 'seo-writing',
         '検索とAIの両方から読まれる技術記事・コラムを、企画から執筆まで代わりに書きます。'),
        ('case-interview', '事例インタビュー記事制作', 'case-interview',
         'お客様や取引先への取材をもとに、説得力のある事例記事をつくります。'),
    ]),
    ('AI活用支援', [
        ('ai-katsuyo', 'AI活用支援（業務効率化・自動化）', 'ai-katsuyo',
         '見積書づくりや問い合わせ対応など、毎日の仕事にAIを取り入れて時間をつくるお手伝いをします。'),
    ]),
]

STUDIO_CSS = '''<style>
  /* Matsuken Studio: light theme */
  html,body{background:#FFFFFF}
  .pwrap.max-w-\[800px\]{max-width:880px}
  .st-alt{background:#F4F6F9}
  .st-cta{background:#FFF9D6}
  .sec-label{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;letter-spacing:.14em;color:#1B3A6B;margin-bottom:16px}
  .sec-ttl{font-size:24px;font-weight:700;line-height:1.45;margin-bottom:20px;color:#0E0E10}
  @media(min-width:768px){.sec-ttl{font-size:30px}}
  .st-logo{display:inline-flex;align-items:center;gap:12px}
  .st-mark{width:40px;height:40px;border-radius:10px;background:#1B3A6B;color:#fff;display:grid;place-items:center;font-weight:700;font-size:22px;position:relative;flex-shrink:0}
  .st-mark::after{content:'';position:absolute;right:-3px;top:-3px;width:12px;height:12px;border-radius:50%;background:#F5DE00;border:2px solid #fff}
  .st-name{display:block;font-weight:800;font-size:20px;letter-spacing:.04em;color:#0E0E10;line-height:1.2}
  .st-by{display:block;font-size:11px;letter-spacing:.14em;color:#5E5E65;margin-top:3px}
  .st-hero{position:relative;overflow:hidden;background:#fff;border-bottom:1px solid #E6E9EE}
  .st-hero::before{content:'';position:absolute;right:-120px;top:-120px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,#FFF4B0 0%,rgba(255,244,176,0) 70%);pointer-events:none}
  .st-hero::after{content:'';position:absolute;right:40px;bottom:40px;width:260px;height:180px;background-image:radial-gradient(#C9D2DF 1.2px,transparent 1.2px);background-size:14px 14px;opacity:.7;pointer-events:none}
  .trust{display:grid;grid-template-columns:1fr;border-top:1px solid #E6E9EE}
  @media(min-width:768px){.trust{grid-template-columns:repeat(3,1fr)}}
  .trust>div{padding:20px 0}
  @media(min-width:768px){.trust>div{padding:24px 28px}.trust>div+div{border-left:1px solid #E6E9EE}.trust>div:first-child{padding-left:0}}
  .trust .t-big{font-size:17px;font-weight:700;color:#0E0E10;margin-bottom:4px}
  .trust .t-sub{font-size:13px;color:#5E5E65;line-height:1.8}
  .card2{position:relative;border:1px solid #E1E5EB;background:#fff;padding:30px 24px 26px;border-top:3px solid #1B3A6B;border-radius:6px}
  .card2.alt{border-top-color:#2E5BA6}
  .card2 .idx{font-family:'JetBrains Mono',monospace;font-size:11px;color:#8a8a86;letter-spacing:.15em;margin-bottom:14px}
  .svc-list{background:#fff;border:1px solid #E1E5EB;border-radius:8px;padding:10px 28px}
  .svc-list li{list-style:none;display:grid;grid-template-columns:22px 1fr;gap:10px;padding:14px 0;border-bottom:1px solid #EEF1F5;font-size:14px;line-height:1.8}
  .svc-list li:last-child{border-bottom:none}
  .svc-list li::before{content:'';width:10px;height:10px;margin-top:8px;border-radius:3px;background:#F5DE00;box-shadow:0 0 0 2px #1B3A6B inset}
  .step2{position:relative;padding:6px 0 30px 32px;border-left:2px solid #DDE3EB}
  .step2:last-child{border-left:2px solid transparent;padding-bottom:2px}
  .step2::before{content:'';position:absolute;left:-7px;top:4px;width:12px;height:12px;border-radius:50%;background:#1B3A6B}
  .step2.alt::before{background:#2E5BA6}
  .step2 .pnum{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.14em;color:#8a8a86;margin-bottom:4px}
  .faq2{display:grid;grid-template-columns:36px 1fr;gap:16px;padding:22px 0;border-top:1px solid #E1E5EB}
  .faq2:last-child{border-bottom:1px solid #E1E5EB}
  .faq2 .qa{font-size:22px;font-weight:700;line-height:1;color:#1B3A6B}
  .price-box{border:1px solid #E1E5EB;border-radius:8px;background:#fff;padding:32px 28px;display:grid;grid-template-columns:1fr;gap:18px}
  @media(min-width:768px){.price-box{grid-template-columns:1fr auto;align-items:center;padding:36px 40px}}
  .case-card{display:grid;grid-template-columns:1fr;border:1px solid #E1E5EB;border-radius:8px;overflow:hidden;background:#fff;transition:border-color .2s,box-shadow .2s}
  .case-card:hover{border-color:#1B3A6B;box-shadow:0 10px 30px -14px rgba(27,58,107,.35)}
  .case-card .c-img{background:linear-gradient(135deg,#EAF0F8,#FFF6C4);min-height:160px;display:grid;place-items:center;color:#1B3A6B;font-size:13px;font-weight:600;letter-spacing:.14em}
  @media(min-width:768px){.case-card{grid-template-columns:280px 1fr}}
  .rel-grid{display:grid;grid-template-columns:1fr;gap:28px}
  @media(min-width:768px){.rel-grid{grid-template-columns:repeat(4,1fr)}}
  .rel-grid a{display:block;padding:9px 0;border-bottom:1px solid #E1E5EB;font-size:14px;transition:color .15s}
  .rel-grid a:hover{color:#2E5BA6}
  .rel-grid a.current{color:#8a8a86;pointer-events:none}
  .svc-card{display:block;background:#fff;border:1px solid #E1E5EB;border-radius:8px;padding:26px 24px;transition:border-color .2s,box-shadow .2s,transform .2s}
  a.svc-card:hover{border-color:#1B3A6B;box-shadow:0 10px 30px -14px rgba(27,58,107,.35);transform:translateY(-2px)}
  .story p{font-size:15px;line-height:2.1;color:#26262B;margin-bottom:20px}
  @media(min-width:768px){.story p{font-size:16px}}
  .story-quote{font-size:clamp(20px,2.6vw,28px);font-weight:700;line-height:1.6;color:#0E0E10;padding-left:20px;border-left:4px solid #F5DE00}
  .target-card{background:#fff;border:1px solid #E1E5EB;border-radius:8px;padding:24px}
  .target-card .tg{display:inline-block;font-size:12px;font-weight:700;color:#1B3A6B;background:#FFF4B0;border-radius:999px;padding:4px 12px;margin-bottom:12px}
</style>
'''

LOGO = '''<div class="st-logo"><span class="st-mark">松</span><span><span class="st-name">マツケンスタジオ</span><span class="st-by">by 松本研磨工業</span></span></div>'''

LINE_ICON = '<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3C6.5 3 2 6.6 2 11c0 3.9 3.5 7.2 8.3 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.5s5.9-3.5 8-6C21.4 14.3 22 12.7 22 11c0-4.4-4.5-8-10-8z"/></svg>'

def btn_main(href, size='md'):
    cls = {
        'lg': 'px-10 py-5 md:px-12 md:py-[22px] text-[17px] md:text-[18px] shadow-[0_12px_30px_-10px_rgba(200,170,0,.7)]',
        'md': 'px-8 py-3.5 md:px-9 md:py-[18px] text-[15px] md:text-[16px] shadow-[0_10px_24px_-10px_rgba(200,170,0,.7)]',
    }[size]
    return f'<a href="{href}" class="inline-flex items-center justify-center gap-[10px] {cls} rounded-full font-bold tracking-[.04em] bg-cta-yellow text-ink hover:bg-cta-yellow-h hover:-translate-y-0.5 transition-all">1分で問い合わせ →</a>'

def btn_line(size='md'):
    return ''  # LINEは使わない方針

def cta_pair(contact, size='md'):
    return f'<div class="flex flex-col sm:flex-row items-center justify-center gap-3">{btn_main(contact, size)}{btn_line(size)}</div>'

def mid_cta(lead, contact):
    return f'''  <section class="py-12 md:py-14 st-cta text-center">
    <div class="pwrap">
      <p class="text-ink text-[15px] md:text-[16px] font-semibold mb-5">{lead}</p>
      {cta_pair(contact)}
    </div>
  </section>
'''

def final_cta(contact):
    return f'''  <section class="py-16 md:py-24 st-cta text-center">
    <div class="pwrap">
      <div class="flex justify-center mb-6">{LOGO}</div>
      <p class="font-bold leading-[1.5] mb-4 text-ink" style="font-size:clamp(22px,3.2vw,32px)">Webのお悩み、<br class="sm:hidden"/>まずは気軽にご相談ください。</p>
      <p class="text-[14px] md:text-[15px] text-muted leading-[1.9] mb-8 max-w-[560px] mx-auto">何から始めればいいか分からない、という段階でも大丈夫です。町工場・職人・小さな会社の方の相談を、同じつくり手としてお聞きします。</p>
      {cta_pair(contact, 'lg')}
    </div>
  </section>
'''

def cards(items, cols=3):
    out = [f'      <div class="grid grid-cols-1 md:grid-cols-{cols} gap-5">']
    for i, (t, d) in enumerate(items):
        out.append(f'''        <div class="card2{' alt' if i % 2 else ''}">
          <div class="idx">{i+1:02d}</div>
          <div class="font-bold text-[16px] mb-2">{t}</div>
          <p class="text-[13px] leading-[1.9] text-muted">{d}</p>
        </div>''')
    out.append('      </div>')
    return '\n'.join(out)

def section(label, title, body, alt=False, narrow=True, sid=''):
    b = ' st-alt' if alt else ''
    w = ' max-w-[800px]' if narrow else ''
    i = f' id="{sid}"' if sid else ''
    return f'''  <section class="py-14 md:py-20{b}"{i}>
    <div class="pwrap{w}">
      <h2 class="sec-ttl">{title}</h2>
{body}
    </div>
  </section>
'''

def trust():
    return '''      <div class="trust mt-12">
        <div><div class="t-big">有効なお問い合わせ 3倍</div><div class="t-sub">自社サイトの制作・SEO対策で出した成果です</div></div>
        <div><div class="t-big">マーケティング歴10年以上</div><div class="t-sub">数百社の支援経験を持つ責任者が担当します</div></div>
        <div><div class="t-big">上場企業出身のマーケター</div><div class="t-sub">大きな会社のやり方と、現場の両方を知っています</div></div>
      </div>'''

def page_exists(slug):
    return os.path.exists(f'web-ai/{slug}/index.html')

def related(current):
    cols = []
    for cat, items in CATEGORIES:
        links = []
        for slug, name, anchor, _ in items:
            if slug == current:
                links.append(f'<a class="current">{name}</a>')
            elif page_exists(slug):
                links.append(f'<a href="../{slug}/">{name}</a>')
            else:
                links.append(f'<a href="../#{anchor}">{name}</a>')
        cols.append(f'''        <div>
          <div class="font-mono text-[12px] font-semibold tracking-[.14em] text-accent mb-3">{cat}</div>
          {''.join(links)}
        </div>''')
    return '      <div class="rel-grid">\n' + '\n'.join(cols) + '\n      </div>'

CASE_CARD = '''      <a href="{href}" class="case-card">
        <div class="c-img">有効なお問い合わせ 3倍</div>
        <div class="p-6 md:p-8">
          <div class="font-mono text-[11px] tracking-[.14em] text-muted mb-2">株式会社松本研磨工業</div>
          <div class="font-bold text-[17px] mb-3">サイト制作とSEO対策で、有効なお問い合わせが3倍に</div>
          <p class="text-[13px] leading-[1.9] text-muted mb-4">松本研磨工業のサイトを作り直し、SEO対策を進めたことで、有効なお問い合わせの数は3倍に増えました。</p>
          <span class="text-[13px] font-bold text-accent-ink">事例を読む →</span>
        </div>
      </a>'''

def set_meta(head, title, desc, url, ld_blocks):
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', head)
    head = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    head = re.sub(r'\s*<style>\s*/\* Matsuken Studio.*?</style>', '', head, flags=re.S)
    head = ogp_meta.apply(head, 'studio')
    lds = ''.join('<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=2) + '\n</script>\n' for b in ld_blocks)
    return head.replace('</head>', lds + STUDIO_CSS + '</head>', 1)

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def build(p):
    shell = open(SERVICE_SHELL, encoding='utf-8').read()
    head, tail = shell[:shell.index('<main')], shell[shell.index('</main>'):]
    url = f'{BASE}/web-ai/{p["slug"]}/'
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in p['faq']]}
    head = set_meta(head, f'{p["name"]}｜マツケンスタジオ by 松本研磨工業', p['desc'], url,
                    [crumbs([('ホーム', f'{BASE}/'), ('Web集客・AI活用支援', f'{BASE}/web-ai/'), (p['name'], url)]), faq_ld])
    C = '../contact/'
    steps = '\n'.join(f'''      <div class="step2{' alt' if i % 2 else ''}">
        <div class="pnum">{i+1:02d}</div>
        <div class="font-bold text-[15px] mb-1">{t}</div>
        <p class="text-[13px] leading-[1.9] text-muted">{d}</p>
      </div>''' for i, (t, d) in enumerate(p['steps']))
    faqs = '\n'.join(f'''      <div class="faq2">
        <div class="qa">Q</div>
        <div>
          <div class="font-bold text-[14px] mb-2">{q}</div>
          <p class="text-[13px] leading-[1.9] text-muted">{a}</p>
        </div>
      </div>''' for q, a in p['faq'])
    what = '\n'.join(f'      <p class="text-[14px] md:text-[15px] leading-[2] text-ink-2 mb-4">{x}</p>' for x in p['what'])
    items = '\n'.join(f'        <li>{x}</li>' for x in p['scope'])
    story = f'''      <div class="grid grid-cols-1 md:grid-cols-[1fr_260px] gap-8 items-center">
        <div>
          <p class="text-[14px] md:text-[15px] leading-[2] text-ink-2 mb-4">マツケンスタジオは、金属研磨の町工場・松本研磨工業の新しい事業です。担当するのは、デジタルマーケティングの仕事を10年以上続けてきた責任者です。</p>
          <p class="text-[14px] md:text-[15px] leading-[2] text-ink-2 mb-5">数百社の集客を支援してきた経験と、町工場の現場の両方を知っているからこそ、製造業・職人・小さな会社の方に、分かる言葉で、無理のない範囲から{p["name"]}をお手伝いします。</p>
          <a href="../#story" class="text-[14px] font-bold text-accent-ink hover:underline">私たちがWebの仕事をする理由 →</a>
        </div>
        <div class="flex md:justify-end">{LOGO}</div>
      </div>'''

    main = f'''<main class="pt-[60px]">

  <section class="st-hero pt-7 pb-12 md:py-20">
    <div class="pwrap relative z-10">
      <p class="font-mono text-[11px] tracking-[.2em] text-muted mb-4 md:mb-8">
        <a href="../../" class="hover:text-accent transition-colors">ホーム</a>
        <span class="mx-2 opacity-40">/</span>
        <a href="../" class="hover:text-accent transition-colors">Web集客・AI活用支援</a>
        <span class="mx-2 opacity-40">/</span>{p["name"]}
      </p>
      <div class="mb-4 md:mb-8">{LOGO}</div>
      <div class="font-mono text-[12px] font-bold tracking-[.16em] text-accent-ink mb-3">{p["cat"]}</div>
      <h1 class="font-bold leading-[1.3] mb-3 md:mb-5 text-ink" style="font-size:clamp(28px,4.8vw,50px)">{p["name"]}</h1>
      <p class="text-[16px] md:text-[19px] font-bold text-ink leading-[1.7] max-w-[680px] mb-3">{p["catch"]}</p>
      <p class="hidden md:block text-[14px] md:text-[15px] text-muted leading-[1.9] max-w-[680px]">{p["lead"]}</p>
      <div class="mt-6 md:mt-9 flex flex-col sm:flex-row gap-2.5 md:gap-3 sm:items-center">{btn_main(C)}{btn_line()}</div>
{trust()}
    </div>
  </section>

{section("", p["name"] + "とは", '      <p class="text-[17px] md:text-[19px] font-bold text-ink leading-[1.7] mb-5">' + p["what_title"] + '</p>' + chr(10) + what)}
{section("得られること", p["name"] + "で得られること", cards(p["benefits"]), alt=True, narrow=False)}
{mid_cta(p["cta"][0], C)}
{section("", p["name"] + "でお手伝いできること", '      <ul class="svc-list">' + chr(10) + items + chr(10) + '      </ul>')}
{mid_cta(p["cta"][1], C)}
{section("", p["name"] + "の支援の流れ", steps, alt=True, sid="flow")}
{section("", "マツケンスタジオの" + p["name"] + "の特徴", cards(p["features"], cols=2), narrow=False)}
{section("", "マツケンスタジオについて", story, alt=True, narrow=False)}
{mid_cta(p["cta"][2], C)}
{section("", p["name"] + "の料金", f"""      <div class="price-box">
        <p class="text-[14px] leading-[2] text-ink-2">{p["price"]}</p>
        {btn_main(C)}
      </div>""")}
{section("実績", "実績・事例", CASE_CARD.format(href="../case/"), alt=True)}
{section("", p["name"] + "のよくある質問", faqs)}
{section("", "関連サービス", related(p["slug"]), alt=True, narrow=False)}
{final_cta(C)}
'''
    os.makedirs(f'web-ai/{p["slug"]}', exist_ok=True)
    open(f'web-ai/{p["slug"]}/index.html', 'w', encoding='utf-8').write(studio_chrome(head + main + tail, '../../'))
    print('built', p['slug'])


def build_hub():
    f = 'web-ai/index.html'
    src = open(f, encoding='utf-8').read()
    head, tail = src[:src.index('<main')], src[src.index('</main>'):]
    url = f'{BASE}/web-ai/'
    desc = '製造業・町工場・職人、中小企業や個人事業主のためのWeb集客・AI活用支援。川崎の研磨工場・松本研磨工業のWeb部門「マツケンスタジオ」が、サイトづくりから検索対策、AI活用まで分かる言葉でお手伝いします。'
    head = set_meta(head, 'Web集客・AI活用支援｜マツケンスタジオ by 松本研磨工業', desc, url,
                    [crumbs([('ホーム', f'{BASE}/'), ('Web集客・AI活用支援', url)])])
    C = 'contact/'

    svc_blocks = []
    for cat, items in CATEGORIES:
        cols = 2 if len(items) != 1 else 1
        cards_html = []
        for slug, name, anchor, d in items:
            if page_exists(slug):
                cards_html.append(f'''        <a href="{slug}/" class="svc-card" id="{anchor}">
          <div class="font-bold text-[17px] mb-2 text-ink">{name}</div>
          <p class="text-[13px] leading-[1.9] text-muted">{d}</p>
          <div class="mt-4 text-[13px] font-bold text-accent-ink">詳しく見る →</div>
        </a>''')
            else:
                cards_html.append(f'''        <div class="svc-card" id="{anchor}">
          <div class="font-bold text-[17px] mb-2 text-ink">{name}</div>
          <p class="text-[13px] leading-[1.9] text-muted">{d}</p>
        </div>''')
        svc_blocks.append(f'''      <div class="mb-10 md:mb-12">
        <div class="font-mono text-[12px] font-bold tracking-[.16em] text-accent-ink mb-4">{cat}</div>
        <div class="grid grid-cols-1 md:grid-cols-{cols} gap-4">
{chr(10).join(cards_html)}
        </div>
      </div>''')

    targets = [
        ('製造業・町工場', '技術には自信があるのに、サイトが古いまま。新しい取引先から見つけてもらえない。'),
        ('職人・工房', '仕事の良さを伝えたいけれど、何をどう発信すればいいのか分からない。'),
        ('中小企業', 'Webの担当者がいない。制作会社に頼んだけれど、作ったあと放ったらかしになっている。'),
        ('個人事業主', '予算は限られている。まずは小さく始めて、少しずつ育てていきたい。'),
    ]
    target_html = '\n'.join(f'''        <div class="target-card">
          <span class="tg">{t}</span>
          <p class="text-[14px] leading-[1.9] text-ink-2">{d}</p>
        </div>''' for t, d in targets)

    values = [
        ('専門用語を使いません', 'SEO、CVR、LLMO。聞き慣れない言葉は、普段の言葉に置きかえて説明します。'),
        ('小さく始められます', 'いきなり大きな予算は必要ありません。今あるサイトの手直しからでも始められます。'),
        ('作って終わりにしません', '公開したあとも、数字を見ながら一緒に直していきます。社内で続けられる形も残します。'),
    ]
    steps = [
        ('1分で問い合わせ', 'お問い合わせフォームから、気軽にご連絡ください。'),
        ('お話をお聞きします', '今の状況や、困っていることをお聞きします。相談は無料です。'),
        ('進め方のご提案', '何から手をつけるか、優先順位をつけてご提案します。'),
        ('一緒に進めます', 'サイトの手直しや記事づくりなど、実際の作業まで対応します。'),
        ('振り返りと次の一手', '結果を見ながら、次にやることを決めていきます。'),
    ]
    step_html = '\n'.join(f'''      <div class="step2{' alt' if i % 2 else ''}">
        <div class="pnum">{i+1:02d}</div>
        <div class="font-bold text-[15px] mb-1">{t}</div>
        <p class="text-[13px] leading-[1.9] text-muted">{d}</p>
      </div>''' for i, (t, d) in enumerate(steps))

    main = f'''<main class="pt-[60px]">

  <section class="st-hero pt-7 pb-12 md:py-24">
    <div class="pwrap relative z-10">
      <p class="font-mono text-[11px] tracking-[.2em] text-muted mb-4 md:mb-8">
        <a href="../" class="hover:text-accent transition-colors">ホーム</a>
        <span class="mx-2 opacity-40">/</span>Web集客・AI活用支援
      </p>
      <div class="mb-4 md:mb-8">{LOGO}</div>
      <h1 class="font-bold leading-[1.35] mb-4 md:mb-6 text-ink max-w-[820px]" style="font-size:clamp(24px,7vw,54px)">いい仕事をしている会社の<br/>「知ってもらう」を、<br/>研磨工場が手伝います。</h1>
      <p class="text-[14px] md:text-[17px] text-muted leading-[1.8] md:leading-[1.9] max-w-[640px]"><span class="md:hidden">製造業・町工場・職人、中小企業や個人事業主のためのWeb集客・AI活用支援です。</span><span class="hidden md:inline">製造業・町工場・職人、中小企業や個人事業主のためのWeb集客・AI活用支援。サイトづくりから検索対策、AIの活用まで、同じつくり手の目線でお手伝いします。</span></p>
      <div class="mt-6 md:mt-9 flex flex-col sm:flex-row gap-2.5 md:gap-3 sm:items-center">{btn_main(C)}{btn_line()}</div>
{trust()}
    </div>
  </section>

  <section class="py-10 md:py-12 st-cta">
    <div class="pwrap flex flex-col md:flex-row md:items-center md:justify-between gap-5">
      <div>
        <div class="inline-block text-[12px] font-bold text-accent-ink bg-white rounded-full px-3 py-1 mb-2">毎月3社まで</div>
        <p class="font-bold text-[18px] md:text-[20px] text-ink leading-[1.6]">事例づくりモニター 受付中</p>
        <p class="text-[13px] md:text-[14px] text-muted leading-[1.8]">事例として紹介させていただくことを条件に、特別な価格で制作します。作った後の月額サポートもご案内しています。</p>
      </div>
      <a href="monitor/" class="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-full font-bold text-[15px] border-2 border-ink text-ink bg-white hover:bg-ink hover:text-white transition-all shrink-0">くわしく見る →</a>
    </div>
  </section>
{section("こんな方へ", "こんなお悩み、ありませんか。", '      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">' + chr(10) + target_html + chr(10) + '      </div>', alt=True, narrow=False)}
  <section class="py-16 md:py-24" id="story">
    <div class="pwrap max-w-[800px]">
      <h2 class="sec-ttl">研磨工場が、Webの仕事をはじめた理由</h2>
      <p class="story-quote my-10">技術があるのに、知られていない。<br/>それは、もったいない。</p>
      <div class="story">
        <p>松本研磨工業は、1967年から川崎で金属を磨いてきた小さな工場です。マツケンスタジオを担当する私は、その社長の息子です。鏡のように仕上げる父たちの技術には、今も誇りを持っています。</p>
        <p>一方で私自身は、上場企業に勤めるなど、10年以上デジタルマーケティングの仕事をしてきました。マーケターとして企業のオウンドメディアを50万PVまで育て、数百社の集客をお手伝いし、1,000万人以上が使うサービスのマーケティングも担当してきました。</p>
        <p>その目で家業を見たとき、もどかしさを感じました。いい技術があるのに、それを知ってもらう手段がほとんどない。町工場の仕事は長く紹介や付き合いが中心でしたが、いまは発注する側も、まずインターネットで探します。</p>
        <p>そこで、まず自分の家のサイトを一つずつ直すことから始めました。文字の読みやすさ、最初に目に入る画面、検索で見つけてもらうための書き方。担当者も大きな予算もない中で、何から手をつけるかを考えながら進めてきました。その結果、有効なお問い合わせの数は3倍に増えました。</p>
        <p>やってみて分かったのは、同じように困っている町工場や職人、小さな会社がたくさんあるということです。大きな会社のやり方をそのまま持ち込んでも、うまくいきません。予算も人手も限られた中で、何を優先するか。その両方を知っているからこそ、できるお手伝いがあると考えました。</p>
        <p>マツケンスタジオは、そうして生まれた松本研磨工業の新しい事業です。金属を少しずつ磨いて光らせるように、あなたの会社の良さを、分かりやすい言葉で、無理のない範囲から磨いていきます。</p>
      </div>
      <div class="mt-10">{LOGO}</div>
    </div>
  </section>

  <section class="py-14 md:py-20 st-alt" id="profile">
    <div class="pwrap max-w-[800px]">
      <h2 class="sec-ttl">責任者紹介</h2>
      <div class="bg-white border border-[#E1E5EB] rounded-lg p-7 md:p-10">
        <div class="text-[13px] font-bold text-accent-ink mb-1">マツケンスタジオ 責任者</div>
        <div class="text-[20px] md:text-[22px] font-bold mb-2">ディレクター／マーケター</div>
        <p class="text-[14px] leading-[2] text-ink-2 mb-6">家業の研磨工場に関わりながら、新しい事業としてマツケンスタジオを立ち上げました。ご相談から実際の作業まで、責任を持って担当します。</p>
        <ul class="svc-list">
          <li>デジタルマーケティング業界で10年以上</li>
          <li>上場企業に勤務</li>
          <li>マーケターとして、企業のオウンドメディアを50万PVまで育成</li>
          <li>これまでに数百社の集客を支援</li>
          <li>事業会社で、1,000万人以上が使うサービスのマーケティングを担当</li>
        </ul>
      </div>
    </div>
  </section>

{section("大切にしていること", "マツケンスタジオの3つの約束", cards(values), narrow=False)}
{mid_cta("まずは、今の状況をお聞かせください。相談は無料です。", C)}
  <section class="py-14 md:py-20" id="services">
    <div class="pwrap">
      <h2 class="sec-ttl">Web集客・AI活用支援のサービス一覧</h2>
      <p class="text-[15px] text-muted mb-10">戦略づくりから制作、AIの活用まで、まとめてご相談いただけます。</p>
{chr(10).join(svc_blocks)}
    </div>
  </section>

{section("実績", "実績・事例", CASE_CARD.format(href="case/"), alt=True)}
{section("流れ", "ご相談の流れ", step_html)}
{final_cta(C)}
'''
    open(f, 'w', encoding='utf-8').write(studio_chrome(head + main + tail, '../'))
    print('built hub')


# ---- Web集客ページ専用のヘッダー・メニュー・フッター（会社の電話・研磨フォームを出さず、専用フォームだけ） ----
def studio_chrome(s, pre):
    s = re.sub(r'\s*<!-- Phone — hidden below md -->\s*<a href="tel:0443338412" class="hidden md:flex.*?</a>', '', s, count=1, flags=re.S)
    s = s.replace(f'<a href="{pre}contact/" class="inline-flex items-center gap-[10px] px-3 py-2',
                  f'<a href="{pre}web-ai/contact/" class="inline-flex items-center gap-[10px] px-3 py-2', 1)
    s = re.sub(r'\s*<a href="tel:0443338412" data-close class="flex-1.*?</a>', '', s, count=1, flags=re.S)
    s = s.replace(f'<a href="{pre}contact/" data-close class="flex-1', f'<a href="{pre}web-ai/contact/" data-close class="flex-1', 1)
    s = re.sub(r'<div class="pt-5 font-mono text-\[10px\] tracking-\[\.1em\] text-muted-ink/70 text-center">044-333-8412[^<]*</div>',
               '<div class="pt-5 text-[11px] text-muted-ink/80 text-center">マツケンスタジオへのご相談は、お問い合わせフォームで受け付けています</div>', s, count=1)
    s = s.replace('<br/>電話 044-333-8412 ／ FAX 044-333-3843', '')
    s = re.sub(r'\s*<li>\s*<a href="tel:0443338412" class="font-serif[^"]*">044-333-8412</a>\s*<div class="font-mono[^"]*">[^<]*<br/>[^<]*</div>\s*</li>', '', s, count=1, flags=re.S)
    s = s.replace(f'<li><a href="{pre}contact/"   class="font-serif', f'<li><a href="{pre}web-ai/contact/"   class="font-serif', 1)
    # 以前入れていたLINE関連の名残を消す
    s = re.sub(r'\s*<div class="line-only">.*?</div>\s*</div>', '', s, flags=re.S)
    s = re.sub(r'\s*<li><a href="#line"[^>]*>.*?</a></li>', '', s, flags=re.S)
    s = re.sub(r'<a href="#line"[^>]*>.*?</a>', '', s, flags=re.S)
    s = re.sub(r'<style>\s*/\* studio-chrome \*/.*?</style>\s*', '', s, flags=re.S)
    s = s.replace('フォームかLINEで受け付けています', 'お問い合わせフォームで受け付けています')
    s = footer.apply(s, pre, studio=True)
    return s

def studio_chrome_all():
    for f in ['web-ai/index.html'] + sorted(glob.glob('web-ai/*/index.html')):
        s = open(f, encoding='utf-8').read()
        t = studio_chrome(s, '../' * f.count('/'))
        if t != s:
            open(f, 'w', encoding='utf-8').write(t)

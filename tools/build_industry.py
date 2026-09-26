"""業種別ホームページ制作ページ（/web-ai/website/<slug>/）を作る。
使い方（リポジトリのルートで）:
  python3 tools/build_industry.py && python3 tools/structured_data.py && python3 tools/llms_txt.py && python3 tools/subset_fonts.py
  npx tailwindcss -i css/input.css -o css/tailwind.css --minify
制作イメージの画像は node output/industry-mock/render.js で作り直す。
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
exec(open(os.path.join(HERE, 'build_webai.py'), encoding='utf-8').read())
from industry_pages import INDUSTRIES

LP = '../../monitor/'
EXTRA_CSS = '''<style>
  .vw-list li{list-style:none;display:grid;grid-template-columns:28px 1fr;gap:10px;padding:12px 0;border-bottom:1px solid #EEF1F5;font-size:15px;line-height:1.8}
  .vw-list li::before{content:'';width:22px;height:22px;border-radius:50%;margin-top:3px;background:#1B3A6B url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'><path d='M6 12l4 4 8-9'/></svg>") center/14px no-repeat}
  .mock{display:grid;grid-template-columns:1fr;gap:18px;align-items:end}
  @media(min-width:768px){.mock{grid-template-columns:1fr 170px}}
  .mock figure{margin:0}
  .mock img{display:block;width:100%;height:auto;border-radius:10px;box-shadow:0 24px 48px -28px rgba(14,14,16,.5);border:1px solid #E1E5EB}
  .mock .sp img{border-radius:18px;border:6px solid #0E0E10}
  .mock figcaption{font-size:12px;color:#5E5E65;margin-top:8px}
  .ind-links{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
  @media(min-width:768px){.ind-links{grid-template-columns:repeat(4,1fr)}}
  .ind-links a{display:block;background:#fff;border:1px solid #E1E5EB;border-radius:8px;padding:16px 18px;font-weight:700;font-size:15px}
  .ind-links a:hover{border-color:#1B3A6B}
  .ind-links a.current{color:#8a8a86;pointer-events:none}
</style>
'''


def industry_links(current):
    out = ''.join(f'<a href="../{i["slug"]}/" class="{"current" if i["slug"] == current else ""}">{i["title"].replace("のホームページ制作", "")} →</a>' for i in INDUSTRIES)
    return f'      <div class="ind-links">{out}</div>\n      <p class="mt-5 text-[14px]"><a href="../" class="font-bold text-accent-ink hover:underline">サイト制作のサービス全体を見る →</a></p>'


def build_industry(p):
    shell = open(SERVICE_SHELL, encoding='utf-8').read()
    shell = shell.replace('href="../../', 'href="../../../').replace('src="../../', 'src="../../../')  # 1階層深いので相対パスを直す
    head, tail = shell[:shell.index('<main')], shell[shell.index('</main>'):]
    url = f'{BASE}/web-ai/website/{p["slug"]}/'
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}
    head = set_meta(head, f'{p["title"]}｜マツケンスタジオ by 松本研磨工業', p['desc'], url,
                    [crumbs([('ホーム', f'{BASE}/'), ('Web集客・AI活用支援', f'{BASE}/web-ai/'), ('サイト制作', f'{BASE}/web-ai/website/'), (p['title'], url)]), faq_ld])
    head = head.replace('</head>', EXTRA_CSS + '</head>', 1)
    C = '../../contact/'
    viewers = '      <ul class="vw-list">' + ''.join(f'<li>{v}</li>' for v in p['viewers']) + '</ul>'
    pages = illust.sitemap(p['pages'], f'{p["name"]}のホームページに入れたいページの構成図')
    pts = ''.join(f'<li>{x}</li>' for x in p['mock_points'])
    faqs = '\n'.join(f'''      <div class="faq2">
        <div class="qa">Q</div>
        <div>
          <div class="font-bold text-[14px] mb-2">{q}</div>
          <p class="text-[13px] leading-[1.9] text-muted">{a}</p>
        </div>
      </div>''' for q, a in p['faq'])
    mock = f'''      <div class="mock">
        <figure><img src="../../../images/web-ai/industry/{p["slug"]}-pc.jpg" alt="{p["name"]}のホームページの制作イメージ（パソコン）" width="1440" height="900" loading="lazy"></figure>
        <figure class="sp"><img src="../../../images/web-ai/industry/{p["slug"]}-sp.jpg" alt="{p["name"]}のホームページの制作イメージ（スマホ）" width="780" height="1560" loading="lazy"></figure>
      </div>
      <p class="text-[12px] text-muted mt-3">制作イメージ</p>
      <h3 class="font-bold text-[17px] mt-8 mb-3">このデザインで考えたこと</h3>
      <ul class="svc-list">{pts}</ul>'''
    price = f'''      <div class="bg-white border border-[#E1E5EB] rounded-lg p-6 md:p-8">
        <p class="text-[14px] md:text-[15px] leading-[2] text-ink-2 mb-2">ページ数と内容で変わります。いまは「事例づくりモニター」として、毎月3社まで特別な価格でお受けしています（2〜5ページ 30万円〜・税別）。</p>
        <a href="{LP}" class="text-[14px] font-bold text-accent-ink hover:underline">モニター価格と内容を見る →</a>
        <div class="mt-6 flex flex-col sm:flex-row gap-3">{btn_main(C)}{btn_line()}</div>
      </div>'''
    main = f'''<main class="pt-[60px]">

  <section class="st-hero pt-7 pb-12 md:py-20">
    <div class="pwrap relative z-10">
      <p class="font-mono text-[11px] tracking-[.2em] text-muted mb-4 md:mb-8">
        <a href="../../../" class="hover:text-accent transition-colors">ホーム</a>
        <span class="mx-2 opacity-40">/</span>
        <a href="../../" class="hover:text-accent transition-colors">Web集客・AI活用支援</a>
        <span class="mx-2 opacity-40">/</span>
        <a href="../" class="hover:text-accent transition-colors">サイト制作</a>
        <span class="mx-2 opacity-40">/</span>{p["name"]}
      </p>
      <div class="mb-4 md:mb-8">{LOGO}</div>
      <div class="font-mono text-[12px] font-bold tracking-[.16em] text-accent-ink mb-3">町工場発のホームページ制作</div>
      <h1 class="font-bold leading-[1.3] mb-3 md:mb-5 text-ink" style="font-size:clamp(28px,4.8vw,50px)">{p["title"]}</h1>
      <p class="text-[16px] md:text-[19px] font-bold text-ink leading-[1.7] max-w-[680px] mb-3">{p["catch"]}</p>
      <p class="text-[14px] md:text-[15px] text-muted leading-[1.9] max-w-[680px]">{p["lead"]}</p>
      <div class="mt-6 md:mt-9 flex flex-col sm:flex-row gap-2.5 md:gap-3 sm:items-center">{btn_main(C)}{btn_line()}</div>
{trust()}
    </div>
  </section>

{section("", p["name"] + "のホームページで、よくある悩み", cards(p["pains"], cols=2), alt=True, narrow=False)}
{section("", p["viewers_title"], '      <div class="grid grid-cols-1 md:grid-cols-[1fr_260px] gap-6 md:gap-10 items-center"><div>' + viewers + '</div><div class="max-w-[240px] md:max-w-none mx-auto w-full">' + illust.ILLUST["btob-marketing" if p["slug"] in ("manufacturing", "construction") else "website"] + '</div></div>')}
{section("", p["name"] + "のホームページに入れたいページ", '      <div class="bg-white border border-[#E1E5EB] rounded-lg p-4 md:p-6">' + pages + '</div>' + chr(10) + f'      <p class="text-[14px] md:text-[15px] leading-[2] text-ink-2 mt-6">{p["pages_note"]}</p>', alt=True, narrow=False)}
{section("", p["name"] + "のホームページの制作イメージ", mock, narrow=False)}
{mid_cta("まずは、今の状況をお聞かせください。相談は無料です。", C)}
{section("", "採用と、AI検索・Googleマップにも", cards([("採用にも効くホームページに", p["recruit"]), ("AI検索・Googleマップにも伝わる形に", p["ai"])], cols=2, icons=["person", "search"]), narrow=False)}
{section("", "料金の目安", price, alt=True)}
{section("実績", "実績・事例", CASE_CARD.format(href="../../case/"))}
{section("", p["name"] + "のホームページ制作でよくある質問", faqs, alt=True)}
{section("", "業種別のホームページ制作", industry_links(p["slug"]), narrow=False)}
{final_cta(C)}
'''
    os.makedirs(f'web-ai/website/{p["slug"]}', exist_ok=True)
    html = studio_chrome(head + main + tail, '../../../')
    open(f'web-ai/website/{p["slug"]}/index.html', 'w', encoding='utf-8').write(html)
    print('built', p['slug'])


if __name__ == '__main__':
    for p in INDUSTRIES:
        build_industry(p)

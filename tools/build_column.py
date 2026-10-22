"""Web集客コラム（/web-ai/column/）を作る：トップ・カテゴリ・記事・著者ページ。
使い方（リポジトリのルートで）:
  python3 tools/build_column.py && python3 tools/structured_data.py && python3 tools/footer.py && python3 tools/llms_txt.py && python3 tools/subset_fonts.py
  npx tailwindcss -i css/input.css -o css/tailwind.css --minify
記事の原稿は tools/column_posts.py。記事が3本未満のカテゴリは検索に出さない（noindex）。
"""
import os, sys, json, re, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
exec(open(os.path.join(HERE, 'build_webai.py'), encoding='utf-8').read())
from column_posts import CATEGORIES, POSTS

COL = f'{BASE}/web-ai/column/'
CAT = {k: (name, desc) for k, name, desc in CATEGORIES}
MIN_INDEX = 3   # これ未満の記事数のカテゴリは noindex
STUDIO_ID = f'{BASE}/web-ai/#studio'
ORG_ID = f'{BASE}/#organization'
AUTHOR_NAME = 'マツケンスタジオ 責任者'
AUTHOR_BIO = ('デジタルマーケティングの仕事を10年以上。上場企業での勤務や、1,000万人以上が使うサービスのマーケティングを経験し、'
              'マーケターとして企業のオウンドメディアを50万PVまで育て、数百社の集客を支援してきました。'
              '家業である松本研磨工業のホームページを作り直し、リニューアルから1か月で有効なお問い合わせを3倍にしています。')

FIGS = {
    'cost': lambda: illust.cost_blocks(),
    'choose': lambda: illust.checklist(['業種の理解', '任せられる範囲', 'ドメインの名義', '作ったあとの更新', '窓口が同じか', '見積りの内訳', '契約とやめるとき'], '制作会社を選ぶときに確かめたい7つのことの図'),
    'signs': lambda: illust.six_signs(),
    'pages': lambda: illust.pages_compare(),
    'story': lambda: illust.flow_story(),
    'estimate': lambda: illust.checklist(['ページ数と中身', '原稿は誰が書くか', '写真・撮影', '自分で更新できる範囲', 'ドメインの名義', '公開後の修正の扱い'], '見積りで確かめたい6つのことの図'),
    'ai': lambda: illust.ILLUST['llmo-consulting'],
    'gbp': lambda: illust.checklist(['会社名・住所・電話', 'カテゴリ', '営業時間', 'ホームページのURL', '写真', '口コミへの返信'], 'Googleビジネスプロフィールで整えたい6つのことの図'),
    'recruit': lambda: illust.checklist(['仕事内容', '一日の流れ', '覚えていく流れ', '給与・休日', '現場の写真', '先輩の声'], '採用ページに載せたい6つのことの図'),
    'llms': lambda: illust.llms_file(),
    'meo': lambda: illust.three_factors(),
    'rcost': lambda: illust.checklist(['ページ数', '原稿と写真', 'デザイン・機能', '今のサイトの確認', '内容の引っ越し', 'アドレスの引き継ぎ'], 'リニューアル費用が決まる要素の図'),
    'interview': lambda: illust.checklist(['入社のきっかけ', '今の仕事', '一日の流れ', '覚えていく流れ', '大変なこと', '求職者へひとこと'], '社員インタビューで聞きたい6つのことの図'),
    'hbmock': lambda: '<figure style="margin:26px 0"><img src="../../../images/web-ai/industry/home-builder-pc.jpg" alt="工務店のホームページの制作イメージ" width="1440" height="900" loading="lazy" style="width:100%;height:auto;border-radius:10px;border:1px solid #E1E5EB"><figcaption style="font-size:12px;color:#5E5E65;margin-top:6px">制作イメージ（マツケンスタジオ）</figcaption></figure>',
    'mfg': lambda: illust.sitemap(['加工内容', '設備一覧', '加工事例', '品質管理', '会社概要', '採用', 'よくある質問', 'お問い合わせ'], '製造業のホームページのページ構成の図'),
    'flow': lambda: illust.checklist(['相談', '構成', '文章と写真', 'デザイン', '確認と修正', '公開'], 'ホームページ制作の6つの段階の図'),
    'photos': lambda: illust.checklist(['建物の外観', '作業の様子', '設備', '製品・事例', '働く人', '代表者'], 'ホームページ用に撮っておきたい6つの写真の図'),
    'subsidy': lambda: illust.checklist(['対象になる会社か', '対象になる費用か', '申請の締切', '発注してよい時期', '支払いは後払い', '公開後の報告'], '補助金を使う前に確かめたい6つのことの図'),
    'cheap': lambda: illust.checklist(['5年間の総額', '最低契約期間', 'やめたあとのサイト', 'ドメインの名義', '文章と写真は誰が', '修正できる範囲'], '格安・月額制のホームページで確かめたい6つのことの図'),
    'switch': lambda: illust.checklist(['契約書を確かめる', '名義と権限を確かめる', '引き継ぐものを集める', '新しい会社を決める', '切り替える', '前の契約をやめる'], '制作会社を乗り換える6つの手順の図'),
    'ssl': lambda: illust.checklist(['証明書を入れる', 'httpsで表示を確かめる', '古いアドレスから転送', 'ページ内のhttpを直す', '外部の登録先を直す', '証明書の期限を確かめる'], 'ホームページをSSL化する6つの手順の図'),
    'domain': lambda: illust.checklist(['ドメインの契約先', 'サーバーの契約先', '契約の名義', '管理画面のID', '更新日と支払い方法', 'メールの設定先'], 'ドメインとサーバーで確かめたい6つのことの図'),
    'wp': lambda: illust.checklist(['更新する回数', '更新する人がいるか', '更新するページの種類', '保守を任せる先', '毎月の費用', '使いたい機能'], 'WordPressを使うか決めるときに確かめたい6つのことの図'),
    'upkeep': lambda: illust.checklist(['ドメイン代', 'サーバー代', 'SSL証明書', '保守・更新の作業', '機能やサービスの利用料', '写真や素材の利用料'], 'ホームページの維持費の内訳の図'),
    'inquiry': lambda: illust.checklist(['見られている数', '検索された言葉', '最初の画面', '頼めることの書き方', '実績と費用の目安', '問い合わせの入口'], '問い合わせが来ないときに確かめたい6つのことの図'),
    'apply': lambda: illust.checklist(['求人の言葉', '給与と休みの書き方', '仕事の中身', '働く人の顔', '会社のホームページ', '応募の手軽さ'], '応募が来ないときに見直したい6つのことの図'),
    'build': lambda: illust.sitemap(['事業内容', '施工実績', '許可・資格', '安全への取り組み', '会社概要', '採用', '協力会社募集', 'お問い合わせ'], '建設業のホームページのページ構成の図'),
    'truck': lambda: illust.sitemap(['輸送サービス', '車両・設備', '対応エリア', '安全への取り組み', '会社概要', 'ドライバー募集', 'よくある質問', 'お見積り'], '運送会社のホームページのページ構成の図'),
    'studio': lambda: illust.checklist(['パスワードの変更', '同じパスワードの変更', 'プレビューURLの削除', 'APIキーの切り替え', 'フォームの回答の確認', '不審なメールに注意'], 'Studioの不正アクセスで、利用者がまず行う6つのことの図'),
    'llmo': lambda: illust.checklist(['言葉の違いを知る', '検索の基本が土台', '会社の情報を文章で', '表記をどこでも統一', '同じ質問で定点観測', '保証する業者に注意'], 'LLMO対策とは？AIO・GEOとの違いと、中小企業のやり方・業者の見分け方の要点の図'),
    'homepage-diy': lambda: illust.checklist(['作る目的を決める', '作り方を選ぶ', 'ドメインは自社名義', '文章と写真を用意', '管理の担当を決める', '公開後も更新する'], 'ホームページを自分で作るには？会社で自作するときの方法と注意点の要点の図'),
    'seo-self': lambda: illust.checklist(['狙う言葉を決める', '事業ごとにページ', 'タイトルと説明文', '事例とよくある質問', 'Search Console', 'Googleマップ'], 'SEO対策は自分でできる？中小企業が今日から始めるやり方と注意点の要点の図'),
    'nocode-migration': lambda: illust.checklist(['今回の対応を済ませる', '乗り換える理由を書く', '契約と更新日を確認', '移すものを洗い出す', 'URLの対応表を作る', '切り替えは最後に'], 'ホームページをノーコードから乗り換えるには？移行の手順と注意点の要点の図'),
    'php-vulnerability': lambda: illust.checklist(['PHPを使っているか', 'PHPのバージョン', 'サーバー会社の案内', '制作会社への確認', '古いサイトの棚卸し', '更新後の確認'], 'PHPの脆弱性（PHP2Shell）とは？自社サイトの確かめ方と対応【10月22日時点】の要点の図'),
    'wordpress-migration': lambda: illust.checklist(['不安の正体を知る', '乗り換えが要るか確認', '乗り換え先を比べる', '移すものを洗い出す', 'URLの対応表を作る', '切り替えは最後に'], 'WordPressから乗り換えるには？乗り換え先の比べ方と移行の手順の要点の図'),
    'static-site': lambda: illust.checklist(['決まったページを配る', 'PHPやDBを使わない', '表示が速い', '攻撃の入口が少ない', '更新には知識がいる', '2段階認証は必須'], '静的サイトとは？動的サイトとの違い、メリット・デメリットと向いている会社の要点の図'),
    'wordpress-security': lambda: illust.checklist(['本体・プラグイン更新', '使わない物を削除', '強いパスワード', '2段階認証', 'バックアップ', '点検の担当を決める'], 'WordPressのセキュリティ対策の要点の図'),
    'wordpress-php-version': lambda: illust.checklist(['今のバージョン確認', 'サポート期間の確認', 'バックアップ', '本体・プラグイン更新', 'PHPの切り替え', '表示と動きの確認'], 'WordPressのPHPバージョンとは？確認方法と安全な更新の手順・注意点の要点の図'),
    'wordpress-hacked': lambda: illust.checklist(['慌てて消さない', '画面と時刻を記録', 'サイトを一時停止', '制作・サーバー会社へ', 'パスワードを変更', '復旧して再審査'], 'WordPressの改ざんの対処法の要点の図'),
    'lp': lambda: illust.checklist(['最初の画面', '悩みへの共感', 'サービスの内容', '実績・お客様の声', 'よくある質問', '問い合わせの入口'], 'LPに入れたい6つの要素の図'),
}

CSS = '''<style>
  .col-cats{display:flex;flex-wrap:wrap;gap:8px}
  .col-cats a{font-size:13px;font-weight:700;padding:7px 14px;border-radius:999px;background:#fff;border:1px solid #E1E5EB;color:#1B3A6B}
  .col-cats a:hover,.col-cats a.on{background:#1B3A6B;color:#fff;border-color:#1B3A6B}
  .col-grid{display:grid;grid-template-columns:1fr;gap:18px}
  @media(min-width:768px){.col-grid{grid-template-columns:repeat(2,1fr)}}
  @media(min-width:1024px){.col-grid.three{grid-template-columns:repeat(3,1fr)}}
  .col-card{display:flex;flex-direction:column;background:#fff;border:1px solid #E1E5EB;border-radius:10px;padding:22px 22px 18px;transition:border-color .2s,box-shadow .2s}
  .col-card:hover{border-color:#1B3A6B;box-shadow:0 10px 30px -16px rgba(27,58,107,.35)}
  .chip{display:inline-block;font-size:12px;font-weight:700;color:#1B3A6B;background:#FFF4B0;border-radius:999px;padding:3px 10px}
  .col-card h3{font-size:17px;font-weight:700;line-height:1.6;margin:12px 0 8px;color:#0E0E10}
  .col-card p{font-size:13px;line-height:1.8;color:#5E5E65;flex:1}
  .col-card time{font-size:12px;color:#8a8a86;margin-top:12px;font-family:'JetBrains Mono',monospace}
  .art{max-width:760px;margin:0 auto}
  .art-body h2{font-size:22px;font-weight:700;line-height:1.5;margin:48px 0 16px;padding-left:14px;border-left:5px solid #F5DE00;scroll-margin-top:90px}
  @media(min-width:768px){.art-body h2{font-size:25px}}
  .art-body h3{font-size:18px;font-weight:700;margin:28px 0 10px;color:#1B3A6B}
  .art-body p{font-size:16px;line-height:2;color:#26262B;margin-bottom:18px}
  .art-body ul,.art-body ol{margin:0 0 20px 1.4em;font-size:16px;line-height:1.9;color:#26262B}
  .art-body li{margin-bottom:6px}
  .art-body ul,.points ul{list-style:disc}
  .art-body ol,.toc ol{list-style:decimal}
  .art-body li::marker,.points li::marker{color:#1B3A6B}
  .art-body a{color:#1B3A6B;font-weight:700;text-decoration:underline;text-underline-offset:3px}
  .art-body .st-illu{margin:26px auto}
  .art-table{width:100%;border-collapse:collapse;margin:8px 0 24px;font-size:14px;background:#fff;border:1px solid #E1E5EB}
  .art-table th,.art-table td{padding:12px 14px;border-bottom:1px solid #EEF1F5;text-align:left;vertical-align:top;line-height:1.7}
  .art-table th{background:#F4F6F9;font-weight:700;color:#1B3A6B}
  .art-body p.ask{font-size:14px;line-height:1.8;background:#F4F6F9;border-left:4px solid #1B3A6B;border-radius:0 8px 8px 0;padding:10px 14px;color:#26262B}
  .points{background:#FFF9D6;border-radius:10px;padding:20px 24px;margin:26px 0}
  .points b{display:block;font-size:14px;margin-bottom:8px;color:#1B3A6B}
  .points li{font-size:15px;line-height:1.8;margin-left:1.2em}
  .toc{background:#F4F6F9;border-radius:10px;padding:20px 24px;margin:0 0 30px}
  .toc b{display:block;font-size:14px;margin-bottom:8px}
  .toc ol{margin-left:1.3em;font-size:14px;line-height:2}
  .toc a{color:#1B3A6B}
  .author{display:grid;grid-template-columns:56px 1fr;gap:16px;background:#fff;border:1px solid #E1E5EB;border-radius:12px;padding:22px}
  .author .av{width:56px;height:56px;border-radius:14px;background:#1B3A6B;color:#fff;display:grid;place-items:center;font-weight:700;font-size:24px;position:relative}
  .author .av::after{content:'';position:absolute;right:-3px;top:-3px;width:14px;height:14px;border-radius:50%;background:#F5DE00;border:2px solid #fff}
  .author b{font-size:15px}.author p{font-size:13px;line-height:1.9;color:#4A4A50;margin-top:6px}
  .art-body .cta-mid a{text-decoration:none}
  .art-body .cta-mid a.bg-cta-yellow{color:#0E0E10}
  .art-body .cta-mid a[href*="line.me"]{color:#fff}
  .cta-top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;border:1px solid #E1E5EB;border-radius:12px;padding:14px 18px;margin:-8px 0 26px;background:#fff}
  .cta-top p{font-size:14px;font-weight:700;color:#0E0E10}
  .cta-top .bt{display:flex;gap:8px;flex-wrap:wrap}
  .cta-top a.btn-s{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:700;border-radius:999px;padding:9px 16px}
  .cta-mid{margin:36px 0;border-radius:14px;background:#FFF9D6;padding:24px 24px 22px;position:relative;overflow:hidden}
  .cta-mid::after{content:'';position:absolute;right:-50px;top:-50px;width:160px;height:160px;border-radius:50%;background:repeating-radial-gradient(circle,rgba(27,58,107,.08) 0 1px,transparent 1px 10px)}
  .cta-mid .lb{display:inline-block;font-size:12px;font-weight:700;color:#fff;background:#1B3A6B;border-radius:999px;padding:3px 10px;margin-bottom:10px}
  .cta-mid b{display:block;font-size:18px;line-height:1.6;margin-bottom:6px;color:#0E0E10}
  .cta-mid p{font-size:14px;line-height:1.8;color:#3A3A40;margin-bottom:16px;position:relative;z-index:1}
  .cta-mid .bt{display:flex;flex-direction:column;gap:10px;position:relative;z-index:1}
  @media(min-width:640px){.cta-mid .bt{flex-direction:row}}
  .cta-end{border-radius:16px;background:#1B3A6B;color:#fff;padding:28px 26px}
  .cta-end b{display:block;font-size:20px;line-height:1.6;margin-bottom:8px}
  .cta-end p{font-size:14px;line-height:1.9;color:rgba(255,255,255,.85);margin-bottom:18px}
  .cta-end .bt{display:flex;flex-direction:column;gap:10px}
  @media(min-width:640px){.cta-end .bt{flex-direction:row;align-items:center}}
  .cta-end .lp{font-size:14px;font-weight:700;color:#F5DE00;text-decoration:underline;text-underline-offset:3px}
  .col-stick{position:fixed;left:0;right:0;bottom:0;z-index:40;display:flex;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.96);border-top:1px solid #E1E5EB;transform:translateY(110%);transition:transform .25s}
  .col-stick.show{transform:none}
  .col-stick a{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:6px;border-radius:999px;padding:12px 8px;font-size:14px;font-weight:700}
  @media(min-width:768px){.col-stick{display:none}}
  .soft-cta{background:#fff;border:1px solid #E1E5EB;border-radius:12px;padding:24px;display:flex;flex-direction:column;gap:14px}
  @media(min-width:768px){.soft-cta{flex-direction:row;align-items:center;justify-content:space-between}}
  .soft-cta p{font-size:14px;line-height:1.8;color:#26262B}
</style>
'''


def shell_parts(depth):
    """depth: web-ai/column = 2, 記事 = 3, カテゴリ = 4"""
    shell = open(SERVICE_SHELL, encoding='utf-8').read()   # depth2 の殻
    if depth != 2:
        shell = shell.replace('href="../../', 'href="' + '../' * depth).replace('src="../../', 'src="' + '../' * depth)
    return shell[:shell.index('<main')], shell[shell.index('</main>'):]


def page(path, depth, title, desc, url, ld, main, noindex=False):
    head, tail = shell_parts(depth)
    head = set_meta(head, title, desc, url, ld)
    head = head.replace('</head>', CSS + '</head>', 1)
    head = re.sub(r'\s*<meta name="robots"[^>]*>', '', head)
    if noindex:
        head = re.sub(r'(<meta charset="[^"]+"\s*/?>)', r'\1\n<meta name="robots" content="noindex, follow">', head, count=1, flags=re.I)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(studio_chrome(head + main + tail, '../' * depth))
    print('built', path)


def crumb_html(items, pre):
    parts = []
    for i, (name, href) in enumerate(items):
        if href is None:
            parts.append(name)
        else:
            parts.append(f'<a href="{href}" class="hover:text-accent transition-colors">{name}</a>')
    return ('      <p class="font-mono text-[11px] tracking-[.2em] text-muted mb-5">'
            + '<span class="mx-2 opacity-40">/</span>'.join(parts) + '</p>')


def updated_html(p):
    """書き直した記事だけ、更新日を表示する（updated を column_posts.py に書く）"""
    u = p.get('updated')
    return f'　／　更新日 <time datetime="{u}">{fmt_date(u)}</time>' if u and u != p['date'] else ''


def fmt_date(d):
    return d.replace('-', '.')


def card(p, pre):
    return (f'<a href="{pre}{p["slug"]}/" class="col-card"><span><span class="chip">{CAT[p["category"]][0]}</span></span>'
            f'<h3>{p["title"]}</h3><p>{p["description"][:70]}…</p><time datetime="{p["date"]}">{fmt_date(p["date"])}</time></a>')


def cat_nav(pre, on=None):
    items = [f'<a href="{pre}" class="{"" if on else "on"}">すべて</a>']
    for k, name, _ in CATEGORIES:
        items.append(f'<a href="{pre}category/{k}/" class="{"on" if k == on else ""}">{name}</a>')
    return '<nav class="col-cats" aria-label="カテゴリ">' + ''.join(items) + '</nav>'


def counts():
    c = {k: 0 for k, _, _ in CATEGORIES}
    for p in POSTS:
        c[p['category']] += 1
    return c


def hero(title, lead, crumbs_html, pre_logo=True):
    return f'''  <section class="st-hero pt-7 pb-10 md:py-16">
    <div class="pwrap relative z-10">
{crumbs_html}
      <div class="mb-4">{LOGO}</div>
      <h1 class="font-bold leading-[1.35] mb-3 text-ink" style="font-size:clamp(26px,4.2vw,42px)">{title}</h1>
      <p class="text-[14px] md:text-[15px] text-muted leading-[1.9] max-w-[680px]">{lead}</p>
    </div>
  </section>'''


MID_CTA = {
    'cost': ('費用や見積りで迷ったら', '見積りの内容が分からない、何にいくらかかるのか知りたい。そんな段階でも、気軽にご相談ください。'),
    'renewal': ('今のサイト、作り直したほうがいい？', '今のホームページを見て、直したほうがいいところを無料でお伝えします。ドメインもメールもそのままで作り直せます。'),
    'homepage': ('何から始めればいいか分からない方へ', '載せたい内容がまとまっていなくても大丈夫です。聞き取りをしながら、合うページ構成をご提案します。'),
    'ai': ('自社がAIにどう紹介されるか、気になったら', '今のホームページが、AIや検索にどう伝わっているかを確かめて、直すところをお伝えします。'),
    'seo': ('Googleマップや検索で見つけてもらいたい方へ', 'Googleマップの登録・整備から、検索で見つけてもらうためのホームページづくりまでお手伝いします。'),
    'recruit': ('応募が来ない、と感じたら', '採用ページだけを先に作ることもできます。現場の様子が伝わるページづくりをお手伝いします。'),
    'industry': ('業種に合ったホームページを作りたい方へ', '業種ごとに、取引先や求職者が見るところは違います。現場の話が通じる担当が、構成から一緒に考えます。'),
    'case': ('同じやり方で、御社のサイトも', '研磨工場のサイトで問い合わせを増やしたやり方で、ホームページづくりをお手伝いします。'),
}


def link_btns(C, size='md'):
    return f'{btn_main(C, size)}{btn_line(size)}'


def cta_top(C):
    return (f'<div class="cta-top"><p>ホームページのご相談は無料です</p><div class="bt">'
            f'<a href="{C}" class="btn-s bg-cta-yellow text-ink hover:bg-cta-yellow-h">1分で問い合わせ →</a>'
            f'<a href="{LINE_URL}" target="_blank" rel="noopener" class="btn-s bg-[#06C755] text-white hover:bg-[#05B34C]">LINEで相談</a></div></div>')


def cta_mid(cat, C):
    t, d = MID_CTA.get(cat, MID_CTA['homepage'])
    return f'<div class="cta-mid"><span class="lb">無料相談</span><b>{t}</b><p>{d}</p><div class="bt">{link_btns(C)}</div></div>'


def cta_end(C, LP):
    return (f'<div class="cta-end"><b>ホームページのこと、まずは気軽にご相談ください。</b>'
            f'<p>「何から始めればいいか分からない」という段階でも大丈夫です。町工場発のマツケンスタジオが、ドメインの取得から公開後の更新まで、まるごとお手伝いします。いまは毎月3社まで、特別な価格で制作する「事例づくりモニター」も受け付けています。</p>'
            f'<div class="bt">{link_btns(C)}<a href="{LP}" class="lp">事例づくりモニターを見る →</a></div></div>')


def sticky(C):
    return (f'<div class="col-stick" id="colStick"><a href="{C}" class="bg-cta-yellow text-ink">1分で問い合わせ</a>'
            f'<a href="{LINE_URL}" target="_blank" rel="noopener" class="bg-[#06C755] text-white">LINEで相談</a></div>'
            '<script>(function(){var s=document.getElementById("colStick");if(!s)return;function u(){s.classList.toggle("show",window.scrollY>500&&(window.innerHeight+window.scrollY)<document.body.scrollHeight-700)}window.addEventListener("scroll",u,{passive:true});u()})();</script>')


def insert_mid(body, block):
    """記事の真ん中あたりの見出し（h2）の前に入れる"""
    pos = [m.start() for m in re.finditer(r'<h2 id=', body)]
    if len(pos) < 3:
        return body + block
    i = pos[len(pos) // 2]
    return body[:i] + block + body[i:]


def soft_cta(C):
    return (f'<div class="soft-cta"><p>ホームページのことで気になることがあれば、気軽にご相談ください。<br>「何から始めればいいか分からない」という段階でも大丈夫です。</p>'
            f'<div class="flex flex-col sm:flex-row gap-3 shrink-0">{btn_main(C)}{btn_line()}</div></div>')


def build_index():
    posts = sorted(POSTS, key=lambda p: p['date'], reverse=True)
    pre = ''
    cards = ''.join(card(p, pre) for p in posts)
    lead = ('ホームページ制作やリニューアル、費用、AI検索対策、Googleマップ、採用など、現場と技術のある中小企業のWeb集客に役立つ情報をまとめています。'
            '町工場発のWeb事業「マツケンスタジオ」が、自社で試してきたことをもとに書いています。')
    main = f'''<main class="pt-[60px]">
{hero('Web集客コラム', lead, crumb_html([('ホーム', '../../'), ('Web集客・AI活用支援', '../'), ('コラム', None)], pre))}
{section("", "カテゴリから探す", '      ' + cat_nav(pre), narrow=False)}
{section("", "新着記事", '      <div class="col-grid three">' + cards + '</div>', alt=True, narrow=False)}
{section("", "このコラムを書いている人", author_box('author/'), narrow=True)}
{final_cta('../contact/')}
'''
    ld = [crumbs([('ホーム', f'{BASE}/'), ('Web集客・AI活用支援', f'{BASE}/web-ai/'), ('Web集客コラム', COL)])]
    page('web-ai/column/index.html', 2, 'Web集客コラム｜マツケンスタジオ by 松本研磨工業',
         'ホームページ制作・リニューアル・費用・AI検索対策・Googleマップ・採用など、現場と技術のある中小企業のWeb集客に役立つ情報をまとめたコラムです。町工場発のWeb事業「マツケンスタジオ」が、自社で試してきたことをもとに書いています。',
         COL, ld, main)


def author_box(href):
    return (f'<div class="author"><div class="av">松</div><div><b>{AUTHOR_NAME}</b>'
            f'<p>{AUTHOR_BIO}</p><a href="{href}" class="text-[13px] font-bold text-accent-ink hover:underline">プロフィールを見る →</a></div></div>')


def build_category(k):
    name, desc = CAT[k]
    posts = sorted([p for p in POSTS if p['category'] == k], key=lambda p: p['date'], reverse=True)
    pre = '../../'
    body = ('      <div class="col-grid three">' + ''.join(card(p, pre) for p in posts) + '</div>') if posts else \
           '      <p class="text-[14px] text-muted">このカテゴリの記事は、いま準備しています。</p>'
    main = f'''<main class="pt-[60px]">
{hero(name + 'の記事一覧', desc, crumb_html([('ホーム', '../../../../'), ('Web集客・AI活用支援', '../../../'), ('コラム', '../../'), (name, None)], pre))}
{section("", "カテゴリから探す", '      ' + cat_nav(pre, k), narrow=False)}
{section("", name + "の記事", body, alt=True, narrow=False)}
{final_cta('../../../contact/')}
'''
    url = f'{COL}category/{k}/'
    ld = [crumbs([('ホーム', f'{BASE}/'), ('Web集客・AI活用支援', f'{BASE}/web-ai/'), ('Web集客コラム', COL), (name, url)])]
    page(f'web-ai/column/category/{k}/index.html', 4, f'{name}の記事一覧｜Web集客コラム｜マツケンスタジオ',
         f'{desc}マツケンスタジオのWeb集客コラムから、{name}に関する記事をまとめています。', url, ld, main,
         noindex=len(posts) < MIN_INDEX)


def build_post(p):
    pre = '../'
    name = CAT[p['category']][0]
    body = p['body']
    for k, f in FIGS.items():
        body = body.replace('{{fig:' + k + '}}', f())
    toc = ''.join(f'<li><a href="#{i}">{H.unescape(re.sub("<[^>]+>", "", t))}</a></li>'
                  for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body))
    points = ''.join(f'<li>{x}</li>' for x in p['points'])
    faqs = '\n'.join(f'''      <div class="faq2">
        <div class="qa">Q</div>
        <div>
          <div class="font-bold text-[14px] mb-2">{q}</div>
          <p class="text-[13px] leading-[1.9] text-muted">{a}</p>
        </div>
      </div>''' for q, a in p['faq'])
    related = [x for x in POSTS if x['slug'] != p['slug'] and x['category'] == p['category']]
    related += [x for x in POSTS if x['slug'] != p['slug'] and x not in related]
    rel_html = ''.join(card(x, '../') for x in related[:3])
    C = '../../contact/'
    body = insert_mid(body, cta_mid(p['category'], C))
    main = f'''<main class="pt-[60px]">
  <section class="pt-8 pb-10 md:pt-12 md:pb-14">
    <div class="pwrap">
      <article class="art">
{crumb_html([('ホーム', '../../../'), ('Web集客・AI活用支援', '../../'), ('コラム', '../'), (name, f'../category/{p["category"]}/')], pre)}
        <a href="../category/{p["category"]}/" class="chip">{name}</a>
        <h1 class="font-bold leading-[1.45] mt-3 mb-4 text-ink" style="font-size:clamp(24px,3.6vw,34px)">{p["title"]}</h1>
        <p class="text-[13px] text-muted mb-6">公開日 <time datetime="{p["date"]}">{fmt_date(p["date"])}</time>{updated_html(p)}　|　{AUTHOR_NAME}</p>
        <div class="points"><b>この記事で分かること</b><ul>{points}</ul></div>
        {cta_top(C)}
        <nav class="toc" aria-label="目次"><b>目次</b><ol>{toc}<li><a href="#faq">よくある質問</a></li></ol></nav>
        <div class="art-body">{body}</div>
        <h2 id="faq" class="font-bold text-[22px] mt-12 mb-4" style="scroll-margin-top:90px">よくある質問</h2>
{faqs}
        <div class="mt-10">{author_box('../author/')}</div>
        <div class="mt-8">{cta_end(C, '../../monitor/')}</div>
      </article>
    </div>
  </section>
{section("", "あわせて読みたい記事", '      <div class="col-grid three">' + rel_html + '</div>', alt=True, narrow=False)}
{section("", "カテゴリから探す", '      ' + cat_nav('../'), narrow=False)}
{sticky(C)}
'''
    url = f'{COL}{p["slug"]}/'
    blog = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p['title'], "description": p['description'],
            "url": url, "image": f'{BASE}/images/ogp-studio.jpg', "datePublished": p['date'], "dateModified": p.get('updated', p['date']),
            "articleSection": name, "inLanguage": "ja",
            "author": {"@type": "Organization", "@id": STUDIO_ID, "name": "マツケンスタジオ", "url": f'{COL}author/'},
            "publisher": {"@id": ORG_ID}, "mainEntityOfPage": {"@type": "WebPage", "@id": url}}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}
    ld = [crumbs([('ホーム', f'{BASE}/'), ('Web集客・AI活用支援', f'{BASE}/web-ai/'), ('Web集客コラム', COL), (name, f'{COL}category/{p["category"]}/'), (p['title'], url)]), blog, faq_ld]
    page(f'web-ai/column/{p["slug"]}/index.html', 3, f'{p["title"]}｜マツケンスタジオ', p['description'], url, ld, main)


def build_author():
    main = f'''<main class="pt-[60px]">
{hero('このコラムを書いている人', 'マツケンスタジオのWeb集客コラムは、責任者が自分で試してきたことをもとに書いています。', crumb_html([('ホーム', '../../../'), ('Web集客・AI活用支援', '../../'), ('コラム', '../'), ('著者', None)], '../'))}
{section("", AUTHOR_NAME, f"""      <div class="author"><div class="av">松</div><div><b>{AUTHOR_NAME}（30代）</b><p>{AUTHOR_BIO}</p></div></div>
      <ul class="svc-list mt-6">
        <li>デジタルマーケティング業界で10年以上</li>
        <li>上場企業に勤務</li>
        <li>マーケターとして、企業のオウンドメディアを50万PVまで育成</li>
        <li>これまでに数百社の集客を支援</li>
        <li>事業会社で、1,000万人以上が使うサービスのマーケティングを担当</li>
        <li>松本研磨工業のホームページを作り直し、リニューアルから1か月で有効なお問い合わせが3倍に</li>
      </ul>""")}
{section("", "書いている記事", '      <div class="col-grid three">' + ''.join(card(p, '../') for p in sorted(POSTS, key=lambda p: p['date'], reverse=True)) + '</div>', alt=True, narrow=False)}
{final_cta('../../contact/')}
'''
    url = f'{COL}author/'
    ld = [crumbs([('ホーム', f'{BASE}/'), ('Web集客・AI活用支援', f'{BASE}/web-ai/'), ('Web集客コラム', COL), ('著者', url)])]
    page('web-ai/column/author/index.html', 3, 'このコラムを書いている人｜Web集客コラム｜マツケンスタジオ',
         'マツケンスタジオのWeb集客コラムを書いている責任者のプロフィールです。デジタルマーケティングの仕事を10年以上続け、家業の研磨工場のホームページでリニューアルから1か月で有効なお問い合わせを3倍にしました。', url, ld, main)


def update_sitemap():
    sm = open('sitemap.xml', encoding='utf-8').read()
    c = counts()
    urls = [COL, f'{COL}author/'] + [f'{COL}{p["slug"]}/' for p in POSTS] + [f'{COL}category/{k}/' for k in c if c[k] >= MIN_INDEX]
    noidx = [f'{COL}category/{k}/' for k in c if c[k] < MIN_INDEX]
    for u in noidx:
        sm = re.sub(r'\s*<url>\s*<loc>' + re.escape(u) + r'</loc>.*?</url>', '', sm, flags=re.S)
    for u in urls:
        if f'<loc>{u}</loc>' not in sm:
            sm = sm.replace('</urlset>', f'  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-09-27</lastmod>\n  </url>\n</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8').write(sm)


if __name__ == '__main__':
    build_index()
    for k, _, _ in CATEGORIES:
        build_category(k)
    for p in POSTS:
        build_post(p)
    build_author()
    update_sitemap()

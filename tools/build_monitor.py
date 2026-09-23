"""マツケンスタジオ「事例づくりモニター」LP（/web-ai/monitor/）を作る。

サイトのヘッダー・パンくず・フッターは使わない、単独のLP。問い合わせフォームもページ内に置く。
文章・価格はこのファイルで直す。
使い方（リポジトリのルートで）:
  python3 tools/build_monitor.py && python3 tools/structured_data.py && python3 tools/llms_txt.py && python3 tools/subset_fonts.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ogp_meta

BASE = 'https://matsumoto-kenma.co.jp'
URL = f'{BASE}/web-ai/monitor/'
# LINE公式アカウントの友だち追加URL（例: https://lin.ee/xxxxxxx）。空のあいだはLINEのボタンを出さない
LINE_URL = 'https://page.line.me/115rhdee'
TITLE = '町工場のホームページ制作｜事例づくりモニター（毎月3社まで）｜マツケンスタジオ by 松本研磨工業'
DESC = ('金属研磨の町工場・松本研磨工業が始めた、町工場・製造業のためのホームページ制作。'
        '事例として紹介させていただくことを条件に、特別な価格で制作します。ドメイン・サーバー・Googleマップの手続きから、公開後の更新までまとめてお任せください。毎月3社まで。')

PAINS = [
    '「うちは紹介で回ってるから」と、後回しにしてきた',
    '制作会社に話しても、図面や加工の話が通じない',
    '求人を出しても、若い人からの応募が来ない',
    'いくらかかるのか、何が必要なのかが分からない',
    'ドメインやサーバーと言われても、正直よく分からない',
    '作ったあと、誰が更新するのかが心配',
]

RENEW_PAINS = [
    '何年も前に作ったまま、更新していない',
    'スマホで見ると、文字が小さく見づらい',
    '自分たちでは直せない・頼んだ業者と連絡がつかない',
    'サイトはあるのに、問い合わせが来ない',
]
RENEW_DO = [
    ('今のドメイン・メールはそのまま', '会社のアドレスやメールを変えずに作り直せます。'),
    ('検索での評価を引き継ぐ', '今のページのアドレスを整理し、評価をできるだけ残します。'),
    ('今のサイトを診断', 'どこで見られて、どこで離れているかを確かめてから作ります。'),
    ('公開3か月後に成果を報告', '作り直して何が変わったかを、数字でお伝えします。'),
]

WHY_NOW = [
    ('応募する人は、まず会社を調べます', '求人を見た人は、応募する前にスマホで会社の名前を検索します。何も出てこないと、それだけで候補から外れてしまうことがあります。'),
    ('新しい取引先も、ネットで確かめます', '初めて取引する会社は、どんな設備で、何ができるのかをホームページで確認します。ないと、話を進めにくくなります。'),
    ('元請けだけに頼らない入口になります', '「この加工ができる会社」を探している人に、御社を見つけてもらえるようになります。'),
]

STRENGTHS = [
    ('図面も、公差も、そのまま通じます',
     '私たちも毎日、金属を磨いている町工場です。加工法、材質、公差、納期の感覚まで、説明しなくても分かります。社長が専門用語の説明に疲れることはありません。'),
    ('自分の会社で、結果を出したやり方です',
     '松本研磨工業のホームページを作り直し、検索対策を進めたことで、有効なお問い合わせが3倍になりました。机の上の理屈ではなく、町工場で実際に効いたやり方で作ります。'),
    ('面倒な手続きは、まるごと引き受けます',
     'ドメインの取得、サーバー、会社のメールアドレス、Googleマップの登録まで、私たちがすべて行います。すでにサイトがある場合も、今のドメインやメールを引き継いで作り直せます。'),
    ('大きな会社のやり方も、知っています',
     '担当するのは、上場企業などでデジタルマーケティングを10年以上続け、数百社の集客を支援してきた責任者です。最初の相談から公開後まで、同じ担当が見ます。'),
]

COMPARE = [
    ('加工や図面の話', 'その都度、説明が必要', 'そのまま通じる'),
    ('ドメイン・サーバー', '自分で契約・管理することが多い', '手続きはすべて代行'),
    ('ドメイン・サイトの名義', '制作会社の名義のことも', 'いつでも御社の名義'),
    ('作ったあと', '更新は別料金・放置になりがち', '3か月無料、その後も月額で'),
    ('窓口', '営業・制作・保守で担当が変わる', '最初から最後まで同じ担当'),
]

PLANS = [
    ('1ページ', '15', 'サービスや事業を、1枚のページでしっかり伝えたい',
     ['縦に長い1枚のページ（LP）', '特徴・強み・お客様の声・問い合わせを1枚に', '新しいサービスの紹介や、まず1枚持ちたい方に'], False),
    ('2〜5ページ', '30', '名刺代わりに、会社のことをきちんと載せたい',
     ['トップページ・会社概要・事業内容', 'お問い合わせ・お知らせ', 'はじめてホームページを作る会社に'], True),
    ('6〜20ページ', '60', '仕事と人材の両方を呼び込みたい',
     ['2〜5ページの内容に加えて', '事業・サービスごとのページ、実績の一覧', '採用・スタッフ紹介・よくある質問'], False),
    ('21ページ以上', '', '採用や複数の事業に、本格的に取り組みたい',
     ['くわしい採用情報（社員の声・働く環境）', '事業ごとの専用ページ', 'コラム記事・製品の一覧 など'], False),
]

INCLUDED = [
    ('ドメインの取得', '◯◯.co.jp などの会社のアドレス'),
    ('サーバーの設定', '公開・バックアップまで'),
    ('会社のメールアドレス', 'info@◯◯.co.jp などを設定'),
    ('Googleマップの整備', '営業時間・写真・加工内容を登録'),
    ('お問い合わせフォーム', 'スマホからも送れる形で'),
    ('アクセス解析', '見られた数が分かるように'),
    ('Web台帳', '管理の情報を紙1枚にまとめてお渡し'),
    ('3か月の無料サポート', '公開後の更新・修正・報告'),
]

SUPPORT = [
    ('ライト', '5,000', 'まず安心して持っておきたい',
     ['ドメイン・サーバーの更新の見守り', 'バックアップ・セキュリティの更新', '困ったときの相談', '小さな修正 月1回まで'], False),
    ('スタンダード', '10,000', 'サイトとGoogleマップを育てたい',
     ['ライトの内容すべて', '小さな修正 月3回まで', 'お知らせの更新 月1本', 'Googleマップの更新 月1回', '見られた数・問い合わせ数の報告 月1回'], True),
    ('しっかり集客', '30,000', '問い合わせ・応募を増やしたい',
     ['スタンダードの内容すべて', 'お知らせ 月2本・Googleマップ 月2回', '報告に改善の提案をつけます', '新しいページ 3か月に1ページ', 'オンライン面談 月1回30分'], False),
]

CONDITIONS = [
    '会社名・ロゴ・サイトの画面を、マツケンスタジオの事例として紹介させていただきます。',
    '公開後に30分ほど、社長のお話（感想）をお聞かせください。',
    '公開3か月後に、出せる範囲で成果（問い合わせ数・応募数など）を教えてください。',
    '取引先の名前など、載せられない情報は事前にご相談のうえで決めます。',
]

STEPS = [
    ('お問い合わせ', 'このページのフォームから。1分ほどで送れます。'),
    ('お話をお聞きする', '東京東部・川崎など訪問できる地域は伺います。遠方の方はオンラインで。'),
    ('お見積り・お申し込み', 'プランと内容を決めます。外部にかかる費用も、ここでご説明します。'),
    ('原稿・写真の準備', '文章はこちらで作ります。社長のお手間は1時間ほどの聞き取りだけです。'),
    ('制作・確認', 'できあがったページを見ていただき、直したいところをお聞きします。'),
    ('公開・手続き', 'ドメイン・サーバー・Googleマップの手続きをして公開。Web台帳をお渡しします。'),
    ('3か月の無料サポート', '更新・修正・毎月の報告。4か月目からは続けるかをお選びいただけます。'),
]

FAQ = [
    ('本当に毎月3社までですか？', 'はい。制作に責任を持てる数にしているためです。4社目以降のお申し込みは、翌月の枠でお受けします。'),
    ('どれくらいで公開できますか？', 'お申し込みから1〜2か月が目安です。お申し込みの順に制作を始めます。'),
    ('パソコンやネットのことがまったく分かりません。', '大丈夫です。ドメインやサーバー、Googleマップの手続きは、私たちがすべて行います。社長にお願いするのは、聞き取りと確認、お支払いの手続きだけです。'),
    ('ドメインやサーバーの費用はどうなりますか？', '御社の名義で、御社から直接お支払いいただきます。サイトだけなら年数千円ほど、会社のメールアドレスも使う場合は月1,000円前後が目安です。'),
    ('月額サポートはやめられますか？', 'はい。公開後3か月の無料期間のあと、続けるかどうかをお選びいただけます。有料で続ける場合は6か月からのご契約で、その後は1か月前までのご連絡でやめられます。やめるときは、管理の権限とWeb台帳をすべてお返しします。'),
    ('事例に載せたくない内容がある場合は？', '取引先の名前、図面、製品など、載せられないものは事前にご相談のうえで外します。'),
    ('今のサイトのドメインやメールは、そのまま使えますか？', 'はい、基本的にそのまま使えます。今の契約の状況を確認して、切り替えの手続きもこちらで行います。検索での評価もできるだけ引き継げるように作り直します。'),
    ('ページ数が決まっていなくても大丈夫ですか？', '大丈夫です。載せたい内容をお聞きして、合うページ数をご提案します。価格の表のページ数と内容は目安です。'),
    ('相談したら、必ず申し込まないといけませんか？', 'いいえ。お話をお聞きして、今は必要ないと思えば、そうお伝えします。無理にすすめることはありません。'),
]

FONTS = ''.join(
    f"@font-face{{font-family:'NS';font-style:normal;font-weight:{w};font-display:swap;src:url(../../fonts/noto-sans-jp-{w}.woff2) format('woff2')}}\n"
    for w in (400, 500, 700))

CSS = FONTS + r"""
:root{--ink:#0E0E10;--ink2:#2A2A30;--muted:#5E5E65;--navy:#1B3A6B;--navy2:#2E5BA6;--y:#F5DE00;--yh:#FFE92E;--ysoft:#FFF7C2;--bg:#FFFFFF;--mist:#F4F6F9;--line:#E1E5EB}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'NS',"Hiragino Sans","Yu Gothic",sans-serif;color:var(--ink);background:var(--bg);font-size:16px;line-height:1.8;letter-spacing:.02em;-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
.wrap{max-width:1160px;margin:0 auto;padding:0 20px}
@media(min-width:768px){.wrap{padding:0 40px}}
.narrow{max-width:860px}
h1,h2,h3{text-wrap:balance;letter-spacing:.01em}
.sec{padding:44px 0}
@media(min-width:768px){.sec{padding:60px 0}}
.sec.mist{background:var(--mist)}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:14px;font-weight:700;color:var(--navy);margin-bottom:12px}
.eyebrow::before{content:'';width:28px;height:3px;background:var(--y);border-radius:2px}
.h2{font-size:clamp(24px,3.6vw,38px);font-weight:700;line-height:1.35;margin-bottom:10px}
.lead{font-size:16px;color:var(--ink2);line-height:2;max-width:720px}
@media(min-width:768px){.lead{font-size:17px}}
mark{background:linear-gradient(transparent 62%,var(--y) 62%);color:inherit;padding:0 .05em}

/* top bar */
.bar{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar .wrap{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{display:inline-flex;align-items:center;gap:11px;text-decoration:none}
.mark{width:38px;height:38px;border-radius:10px;background:var(--navy);color:#fff;display:grid;place-items:center;font-weight:700;font-size:20px;position:relative;flex:none}
.mark::after{content:'';position:absolute;right:-3px;top:-3px;width:12px;height:12px;border-radius:50%;background:var(--y);border:2px solid #fff}
.logo b{display:block;font-size:17px;font-weight:700;letter-spacing:.04em;line-height:1.2}
.logo small{display:block;font-size:11px;color:var(--muted);letter-spacing:.12em}
.bar .btn.md{padding:10px 20px;font-size:14px;box-shadow:none}
@media(max-width:520px){.bar .btn{display:none}}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;border-radius:999px;background:var(--y);color:var(--ink);font-weight:700;text-decoration:none;letter-spacing:.04em;transition:background .2s,transform .2s,box-shadow .2s;box-shadow:0 10px 24px -12px rgba(190,160,0,.9);border:none;cursor:pointer;font-family:inherit}
.btn:hover{background:var(--yh);transform:translateY(-2px)}
.btn:focus-visible,a:focus-visible,summary:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid var(--navy2);outline-offset:3px}
.btn.lg{padding:20px 44px;font-size:18px}
.btn.md{padding:16px 34px;font-size:16px}
.btn .btn-s{font-size:11px;font-weight:700;line-height:1;background:rgba(14,14,16,.12);border-radius:999px;padding:4px 8px;letter-spacing:.02em}
.btn.lg .btn-s{font-size:12px}
.btn .arr{transition:transform .2s}.btn:hover .arr{transform:translateX(3px)}
.micro{font-size:13px;color:var(--muted);margin-top:12px}

/* hero */
.hero{position:relative;overflow:hidden;padding:24px 0 36px}
@media(min-width:960px){.hero{padding:32px 0 48px}}
.hero .grid{display:grid;gap:44px;align-items:center;position:relative;z-index:1}
@media(min-width:960px){.hero .grid{grid-template-columns:1.05fr .95fr;gap:40px}}
.buff{position:absolute;pointer-events:none;border-radius:50%;background:repeating-radial-gradient(circle at center,rgba(27,58,107,.07) 0 1px,transparent 1px 14px)}
.hero .buff.b1{width:760px;height:760px;right:-260px;top:-200px}
.hero .glow{position:absolute;right:-120px;top:40px;width:620px;height:620px;border-radius:50%;background:radial-gradient(circle,#FFF3A0 0%,rgba(255,243,160,0) 68%);pointer-events:none}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px}
.tag{font-size:13px;font-weight:700;border-radius:999px;padding:6px 14px;background:var(--ink);color:#fff}
.tag.y{background:var(--y);color:var(--ink)}
.tag.o{background:#fff;color:var(--navy);box-shadow:inset 0 0 0 1.5px var(--navy)}
.kick{font-size:15px;font-weight:700;color:var(--navy);margin-bottom:12px}
@media(min-width:768px){.kick{font-size:17px}}
.hero h1{font-size:clamp(38px,5.6vw,66px);font-weight:700;line-height:1.22;letter-spacing:0;margin-bottom:24px}
.hero h1 .small{display:block;font-size:.5em;line-height:1.5;margin-bottom:.2em;color:var(--ink2)}
.hero .sub{font-size:16px;line-height:1.95;color:var(--ink2);max-width:560px;margin-bottom:22px}
@media(min-width:768px){.hero .sub{font-size:17px}}
.proof{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:24px;max-width:560px}
.proof div{background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 10px;text-align:center;line-height:1.45}
.proof b{display:block;font-size:clamp(18px,2.4vw,24px);font-weight:700;color:var(--navy)}
.proof span{font-size:11.5px;color:var(--muted);font-weight:500}
.price-tease{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:18px}
.price-tease .l{font-size:14px;font-weight:700;color:var(--muted)}
.price-tease .v{font-size:40px;font-weight:700;line-height:1;font-variant-numeric:tabular-nums}
.price-tease .v small{font-size:18px;margin-left:2px}
.price-tease .t{font-size:13px;color:var(--muted)}
.visual{position:relative;min-height:340px}
.pc{position:relative;border-radius:12px;background:#fff;box-shadow:0 40px 80px -30px rgba(14,14,16,.45),0 0 0 1px rgba(14,14,16,.06);overflow:hidden}
.pc .chrome{height:28px;background:#EEF1F5;display:flex;align-items:center;gap:6px;padding:0 12px}
.pc .chrome i{width:9px;height:9px;border-radius:50%;background:#CBD2DB}
.sp{position:absolute;right:-6px;bottom:-40px;width:31%;border-radius:22px;border:7px solid var(--ink);background:var(--ink);overflow:hidden;box-shadow:0 30px 60px -20px rgba(14,14,16,.55)}
.sp img{border-radius:14px}
.stamp{position:absolute;left:-34px;top:-58px;width:112px;height:112px;border-radius:50%;background:var(--y);display:grid;place-items:center;text-align:center;font-weight:700;line-height:1.3;box-shadow:0 18px 30px -14px rgba(140,120,0,.8);transform:rotate(-8deg);z-index:2}
.stamp small{display:block;font-size:11px}
.stamp b{display:block;font-size:30px;line-height:1}
.cap{font-size:12px;color:var(--muted);margin-top:14px;max-width:64%}
@media(max-width:959px){.visual{margin:44px 8px 30px}.stamp{width:92px;height:92px;left:-6px;top:-50px}.stamp b{font-size:26px}.stamp small{font-size:10px}}

/* pains */
.checks{display:grid;gap:10px;margin-top:24px}
@media(min-width:768px){.checks{grid-template-columns:1fr 1fr;gap:16px}}
.checks li{list-style:none;display:grid;grid-template-columns:30px 1fr;gap:12px;align-items:start;background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 20px;font-size:16px;font-weight:500;line-height:1.7}
.checks li::before{content:'';width:24px;height:24px;border-radius:6px;background:var(--navy) url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'><path d='M5 12l5 5 9-10'/></svg>") center/15px no-repeat;margin-top:2px}
.turn{margin-top:20px;text-align:center;font-size:clamp(20px,2.8vw,28px);font-weight:700;line-height:1.6}
.turn::before{content:'';display:block;width:2px;height:28px;background:var(--navy);margin:0 auto 14px}

/* why now */
.cards3{display:grid;gap:14px;margin-top:24px}
@media(min-width:900px){.cards3{grid-template-columns:repeat(3,1fr);gap:22px}}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:30px 26px}
.card h3{font-size:19px;font-weight:700;line-height:1.5;margin-bottom:10px}
.card p{font-size:15px;color:var(--ink2);line-height:1.9}

/* about */
.about{display:grid;gap:28px;align-items:center}
@media(min-width:900px){.about{grid-template-columns:.9fr 1.1fr;gap:64px}}
.photo{position:relative}
.photo img{border-radius:14px;width:100%;aspect-ratio:4/3;object-fit:cover}
.photo .buff{width:320px;height:320px;left:-120px;bottom:-110px;z-index:0}
.photo img{position:relative;z-index:1}
.photo figcaption{font-size:12px;color:var(--muted);margin-top:10px}
.about .big{font-size:clamp(26px,3.6vw,38px);font-weight:700;line-height:1.5;margin-bottom:22px}
.about p{font-size:16px;line-height:2.05;color:var(--ink2);margin-bottom:18px}
.sign{display:flex;align-items:center;gap:14px;margin-top:26px;padding-top:24px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}

/* strengths */
.str{display:grid;gap:14px;margin-top:24px}
@media(min-width:900px){.str{grid-template-columns:1fr 1fr;gap:22px}}
.str .card{position:relative;padding:34px 30px 30px;overflow:hidden}
.str .card::after{content:'';position:absolute;right:-50px;top:-50px;width:140px;height:140px;border-radius:50%;background:repeating-radial-gradient(circle,rgba(27,58,107,.08) 0 1px,transparent 1px 10px)}
.str .card h3{font-size:21px;padding-left:16px;border-left:4px solid var(--y)}

/* result */
.result{display:grid;gap:28px;align-items:center;background:var(--ink);color:#fff;border-radius:18px;padding:44px 28px;position:relative;overflow:hidden}
@media(min-width:900px){.result{grid-template-columns:1fr 1.1fr;padding:52px 56px;gap:48px}}
.result .buff{width:520px;height:520px;right:-180px;top:-180px;background:repeating-radial-gradient(circle,rgba(255,255,255,.07) 0 1px,transparent 1px 16px)}
.result .num{font-size:clamp(84px,12vw,140px);font-weight:700;line-height:1;color:var(--y);letter-spacing:-.02em}
.result .num small{font-size:.36em;margin-left:6px;color:#fff}
.result .lbl{font-size:18px;font-weight:700;margin:6px 0 16px}
.result p{font-size:15px;line-height:1.95;color:rgba(255,255,255,.82)}
.result .shot{position:relative;z-index:1}
.result .shot .pc{box-shadow:0 30px 60px -20px rgba(0,0,0,.6)}

/* compare */
.cmp{width:100%;border-collapse:separate;border-spacing:0;margin-top:24px;font-size:15px;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;min-width:600px}
.cmp th,.cmp td{padding:18px 18px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle;line-height:1.6}
.cmp tr:last-child th,.cmp tr:last-child td{border-bottom:none}
.cmp thead th{background:var(--mist);font-size:14px;color:var(--muted)}
.cmp thead th.us{background:var(--navy);color:#fff;font-size:15px}
.cmp tbody th{font-weight:700;width:26%}
.cmp td.them{color:var(--muted);width:34%}
.cmp td.us{font-weight:700;background:var(--ysoft);width:40%}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}

/* plans */
.plans{display:grid;gap:16px;margin-top:28px}
@media(min-width:720px){.plans{grid-template-columns:1fr 1fr}}
@media(min-width:1100px){.plans.p4{grid-template-columns:repeat(4,1fr)}.plans.p3{grid-template-columns:repeat(3,1fr)}}
.plan{position:relative;display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:14px;padding:30px 24px 26px}
.plan.rec{border:2px solid var(--navy);box-shadow:0 24px 50px -30px rgba(27,58,107,.55)}
.plan.rec::before{content:'おすすめ';position:absolute;top:-14px;left:22px;font-size:12px;font-weight:700;background:var(--y);border-radius:999px;padding:4px 14px}
.plan h3{font-size:18px;font-weight:700;line-height:1.45;margin-bottom:4px}
.plan .for{font-size:13px;color:var(--muted);line-height:1.7;min-height:2.6em;margin-bottom:16px}
.plan .pr{font-size:44px;font-weight:700;line-height:1;font-variant-numeric:tabular-nums;margin-bottom:4px}
.plan .pr small{font-size:18px;margin-left:2px}
.plan .pr.ask{font-size:20px;line-height:1.5;padding:8px 0 6px}
.plan .unit{font-size:12px;color:var(--muted);margin-bottom:18px}
.plan ul{border-top:1px solid var(--line);padding-top:14px;margin-bottom:20px}
.plan li{list-style:none;position:relative;padding:6px 0 6px 22px;font-size:14px;line-height:1.7;color:var(--ink2)}
.plan li::before{content:'';position:absolute;left:0;top:13px;width:10px;height:10px;border-radius:3px;background:var(--y);box-shadow:0 0 0 2px var(--navy) inset}
.plan .pick{margin-top:auto;display:block;text-align:center;padding:12px;border-radius:999px;font-size:14px;font-weight:700;text-decoration:none;box-shadow:inset 0 0 0 1.5px var(--ink);transition:background .2s,color .2s}
.plan .pick:hover{background:var(--ink);color:#fff}
.plan.rec .pick{background:var(--y);box-shadow:none}
.plan.rec .pick:hover{background:var(--yh);color:var(--ink)}
.note{font-size:13px;color:var(--muted);line-height:1.8;margin-top:16px}

/* renewal */
.renew{display:grid;gap:16px;margin-top:24px}
@media(min-width:900px){.renew{grid-template-columns:.9fr 1.1fr;gap:22px;align-items:stretch}}
.renew .before{background:#fff;border:1px solid var(--line);border-radius:14px;padding:24px 22px}
.renew .before h3,.renew .after h3{font-size:16px;font-weight:700;margin-bottom:10px}
.renew .before li{list-style:none;position:relative;padding:7px 0 7px 22px;font-size:15px;line-height:1.7;color:var(--ink2);border-bottom:1px dashed var(--line)}
.renew .before li:last-child{border-bottom:none}
.renew .before li::before{content:'';position:absolute;left:2px;top:15px;width:10px;height:2px;background:var(--muted)}
.renew .after{background:var(--navy);color:#fff;border-radius:14px;padding:24px 22px}
.renew .after h3{color:var(--y)}
.renew .after .g{display:grid;gap:10px}
@media(min-width:600px){.renew .after .g{grid-template-columns:1fr 1fr}}
.renew .after .g div{background:rgba(255,255,255,.08);border-radius:10px;padding:14px 16px}
.renew .after b{display:block;font-size:15px;margin-bottom:2px}
.renew .after span{font-size:13px;color:rgba(255,255,255,.8);line-height:1.7}
.same{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin-top:18px;background:var(--ysoft);border-radius:10px;padding:14px 18px;font-size:14px;line-height:1.7}
.same b{font-size:15px}

/* included */
.inc{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:24px}
@media(min-width:900px){.inc{grid-template-columns:repeat(4,1fr);gap:16px}}
.inc div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px 18px}
.inc b{display:block;font-size:16px;font-weight:700;margin-bottom:4px}
.inc span{font-size:13px;color:var(--muted);line-height:1.7}
.own{display:grid;gap:22px;margin-top:20px;background:#fff;border-radius:14px;border:1px solid var(--line);padding:30px 26px}
@media(min-width:900px){.own{grid-template-columns:1fr 1fr;padding:40px 44px;gap:44px;align-items:center}}
.own .msg{font-size:clamp(20px,2.4vw,26px);font-weight:700;line-height:1.6}
.own .msg em{font-style:normal;background:linear-gradient(transparent 62%,var(--y) 62%)}
.own table{width:100%;border-collapse:collapse;font-size:14px}
.own th,.own td{padding:14px 0;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;line-height:1.7}
.own th{width:48%;font-weight:700;padding-right:12px}
.own tr:last-child th,.own tr:last-child td{border-bottom:none}

/* conditions */
.cond{counter-reset:c;display:grid;gap:10px;margin-top:24px}
.cond li{list-style:none;counter-increment:c;display:grid;grid-template-columns:36px 1fr;gap:14px;align-items:start;background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px 20px;font-size:15px;line-height:1.8}
.cond li::before{content:counter(c);width:32px;height:32px;border-radius:50%;background:var(--navy);color:#fff;display:grid;place-items:center;font-weight:700;font-size:14px}

/* flow */
.flow{display:grid;gap:0;margin-top:24px;counter-reset:f}
.flow li{list-style:none;counter-increment:f;position:relative;display:grid;grid-template-columns:52px 1fr;gap:18px;padding-bottom:18px}
.flow li::before{content:counter(f,decimal-leading-zero);width:52px;height:52px;border-radius:50%;background:#fff;border:2px solid var(--navy);color:var(--navy);display:grid;place-items:center;font-weight:700;font-size:16px;position:relative;z-index:1}
.flow li::after{content:'';position:absolute;left:25px;top:52px;bottom:0;width:2px;background:var(--line)}
.flow li:last-child::after{display:none}
.flow li:last-child{padding-bottom:0}
.flow b{display:block;font-size:17px;font-weight:700;margin:12px 0 4px}
.flow p{font-size:14px;color:var(--ink2);line-height:1.85}

/* faq */
.faq{margin-top:20px;border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:30px 1fr 24px;gap:12px;align-items:start;padding:18px 4px;font-size:16px;font-weight:700;line-height:1.6}
.faq summary::-webkit-details-marker{display:none}
.faq summary::before{content:'Q';color:var(--navy);font-size:20px;line-height:1.3}
.faq summary::after{content:'+';font-size:24px;line-height:1;color:var(--navy);transition:transform .2s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{padding:0 4px 22px 46px;font-size:15px;color:var(--ink2);line-height:1.95}

/* mid cta */
.mid{background:var(--ysoft);padding:30px 0;text-align:center;position:relative;overflow:hidden}
.mid .buff{width:420px;height:420px;left:-160px;top:-160px}
.mid p{font-size:clamp(18px,2.4vw,24px);font-weight:700;line-height:1.6;margin-bottom:16px;position:relative}

/* form */
.formsec{background:var(--ink);color:#fff;padding:44px 0 48px;position:relative;overflow:hidden}
@media(min-width:768px){.formsec{padding:60px 0}}
.formsec .buff{width:700px;height:700px;right:-260px;top:-240px;background:repeating-radial-gradient(circle,rgba(255,255,255,.06) 0 1px,transparent 1px 16px)}
.formsec .h2{color:#fff}
.formsec .lead{color:rgba(255,255,255,.8)}
.fbox{position:relative;background:#fff;color:var(--ink);border-radius:16px;padding:26px 20px;margin-top:22px}
@media(min-width:768px){.fbox{padding:44px 48px}}
.wf{display:grid;gap:22px}
.wf .row2{display:grid;gap:22px}
@media(min-width:680px){.wf .row2{grid-template-columns:1fr 1fr}}
.wf-label{display:block;font-size:15px;font-weight:700;margin-bottom:8px}
.req,.opt{margin-left:8px;font-size:11px;font-weight:700;border-radius:3px;padding:2px 7px;vertical-align:2px}
.req{color:#fff;background:#C62828}.opt{color:var(--muted);background:var(--mist)}
.wf input[type=text],.wf input[type=email],.wf input[type=tel],.wf input[type=url],.wf textarea{width:100%;border:1.5px solid #CFD6DF;border-radius:8px;padding:14px 14px;font-size:16px;font-family:inherit;background:#fff;transition:border-color .2s,box-shadow .2s}
.wf input:focus,.wf textarea:focus{outline:none;border-color:var(--navy);box-shadow:0 0 0 3px rgba(27,58,107,.15)}
.chips{display:grid;gap:8px}
@media(min-width:680px){.chips{grid-template-columns:repeat(3,1fr)}}
.chip{display:flex;align-items:center;gap:10px;border:1.5px solid #CFD6DF;border-radius:8px;padding:12px 14px;font-size:15px;cursor:pointer;transition:border-color .2s,background .2s}
.chip:has(input:checked){border-color:var(--navy);background:#EEF3FA}
.chip input{width:18px;height:18px;accent-color:var(--navy);flex:none}
.ferr{padding:14px 16px;background:#FDECEA;border:1px solid #F5C2BD;color:#B3261E;border-radius:8px;font-size:14px}
.hidden{display:none!important}
.fsubmit{width:100%;padding:20px;font-size:18px}
.fnote{font-size:12.5px;color:var(--muted);text-align:center;line-height:1.8}
.fnote a{text-decoration:underline}
.fok{text-align:center;padding:20px 0}
.fok b{display:block;font-size:24px;margin-bottom:12px}
.fok p{font-size:15px;line-height:2;color:var(--ink2)}
.assure{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:22px;font-size:14px;color:rgba(255,255,255,.85)}
.assure span::before{content:'✓';color:var(--y);font-weight:700;margin-right:6px}

/* line */
.line-link{margin-top:10px;font-size:14px}
.line-link a{color:#06C755;font-weight:700;text-decoration:underline;text-underline-offset:3px}
.line-box{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-top:20px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:16px 18px;font-size:14px}
.line-txt{display:flex;flex-direction:column;align-items:flex-start;gap:10px}
.line-pc{display:none;font-size:13px;color:rgba(255,255,255,.75)}
.line-qr{display:none;width:132px;height:132px;background:#fff;border-radius:10px;padding:8px;flex:none}
@media(min-width:768px){.line-pc{display:block}.line-qr{display:block}.line-box{padding:18px 22px}}
.line-btn{display:inline-flex;align-items:center;gap:8px;background:#06C755;color:#fff;font-weight:700;border-radius:999px;padding:10px 20px;text-decoration:none}
.line-btn:hover{background:#05b34c}

.line-hero-qr{display:none}
@media(min-width:768px){.line-link{display:none}.line-hero-qr{display:flex;align-items:center;gap:14px;margin-top:16px;padding:10px 16px 10px 10px;border:1px solid var(--line);border-radius:12px;background:#fff;width:max-content}.line-hero-qr img{width:96px;height:96px}.line-hero-qr b{display:block;font-size:15px;color:#06A049}.line-hero-qr span{font-size:13px;color:var(--muted)}}

/* footer */
.foot{padding:22px 0 96px;font-size:13px;color:var(--muted);text-align:center;line-height:1.9}
@media(min-width:768px){.foot{padding:40px 0}}
.foot a{text-decoration:underline}

/* sticky cta (mobile) */
.stick{position:fixed;left:0;right:0;bottom:0;z-index:50;padding:10px 14px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.96);border-top:1px solid var(--line);display:flex;align-items:center;gap:10px;transform:translateY(110%);transition:transform .25s}
.stick.show{transform:none}
.stick .t{font-size:12px;line-height:1.4;font-weight:700;flex:none}
.stick .t small{display:block;font-weight:500;color:var(--muted)}
.stick .btn{flex:1;padding:14px 10px;font-size:15px}
@media(min-width:768px){.stick{display:none}}

@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
"""


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def cta(size='lg', text='無料で相談する'):
    return f'<a href="#form" class="btn {size}"><span class="btn-s">最短1分</span>{text}<span class="arr">→</span></a>'


def plan_cards(items, unit, kind):
    out = []
    for name, price, for_, pts, rec in items:
        if price:
            pr = f'<div class="pr">{price}<small>{"万円" if kind == "make" else "円"}</small></div><div class="unit">{unit}</div>'
        else:
            pr = '<div class="pr ask">ご要望に合わせて<br>お見積り</div><div class="unit">&nbsp;</div>'
        lis = ''.join(f'<li>{x}</li>' for x in pts)
        pick = (f'<a href="#form" class="pick" data-plan="{name}">このプランで相談する</a>' if kind == 'make' else '')
        out.append(f'<div class="plan{" rec" if rec else ""}"><h3>{name}</h3><div class="for">{for_}方に</div>{pr}<ul>{lis}</ul>{pick}</div>')
    return ''.join(out)


def page():
    pains = ''.join(f'<li>{x}</li>' for x in PAINS)
    line_hero = (f'<p class="line-link"><a href="{LINE_URL}" target="_blank" rel="noopener">LINEで気軽に質問する</a></p>'
                 f'<div class="line-hero-qr"><img src="../../images/lp/line-qr.svg" alt="LINE友だち追加のQRコード" width="96" height="96"><div><b>LINEでも気軽に相談できます</b><span>スマホのカメラで読み取ると、友だち追加できます。</span></div></div>' if LINE_URL else '')
    line_form = (f'<div class="line-box"><div class="line-txt"><span>フォームが面倒な方は、LINEでも相談できます。</span><span class="line-pc">スマホのカメラでQRコードを読み取ると、友だち追加できます。</span><a href="{LINE_URL}" target="_blank" rel="noopener" class="line-btn">LINEで相談する</a></div><img class="line-qr" src="../../images/lp/line-qr.svg" alt="LINE友だち追加のQRコード" width="150" height="150" loading="lazy"></div>' if LINE_URL else '')
    renew_pains = ''.join(f'<li>{x}</li>' for x in RENEW_PAINS)
    renew_do = ''.join(f'<div><b>{t}</b><span>{d}</span></div>' for t, d in RENEW_DO)
    why = ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in WHY_NOW)
    strengths = ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in STRENGTHS)
    cmp_rows = ''.join(f'<tr><th>{a}</th><td class="them">{b}</td><td class="us">{c}</td></tr>' for a, b, c in COMPARE)
    inc = ''.join(f'<div><b>{t}</b><span>{d}</span></div>' for t, d in INCLUDED)
    cond = ''.join(f'<li>{x}</li>' for x in CONDITIONS)
    flow = ''.join(f'<li><div><b>{t}</b><p>{d}</p></div></li>' for t, d in STEPS)
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    plan_opts = ''.join(f'<label class="chip"><input type="radio" name="plan" value="{v}" data-label="ご希望のプラン"/> {v}</label>'
                        for v in [p[0] for p in PLANS] + ['まだ決めていない'])
    site_opts = ''.join(f'<label class="chip"><input type="radio" name="has_site" value="{v}" data-label="今のホームページ" required/> {v}</label>'
                        for v in ['ない', 'ある'])
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Web集客・AI活用支援", "item": f"{BASE}/web-ai/"},
        {"@type": "ListItem", "position": 3, "name": "事例づくりモニター", "item": URL}]}
    ld = ''.join('<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=2) + '\n</script>\n' for b in (crumbs, faq_ld))

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}">
<meta property="og:locale" content="ja_JP">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" type="image/svg+xml" href="../../favicon.svg">
<link rel="preload" href="../../fonts/noto-sans-jp-700.woff2" as="font" type="font/woff2" crossorigin>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5F157JYQD2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-5F157JYQD2');</script>
<style>{CSS}</style>
{ld}</head>
<body>

<header class="bar">
  <div class="wrap">
    <span class="logo"><span class="mark">松</span><span><b>マツケンスタジオ</b><small>by 松本研磨工業</small></span></span>
    {cta('md')}
  </div>
</header>

<main>

<section class="hero">
  <div class="glow"></div><div class="buff b1"></div>
  <div class="wrap grid">
    <div>
      <div class="tags"><span class="tag y">毎月3社まで</span><span class="tag">新規制作・リニューアル</span><span class="tag o">町工場・製造業</span></div>
      <p class="kick">金属研磨の松本研磨工業が始めた、Webの新事業</p>
      <h1><span class="small">町工場のホームページは、</span><mark>町工場</mark>がつくる。</h1>
      <p class="sub">図面も、公差も、加工の話もそのまま通じる担当が、ドメインの取得から公開後の更新まで、まるごと引き受けます。これから作る会社も、今のサイトを作り直したい会社も。</p>
      <div class="proof">
        <div><b>3倍</b><span>自社サイトの<br>有効なお問い合わせ</span></div>
        <div><b>御社名義</b><span>ドメインも<br>サイトも</span></div>
        <div><b>3か月</b><span>公開後の<br>サポート無料</span></div>
      </div>
      <div class="price-tease"><span class="l">モニター価格</span><span class="v">15<small>万円〜</small></span><span class="t">（税別）</span></div>
      {cta('lg')}
      <p class="micro">相談だけでも大丈夫です。無理な営業はしません。</p>{line_hero}
    </div>
    <div class="visual">
      <div class="stamp"><div><small>有効な<br>お問い合わせ</small><b>3倍</b></div></div>
      <div class="pc"><div class="chrome"><i></i><i></i><i></i></div><img src="../../images/lp/case-pc.jpg" alt="松本研磨工業のホームページ（パソコン表示）" width="1280" height="800" fetchpriority="high"></div>
      <div class="sp"><img src="../../images/lp/case-sp.jpg" alt="松本研磨工業のホームページ（スマホ表示）" width="585" height="1266"></div>
      <p class="cap">制作実績：株式会社松本研磨工業（自社）</p>
    </div>
  </div>
</section>

<section class="sec mist">
  <div class="wrap narrow">
    <p class="eyebrow">こんなこと、ありませんか</p>
    <h2 class="h2">ホームページ、<br>ずっと後回しにしていませんか。</h2>
    <ul class="checks">{pains}</ul>
    <p class="turn">その「分からない」「面倒」を、<br><mark>同じ町工場</mark>が引き受けます。</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow">なぜ今、必要なのか</p>
    <h2 class="h2">法人と取引する会社ほど、<br>「信頼」が大切です。</h2>
    <p class="lead">取引を始める前に、相手の会社はホームページを見て「この会社に任せて大丈夫か」を確かめます。ホームページは、会社の信用を伝える入口です。</p>
    <div class="cards3">{why}</div>
  </div>
</section>

<section class="sec mist">
  <div class="wrap">
    <p class="eyebrow">すでにサイトがある会社へ</p>
    <h2 class="h2">今のホームページを、<br>「信頼される形」に作り直します。</h2>
    <div class="renew">
      <div class="before"><h3>こんなサイトになっていませんか</h3><ul>{renew_pains}</ul></div>
      <div class="after"><h3>リニューアルでやること</h3><div class="g">{renew_do}</div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap about">
    <figure class="photo"><div class="buff"></div><img src="../../images/work-05.jpg" alt="松本研磨工業で鏡面に仕上げたステンレス製モニュメント" width="1200" height="900" loading="lazy"><figcaption>松本研磨工業の仕事（ステンレス製モニュメントの鏡面仕上げ）</figcaption></figure>
    <div>
      <p class="eyebrow">マツケンスタジオとは</p>
      <p class="big">毎日、金属を磨いている<br>町工場の、Webの事業です。</p>
      <p>マツケンスタジオは、神奈川県川崎市で金属研磨を営む株式会社松本研磨工業が始めた、新しい事業です。</p>
      <p>町工場の仕事の良さは、なかなか外に伝わりません。私たち自身も、そう感じてきました。だからこそ、自社のホームページを作り直し、検索対策を進め、有効なお問い合わせを3倍にしてきました。</p>
      <p>そのやり方を、同じように「いい仕事をしているのに、知られていない」会社のために使いたい。それが、この事業を始めた理由です。</p>
      <div class="sign"><span class="logo"><span class="mark">松</span><span><b>マツケンスタジオ</b><small>by 松本研磨工業</small></span></span></div>
    </div>
  </div>
</section>

<section class="sec mist">
  <div class="wrap">
    <p class="eyebrow">選ばれる理由</p>
    <h2 class="h2">町工場だから、<br>できることがあります。</h2>
    <div class="str">{strengths}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="result">
      <div class="buff"></div>
      <div style="position:relative;z-index:1">
        <p class="eyebrow" style="color:var(--y)">実績</p>
        <div class="num">3<small>倍</small></div>
        <p class="lbl">有効なお問い合わせの数</p>
        <p>松本研磨工業のホームページを作り直し、検索対策を進めたことで、有効なお問い合わせの数が3倍になりました。お客様のサイトも、このやり方で作ります。</p>
      </div>
      <div class="shot"><div class="pc"><div class="chrome"><i></i><i></i><i></i></div><img src="../../images/lp/case-pc.jpg" alt="松本研磨工業のホームページ" width="1280" height="800" loading="lazy"></div></div>
    </div>
  </div>
</section>

<section class="sec mist">
  <div class="wrap narrow">
    <p class="eyebrow">ほかとの違い</p>
    <h2 class="h2">一般的な制作会社と、<br>ここが違います。</h2>
    <div class="scroll"><table class="cmp">
      <thead><tr><th></th><th>よくある制作会社</th><th class="us">マツケンスタジオ</th></tr></thead>
      <tbody>{cmp_rows}</tbody>
    </table></div>
  </div>
</section>

<div class="mid"><div class="buff"></div><div class="wrap"><p>毎月3社までの受付です。<br>まずは、今の状況をお聞かせください。</p>{cta('lg')}</div></div>

<section class="sec" id="plans">
  <div class="wrap">
    <p class="eyebrow">プランと価格</p>
    <h2 class="h2">事例づくりモニター価格</h2>
    <p class="lead">事例として紹介させていただくことを条件に、特別な価格で制作します。ページ数は目安です。内容をお聞きして、合う形をご提案します。</p>
    <div class="same"><b>新規制作もリニューアルも、同じ価格です。</b><span>リニューアルの場合は、今のサイトの診断と、ドメイン・メールの引き継ぎも含みます。</span></div>
    <div class="plans p4">{plan_cards(PLANS, '税別・1回のみ', 'make')}</div>
    <p class="note">※ページ数・内容は目安で、お見積りで確定します。モニター価格は、下の「モニターの条件」にご協力いただくことが条件です。外部のサービス（ドメイン・サーバー）の費用は別途かかります。</p>
  </div>
</section>

<section class="sec mist">
  <div class="wrap">
    <p class="eyebrow">すべてのプランに含まれるもの</p>
    <h2 class="h2">面倒な手続きは、<br>まるごとお任せください。</h2>
    <div class="inc">{inc}</div>
    <div class="own">
      <p class="msg">ドメインもサーバーも、<em>御社の名義</em>です。<br>やめても、サイトは御社のものとして残ります。</p>
      <div>
        <p style="font-size:14px;color:var(--ink2);line-height:1.9;margin-bottom:10px">外部のサービスの費用は、御社から直接お支払いいただきます（手続きは私たちが行います）。</p>
        <table>
          <tr><th>サイトだけ（メールは今のまま）</th><td>ドメイン代のみ<br><b>年数千円</b>ほど</td></tr>
          <tr><th>サイト＋会社のメールアドレス</th><td>レンタルサーバー代<br><b>月1,000円前後</b></td></tr>
        </table>
        <p class="note">※金額は目安です。お申し込みの前に最新の金額をご案内します。</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow">作ったあとも安心</p>
    <h2 class="h2">月額サポート</h2>
    <p class="lead">公開後3か月は「スタンダード」を無料でお付けします。4か月目からは、プランを選ぶか、やめるかをお選びいただけます。</p>
    <div class="plans p3">{plan_cards(SUPPORT, '税別・月額', 'support')}</div>
    <p class="note">※有料で続ける場合は6か月からのご契約で、その後は1か月前までのご連絡でやめられます。サイトの作り直しや大きな追加は、別にお見積りします。</p>
  </div>
</section>

<section class="sec mist">
  <div class="wrap narrow">
    <p class="eyebrow">モニターの条件</p>
    <h2 class="h2">特別な価格の代わりに、<br>4つだけお願いがあります。</h2>
    <ol class="cond">{cond}</ol>
  </div>
</section>

<section class="sec" id="flow">
  <div class="wrap narrow">
    <p class="eyebrow">公開までの流れ</p>
    <h2 class="h2">社長のお手間は、<br>1時間の聞き取りだけ。</h2>
    <p class="lead">お申し込みから公開までは1〜2か月が目安です。</p>
    <ol class="flow">{flow}</ol>
  </div>
</section>

<section class="sec mist" id="faq">
  <div class="wrap narrow">
    <p class="eyebrow">よくある質問</p>
    <h2 class="h2">よくある質問</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="formsec" id="form">
  <div class="buff"></div>
  <div class="wrap narrow" style="position:relative">
    <p class="eyebrow" style="color:var(--y)">お問い合わせ</p>
    <h2 class="h2">まずは1分で、<br>ご相談ください。</h2>
    <p class="lead">「何から始めればいいか分からない」という段階でも大丈夫です。内容を確認して、担当者からご連絡します。</p>
    <div class="assure"><span>相談は無料</span><span>無理な営業はしません</span><span>毎月3社まで・先着順</span></div>
{line_form}
    <div class="fbox" data-form-wrap>
      <form class="wf" data-contact-form="web" novalidate>
        <div class="hidden" aria-hidden="true"><label>ウェブサイト<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <input type="hidden" name="topic" value="事例づくりモニター（LP）" data-label="お問い合わせの種類">
        <div><div class="wf-label">ご希望のプラン<span class="opt">任意</span></div><div class="chips">{plan_opts}</div></div>
        <div><div class="wf-label">今のホームページ<span class="req">必須</span></div><div class="chips">{site_opts}</div></div>
        <div class="row2">
          <div><label class="wf-label" for="f-company">会社名・屋号<span class="req">必須</span></label><input id="f-company" type="text" name="company" data-label="会社名・屋号" required autocomplete="organization" placeholder="株式会社〇〇製作所"></div>
          <div><label class="wf-label" for="f-name">お名前<span class="req">必須</span></label><input id="f-name" type="text" name="name" data-label="お名前" required autocomplete="name" placeholder="山田 太郎"></div>
          <div><label class="wf-label" for="f-email">メールアドレス<span class="req">必須</span></label><input id="f-email" type="email" name="email" data-label="メールアドレス" required autocomplete="email" placeholder="example@mail.com"></div>
          <div><label class="wf-label" for="f-tel">電話番号<span class="opt">任意</span></label><input id="f-tel" type="tel" name="tel" data-label="電話番号" autocomplete="tel" placeholder="03-0000-0000"></div>
        </div>
        <div><label class="wf-label" for="f-url">今のサイトのURL<span class="opt">任意</span></label><input id="f-url" type="url" name="site_url" data-label="今のサイトのURL" placeholder="https://"></div>
        <div><label class="wf-label" for="f-msg">ご相談内容<span class="opt">任意</span></label><textarea id="f-msg" name="message" data-label="ご相談内容" rows="4" placeholder="困っていること、やりたいことを、分かる範囲でどうぞ。"></textarea></div>
        <div data-form-error class="ferr hidden"></div>
        <button type="submit" class="btn fsubmit"><span data-btn-text>この内容で相談する</span> <span class="arr">→</span></button>
        <p class="fnote">送信後、入力内容の控えを自動でメールでお送りします。<br><a href="../../privacy/" target="_blank" rel="noopener">プライバシーポリシー</a>をご確認のうえ送信してください。</p>
      </form>
      <div data-form-success class="fok hidden"><b>ありがとうございます。</b><p>ご相談を受け付けました。<br>入力内容の控えをメールでお送りしています。<br>内容を確認のうえ、担当者からご連絡します。</p></div>
    </div>
  </div>
</section>

</main>

<div class="foot">
  <div class="wrap">マツケンスタジオ（運営：株式会社松本研磨工業）<br>〒210-0851 神奈川県川崎市川崎区浜町3-9-22　｜　<a href="../../privacy/" target="_blank" rel="noopener">プライバシーポリシー</a><br>© 2026 株式会社松本研磨工業</div>
</div>

<div class="stick" id="stick"><div class="t">毎月3社まで<small>相談は無料</small></div>{cta('md')}</div>

<script src="../../js/contact-form.js"></script>
<script>
(function(){{
  // プランのボタンから来たら、フォームのプランを選んでおく
  document.querySelectorAll('[data-plan]').forEach(function(a){{
    a.addEventListener('click',function(){{
      var r=document.querySelector('input[name="plan"][value="'+a.dataset.plan+'"]'); if(r) r.checked=true;
    }});
  }});
  // スマホの下部ボタン：最初の画面を過ぎたら出し、フォームが見えたら隠す
  var stick=document.getElementById('stick'), hero=document.querySelector('.hero'), form=document.getElementById('form');
  if('IntersectionObserver' in window){{
    var heroOut=false, formIn=false;
    function upd(){{ stick.classList.toggle('show', heroOut && !formIn); }}
    new IntersectionObserver(function(e){{ heroOut=!e[0].isIntersecting; upd(); }}).observe(hero);
    new IntersectionObserver(function(e){{ formIn=e[0].isIntersecting; upd(); }},{{rootMargin:'0px 0px -20% 0px'}}).observe(form);
  }}
}})();
</script>
</body>
</html>
'''


if __name__ == '__main__':
    html = ogp_meta.apply(page(), 'studio')
    os.makedirs('web-ai/monitor', exist_ok=True)
    open('web-ai/monitor/index.html', 'w', encoding='utf-8').write(html)
    print('built monitor LP')

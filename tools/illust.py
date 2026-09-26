"""マツケンスタジオのページで使う図（SVG）。紺の線＋黄色の差し色で、既存デザインにそろえる。

ILLUST[slug] … サービスページの「〇〇とは」の横に置く図（viewBox 300x220）
ICON[name]   … カードの見出しの上に置く小さなアイコン（viewBox 48x48）
"""
N = '#1B3A6B'   # 紺
Y = '#F5DE00'   # 黄
L = '#EEF2F8'   # 淡い青
G = '#C9D2DF'   # 線の薄い色


def svg(body, label, vb='0 0 300 220'):
    return (f'<svg viewBox="{vb}" role="img" aria-label="{label}" class="st-illu" '
            f'fill="none" stroke="{N}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


def t(x, y, s, size=13, anchor='middle', fill=N, weight=700):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" stroke="none">{s}</text>'


ILLUST = {
    # 優先順位の整理（効果×手間の図）
    'consulting': svg(
        f'<rect x="40" y="20" width="230" height="170" rx="10" fill="{L}" stroke="none"/>'
        f'<path d="M40 190V20M40 190h230" />'
        f'<path d="M155 20v170M40 105h230" stroke="{G}" stroke-dasharray="5 6"/>'
        f'<circle cx="92" cy="150" r="9" fill="#fff"/><circle cx="210" cy="150" r="9" fill="#fff"/><circle cx="100" cy="62" r="9" fill="#fff"/>'
        f'<circle cx="215" cy="58" r="15" fill="{Y}"/><path d="M209 58l5 5 9-10"/>'
        + t(215, 94, 'まずここから', 12) + t(24, 110, '効果', 12, fill=N) + t(155, 212, '手間の少なさ', 12),
        '効果と手間で、何から手をつけるかを整理する図'),
    # 発注までの流れ
    'btob-marketing': svg(
        ''.join(f'<circle cx="{x}" cy="95" r="26" fill="{c}"/>' for x, c in ((45, L), (115, L), (185, L), (255, Y)))
        + '<path d="M75 95h10M145 95h10M215 95h10"/><path d="M81 90l5 5-5 5M151 90l5 5-5 5M221 90l5 5-5 5"/>'
        + ''.join(t(x, 100, s, 13) for x, s in ((45, '検索'), (115, '比較'), (185, '相談'), (255, '発注')))
        + f'<rect x="30" y="146" width="240" height="60" rx="10" stroke="{G}"/>'
        + t(150, 171, '担当者が社内で説明しやすい情報を、', 12, weight=500)
        + t(150, 190, '段階ごとに用意します', 12, weight=500),
        '検索から発注までの流れの図'),
    # 検索 → 記事 → 問い合わせ
    'seo-consulting': svg(
        f'<rect x="18" y="30" width="264" height="40" rx="20" fill="#fff"/><circle cx="44" cy="50" r="8"/><path d="M50 56l6 6"/>'
        + t(160, 55, '〇〇加工 神奈川', 13, weight=500)
        + '<path d="M150 78v18"/><path d="M144 90l6 6 6-6"/>'
        + f'<rect x="60" y="104" width="180" height="62" rx="8" fill="{L}" stroke="none"/>'
        + f'<path d="M78 122h90M78 136h140M78 150h110" stroke="{G}"/>'
        + '<path d="M150 170v12"/><path d="M144 176l6 6 6-6"/>'
        + f'<rect x="112" y="186" width="76" height="28" rx="6" fill="{Y}" stroke="none"/>' + t(150, 205, 'お問い合わせ', 12),
        '検索から記事、問い合わせにつながる流れの図'),
    # 広告の段階
    'ad-consulting': svg(
        f'<path d="M30 30h240l-30 50H60z" fill="{L}" stroke="none"/>'
        f'<path d="M64 88h172l-28 46H92z" fill="{L}" stroke="none"/>'
        f'<path d="M96 142h108l-26 44h-56z" fill="{Y}" stroke="none"/>'
        + t(150, 60, '広告が表示される', 13) + t(150, 116, 'クリックされる', 13) + t(150, 170, '問い合わせ', 13)
        + t(150, 210, '1件あたりの費用で効果を測る', 12, weight=500),
        '広告の表示からクリック、問い合わせまでの段階の図'),
    # 離脱している場所を見つける
    'cro-consulting': svg(
        f'<rect x="30" y="26" width="240" height="30" rx="6" fill="{L}" stroke="none"/>'
        f'<rect x="60" y="78" width="180" height="30" rx="6" fill="{L}" stroke="none"/>'
        f'<rect x="100" y="130" width="100" height="30" rx="6" fill="{L}" stroke="none"/>'
        f'<rect x="126" y="182" width="48" height="26" rx="6" fill="{Y}" stroke="none"/>'
        + t(150, 46, 'サイトを見た', 12) + t(150, 98, '料金を見た', 12) + t(150, 150, 'フォームを開いた', 12) + t(150, 200, '送信', 12)
        + f'<path d="M244 118q16 8 8 24" stroke="{N}"/><circle cx="262" cy="150" r="14" fill="{Y}" stroke="none"/>'
        + t(262, 155, '!', 16) + t(262, 180, 'ここで', 11) + t(262, 194, '止まる', 11),
        'どこで問い合わせをやめているかを見つける図'),
    # AIに正しく伝わる
    'llmo-consulting': svg(
        f'<rect x="20" y="40" width="110" height="140" rx="8" fill="#fff"/>'
        f'<path d="M36 64h60M36 84h78M36 104h70M36 124h78M36 144h50" stroke="{G}"/>'
        + t(75, 200, '会社のサイト', 12)
        + '<path d="M140 110h26"/><path d="M160 104l6 6-6 6"/>'
        + f'<path d="M176 56h104a10 10 0 0 1 10 10v70a10 10 0 0 1-10 10h-60l-18 16v-16h-26a10 10 0 0 1-10-10V66a10 10 0 0 1 10-10z" fill="{L}" stroke="none"/>'
        + t(228, 86, 'AIの答え', 12) + t(228, 110, '「〇〇が得意な', 12, weight=500) + t(228, 128, '　会社です」', 12, weight=500)
        + f'<circle cx="278" cy="52" r="12" fill="{Y}" stroke="none"/>' + t(278, 57, 'AI', 11),
        'サイトの内容がAIの答えに正しく使われる図'),
    # 会社のサイト（パソコン＋スマホ）
    'website': svg(
        f'<rect x="14" y="24" width="210" height="150" rx="8" fill="#fff"/><path d="M14 44h210" stroke="{G}"/>'
        f'<circle cx="28" cy="34" r="3" fill="{G}" stroke="none"/><circle cx="40" cy="34" r="3" fill="{G}" stroke="none"/>'
        f'<rect x="28" y="56" width="120" height="12" rx="3" fill="{N}" stroke="none"/><rect x="28" y="76" width="90" height="8" rx="3" fill="{G}" stroke="none"/>'
        f'<rect x="28" y="94" width="58" height="18" rx="9" fill="{Y}" stroke="none"/>'
        f'<rect x="28" y="124" width="56" height="36" rx="4" fill="{L}" stroke="none"/><rect x="92" y="124" width="56" height="36" rx="4" fill="{L}" stroke="none"/><rect x="156" y="124" width="56" height="36" rx="4" fill="{L}" stroke="none"/>'
        f'<rect x="206" y="80" width="80" height="130" rx="12" fill="#fff"/>'
        f'<rect x="216" y="100" width="46" height="8" rx="3" fill="{N}" stroke="none"/><rect x="216" y="114" width="58" height="6" rx="3" fill="{G}" stroke="none"/>'
        f'<rect x="216" y="130" width="60" height="30" rx="4" fill="{L}" stroke="none"/><rect x="216" y="184" width="60" height="16" rx="8" fill="{Y}" stroke="none"/>',
        'パソコンとスマホで見やすい会社のサイトの図'),
    # 縦長の1枚ページ
    'lp': svg(
        f'<rect x="100" y="8" width="100" height="204" rx="14" fill="#fff"/>'
        f'<rect x="112" y="24" width="76" height="40" rx="4" fill="{L}" stroke="none"/>'
        f'<rect x="112" y="72" width="60" height="7" rx="3" fill="{N}" stroke="none"/><rect x="112" y="86" width="76" height="5" rx="2" fill="{G}" stroke="none"/><rect x="112" y="96" width="70" height="5" rx="2" fill="{G}" stroke="none"/>'
        f'<rect x="112" y="112" width="34" height="30" rx="4" fill="{L}" stroke="none"/><rect x="154" y="112" width="34" height="30" rx="4" fill="{L}" stroke="none"/>'
        f'<rect x="112" y="150" width="76" height="22" rx="4" fill="{L}" stroke="none"/><rect x="112" y="182" width="76" height="16" rx="8" fill="{Y}" stroke="none"/>'
        + t(58, 48, '悩み', 12) + t(58, 96, '強み', 12) + t(58, 144, '声', 12) + t(58, 192, '申込み', 12)
        + '<path d="M78 44h26M78 92h26M78 140h26M84 188h20" stroke="' + G + '" stroke-dasharray="3 4"/>'
        + f'<path d="M232 40v140" stroke="{G}"/><path d="M226 172l6 8 6-8"/>' + t(262, 114, '1枚で', 12) + t(262, 130, '伝える', 12),
        '1枚の縦長ページで、悩みから申込みまで伝える図'),
    # 記事づくり
    'seo-writing': svg(
        f'<rect x="30" y="20" width="150" height="180" rx="8" fill="#fff"/>'
        f'<rect x="46" y="38" width="100" height="10" rx="3" fill="{N}" stroke="none"/>'
        f'<path d="M46 66h118M46 80h104M46 94h112" stroke="{G}"/><rect x="46" y="108" width="60" height="8" rx="3" fill="{Y}" stroke="none"/>'
        f'<path d="M46 130h118M46 144h96M46 158h110M46 172h80" stroke="{G}"/>'
        f'<path d="M200 170l24-30 20 14 32-50" /><circle cx="276" cy="104" r="7" fill="{Y}" stroke="none"/>'
        f'<path d="M200 190h80" stroke="{G}"/>' + t(240, 208, '読まれる記事が増える', 11, weight=500),
        '記事を積み重ねて、読まれる数が増えていく図'),
    # 事例インタビュー
    'case-interview': svg(
        f'<path d="M24 40h150a10 10 0 0 1 10 10v44a10 10 0 0 1-10 10H70l-20 18v-18H24a10 10 0 0 1-10-10V50a10 10 0 0 1 10-10z" fill="{L}" stroke="none"/>'
        + t(99, 70, '導入前は、何に', 12, weight=500) + t(99, 88, '困っていましたか？', 12, weight=500)
        + f'<path d="M126 118h150a10 10 0 0 1 10 10v44a10 10 0 0 1-10 10h-26v18l-20-18h-104a10 10 0 0 1-10-10v-44a10 10 0 0 1 10-10z" fill="{Y}" stroke="none"/>'
        + t(201, 148, '相談できる相手が', 12, weight=500) + t(201, 166, 'できたことです', 12, weight=500)
        + t(250, 70, '“', 44, fill=G),
        'お客様の声を聞き取って記事にする図'),
    # AIで作業時間を減らす
    'ai-katsuyo': svg(
        t(20, 50, '今まで', 13, anchor='start')
        + f'<rect x="90" y="34" width="190" height="24" rx="6" fill="{L}" stroke="none"/>'
        + t(20, 110, 'AIを使うと', 13, anchor='start')
        + f'<rect x="90" y="94" width="80" height="24" rx="6" fill="{Y}" stroke="none"/>'
        + f'<path d="M180 106h90" stroke="{G}" stroke-dasharray="5 6"/>' + t(226, 100, '空いた時間', 11, weight=500)
        + f'<circle cx="150" cy="172" r="26" fill="#fff"/><path d="M150 156v16l11 8"/>'
        + t(150, 214, '見積書・返信・議事録の下書きを短く', 11, weight=500),
        'AIを使って作業時間を短くする図'),
}

ICON = {
    'talk': '<path d="M8 12h32v20H22l-9 8v-8H8z"/><path d="M16 20h16M16 26h10"/>',
    'step': '<path d="M8 38h10v-9h10v-9h12v18"/><circle cx="36" cy="12" r="4" fill="%Y%" stroke="none"/>',
    'loop': '<path d="M38 24a14 14 0 1 1-4-10"/><path d="M34 6v8h-8"/>',
    'search': '<circle cx="21" cy="21" r="11"/><path d="M29 29l10 10"/>',
    'handshake': '<path d="M6 22l8-8 8 4 6-4 8 2 6 6"/><path d="M14 26l8 8 4-2 4 4 4-2 6-8"/>',
    'arrowup': '<path d="M8 38l10-12 8 6 14-18"/><path d="M32 14h8v8"/>',
    'check': '<circle cx="24" cy="24" r="16"/><path d="M16 24l6 6 11-12"/>',
    'tool': '<path d="M30 8a10 10 0 0 0-9 14L8 35l5 5 13-13a10 10 0 0 0 14-9l-6 4-5-5z"/>',
    'mail': '<rect x="7" y="12" width="34" height="24" rx="3"/><path d="M8 14l16 12 16-12"/>',
    'factory': '<path d="M6 40V20l10 6v-6l10 6v-6l10 6V10h6v30z"/>',
    'person': '<circle cx="24" cy="16" r="7"/><path d="M10 40c2-9 8-13 14-13s12 4 14 13"/>',
}


def icon(name, size=40):
    body = ICON[name].replace('%Y%', Y)
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" aria-hidden="true" fill="none" stroke="{N}" '
            f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="st-icon">'
            f'<circle cx="34" cy="14" r="9" fill="{Y}" stroke="none" opacity=".55"/>{body}</svg>')


def flow_story():
    """はじめた理由：工場 → サイト → 問い合わせ3倍"""
    return svg(
        f'<rect x="10" y="30" width="80" height="70" rx="10" fill="{L}" stroke="none"/>'
        f'<path d="M26 88V60l12 7v-7l12 7v-7l12 7V48h8v40z" fill="#fff"/>' + t(50, 122, '研磨工場', 12)
        + '<path d="M100 65h30"/><path d="M124 59l6 6-6 6"/>'
        + f'<rect x="140" y="30" width="80" height="70" rx="10" fill="#fff"/><path d="M140 46h80" stroke="{G}"/>'
        f'<rect x="152" y="56" width="44" height="8" rx="3" fill="{N}" stroke="none"/><rect x="152" y="72" width="30" height="12" rx="6" fill="{Y}" stroke="none"/>'
        + t(180, 122, 'サイトを直す', 12)
        + '<path d="M230 65h30"/><path d="M254 59l6 6-6 6"/>'
        + f'<rect x="270" y="30" width="80" height="70" rx="10" fill="{Y}" stroke="none"/>' + t(310, 74, '3倍', 26)
        + t(310, 122, '有効な問い合わせ', 12),
        '研磨工場のサイトを直して、有効な問い合わせが3倍になった流れの図', vb='0 0 360 132')


def bars_3x():
    """実績：有効な問い合わせ 1 → 3（比率だけを示す）"""
    return svg(
        f'<path d="M40 190h240" stroke="{G}"/>'
        f'<rect x="80" y="150" width="60" height="40" rx="6" fill="{L}" stroke="none"/>'
        f'<rect x="180" y="70" width="60" height="120" rx="6" fill="{Y}" stroke="none"/>'
        + t(110, 140, '1', 18) + t(210, 60, '3倍', 20)
        + t(110, 210, '作り直す前', 12, weight=500) + t(210, 210, '作り直した後', 12, weight=500)
        + '<path d="M150 120q14-40 26-50"/><path d="M168 66l9 4-3 9"/>',
        '有効な問い合わせが、作り直す前の3倍になったことを示す棒グラフ')

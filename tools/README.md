# tools

サイト運用の補助スクリプト（リポジトリのルートで実行する）。

- `python3 tools/subset_fonts.py` … 新しい記事・ページで使った漢字をフォントに追加する。コラムなどを追加したら実行。
- `python3 -c "import sys; sys.path.insert(0,'tools'); exec(open('tools/build_webai.py').read()); exec(open('tools/webai_pages.py').read()); [build(p) for p in PAGES]; [build(p) for p in PAGES]; build_hub()"`
  … Web集客・AI活用支援（/web-ai/）のサービスページとトップを作り直す。文章は `webai_pages.py`、デザインは `build_webai.py`。
  実行後は `python3 tools/structured_data.py` で構造化データを入れ直し、`npx tailwindcss -i css/input.css -o css/tailwind.css --minify` でCSSも作り直す。
- `python3 tools/structured_data.py` … 全ページの構造化データ（会社・サイト・ページの種類・サービス・よくある質問）を入れ直す。ページを追加・変更したら実行。
- `python3 tools/llms_txt.py` … AI検索向けの案内ファイル `llms.txt` を作り直す。ページを追加したら実行。
- `python3 tools/footer.py` … 全ページのフッターを共通の形に置きかえる。フッターを直すときはこのファイルを直して実行。
- `python3 tools/ogp_meta.py` … OGP（SNSで共有したときの画像など）のタグを全ページに入れ直す。元画像のデザインは `tools/ogp-source.html`。

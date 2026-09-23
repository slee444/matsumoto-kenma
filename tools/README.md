# tools

サイト運用の補助スクリプト（リポジトリのルートで実行する）。

- `python3 tools/subset_fonts.py` … 新しい記事・ページで使った漢字をフォントに追加する。コラムなどを追加したら実行。
- `python3 -c "exec(open('tools/build_webai.py').read()); exec(open('tools/webai_pages.py').read()); [build(p) for p in PAGES]; [build(p) for p in PAGES]; build_hub()"`
  … Web集客・AI活用支援（/web-ai/）のサービスページとトップを作り直す。文章は `webai_pages.py`、デザインは `build_webai.py`。
  実行後は `npx tailwindcss -i css/input.css -o css/tailwind.css --minify` でCSSも作り直す。

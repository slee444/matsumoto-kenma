"""Rebuild the self-hosted Noto Sans JP subset fonts so they cover every character used on the site.

Run after adding pages/articles with new kanji:
    python3 tools/subset_fonts.py
Needs: pip install fonttools brotli
"""
import glob, html, os, re, subprocess, sys, urllib.request

SRC_URL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf'
SRC = '/tmp/NotoSansJP-VF.ttf'
WEIGHTS = [300, 400, 500, 600, 700]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def site_chars():
    text = ''
    for fn in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        if 'node_modules' in fn:
            continue
        s = open(fn, encoding='utf-8').read()
        s = re.sub(r'<script(?![^>]*ld\+json).*?</script>|<style.*?</style>', '', s, flags=re.S)
        text += html.unescape(re.sub(r'<[^>]+>', ' ', s))
    for extra in ['news/posts.txt']:
        p = os.path.join(ROOT, extra)
        if os.path.exists(p):
            text += open(p, encoding='utf-8').read()
    cps = {ord(c) for c in text if ord(c) >= 0x20}
    cps |= set(range(0x20, 0x7F))            # ASCII
    cps |= set(range(0x3000, 0x3100))        # CJK punctuation, hiragana, katakana
    cps |= set(range(0xFF00, 0xFFF0))        # full/half-width forms
    return cps

def main():
    if not os.path.exists(SRC):
        print('downloading source font...')
        urllib.request.urlretrieve(SRC_URL, SRC)
    cps = site_chars()
    uni = '/tmp/mk_unicodes.txt'
    open(uni, 'w').write('\n'.join('U+%04X' % c for c in sorted(cps)))
    print('characters:', len(cps))
    for w in WEIGHTS:
        inst = f'/tmp/NotoSansJP-{w}.ttf'
        subprocess.run([sys.executable, '-m', 'fontTools.varLib.instancer', SRC, f'wght={w}',
                        '--update-name-table', '-o', inst], check=True, capture_output=True)
        out = os.path.join(ROOT, 'fonts', f'noto-sans-jp-{w}.woff2')
        subprocess.run([sys.executable, '-m', 'fontTools.subset', inst, f'--unicodes-file={uni}',
                        '--flavor=woff2', '--layout-features=*', f'--output-file={out}'], check=True)
        print(w, os.path.getsize(out) // 1024, 'KB')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build the deployable copies of the deck into deploy/.

index.html            — one page with every image inside it, the two
                        recordings sitting beside it in assets/
index-standalone.html — the same page with the recordings inlined too, so
                        the whole deck is a single file

Images are re-encoded to JPEG (the cover art stays PNG for its
transparency) and the recordings to a lighter preset, because the
originals are sized for archiving rather than for a page load. Each image
is inlined once and referenced by name, since several appear on more than
one slide.

Usage: python3 build-deploy.py
"""
import base64, os, re, shutil, subprocess, sys, tempfile

SRC   = 'index.html'
OUT   = 'deploy'
KEEP_PNG = {'cover-cards'}          # needs its alpha channel
VIDEO_PRESET = {'walkthrough': 'Preset640x480',        # phone, drawn small
                'web-walkthrough': 'Preset960x540'}    # web, drawn wide

def sh(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    html = open(SRC).read()
    names = sorted({m for m in re.findall(r"assets/([a-z0-9-]+)\.png", html)
                    if os.path.exists(f'assets/{m}.png')})
    vids  = sorted(set(re.findall(r"assets/([a-z0-9-]+)\.mp4", html)))

    os.makedirs(f'{OUT}/assets', exist_ok=True)
    tmp = tempfile.mkdtemp()
    uris = {}
    for n in names:
        src = f'assets/{n}.png'
        if n in KEEP_PNG:
            dst = f'{tmp}/{n}.png'; shutil.copy(src, dst); sh('sips', '-Z', '1600', dst)
            mime = 'image/png'
        else:
            dst = f'{tmp}/{n}.jpg'
            sh('sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '82', src, '--out', dst)
            mime = 'image/jpeg'
        uris[n] = f'data:{mime};base64,' + base64.b64encode(open(dst, 'rb').read()).decode()

    for v in vids:
        sh('avconvert', '--source', f'assets/{v}.mp4', '--output', f'{OUT}/assets/{v}.mp4',
           '--preset', VIDEO_PRESET.get(v, 'Preset960x540'), '--replace')

    # one copy of each image, referenced by name — several slides share them
    table = 'const A = {\n' + ''.join(f'  {n!r}: {uris[n]!r},\n' for n in names) + '};\n'
    page  = html
    for n in names:
        page = page.replace(f'"assets/{n}.png"', f'"${{A[{n!r}]}}"')   # inside markup
        page = page.replace(f"'assets/{n}.png'", f'A[{n!r}]')          # inside data
    marker = '<script>\n'
    i = page.index(marker, page.index('</style>'))
    page = page[:i + len(marker)] + table + page[i + len(marker):]
    open(f'{OUT}/index.html', 'w').write(page)

    one = page
    for v in vids:
        uri = 'data:video/mp4;base64,' + base64.b64encode(open(f'{OUT}/assets/{v}.mp4','rb').read()).decode()
        one = one.replace(f"'assets/{v}.mp4'", repr(uri))
    open(f'{OUT}/index-standalone.html', 'w').write(one)

    for f in (f'{OUT}/index.html', f'{OUT}/index-standalone.html'):
        print(f'{f:32} {os.path.getsize(f)/1048576:5.1f} MB')
    shutil.rmtree(tmp)

if __name__ == '__main__':
    main()

"""Build everything generated in this repo from its sources.

  python3 tools/build.py           tokens.css, components, prototypes, previews and the home page
  python3 tools/build.py --site    the same, then the Vite build into site/dist (run `npm install` in site/ once)
  python3 tools/build.py --check   rebuild, then fail if a committed file changed (CI runs this)

Sources                                   Generated
design-system/tokens.json            ->   design-system/tokens.css
tools/src/bundle.src.js + icons      ->   design-system/components/bundle.js
tools/src/onboarding-components.src.js,
tools/src/components.css             ->   design-system/components/onboarding.{js,css}
tools/src/proto.html                 ->   prototype/cashout-prototype.html
tools/src/onboarding.html            ->   prototype/onboarding-prototype.html
tools/src/boost.html                 ->   prototype/boost-prototype.html
tools/src/popup.css                       is shared by the last two and by components.css
design-system/DesignTokens.swift     ->   SwiftTokens and Typography previews
all of the above                     ->   the marked blocks in website/index.html
"""
import base64, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)
def read(p): return open(p, encoding='utf-8').read()
def write(p, s): open(p, 'w', encoding='utf-8').write(s)

MIME = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'svg': 'image/svg+xml', 'webp': 'image/webp'}
GENERATED = ['design-system/tokens.css', 'design-system/components/bundle.js', 'design-system/components/onboarding.js',
             'design-system/components/onboarding.css', 'prototype/cashout-prototype.html', 'prototype/onboarding-prototype.html',
             'prototype/boost-prototype.html', 'design-system/components/SwiftTokens/preview.html',
             'design-system/components/Typography/preview.html', 'website/index.html']


def uri(path):
    return 'data:%s;base64,%s' % (MIME[path.rsplit('.', 1)[1].lower()], base64.b64encode(open(path, 'rb').read()).decode())


def fill(text, files, pattern='{{%s}}'):
    """Replace each placeholder with the file as a data URI, then make sure none is left."""
    for key, path in files.items():
        text = text.replace(pattern % key, uri(path))
    left = re.findall(re.escape(pattern).replace('%s', r'(\w+)'), text)
    assert not left, 'unfilled placeholders: %s' % sorted(set(left))
    return text


# ---------- tokens ----------
def tokens_css():
    t = json.load(open(P('design-system', 'tokens.json'), encoding='utf-8'))
    themes = [x['id'] for x in t['color']['themes']]
    def v(tok, theme):
        val = tok['value']; return val if isinstance(val, str) else val.get(theme, val[themes[0]])
    out = ['/* Cashout iOS Design System — generated from tokens.json */']
    first = ['  --%s: %s;' % (c['name'], v(c, themes[0])) for c in t['color']['tokens'] + t['shadow']['tokens']]
    out.append(':root, [data-theme="%s"] {\n%s\n}' % (themes[0], '\n'.join(first)))
    for x in themes[1:]:
        b = ['  --%s: %s;' % (c['name'], v(c, x)) for c in t['color']['tokens'] + t['shadow']['tokens'] if not isinstance(c['value'], str) and x in c['value']]
        out.append('[data-theme="%s"] {\n%s\n}' % (x, '\n'.join(b)))
    root = ['  --%s: %s;' % (c['name'], c['value']) for fam in ('spacing', 'radius', 'size', 'duration', 'easing') for c in t[fam]['tokens']]
    root += ['  --font-%s: %s;' % (k, s) for k, s in t['type']['families'].items()]
    out.append(':root {\n%s\n}' % '\n'.join(root))
    for g in t['type']['groups']:
        for s in g['styles']:
            ls = ' letter-spacing: %s;' % s['letterSpacing'] if 'letterSpacing' in s else ''
            out.append('.%s { font-family: var(--font-%s); font-size: %s; line-height: %s; font-weight: %s;%s }'
                       % (s['name'], s.get('family', g['family']), s['fontSize'], s['lineHeight'], s['fontWeight'], ls))
    write(P('design-system', 'tokens.css'), '\n'.join(out) + '\n')


# ---------- components ----------
def bundle_js():
    icons = P('tools', 'assets', 'icons')
    js = fill(read(P('tools', 'src', 'bundle.src.js')), {'HISTORY': os.path.join(icons, 'history.svg'), 'STAR': os.path.join(icons, 'coin.svg'),
                                                        'TIP': os.path.join(icons, 'tip96.png')}, '__%s__')
    assert '</script' not in js.lower()
    write(P('design-system', 'components', 'bundle.js'), js)


def mission_css():
    return re.search(r'/\* ---------- MissionCard ---------- \*/.*?(?=/\* ---------- CoachMark ---------- \*/)', read(P('tools', 'src', 'onboarding.html')), re.S).group(0)


def boost_css():
    b = read(P('tools', 'src', 'boost.html'))
    return b[b.index('/* ---------- EventBanner'):b.index('/* rewarded video and game stand-in */')].replace('{{popup_css}}\n', '')


def glow_js():
    return re.search(r'/\* glow:start \*/(.*?)/\* glow:end \*/', read(P('tools', 'src', 'onboarding.html')), re.S).group(1)


def components():
    ob, bo = P('tools', 'assets', 'onboarding'), P('tools', 'assets', 'boost')
    js = read(P('tools', 'src', 'onboarding-components.src.js'))
    js = js.replace('__GLOW__', '  /* God rays and light motes: shared with the prototype (tools/src/onboarding.html). */' + glow_js())
    js = fill(js, {'COIN': os.path.join(ob, 'coin.svg'), 'FOX': os.path.join(ob, 'fox.png'), 'HAND': os.path.join(ob, 'hand.png'),
                   'PILE': os.path.join(ob, 'pile.png'), 'CLOCK': os.path.join(ob, 'clock.svg'),
                   'LOGO': os.path.join(bo, 'logo.png'), 'TOPCOINS': os.path.join(bo, 'topcoins.png')}, '__%s__')
    assert '</script' not in js.lower()
    write(P('design-system', 'components', 'onboarding.js'), js)
    css = read(P('tools', 'src', 'components.css'))
    for name, text in (('mission rows from tools/src/onboarding.html', mission_css()), ('tools/src/popup.css', read(P('tools', 'src', 'popup.css'))),
                       ('2x coins from tools/src/boost.html', boost_css())):
        marker = '/* @include %s */\n' % name
        assert css.count(marker) == 1, marker
        css = css.replace(marker, text)
    write(P('design-system', 'components', 'onboarding.css'), css)


# ---------- prototypes ----------
def prototype(src, out, assets, extra=None):
    h = read(P('tools', 'src', src)).replace('{{popup_css}}', read(P('tools', 'src', 'popup.css')))
    files = {k: P('tools', 'assets', assets, f) for k, f in assets_map(assets).items()}
    files.update(extra or {})
    write(P('prototype', out), fill(h, files))


def assets_map(folder):
    return {
        'prototype': {'home_top': 'home-top.jpg', 'home_body': 'home-body.jpg', 'tabbar': 'tabbar.jpg', 'pattern': 'pattern.png',
                      'success_art': 'success-art.jpg', 'cash': 'cash.png', 'wallet': 'wallet.png', 'fox_briefcase': 'fox-briefcase.png',
                      'fox_think': 'fox-think.png', 'fox_thumb': 'fox-thumb.png', 'timer': 'timer.png', 'games': 'games.png',
                      'coin': 'coin.svg', 'arrow': 'arrow.svg'},
        'onboarding': {'banner': 'banner.jpg', 'below': 'below.jpg', 'tabbar': 'tabbar.jpg', 'fox': 'fox.png', 'hand': 'hand.png',
                       'pile': 'pile.png', 'coin': 'coin.svg', 'clock': 'clock.svg', 'handshake': 'handshake.png'},
        'boost': {'banner': 'banner.jpg', 'body': 'body.jpg', 'tabbar': 'tabbar.jpg', 'logo': 'logo.png', 'topcoins': 'topcoins.png',
                  'pile': 'pile.png', 'coin': 'coin.svg', 'clock': 'clock.svg'},
    }[folder]


def prototypes():
    icons = P('tools', 'assets', 'icons')
    prototype('proto.html', 'cashout-prototype.html', 'prototype', {'star': os.path.join(icons, 'coin.svg'), 'tip': os.path.join(icons, 'tip96.png')})
    prototype('onboarding.html', 'onboarding-prototype.html', 'onboarding')
    prototype('boost.html', 'boost-prototype.html', 'boost')


# ---------- previews ----------
WEIGHT_NAME = {400: 'Regular 400', 500: 'Medium 500', 600: 'SemiBold 600', 700: 'Bold 700', 800: 'ExtraBold 800'}


def previews():
    swift = read(P('design-system', 'DesignTokens.swift'))
    p = P('design-system', 'components', 'SwiftTokens', 'preview.html'); s = read(p)
    s, n = re.subn(r"code:\"(?:[^\"\\]|\\.)*\"", lambda m: 'code:' + json.dumps(swift), s, count=1)
    assert n == 1, 'SwiftTokens preview: code block not found'
    write(p, s)

    tok = json.load(open(P('design-system', 'tokens.json'), encoding='utf-8'))
    styles = {s['name']: s for g in tok['type']['groups'] for s in g['styles']}
    p = P('design-system', 'components', 'Typography', 'preview.html'); s = read(p)
    m = re.search(r'var T = (\[.*?\]);\n', s, re.S)
    rows = json.loads(m.group(1))
    if not any(r['cls'] == 'title1' for r in rows):
        at = next(i for i, r in enumerate(rows) if r['cls'] == 'large-title') + 1
        rows.insert(at, {'cls': 'title1', 'sample': 'Congrats!', 'figma': 'Cashout/Text/Title 1', 'size': '', 'weight': '', 'track': '0',
                         'rel': '.title', 'code': 'Text("Congrats!").font(.ds(.title1))'})
    for r in rows:
        t = styles.get(r['cls'])
        if t:
            r['size'] = '%s / %s' % (t['fontSize'][:-2], t['lineHeight'][:-2])
            r['weight'] = WEIGHT_NAME.get(t['fontWeight'], str(t['fontWeight']))
            r['track'] = t.get('letterSpacing', '0').replace('px', '') if t.get('letterSpacing') else '0'
    write(p, s[:m.start(1)] + json.dumps(rows) + s[m.end(1):])


# ---------- home page ----------
def inline(page, name, text):
    """Replace what sits between /* @gen name */ and /* @end name */ (each exactly once, in that order)."""
    start, end = '/* @gen %s */\n' % name, '/* @end %s */' % name
    assert page.count(start) == 1 and page.count(end) == 1, 'website/index.html: markers for %s must appear once each' % name
    a, b = page.index(start) + len(start), page.index(end)
    assert a <= b, 'website/index.html: markers for %s are out of order' % name
    return page[:a] + text.rstrip('\n') + '\n' + page[b:]


def home_page():
    page = read(P('website', 'index.html'))
    page = inline(page, 'tokens.css', read(P('design-system', 'tokens.css')))
    bundle_css = ''.join(l for l in read(P('design-system', 'components', 'bundle.css')).splitlines(True)
                         if not l.startswith('@import') and not l.startswith('body '))
    page = inline(page, 'bundle.css', bundle_css.strip())
    page = inline(page, 'onboarding.css', read(P('design-system', 'components', 'onboarding.css')))
    page = inline(page, 'bundle.js', read(P('design-system', 'components', 'bundle.js')).strip())
    page = inline(page, 'onboarding.js', read(P('design-system', 'components', 'onboarding.js')))
    tok = json.load(open(P('design-system', 'tokens.json'), encoding='utf-8'))
    page = inline(page, 'tokens.json', '  var TOKENS = ' + json.dumps(tok) + ';')
    write(P('website', 'index.html'), page)


def site():
    if not os.path.isdir(P('site', 'node_modules')):
        sys.exit('site/node_modules is missing: run `npm install` in site/ once, then build with --site again.')
    subprocess.run(['npm', 'run', 'build'], cwd=P('site'), check=True)


def build_all(with_site=False):
    tokens_css(); bundle_js(); components(); prototypes(); previews(); home_page()
    if with_site: site()


if __name__ == '__main__':
    args = sys.argv[1:]
    build_all('--site' in args)
    if '--check' in args:
        r = subprocess.run(['git', 'status', '--porcelain', '--'] + GENERATED, cwd=ROOT, capture_output=True, text=True)
        if r.stdout.strip():
            sys.exit('Generated files are out of date. Run `python3 tools/build.py` and commit the result:\n' + r.stdout)
    print('built: tokens.css, components, 3 prototypes, previews, website/index.html' + (', site/dist' if '--site' in args else ''))

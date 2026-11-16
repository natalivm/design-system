"""Build everything generated in this repo from its sources.

  python3 tools/build.py           tokens.css, components, prototypes, previews and the home page
  python3 tools/build.py --site    the same, then the published site in dist/ (what GitHub Pages serves)
  python3 tools/build.py --check   rebuild, then fail if a committed file changed (CI runs this)

Sources                                   Generated
design-system/tokens.json            ->   design-system/tokens.css
tools/src/bundle.src.js + icons      ->   design-system/components/bundle.js
tools/src/onboarding-components.src.js,
tools/src/components.css             ->   design-system/components/onboarding.{js,css}
tools/src/proto.html                 ->   prototype/cashout-prototype.html
tools/src/onboarding.html            ->   prototype/onboarding-prototype.html
tools/src/boost.html                 ->   prototype/boost-prototype.html
tools/src/survey.html                ->   prototype/survey-prototype.html
tools/src/popup.css, tools/src/kit.js       are shared by the prototypes (popup.css also by components.css)
design-system/DesignTokens.swift     ->   SwiftTokens and Typography previews
all of the above                     ->   the marked blocks in website/index.html
"""
import base64, hashlib, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)
def read(p): return open(p, encoding='utf-8').read()
def write(p, s): open(p, 'w', encoding='utf-8').write(s)

MIME = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'svg': 'image/svg+xml', 'webp': 'image/webp'}
GENERATED = ['design-system/tokens.css', 'ios/Cashout/Sources/DesignTokens.swift', 'ios/Cashout/Assets.xcassets', 'design-system/components/bundle.js', 'design-system/components/onboarding.js',
             'design-system/components/onboarding.css', 'prototype/cashout-prototype.html', 'prototype/onboarding-prototype.html',
             'prototype/boost-prototype.html', 'prototype/survey-prototype.html', 'design-system/components/SwiftTokens/preview.html',
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
    # the ramp as variables as well as classes, so component CSS can reference a step
    # without taking the whole class on the element
    for g in t['type']['groups']:
        for st in g['styles']:
            root += ['  --text-%s-size: %s;' % (st['name'], st['fontSize']),
                     '  --text-%s-line: %s;' % (st['name'], st['lineHeight']),
                     '  --text-%s-weight: %s;' % (st['name'], st['fontWeight'])]
            if 'letterSpacing' in st:
                root.append('  --text-%s-track: %s;' % (st['name'], st['letterSpacing']))
    out.append(':root {\n%s\n}' % '\n'.join(root))
    for g in t['type']['groups']:
        for s in g['styles']:
            ls = ' letter-spacing: %s;' % s['letterSpacing'] if 'letterSpacing' in s else ''
            out.append('.%s { font-family: var(--font-%s); font-size: %s; line-height: %s; font-weight: %s;%s }'
                       % (s['name'], s.get('family', g['family']), s['fontSize'], s['lineHeight'], s['fontWeight'], ls))
    write(P('design-system', 'tokens.css'), '\n'.join(out) + '\n')


# ---------- iOS tokens ----------
# How each text style scales with Dynamic Type. This is an iOS mapping, not a design token,
# so it lives here; every style must be listed, or the build stops rather than guessing .body.
RELATIVE_TO = {'amount': 'largeTitle', 'large-title': 'largeTitle', 'popup-title': 'largeTitle',
               'button-large': 'title2', 'popup-body': 'body', 'title1': 'title', 'title2': 'title2',
               'title3': 'title3', 'headline': 'headline', 'body': 'body', 'callout': 'callout',
               'subheadline': 'subheadline', 'footnote': 'footnote', 'caption': 'caption', 'tab-label': 'caption2'}
WEIGHTS = {800: 'heavy', 700: 'bold', 600: 'semibold', 500: 'medium', 400: 'regular'}


def camel(name, strip=''):
    if strip and name.startswith(strip):
        name = name[len(strip):]
    head, *rest = name.split('-')
    return head + ''.join(w[:1].upper() + w[1:] for w in rest)


def pt(v):
    n = float(str(v).replace('px', ''))
    return str(int(n)) if n == int(n) else str(n)


def design_tokens_swift():
    t = json.load(open(P('design-system', 'tokens.json'), encoding='utf-8'))
    src = read(P('tools', 'src', 'DesignTokens.swift'))
    W = 'design-system/DesignTokens.swift'

    pad = max(len(camel(c['name'])) for c in t['color']['tokens'])
    colors = ['    static let %-*s = Color("%s")' % (pad, camel(c['name']), c['name']) for c in t['color']['tokens']]
    src = inline(src, 'colors', '\n'.join(colors), W)

    styles = [(s, g) for g in t['type']['groups'] for s in g['styles']]
    missing = [s['name'] for s, _ in styles if s['name'] not in RELATIVE_TO]
    assert not missing, 'tokens.json adds text styles with no Dynamic Type mapping in RELATIVE_TO: %s' % missing
    src = inline(src, 'type-cases', '    case ' + ', '.join(camel(s['name']) for s, _ in styles), W)

    spad = max(len(camel(s['name'])) for s, _ in styles)
    spec = ['        case .%-*s (%s, .%s, .%s)' % (spad + 1, camel(s['name']) + ':', pt(s['fontSize']),
                                                   WEIGHTS[s['fontWeight']], RELATIVE_TO[s['name']]) for s, _ in styles]
    src = inline(src, 'type-spec', '\n'.join(spec), W)

    display = [camel(s['name']) for s, g in styles if s.get('family', g['family']) == 'display']
    sans = [camel(s['name']) for s, g in styles if s.get('family', g['family']) != 'display']
    src = inline(src, 'type-family', '        case %s: "Nunito-ExtraBold"\n        case %s: "PlusJakartaSans"'
                 % (', '.join('.' + n for n in display), ', '.join('.' + n for n in sans)), W)

    def group(enum, fam, strip, rename=None):
        items = [((rename or camel)(c['name'], strip) if rename else camel(c['name'], strip), pt(c['value']))
                 for c in t[fam]['tokens']]
        return 'enum %s { static let %s }' % (enum, ', '.join('%s: CGFloat = %s' % (n, v) for n, v in items))
    metrics = [group('Space', 'spacing', 'space-', lambda n, s: 's' + n[len(s):]),
               group('Radius', 'radius', 'radius-'), group('Size', 'size', '')]
    src = inline(src, 'metrics', '\n'.join(metrics), W)

    durs = ['%s: Double = %s' % (camel(c['name'], 'duration-'), float(c['value'].replace('ms', '')) / 1000)
            for c in t['duration']['tokens']]
    curves = ['enum Duration { static let %s }' % ', '.join(durs), '', 'enum Curve {']
    for c in t['easing']['tokens']:
        pts = c['value'][c['value'].index('(') + 1:c['value'].rindex(')')]
        curves.append('    /// %s' % c['usage'].strip())
        curves.append('    static func %s(_ d: Double = Duration.base) -> Animation { .timingCurve(%s, duration: d) }'
                      % (camel(c['name'], 'easing-'), ', '.join(x.strip() for x in pts.split(','))))
    curves.append('}')
    src = inline(src, 'motion', '\n'.join(curves), W)

    out = P('ios', 'Cashout', 'Sources', 'DesignTokens.swift')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    write(out, src)


# ---------- iOS asset catalog ----------
# Every raster we own sits between 1.3x and 3x of the size it is drawn at, so each one goes in
# the 2x slot: that is the closest honest declaration, and the views set explicit frames anyway.
# tools/audit-assets.md records what each would need to be properly 3x.
XCINFO = {'author': 'xcode', 'version': 1}


def _rgba(v):
    v = v.strip()
    if v.startswith('#'):
        h = v[1:]
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [1.0]
    m = re.match(r'rgba?\(([^)]+)\)', v)
    assert m, 'colour the asset catalog cannot parse: %s' % v
    parts = [x.strip() for x in m.group(1).split(',')]
    return [int(parts[0]) / 255, int(parts[1]) / 255, int(parts[2]) / 255,
            float(parts[3]) if len(parts) > 3 else 1.0]


def _colorset(value, themes):
    def entry(v, dark=False):
        r, g, b, a = _rgba(v)
        e = {'idiom': 'universal',
             'color': {'color-space': 'srgb',
                       'components': {k: '%.3f' % x for k, x in (('alpha', a), ('red', r), ('green', g), ('blue', b))}}}
        if dark:
            e['appearances'] = [{'appearance': 'luminosity', 'value': 'dark'}]
        return e
    light = value if isinstance(value, str) else value[themes[0]]
    out = [entry(light)]
    if not isinstance(value, str) and len(themes) > 1 and value.get(themes[1], light) != light:
        out.append(entry(value[themes[1]], dark=True))
    return {'colors': out, 'info': XCINFO}


def ios_assets():
    """design-system/tokens.json + tools/assets -> ios/Cashout/Assets.xcassets"""
    t = json.load(open(P('design-system', 'tokens.json'), encoding='utf-8'))
    themes = [x['id'] for x in t['color']['themes']]
    root = P('ios', 'Cashout', 'Assets.xcassets')
    if os.path.isdir(root):
        shutil.rmtree(root)
    for d in (root, os.path.join(root, 'Colors'), os.path.join(root, 'Images')):
        os.makedirs(d)
        write(os.path.join(d, 'Contents.json'), json.dumps({'info': XCINFO}, indent=2) + '\n')

    for c in t['color']['tokens']:
        d = os.path.join(root, 'Colors', c['name'] + '.colorset')
        os.makedirs(d)
        write(os.path.join(d, 'Contents.json'), json.dumps(_colorset(c['value'], themes), indent=2) + '\n')

    # one imageset per distinct file; identical bytes in two prototype folders share a name
    files, by_digest = [], {}
    for folder in sorted(os.listdir(P('tools', 'assets'))):
        fdir = P('tools', 'assets', folder)
        if not os.path.isdir(fdir):
            continue
        for f in sorted(os.listdir(fdir)):
            if os.path.splitext(f)[1].lower() not in ('.png', '.jpg', '.svg'):
                continue
            full = os.path.join(fdir, f)
            digest = hashlib.sha256(open(full, 'rb').read()).hexdigest()
            if digest in by_digest:
                continue
            by_digest[digest] = full
            files.append((folder, f, full))

    stems = [os.path.splitext(f)[0] for _, f, _ in files]
    images = []
    for folder, f, full in files:
        stem, ext = os.path.splitext(f)
        name = stem if stems.count(stem) == 1 else '%s-%s' % (folder, stem)
        d = os.path.join(root, 'Images', name + '.imageset')
        os.makedirs(d)
        shutil.copyfile(full, os.path.join(d, f))
        if ext.lower() == '.svg':
            body = {'images': [{'idiom': 'universal', 'filename': f}], 'info': XCINFO,
                    'properties': {'preserves-vector-representation': True}}
        else:
            body = {'images': [{'idiom': 'universal', 'scale': '1x'},
                               {'idiom': 'universal', 'filename': f, 'scale': '2x'},
                               {'idiom': 'universal', 'scale': '3x'}], 'info': XCINFO}
        write(os.path.join(d, 'Contents.json'), json.dumps(body, indent=2) + '\n')
        images.append(name)
    return images


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
def tokens_vars():
    """The token custom properties for the prototypes: light values and layout, without the type classes."""
    blocks = read(P('design-system', 'tokens.css')).split('\n}\n')
    keep = [b for b in blocks if b.lstrip().startswith((':root', '/*')) and '.%s {' not in b]
    return '\n}\n'.join(b.split('*/\n', 1)[-1] if b.startswith('/*') else b for b in keep[:2]) + '\n}\n'


def prototype(src, out, assets, extra=None):
    h = read(P('tools', 'src', src)).replace('{{tokens_css}}', tokens_vars()).replace('{{popup_css}}', read(P('tools', 'src', 'popup.css'))).replace('{{kit_js}}', read(P('tools', 'src', 'kit.js')))
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
                       'pile': 'pile.png', 'coin': 'coin.svg', 'clock': 'clock.svg', 'handshake': 'handshake.png',
                       'topcoins': '../boost/topcoins.png'},
        'boost': {'banner': 'banner.jpg', 'body': 'body.jpg', 'tabbar': 'tabbar.jpg', 'logo': 'logo.png', 'topcoins': 'topcoins.png',
                  'pile': 'pile.png', 'coin': 'coin.svg', 'clock': 'clock.svg'},
        'survey': {'home_top': 'home-top.jpg', 'home_body': 'home-body.jpg', 'tabbar': 'tabbar.jpg', 'fox': 'fox.png',
                   'head': 'head.png', 'body_pattern': 'body-pattern.png', 'coin': 'coin.svg'},
    }[folder]


def prototypes():
    icons = P('tools', 'assets', 'icons')
    prototype('proto.html', 'cashout-prototype.html', 'prototype', {'star': os.path.join(icons, 'coin.svg'), 'tip': os.path.join(icons, 'tip96.png')})
    prototype('onboarding.html', 'onboarding-prototype.html', 'onboarding')
    prototype('boost.html', 'boost-prototype.html', 'boost')
    prototype('survey.html', 'survey-prototype.html', 'survey')


# ---------- previews ----------
WEIGHT_NAME = {400: 'Regular 400', 500: 'Medium 500', 600: 'SemiBold 600', 700: 'Bold 700', 800: 'ExtraBold 800'}


def previews():
    swift = read(P('ios', 'Cashout', 'Sources', 'DesignTokens.swift'))
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
def inline(page, name, text, where='website/index.html'):
    """Replace what sits between /* @gen name */ and /* @end name */ (each exactly once, in that order)."""
    start, end = '/* @gen %s */\n' % name, '/* @end %s */' % name
    assert page.count(start) == 1 and page.count(end) == 1, '%s: markers for %s must appear once each' % (where, name)
    a, b = page.index(start) + len(start), page.index(end)
    assert a <= b, '%s: markers for %s are out of order' % (where, name)
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
    """dist/: the home page at the root and the three prototypes under prototype/, as GitHub Pages serves them."""
    out = P('dist')
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(os.path.join(out, 'prototype'))
    shutil.copyfile(P('website', 'index.html'), os.path.join(out, 'index.html'))
    for src, name in (('cashout-prototype.html', 'index.html'), ('onboarding-prototype.html', 'onboarding.html'),
                      ('boost-prototype.html', 'boost.html'), ('survey-prototype.html', 'survey.html')):
        body = read(P('prototype', src))
        if not body.lstrip().lower().startswith('<!doctype'):
            body = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                    '<style>html,body{margin:0}</style>\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
        write(os.path.join(out, 'prototype', name), body)


def build_all(with_site=False):
    tokens_css(); design_tokens_swift(); ios_assets(); bundle_js(); components(); prototypes(); previews(); home_page()
    if with_site: site()


if __name__ == '__main__':
    args = sys.argv[1:]
    build_all('--site' in args)
    if '--check' in args:
        r = subprocess.run(['git', 'status', '--porcelain', '--'] + GENERATED, cwd=ROOT, capture_output=True, text=True)
        if r.stdout.strip():
            sys.exit('Generated files are out of date. Run `python3 tools/build.py` and commit the result:\n' + r.stdout)
    print('built: tokens.css, components, 4 prototypes, previews, website/index.html' + (', dist/' if '--site' in args else ''))

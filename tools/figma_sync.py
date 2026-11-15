"""Sync the design system from a Figma snapshot, then rebuild everything that uses it.

  python3 tools/figma_sync.py figma/snapshot.json            report what differs, change nothing
  python3 tools/figma_sync.py figma/snapshot.json --apply    write the changes and rebuild
  add --site to either to also write the published site to dist/
  python3 tools/build.py                                     rebuild without reading Figma

The snapshot comes from tools/figma_snapshot.js run in the Figma file. Figma is the source of truth for
colours (Cashout/Color, both modes), spacing, radii and sizes (Cashout/Layout) and text styles (Cashout/*).
A colour change is written to tokens.json, tokens.css, DesignTokens.swift and the site, and its old hex is
replaced in the prototype and component sources, unless another token still uses that hex (then it is
reported for a person to place). Layout and text changes update the tokens and Swift; places in the
prototypes that hard-code those sizes are not changed and are listed instead.
"""
import glob, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
TOKENS = P('design-system', 'tokens.json')
_spec = importlib.util.spec_from_file_location('build', P('tools', 'build.py'))
build = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(build)
WEB = re.compile(r'var\(--([\w-]+)\)')
SWIFT = P('design-system', 'DesignTokens.swift')
WEIGHT = {'Regular': 400, 'Medium': 500, 'SemiBold': 600, 'Bold': 700, 'ExtraBold': 800}
SWIFT_WEIGHT = {400: '.regular', 500: '.medium', 600: '.semibold', 700: '.bold', 800: '.heavy'}
TEXT_NAME = {'Amount': 'amount', 'Large Title': 'large-title', 'Title 1': 'title1', 'Title 2': 'title2', 'Title 3': 'title3',
             'Headline': 'headline', 'Body': 'body', 'Callout': 'callout', 'Subheadline': 'subheadline',
             'Footnote': 'footnote', 'Caption': 'caption', 'Tab Label': 'tab-label'}
# Sources that hard-code token hex values. Generated files are rebuilt from these.
SOURCES = ['tools/src/*.html', 'tools/src/*.css', 'tools/src/*.js', 'tools/build_onboarding_components.py',
           'design-system/components/bundle.css', 'design-system/components/*/preview.html']


def read(p): return open(p, encoding='utf-8').read()
def write(p, s): open(p, 'w', encoding='utf-8').write(s)
def camel(n): return re.sub(r'-(\w)', lambda m: m.group(1).upper(), n)


def rgba(v):
    """'#rrggbb', '#rrggbbaa' or 'rgba(r,g,b,a)' -> (r, g, b, a) with a rounded to 2 places."""
    v = v.strip().lower()
    if v.startswith('#'):
        h = v[1:]
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), round(a, 2))
    m = re.match(r'rgba?\(([^)]*)\)', v)
    parts = [x.strip() for x in m.group(1).split(',')]
    return (int(parts[0]), int(parts[1]), int(parts[2]), round(float(parts[3]) if len(parts) > 3 else 1.0, 2))


def css_value(t):
    r, g, b, a = t
    return '#%02x%02x%02x' % (r, g, b) if a >= 1 else 'rgba(%d,%d,%d,%s)' % (r, g, b, ('%g' % a))


def diff(snap, tok):
    out = {'color': [], 'new_color': [], 'layout': [], 'text': [], 'code_only': [], 'figma_only': []}
    colors = {c['name']: c for c in tok['color']['tokens']}
    seen = set()
    for v in snap['collections'].get('Cashout/Color', {}).get('vars', []):
        m = WEB.fullmatch(v.get('web') or '')
        if not m: out['figma_only'].append('%s (web code name %r is not var(--name))' % (v['name'], v.get('web'))); continue
        name = m.group(1); seen.add(name)
        fig = {'light': v['values'].get('Light'), 'dark': v['values'].get('Dark', v['values'].get('Light'))}
        if name not in colors:
            out['new_color'].append({'name': name, 'figma': v['name'], 'value': {k: css_value(rgba(x)) for k, x in fig.items()}, 'usage': v.get('description') or 'Added from Figma (%s).' % v['name']}); continue
        cur = colors[name]['value']
        cur = cur if isinstance(cur, dict) else {'light': cur, 'dark': cur}
        for theme in ('light', 'dark'):
            if fig[theme] and rgba(fig[theme]) != rgba(cur.get(theme, cur['light'])):
                out['color'].append({'name': name, 'theme': theme, 'old': cur.get(theme, cur['light']), 'new': css_value(rgba(fig[theme]))})
    out['code_only'] += [n for n in colors if n not in seen]
    fam = lambda n: 'spacing' if n.startswith('space-') else 'radius' if n.startswith('radius-') else 'size'
    layout = {c['name']: (f, c) for f in ('spacing', 'radius', 'size') for c in tok[f]['tokens']}
    seen_layout = set()
    for v in snap['collections'].get('Cashout/Layout', {}).get('vars', []):
        m = WEB.fullmatch(v.get('web') or '')
        if not m: out['figma_only'].append('%s (web code name %r is not var(--name))' % (v['name'], v.get('web'))); continue
        name = m.group(1); seen_layout.add(name); val = '%gpx' % list(v['values'].values())[0]
        if name not in layout: out['layout'].append({'name': name, 'family': fam(name), 'old': None, 'new': val})
        elif layout[name][1]['value'] != val: out['layout'].append({'name': name, 'family': layout[name][0], 'old': layout[name][1]['value'], 'new': val})
    out['code_only'] += [n for n in layout if n not in seen_layout]
    styles = {s['name']: s for g in tok['type']['groups'] for s in g['styles']}
    for s in snap.get('textStyles', []):
        key = TEXT_NAME.get(s['name'].split('/')[-1])
        if not key or key not in styles: continue
        want = {'fontSize': '%gpx' % s['size'], 'lineHeight': ('%gpx' % s['lineHeight']) if isinstance(s['lineHeight'], (int, float)) else styles[key]['lineHeight'],
                'fontWeight': WEIGHT.get(s['style'], styles[key]['fontWeight'])}
        want['letterSpacing'] = s['letterSpacing'] if s.get('letterSpacing') else None
        changes = {k: (styles[key].get(k), v) for k, v in want.items() if styles[key].get(k) != v}
        if changes: out['text'].append({'name': key, 'figma': s['name'], 'changes': changes})
    return out


def report(d):
    lines = []
    for c in d['color']: lines.append('colour   %-16s %-5s %s -> %s' % (c['name'], c['theme'], c['old'], c['new']))
    for c in d['new_color']: lines.append('new      %-16s light %s, dark %s  (Figma: %s)' % (c['name'], c['value']['light'], c['value']['dark'], c['figma']))
    for c in d['layout']: lines.append('layout   %-16s %s -> %s' % (c['name'], c['old'], c['new']))
    for c in d['text']: lines.append('text     %-16s %s' % (c['name'], ', '.join('%s %s -> %s' % (k, a, b) for k, (a, b) in c['changes'].items())))
    if d['code_only']: lines.append('in code, not in Figma: ' + ', '.join(d['code_only']))
    if d['figma_only']: lines.append('in Figma, not mapped: ' + ', '.join(d['figma_only']))
    return '\n'.join(lines) or 'In sync: nothing differs.'


def apply(d, tok):
    notes = []
    colors = {c['name']: c for c in tok['color']['tokens']}
    for c in d['color']:
        val = colors[c['name']]['value']
        if not isinstance(val, dict): val = colors[c['name']]['value'] = {'light': val, 'dark': val}
        val[c['theme']] = c['new']
    for c in d['new_color']:
        tok['color']['tokens'].append({'name': c['name'], 'value': c['value'], 'usage': c['usage']})
    for c in d['layout']:
        fam = tok[c['family']]['tokens']; hit = [t for t in fam if t['name'] == c['name']]
        if hit: hit[0]['value'] = c['new']
        else: fam.append({'name': c['name'], 'value': c['new']})
    styles = {s['name']: s for g in tok['type']['groups'] for s in g['styles']}
    for c in d['text']:
        for k, (_, v) in c['changes'].items():
            if v is None: styles[c['name']].pop(k, None)
            else: styles[c['name']][k] = v
    write(TOKENS, json.dumps(tok, indent=2, ensure_ascii=False) + '\n')

    # Swift
    sw = read(SWIFT)
    for c in d['new_color']:
        lines = re.findall(r'^    static let \w+\s*= Color\("[^"]+"\)\n', sw, re.M)
        sw = sw.replace(lines[-1], lines[-1] + '    static let %-14s = Color("%s")\n' % (camel(c['name']), c['name']), 1)
    for c in d['text']:
        s = styles[c['name']]; case = camel(c['name'])
        sw = re.sub(r'(case \.%s:\s*\()\s*[\d.]+,\s*\.\w+' % case, lambda m: '%s%g, %s' % (m.group(1), float(s['fontSize'][:-2]), SWIFT_WEIGHT[s['fontWeight']]), sw)
    if d['layout']:
        num = lambda v: '%g' % float(v[:-2])
        sp = ', '.join('s%s: CGFloat = %s' % (t['name'].split('-')[1], num(t['value'])) for t in tok['spacing']['tokens'])
        ra = ', '.join('%s: CGFloat = %s' % (t['name'].split('-', 1)[1], num(t['value'])) for t in tok['radius']['tokens'] if t['name'] != 'radius-pill')
        si = ', '.join('%s: CGFloat = %s' % (camel(t['name']), num(t['value'])) for t in tok['size']['tokens'])
        sw = re.sub(r'enum Space \{[^}]*\}', 'enum Space { static let %s }' % sp, sw)
        sw = re.sub(r'enum Radius \{[^}]*\}', 'enum Radius { static let %s }' % ra, sw)
        sw = re.sub(r'enum Size \{[^}]*\}', 'enum Size { static let %s }' % si, sw)
        notes.append('Layout values changed: the prototypes hard-code some sizes, so check them by eye.')
    if d['text']: notes.append('Text styles changed: the prototypes hard-code some font sizes, so check them by eye.')
    write(SWIFT, sw)

    # Old hex -> new hex in sources, only where the old hex belongs to the changed token alone.
    still = {}
    for t in tok['color']['tokens']:
        v = t['value'] if isinstance(t['value'], dict) else {'light': t['value'], 'dark': t['value']}
        for th, x in v.items(): still.setdefault(rgba(x), set()).add((t['name'], th))
    files = sorted({f for g in SOURCES for f in glob.glob(P(g))})
    for c in d['color']:
        old, new = rgba(c['old']), rgba(c['new'])
        if old[3] < 1 or old[:3] in ((255, 255, 255), (0, 0, 0)):
            notes.append('%s %s: %s is not replaced automatically (white, black or transparent).' % (c['name'], c['theme'], c['old'])); continue
        if still.get(old):
            notes.append('%s %s: %s is still used by %s, so it was not replaced in the sources.' % (c['name'], c['theme'], c['old'], ', '.join(sorted(n for n, _ in still[old]))))
            continue
        pat = re.compile(re.escape(css_value(old)) + r'(?![0-9a-f])', re.I)
        for f in files:
            s = read(f); s2 = pat.sub(css_value(new), s)
            if s2 != s: write(f, s2)
    return notes


if __name__ == '__main__':
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    paths = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--rebuild' in flags: build.build_all('--site' in flags); sys.exit(0)
    if len(paths) != 1: sys.exit(__doc__)
    snap = json.load(open(paths[0], encoding='utf-8')); tok = json.load(open(TOKENS, encoding='utf-8'))
    d = diff(snap, tok)
    print(report(d))
    if '--apply' in flags and any(d[k] for k in ('color', 'new_color', 'layout', 'text')):
        for n in apply(d, tok): print('note: ' + n)
        build.build_all('--site' in flags)
        print('rebuilt everything from the new tokens')

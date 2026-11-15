"""Builds prototype/boost-prototype.html from tools/src/boost.html and tools/assets/boost/.
Run from the repo root:  python3 tools/build_boost.py"""
import base64, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(root, 'tools', 'assets', 'boost')
def uri(name):
    mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'svg': 'image/svg+xml'}[name.rsplit('.', 1)[1]]
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(os.path.join(A, name), 'rb').read()).decode())
h = open(os.path.join(root, 'tools', 'src', 'boost.html')).read()
h = h.replace('{{popup_css}}', open(os.path.join(root, 'tools', 'src', 'popup.css')).read())
for key, name in {'banner': 'banner.jpg', 'body': 'body.jpg', 'tabbar': 'tabbar.jpg', 'logo': 'logo.png', 'topcoins': 'topcoins.png',
                  'pile': 'pile.png', 'coin': 'coin.svg', 'clock': 'clock.svg'}.items():
    h = h.replace('{{%s}}' % key, uri(name))
assert '{{' not in h
out = os.path.join(root, 'prototype', 'boost-prototype.html')
open(out, 'w').write(h)
print(out, len(h) // 1024, 'KB')

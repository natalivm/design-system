"""Builds prototype/onboarding-prototype.html from tools/src/onboarding.html and tools/assets/onboarding/.
Run from the repo root:  python3 tools/build_onboarding.py"""
import base64, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(root, 'tools', 'assets', 'onboarding')
def uri(name):
    mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'svg': 'image/svg+xml'}[name.rsplit('.', 1)[1]]
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(os.path.join(A, name), 'rb').read()).decode())
h = open(os.path.join(root, 'tools', 'src', 'onboarding.html')).read()
for key, name in {'banner': 'banner.jpg', 'below': 'below.jpg', 'tabbar': 'tabbar.jpg', 'fox': 'fox.png', 'hand': 'hand.png',
                  'pile': 'pile.png', 'coin': 'coin.svg', 'clock': 'clock.svg'}.items():
    h = h.replace('{{%s}}' % key, uri(name))
assert '{{' not in h
out = os.path.join(root, 'prototype', 'onboarding-prototype.html')
open(out, 'w').write(h)
print(out, len(h) // 1024, 'KB')

import sys, os, base64
S = sys.argv[1]; out = sys.argv[2]
O = os.path.join(S, 'proto-assets'); DL = os.path.join(S, 'dl')
def uri(p):
    ext = p.rsplit('.', 1)[1]; mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'svg': 'image/svg+xml'}[ext]
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(p, 'rb').read()).decode())
m = {'home_top': 'home-top.jpg', 'home_body': 'home-body.jpg', 'tabbar': 'tabbar.jpg', 'pattern': 'pattern.png', 'success_art': 'success-art.jpg',
     'cash': 'cash.png', 'wallet': 'wallet.png', 'fox_briefcase': 'fox-briefcase.png', 'fox_think': 'fox-think.png', 'fox_thumb': 'fox-thumb.png',
     'timer': 'timer.png', 'games': 'games.png', 'coin': 'coin.svg', 'arrow': 'arrow.svg'}
h = open(os.path.join(S, 'src', 'proto.html')).read()
for k, f in m.items(): h = h.replace('{{%s}}' % k, uri(os.path.join(O, f)))
h = h.replace('{{star}}', uri(os.path.join(DL, 'coin.svg'))).replace('{{tip}}', uri(os.path.join(DL, 'tip96.png')))
assert '{{' not in h, [x for x in h.split('{{')[1:3]]
open(out, 'w').write(h); print(len(h) // 1024, 'KB')

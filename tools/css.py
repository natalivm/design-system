import json,sys
t=json.load(open(sys.argv[1])); out=["/* Cashout iOS Design System — generated from tokens.json */"]
th=[x['id'] for x in t['color']['themes']]
def v(tok,theme): 
    val=tok['value']; return val if isinstance(val,str) else val.get(theme,val[th[0]])
first=[f"  --{c['name']}: {v(c,th[0])};" for c in t['color']['tokens']]+[f"  --{c['name']}: {v(c,th[0])};" for c in t['shadow']['tokens']]
out.append(f':root, [data-theme="{th[0]}"] {{\n'+"\n".join(first)+"\n}")
for x in th[1:]:
    b=[f"  --{c['name']}: {v(c,x)};" for c in t['color']['tokens']+t['shadow']['tokens'] if not isinstance(c['value'],str) and x in c['value']]
    out.append(f'[data-theme="{x}"] {{\n'+"\n".join(b)+"\n}")
root=[]
for fam in ('spacing','radius','size','duration','easing'):
    root+= [f"  --{c['name']}: {c['value']};" for c in t[fam]['tokens']]
root+= [f"  --font-{k}: {s};" for k,s in t['type']['families'].items()]
out.append(":root {\n"+"\n".join(root)+"\n}")
for g in t['type']['groups']:
    for s in g['styles']:
        fam=s.get('family',g['family'])
        ls=f" letter-spacing: {s['letterSpacing']};" if 'letterSpacing' in s else ""
        out.append(f".{s['name']} {{ font-family: var(--font-{fam}); font-size: {s['fontSize']}; line-height: {s['lineHeight']}; font-weight: {s['fontWeight']};{ls} }}")
open(sys.argv[2],'w').write("\n".join(out)+"\n")

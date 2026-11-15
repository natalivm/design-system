import os, sys, json, base64
S = sys.argv[1]
P = os.path.join(S, 'ds', 'project')
DL = os.path.join(S, 'dl')

def w(rel, text):
    p = os.path.join(P, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(text)

# ---------- bundle.js with inlined icons ----------
def uri(path, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(path, 'rb').read()).decode())
src = open(os.path.join(S, 'src', 'bundle.src.js')).read()
src = src.replace('__HISTORY__', uri(os.path.join(DL, 'history.svg'), 'image/svg+xml')) \
         .replace('__STAR__', uri(os.path.join(DL, 'coin.svg'), 'image/svg+xml')) \
         .replace('__TIP__', uri(os.path.join(DL, 'tip96.png'), 'image/png'))
assert '</script' not in src.lower() and '<!--' not in src
w('components/bundle.js', src)

# ---------- tokens: motion families ----------
tp = os.path.join(P, 'tokens.json'); t = json.load(open(tp))
t['duration'] = {"note": "Animation durations. In SwiftUI prefer the named springs; these are their web equivalents.", "tokens": [
    {"name": "duration-fast", "value": "150ms", "usage": "Press feedback on buttons and pills. SwiftUI: .snappy(duration: 0.15)."},
    {"name": "duration-base", "value": "250ms", "usage": "Fades, digit roll on the countdown, content rising in."},
    {"name": "duration-slow", "value": "400ms", "usage": "Sheet presentation, success pop."},
    {"name": "duration-count", "value": "600ms", "usage": "Balance count-up after a cash out."}]}
t['easing'] = {"note": "Curves that approximate SwiftUI's springs on the web.", "tokens": [
    {"name": "easing-snappy", "value": "cubic-bezier(0.2, 0.9, 0.3, 1)", "usage": "SwiftUI .snappy. Presses, digit changes."},
    {"name": "easing-smooth", "value": "cubic-bezier(0.4, 0, 0.2, 1)", "usage": "SwiftUI .smooth. Sheets, fades, layout changes."},
    {"name": "easing-bouncy", "value": "cubic-bezier(0.34, 1.56, 0.64, 1)", "usage": "SwiftUI .bouncy. Only the success moment."}]}
json.dump(t, open(tp, 'w'), indent=2, ensure_ascii=False)

# ---------- previews ----------
def card(group, height, script, page=False, sub=''):
    attrs = 'group="%s" height=%d' % (group, height)
    if sub: attrs += ' subtitle="%s"' % sub
    if page: attrs += ' page'
    return '''<!-- @dsCard %s -->
<!doctype html>
<html>
<head><meta charset="utf-8"></head>
<body>
<div id="root"></div>
<script>
var C = window.Cashout, h = React.createElement, D = C.Demo, Copy = C.Copy;
%s
</script>
</body>
</html>
''' % (attrs, script.strip())

def render(expr):
    return "ReactDOM.createRoot(document.getElementById('root')).render(%s);" % expr

def js(s):
    return json.dumps(s)

SW = {}
SW['Button'] = '''Button("Cash out", action: cashOut)
    .buttonStyle(PrimaryButtonStyle())   // 50pt, Capsule, blue500

Button("Keep playing", action: dismiss)
    .font(.ds(.headline)).tint(.link)
    .frame(minHeight: 44)'''
SW['AmountHero'] = '''AmountHero(state: .earned, amount: 0.32) {
    HistoryPill()
}
// amount → Text(amount, format: .currency(code: "USD"))
//          .font(.ds(.amount)).monospacedDigit()'''
SW['Pill'] = '''Label("History", systemImage: "list.bullet.rectangle")
    .font(.ds(.caption))
    .padding(.horizontal, 12).frame(height: 32)
    .background(Color.green700, in: Capsule())
    .foregroundStyle(Color.onAccent)'''
SW['InfoRow'] = '''Text("Your \\(Image(.star)) turn into rewards in **\\(timeLeft)**.")
    .font(.ds(.subheadline))
    .foregroundStyle(Color.ink)'''
SW['Countdown'] = '''Text(timerInterval: .now...unlockDate, countsDown: true)
    .font(.ds(.largeTitle))
    .monospacedDigit()'''
SW['HistoryList'] = '''List(payouts) { p in
    LabeledContent {
        Text(p.amount, format: .currency(code: p.currency))
    } label: {
        Text(p.date, format: .dateTime.month(.wide).day())
        Text(p.status.label).foregroundStyle(p.status.color)
    }
}
.listStyle(.insetGrouped)'''
SW['StatTile'] = '''StatTile(label: "Game coins",
         value: coins.formatted(),
         icon: Image(.star))'''
SW['InlineMessage'] = '''Label(message, systemImage: "exclamationmark.circle")
    .font(.ds(.subheadline))
    .foregroundStyle(Color.danger)
    .padding(12)
    .background(Color.dangerSurface, in: .rect(cornerRadius: 12))'''
SW['TabBar'] = '''TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Cash out", systemImage: "banknote") { CashoutView() }
    Tab("History", systemImage: "clock.arrow.circlepath") { HistoryView() }
    Tab("Profile", systemImage: "person.crop.circle") { ProfileView() }
}
.tint(.blue500)'''
SW['CashoutSheet'] = '''.sheet(isPresented: $showCashout) {
    CashoutSheet(state: .earned, amount: balance)
        .presentationDetents([.large])
        .presentationDragIndicator(.visible)
}'''

def codes(name, figma):
    return "h('div',{className:'co-codes'},h(Copy,{label:'SwiftUI',code:%s}),h(Copy,{label:'Figma',inline:true,code:%s}))" % (js(SW[name]), js(figma))

def grid(*items):
    return "h('div',{className:'co-grid'},%s)" % ','.join(items)
def demo(cap, el):
    return "h(D,{caption:%s},%s)" % (js(cap), el)

P_ = {}
P_['Button'] = ('Actions', 300, grid(
    demo('Filled', "h(C.Button,{style:{width:220}},'Cash out')"),
    demo('Plain', "h(C.Button,{variant:'plain'},'Keep playing')"),
    demo('Loading', "h(C.Button,{loading:true,style:{width:220}})"),
    demo('Disabled', "h(C.Button,{disabled:true,style:{width:220}},'Cash out')")), 'Button · Style=Filled, State=Default')
P_['AmountHero'] = ('Cashout', 380, grid(
    demo('Earned', "h(C.AmountHero,{className:'co-mini',amount:0.32},h(C.Pill,{glass:true}))"),
    demo('Empty', "h(C.AmountHero,{className:'co-mini',state:'empty',amount:0})"),
    demo('Success', "h(C.AmountHero,{className:'co-mini',state:'success',amount:2.81})")), 'AmountHero · State=Earned')
P_['Pill'] = ('Actions', 210, grid(
    demo('Solid', "h(C.Pill)"),
    demo('Glass · on green', "h('div',{style:{background:'var(--green-700)',padding:12,borderRadius:'var(--radius-md)'}},h(C.Pill,{glass:true}))")), 'Pill · Style=Solid')
P_['InfoRow'] = ('Cashout', 240, grid(demo('Default', "h('div',{style:{width:360}},h(C.InfoRow,{secondsLeft:13500}))")), 'InfoRow')
P_['Countdown'] = ('Cashout', 280, grid(
    demo('Card · live', "h('div',{style:{width:260}},h(C.Countdown,{size:'card',seconds:11643,live:true}))"),
    demo('Inline', "h('span',{style:{fontSize:15}},'Next update in ',h(C.Countdown,{size:'small',seconds:8707,live:true}))")), 'Countdown · Size=Card')
P_['HistoryList'] = ('Cashout', 330, grid(demo('Paid · Pending · Failed', "h('div',{style:{width:340}},h(C.HistoryList,{items:[{date:'April 26',amount:1.3},{date:'April 3',amount:0.32},{date:'March 22',amount:0.86,status:'pending'},{date:'March 14',amount:1.12,status:'failed'}]}))")), 'HistoryList')
P_['StatTile'] = ('Home', 220, grid(
    demo('With icon', "h('div',{style:{width:180,display:'flex'}},h(C.StatTile,{icon:'star',label:'Game coins',value:'66,378'}))"),
    demo('Money', "h('div',{style:{width:180,display:'flex'}},h(C.StatTile,{label:'Ready to cash',value:C.format.money(5378.11)}))")), 'StatTile')
P_['InlineMessage'] = ('Feedback', 240, grid(
    demo('Danger', "h('div',{style:{width:300}},h(C.InlineMessage,null,\"You've reached the maximum balance. Cash out to keep earning.\"))"),
    demo('Info', "h('div',{style:{width:300}},h(C.InlineMessage,{tone:'info'},'Payouts usually arrive within 24 hours.'))")), 'InlineMessage · Tone=Danger')
P_['TabBar'] = ('Navigation', 220, grid(demo('Tap a tab', "h('div',{style:{width:360}},h(C.TabBar,{selected:'cashout'}))")), 'TabBar')
P_['CashoutSheet'] = ('Cashout', 520, "h('div',{className:'co-grid',style:{flexWrap:'nowrap',overflowX:'auto'}},%s)" % ','.join(
    demo(cap, "h('div',{style:{zoom:0.55,width:393}},h(C.CashoutSheet,%s))" % props)
    for cap, hgt, props in [('Earned', 300, "{amount:0.32}"), ('Pending', 300, "{state:'pending',seconds:11643,live:true}"), ('Empty', 300, "{state:'empty',amount:0}"), ('Success', 300, "{state:'success',amount:2.81}")]), 'CashoutSheet · State=Earned')

for name, (group, height, g, figma) in P_.items():
    w('components/%s/preview.html' % name, card(group, height, render("h('div',null,%s,%s)" % (g, codes(name, figma)))))

# ---------- short READMEs ----------
R = {
 'Button': ('Capsule button: one Filled primary action per screen, Plain for the way out.', ['50pt tall, full width minus 16pt margins', 'Verbs in sentence case: "Cash out", "Keep playing"', 'Plain buttons still get a 44pt tap area']),
 'AmountHero': ('The balance card: green means money, navy means waiting.', ['Pass a number and currency code, never a formatted string', 'Digits are monospaced so the amount does not jump', 'Reads as one VoiceOver element']),
 'Pill': ('Small capsule shortcut, used for History.', ['Solid on light surfaces, Glass on the green hero', '32pt visible, 44pt tap area']),
 'InfoRow': ('Explains when stars turn into rewards.', ['Bold only the duration', 'The star icon sits inside the sentence, never placed with spaces']),
 'Countdown': ('Live timer for the wait before stars convert.', ['Format 3:14:03, not 03h:14m:03s', 'VoiceOver reads "3 hours, 14 minutes"']),
 'HistoryList': ('Inset grouped list of past payouts.', ['Status is text plus color, never color alone', 'Amounts right-aligned with tabular digits']),
 'StatTile': ('Label and value tile for balances on Home.', ['Two side by side, equal width', 'Coins are whole numbers; money uses currency format']),
 'InlineMessage': ('Tinted message for limits, errors and short notices.', ['Danger for limits and failures, Info for neutral notes', 'Always with an icon']),
 'TabBar': ('The four root destinations, drawn by the system TabView.', ['Use SF Symbols; the selected tab is tinted blue-500', 'Never draw the tab bar or safe area into a screen']),
 'CashoutSheet': ('The cash-out screen as a system sheet, in four states.', ['Earned: Cash out / Keep playing', 'Pending and Empty: Play games / Back to home', 'Success: Done']),
}
for name, (first, bullets) in R.items():
    w('components/%s/README.md' % name, '# %s\n\n%s\n\n%s\n' % (name, first, '\n'.join('- ' + b for b in bullets)))

# ---------- Foundations cards ----------
types = [('amount', '$0.32', 'Display/Amount', '54 / 60', 'ExtraBold 800', '-0.5', '.largeTitle', 'Text(amount, format: .currency(code: "USD"))\n    .font(.ds(.amount)).monospacedDigit()'),
 ('large-title', 'Cash out', 'Display/Large Title', '34 / 41', 'Bold 700', '0', '.largeTitle', 'Text("Cash out").font(.ds(.largeTitle))'),
 ('title2', 'Cash out successful', 'Text/Title 2', '22 / 28', 'Bold 700', '0', '.title2', 'Text("Cash out successful").font(.ds(.title2))'),
 ('title3', 'Mission board', 'Text/Title 3', '20 / 25', 'SemiBold 600', '0', '.title3', 'Text("Mission board").font(.ds(.title3))'),
 ('headline', 'Keep playing', 'Text/Headline', '17 / 22', 'SemiBold 600', '0', '.headline', 'Text("Keep playing").font(.ds(.headline))'),
 ('body', 'Earned and ready to cash out.', 'Text/Body', '17 / 22', 'Regular 400', '0', '.body', 'Text("Earned and ready to cash out.").font(.ds(.body))'),
 ('callout', 'Well done!', 'Text/Callout', '16 / 21', 'Medium 500', '0', '.callout', 'Text("Well done!").font(.ds(.callout))'),
 ('subheadline', 'Your stars turn into rewards in 3h 45m.', 'Text/Subheadline', '15 / 20', 'Medium 500', '0', '.subheadline', 'Text("Your stars turn into rewards in **3h 45m**.")\n    .font(.ds(.subheadline))'),
 ('footnote', 'April 26 · Paid', 'Text/Footnote', '13 / 18', 'Medium 500', '0', '.footnote', 'Text("Paid").font(.ds(.footnote))\n    .foregroundStyle(Color.success)'),
 ('caption', 'Game coins', 'Text/Caption', '12 / 16', 'SemiBold 600', '0', '.caption', 'Text("Game coins").font(.ds(.caption))\n    .foregroundStyle(Color.inkSecondary)'),
 ('tab-label', 'Cash out', 'Text/Tab Label', '10 / 12', 'SemiBold 600', '0', '.caption2', 'Tab("Cash out", systemImage: "banknote")')]
type_js = json.dumps([{'cls': a, 'sample': b, 'figma': 'Cashout/' + c, 'size': d, 'weight': e, 'track': f, 'rel': g, 'code': h} for a, b, c, d, e, f, g, h in types])
w('components/Typography/preview.html', card('Foundations', 900, '''
var T = %s;
var css = '.ty{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,300px);gap:16px;align-items:center;padding:14px 16px;border-bottom:1px solid var(--separator)}'
 + '.ty-s{color:var(--ink);min-width:0;overflow-wrap:anywhere}.ty-m{display:flex;flex-direction:column;gap:8px;min-width:0}'
 + '@media (max-width:640px){.ty{grid-template-columns:1fr}}';
var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
''' % type_js + render("h('div',null,T.map(function(t){return h('div',{key:t.cls,className:'ty'},h('div',{className:'ty-s '+t.cls},t.sample),h('div',{className:'ty-m'},h('div',{className:'co-chips'},h('span',{className:'co-chip'},t.size),h('span',{className:'co-chip'},t.weight),h('span',{className:'co-chip'},'tracking '+t.track),h('span',{className:'co-chip'},'scales like '+t.rel)),h(Copy,{code:t.code}),h(Copy,{inline:true,code:t.figma})));}))"), page=True, sub='Every style with its attributes. Copy the SwiftUI line or the Figma style name.'))

pairs = [('Ink on surface', 'ink', 'surface', '12.7 : 1', '.foregroundStyle(Color.ink)\n.background(Color.surface)'),
 ('Secondary on surface', 'ink-secondary', 'surface', '6.0 : 1', '.foregroundStyle(Color.inkSecondary)'),
 ('White on blue-500', 'on-accent', 'blue-500', '4.9 : 1', '.foregroundStyle(Color.onAccent)\n.background(Color.blue500, in: Capsule())'),
 ('White on green-700', 'on-accent', 'green-700', '5.3 : 1', '.foregroundStyle(Color.onAccent)\n.background(Color.green700)'),
 ('White on navy-900', 'on-accent', 'navy-900', '18.7 : 1', '.foregroundStyle(Color.onAccent)\n.background(Color.navy900)'),
 ('Ink on info', 'ink', 'surface-info', '12.7 : 1', '.foregroundStyle(Color.ink)\n.background(Color.surfaceInfo)'),
 ('Danger on danger', 'danger', 'danger-surface', '6.0 : 1', '.foregroundStyle(Color.danger)\n.background(Color.dangerSurface)'),
 ('Link on surface', 'link', 'surface', '4.9 : 1', '.tint(.link)')]
pairs_js = json.dumps([{'n': a, 'fg': b, 'bg': c, 'r': d, 'code': e} for a, b, c, d, e in pairs])
w('components/ColorPairs/preview.html', card('Foundations', 560, '''
var Pp = %s;
var st = document.createElement('style'); st.textContent = '.cp{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;padding:16px}.cp-t{border-radius:var(--radius-lg);padding:16px;min-height:76px;display:flex;flex-direction:column;justify-content:space-between;gap:8px;border:1px solid var(--separator)}.cp-n{font:700 17px/22px var(--font-sans)}.cp-r{font:600 12px/16px var(--font-sans);opacity:.9}';
document.head.appendChild(st);
''' % pairs_js + render("h('div',{className:'cp'},Pp.map(function(p){return h('div',{key:p.n,style:{display:'flex',flexDirection:'column',gap:8}},h('div',{className:'cp-t',style:{background:'var(--'+p.bg+')',color:'var(--'+p.fg+')'}},h('span',{className:'cp-n'},p.n),h('span',{className:'cp-r'},'✓ '+p.r)),h(Copy,{code:p.code}));}))"), page=True, sub='Approved text and background pairs, with contrast. Use only these.'))

fixes = [('Contrast', 'white-lime', '1.7 : 1', 'Text on #60E041', 'white-green', '5.3 : 1', 'Text on green-700'),
 ('Button', 'btn-old', '67pt + shadow', '', 'btn-new', '50pt, flat', ''),
 ('Timer', 'txt:03h:14m:03s', '', '', 'txt:3:14:03', '', ''),
 ('Money', 'txt:$30,00', 'typed by hand', '', 'txt:$30.00', 'locale format', ''),
 ('Fonts', 'txt3:Aa Aa Aa', '3 families', '', 'txt1:Aa', 'Plus Jakarta Sans', ''),
 ('Radius', 'radii-old', '13 values', '', 'radii-new', '5 + capsule', ''),
 ('Copy', 'txt:Cashout · Cash-out · cashout', '', '', 'txt:Cash out', 'verb, sentence case', ''),
 ('Icon placement', 'txt:Your ______ will turn', '15 typed spaces', '', 'star', 'inline image', '')]
fixes_js = json.dumps(fixes)
w('components/Fixes/preview.html', card('Foundations', 620, '''
var F = %s;
var st = document.createElement('style'); st.textContent = '.fx{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;padding:16px}.fx-c{border:1px solid var(--separator);border-radius:var(--radius-lg);padding:12px;display:flex;flex-direction:column;gap:10px}.fx-h{font:700 13px/16px var(--font-sans);color:var(--ink)}.fx-r{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center}.fx-s{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;font:600 11px/14px var(--font-sans);color:var(--ink-secondary)}.fx-box{height:56px;width:100%%;border-radius:var(--radius-md);display:grid;place-items:center;font:700 15px/20px var(--font-sans);background:var(--surface-grouped);color:var(--ink);overflow:hidden;padding:0 6px;box-sizing:border-box}.fx-bad{outline:2px solid var(--danger);outline-offset:-2px}.fx-good{outline:2px solid var(--success);outline-offset:-2px}.fx-a{color:var(--ink-secondary);font-size:18px}';
document.head.appendChild(st);
function vis(k){
  if(k==='white-lime') return h('div',{className:'fx-box',style:{background:'var(--lime-400)',color:'#fff'}},'$0.32');
  if(k==='white-green') return h('div',{className:'fx-box',style:{background:'var(--green-700)',color:'var(--on-accent)'}},'$0.32');
  if(k==='btn-old') return h('div',{className:'fx-box',style:{background:'none'}},h('div',{style:{background:'var(--blue-500)',color:'#fff',borderRadius:999,height:48,width:'90%%',display:'grid',placeItems:'center',boxShadow:'0 4px 2px rgba(0,0,0,.3)',fontSize:18}},'Cashout'));
  if(k==='btn-new') return h('div',{className:'fx-box',style:{background:'none'}},h(C.Button,{style:{height:36,width:'90%%',fontSize:15}},'Cash out'));
  if(k==='radii-old') return h('div',{className:'fx-box',style:{gap:3,display:'flex',justifyContent:'center'}},[4,8,10,12,16,20,24,27,50].map(function(r){return h('span',{key:r,style:{width:14,height:28,border:'2px solid var(--ink-secondary)',borderRadius:r/3}})}));
  if(k==='radii-new') return h('div',{className:'fx-box',style:{gap:5,display:'flex',justifyContent:'center'}},[8,12,16,24,999].map(function(r){return h('span',{key:r,style:{width:20,height:28,border:'2px solid var(--blue-500)',borderRadius:r/2.5}})}));
  if(k==='star') return h('div',{className:'fx-box',style:{fontWeight:500,fontSize:13}},h('span',null,'Your ',h('img',{src:C.assets.star,style:{width:16,verticalAlign:-3}}),' turn into'));
  if(k.indexOf('txt3:')===0) return h('div',{className:'fx-box'},h('span',null,h('span',{style:{fontFamily:'Georgia,serif'}},'Aa '),h('span',{style:{fontFamily:'ui-monospace,monospace'}},'Aa '),h('span',null,'Aa')));
  return h('div',{className:'fx-box'},k.replace(/^txt1?:/,''));
}
''' % fixes_js + render("h('div',{className:'fx'},F.map(function(f){return h('div',{key:f[0],className:'fx-c'},h('div',{className:'fx-h'},f[0]),h('div',{className:'fx-r'},h('div',{className:'fx-s'},h('div',{className:'fx-box fx-bad',style:{padding:0,background:'none'}},vis(f[1])),'✕ '+(f[2]||'Before')),h('span',{className:'fx-a','aria-hidden':'true'},'→'),h('div',{className:'fx-s'},h('div',{className:'fx-box fx-good',style:{padding:0,background:'none'}},vis(f[4])),'✓ '+(f[5]||'After'))));}))"), page=True, sub='What changed from the Figma file, before and after.'))

swift_tokens = open(os.path.join(S, 'src', 'DesignTokens.swift')).read()
w('components/SwiftTokens/preview.html', card('Foundations', 260, render("h('div',{style:{padding:16,display:'grid',gap:14}},h(Copy,{label:'DesignTokens.swift',code:%s}))" % js(swift_tokens)), page=True, sub='Colors, fonts, spacing and radii as one Swift file. Copy into the app.'))

# ---------- Motion cards ----------
def motion(name, height, sub, stage, chips, code, extra=''):
    chips_js = ','.join("h('span',{className:'co-chip'},%s)" % js(c) for c in chips)
    body = extra + render("h('div',{style:{display:'grid',gridTemplateColumns:'minmax(0,1fr) minmax(0,1fr)',gap:16,padding:16,alignItems:'start'},className:'mo'},h('div',{style:{display:'flex',flexDirection:'column',gap:12,alignItems:'center'}},%s),h('div',{style:{display:'flex',flexDirection:'column',gap:12,minWidth:0}},h('div',{className:'co-chips'},%s),h(Copy,{label:'SwiftUI',code:%s})))" % (stage, chips_js, js(code)))
    body = "var st=document.createElement('style');st.textContent='@media (max-width:640px){.mo{grid-template-columns:1fr!important}}';document.head.appendChild(st);\n" + body
    w('components/%s/preview.html' % name, card('Motion', height, body, page=True, sub=sub))

REPLAY = '''
function useReplay(){var s=React.useState(0);return [s[0],function(){s[1](s[0]+1)}];}
'''
motion('MotionPress', 250, 'Press a button: it dips and dims, then springs back.',
  "h(C.Button,{style:{width:240}},'Press me'),h(C.Pill,null)",
  ['duration-fast 150ms', 'easing-snappy', 'scale 0.98', 'opacity 0.7'],
  '''struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.98 : 1)
            .opacity(configuration.isPressed ? 0.7 : 1)
            .animation(.snappy(duration: 0.15),
                       value: configuration.isPressed)
    }
}''')

motion('MotionCountUp', 300, 'After a cash out the balance rolls to its new value.',
  "h(CountUp)",
  ['duration-count 600ms', 'easing-snappy', '.numericText()', 'haptic .success'],
  '''Text(balance, format: .currency(code: "USD"))
    .font(.ds(.amount))
    .monospacedDigit()
    .contentTransition(.numericText(value: balance))

withAnimation(.snappy(duration: 0.6)) {
    balance = newBalance
}''',
  REPLAY + '''
function CountUp(){var r=useReplay(),k=r[0],go=r[1];var s=React.useState(0),v=s[0],set=s[1];
React.useEffect(function(){var t0=null,to=k%2?2.81:0.32,raf;function f(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/600);var e=1-Math.pow(1-p,3);set(to*e);if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);return function(){cancelAnimationFrame(raf)};},[k]);
return h('div',{style:{display:'flex',flexDirection:'column',gap:12,alignItems:'center'}},h(C.AmountHero,{className:'co-mini',amount:v}),h('button',{className:'co-replay',onClick:go},'↻ Replay'));}
''')

motion('MotionSheet', 420, 'The cash-out sheet slides up while the background dims.',
  "h(SheetDemo)",
  ['duration-slow 400ms', 'easing-smooth', 'scrim 250ms', 'system .sheet'],
  '''// The system animates the sheet, the scrim
// and the drag-to-dismiss. Don't rebuild it.
.sheet(isPresented: $showCashout) {
    CashoutSheet(state: .earned, amount: balance)
        .presentationDetents([.large])
        .presentationDragIndicator(.visible)
}''',
  REPLAY + '''
function SheetDemo(){var r=useReplay(),k=r[0],go=r[1];
return h('div',{style:{display:'flex',flexDirection:'column',gap:12,alignItems:'center'}},
 h('div',{style:{width:217,height:340,overflow:'hidden',borderRadius:28,position:'relative',background:'var(--surface-grouped)',border:'1px solid var(--separator)'}},
  h('div',{key:'s'+k,className:'co-anim-scrim-in',style:{position:'absolute',inset:0,background:'var(--scrim)'}}),
  h('div',{key:'m'+k,className:'co-anim-sheet-in',style:{position:'absolute',left:0,right:0,bottom:0}},h('div',{style:{zoom:0.55,width:393}},h(C.CashoutSheet,{amount:0.32})))),
 h('button',{className:'co-replay',onClick:go},'↻ Replay'));}
''')

motion('MotionSuccess', 340, 'Cash out succeeds: the card pops into the success state with a haptic.',
  "h(SuccessDemo)",
  ['duration-slow 400ms', 'easing-bouncy', 'scale 0.85 → 1', 'haptic .success'],
  '''if didCashOut {
    AmountHero(state: .success, amount: paid)
        .transition(.scale(scale: 0.85).combined(with: .opacity))
}

// trigger
withAnimation(.bouncy) { didCashOut = true }
.sensoryFeedback(.success, trigger: didCashOut)''',
  REPLAY + '''
function SuccessDemo(){var r=useReplay(),k=r[0],go=r[1];var done=k%2===1;
return h('div',{style:{display:'flex',flexDirection:'column',gap:12,alignItems:'center'}},
 h('div',{key:k,className:done?'co-anim-pop':'co-anim-fade'},h(C.AmountHero,{className:'co-mini',state:done?'success':'earned',amount:done?2.81:0.32})),
 h('button',{className:'co-replay',onClick:go},done?'↻ Reset':'▶ Cash out'));}
''')

motion('MotionCountdown', 280, 'Each second the changing digits roll in; the rest stay still.',
  "h('div',{style:{width:260}},h(C.Countdown,{size:'card',seconds:11643,live:true}))",
  ['duration-base 250ms', 'easing-snappy', 'countsDown: true', 'monospaced digits'],
  '''Text(timerInterval: .now...unlockDate, countsDown: true)
    .font(.ds(.largeTitle))
    .monospacedDigit()
    .contentTransition(.numericText(countsDown: true))''')

motion('MotionReveal', 360, 'Sheet content rises in one after another, 50ms apart.',
  "h(RevealDemo)",
  ['duration-base 250ms', 'easing-smooth', 'stagger 50ms', 'offset y 12pt'],
  '''ForEach(Array(sections.enumerated()), id: \\.offset) { i, section in
    section
        .opacity(appeared ? 1 : 0)
        .offset(y: appeared ? 0 : 12)
        .animation(.smooth(duration: 0.25).delay(Double(i) * 0.05),
                   value: appeared)
}
.onAppear { appeared = true }''',
  REPLAY + '''
function RevealDemo(){var r=useReplay(),k=r[0],go=r[1];
var parts=[h(C.InfoRow,{secondsLeft:13500}),h(C.Button,{fullWidth:true},'Cash out'),h(C.Button,{variant:'plain'},'Keep playing')];
return h('div',{style:{display:'flex',flexDirection:'column',gap:12,alignItems:'center'}},
 h('div',{key:k,style:{width:300,display:'flex',flexDirection:'column',gap:10,alignItems:'center'}},parts.map(function(p,i){return h('div',{key:i,className:'co-anim-rise',style:{animationDelay:(i*50)+'ms',width:'100%',display:'flex',justifyContent:'center'}},p);})),
 h('button',{className:'co-replay',onClick:go},'↻ Replay'));}
''')

motion('ReduceMotion', 260, 'With Reduce Motion on, every move becomes a short crossfade.',
  "h('div',{style:{display:'grid',gap:8,justifyItems:'center'}},h('span',{className:'co-chip'},'Slide → Fade'),h('span',{className:'co-chip'},'Pop → Fade'),h('span',{className:'co-chip'},'Digit roll → Fade'),h('span',{className:'co-chip'},'Haptics stay'))",
  ['@Environment', 'accessibilityReduceMotion'],
  '''@Environment(\\.accessibilityReduceMotion) private var reduceMotion

.transition(reduceMotion
    ? .opacity
    : .scale(scale: 0.85).combined(with: .opacity))''')

# ---------- README: one section ----------
w('README.md', '''## The rules

| | Do | Instead of |
|---|---|---|
| **Units** | Points on a 393 x 852 canvas | 1074px frames |
| **Chrome** | System sheet, tab bar, safe areas | Drawn status bars, grabbers, tab bars |
| **Color** | Green = money, navy = waiting, blue = action | A new hero color per variant |
| **Text** | One family, iOS text styles, Dynamic Type | Three fonts, fixed 57px line height |
| **Shape** | 5 radii + Capsule, continuous corners | 13 radii |
| **Touch** | 44pt minimum tap area | 18pt text buttons |
| **Words** | "Cash out" (verb), sentence case, locale money | Cashout / Cash-out, "$30,00" |
| **Motion** | System springs; crossfade under Reduce Motion | Custom timing per screen |
''')
print('ok')

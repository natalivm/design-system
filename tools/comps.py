import os,sys
P=sys.argv[1]
def prev(name, group, height, body, sub=""):
    s=f' subtitle="{sub}"' if sub else ""
    return f'''<!-- @dsCard group="{group}" height={height}{s} -->
<!doctype html>
<html>
<head><meta charset="utf-8"><title>{name} preview</title></head>
<body>
<div id="root"></div>
<script>
  var C = window.Cashout, h = React.createElement;
  ReactDOM.createRoot(document.getElementById('root')).render({body});
</script>
</body>
</html>
'''
L=lambda txt: f"h('div',{{className:'co-label'}},'{txt}')"
C={}
C['Button']=("Actions",230,"h('div',{className:'co-stack'},"+L('Filled, large')+",h(C.Button,{fullWidth:true},'Cash out'),"+L('Plain')+",h('div',null,h(C.Button,{variant:'plain'},'Keep playing')),"+L('Loading and disabled')+",h(C.Button,{fullWidth:true,loading:true}),h(C.Button,{fullWidth:true,disabled:true},'Cash out'))",
"""# Button

A capsule button: one filled primary action per screen, with plain text buttons for everything else.

**Figma source:** `Button_green` instance (fill was blue `#1464FF`, so the name was wrong), plus the loose "Keep playing" text layer.

## Use
- One `filled` button per screen, pinned above the bottom safe area: **Cash out**, **Play games**, **Done**.
- `plain` for the secondary path directly under it: **Keep playing**, **Back to home**.
- Labels are verbs in sentence case. "Cash out" is the verb (two words); "cashout" is only a noun.
- Show `loading` while the request runs and keep the label width stable. Fire a `.success` haptic when the payout succeeds.

## Fixed from Figma
| Figma | System |
|---|---|
| 184px at 3x = 67pt tall | `control-height` 50pt (`.controlSize(.large)`) |
| Drop shadow `0 4 2 rgba(0,0,0,.3)` | None; iOS buttons are flat |
| Label 62px = 22.5pt bold | `headline` 17pt semibold, scales with Dynamic Type |
| "Keep playing" text with an 18pt tall hit area | `plain` button with a 44pt `hit-target` |
| Two blues, `#1464FF` and `#1364FF` | `blue-500` |

## SwiftUI
```swift
struct PrimaryButtonStyle: ButtonStyle {
    @Environment(\\.isEnabled) private var isEnabled
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.ds(.headline))
            .frame(maxWidth: .infinity, minHeight: 50)
            .foregroundStyle(Color.onAccent)
            .background(Color.blue500, in: Capsule())
            .opacity(isEnabled ? (configuration.isPressed ? 0.7 : 1) : 0.4)
            .scaleEffect(configuration.isPressed ? 0.98 : 1)
            .animation(.snappy(duration: 0.15), value: configuration.isPressed)
    }
}

Button("Cash out", action: cashOut)
    .buttonStyle(PrimaryButtonStyle())
    .sensoryFeedback(.success, trigger: didCashOut)

Button("Keep playing", action: dismiss)
    .font(.ds(.headline))
    .tint(.link)
    .frame(minHeight: 44)
```
""")
C['AmountHero']=("Cashout",470,"h('div',{className:'co-stack'},h(C.AmountHero,{amount:0.32},h(C.Pill,{glass:true})),h(C.AmountHero,{state:'empty',amount:0}),h(C.AmountHero,{state:'success',amount:2.81,currency:'EUR',locale:'de-DE'}))",
"""# AmountHero

The card at the top of the cash-out sheet that shows the balance, in one of four states.

**Figma source:** `Group 1000005379` (gradient rectangle with three loose text layers) and its copies in variants A to D, "< 0 cash", "= 0 cash already cashed out" and "Cashout Successful!".

## States
| `state` | Eyebrow | Fill |
|---|---|---|
| `earned` | Well done! | reward gradient, `green-500` to `green-700` |
| `empty` | Oh no! | `navy-900` |
| `pending` | use `Countdown` size `card` instead | `navy-900` |
| `success` | Cash out successful | reward gradient |

## Use
- The consumer supplies `amount`, `currency` (ISO code) and optionally `locale`. Never pass a preformatted string: Figma had `$0.32`, `€0.32` and `$30,00` side by side.
- The `children` slot holds the History pill on the earned state.
- Keep the mascot illustration outside the card, above it, so the card can grow with Dynamic Type.

## Fixed from Figma
| Figma | System |
|---|---|
| Amount in Figtree ExtraBold, the only Figtree on the page | `amount` style in the brand family, `.monospacedDigit()` |
| Line height 57px on 150px text (clipped) | 60pt on 54pt |
| White on gradient ending at `#60E041` (1.72:1) | Gradient ends on `green-700` where the subtitle sits (5.33:1) |
| Radius 75px at 3x | `radius-xl` 24pt, continuous |
| Absolute-positioned text | A VStack that wraps and scales |

## SwiftUI
```swift
struct AmountHero: View {
    enum State { case earned, empty, success }
    var state: State
    var amount: Decimal
    var currency: String = Locale.current.currency?.identifier ?? "USD"

    var body: some View {
        VStack(spacing: 8) {
            Text(state.eyebrow).font(.ds(.callout))
            Text(amount, format: .currency(code: currency))
                .font(.ds(.amount))
                .monospacedDigit()
                .contentTransition(.numericText(value: (amount as NSDecimalNumber).doubleValue))
                .minimumScaleFactor(0.6)
                .lineLimit(1)
            Text(state.subtitle).font(.ds(.subheadline)).opacity(0.9)
        }
        .foregroundStyle(Color.onAccent)
        .multilineTextAlignment(.center)
        .padding(.vertical, 24).padding(.horizontal, 20)
        .frame(maxWidth: .infinity)
        .background(state.fill, in: RoundedRectangle(cornerRadius: 24, style: .continuous))
        .accessibilityElement(children: .combine)
    }
}
```
""")
C['Pill']=("Actions",110,"h('div',{className:'co-row'},h(C.Pill,null),h('div',{style:{background:'var(--green-700)',padding:'12px',borderRadius:'var(--radius-md)'}},h(C.Pill,{glass:true})))",
"""# Pill

A small capsule button with an icon, used for the History shortcut.

**Figma source:** `Group 1000005376` (rectangle, text and SVG grouped, not a component).

## Use
- Solid (`green-700`) on light surfaces; `glass` (20% white) when it sits on the green AmountHero.
- The visible pill is 32pt tall; its hit area is padded to 44pt.
- The icon is the History glyph from the Figma file. On device prefer the SF Symbol `list.bullet.rectangle`, which follows Dynamic Type and Bold Text.

## Fixed from Figma
| Figma | System |
|---|---|
| Text `#F9F8F4` on `#0C9971`, 35px at 3x = 12.7pt (3.4:1) | `on-accent` on `green-700` (5.33:1) |
| 34.5pt tall, no hit area rule | 32pt visible, 44pt hit area |

## SwiftUI
```swift
Button { showHistory = true } label: {
    Label("History", systemImage: "list.bullet.rectangle")
        .font(.ds(.caption))
        .padding(.horizontal, 12)
        .frame(height: 32)
        .background(Color.green700, in: Capsule())
        .foregroundStyle(Color.onAccent)
}
.contentShape(Rectangle().inset(by: -6))
```
""")
C['InfoRow']=("Cashout",120,"h('div',{className:'co-stack'},h(C.InfoRow,{secondsLeft:13500}))",
"""# InfoRow

A tinted notice that explains when stars convert into rewards, with an inline star icon and a bold duration.

**Figma source:** `Group 1000005378`.

## Use
- One per sheet, directly under AmountHero.
- The consumer supplies `secondsLeft`; the row formats it as `3h 45m`.
- Copy is one sentence about the timing, one about the incentive. Keep "stars" (the iOS counterpart's word); the Android frame said "coins" and had a missing word ("turn into in 3h 45m").

## Fixed from Figma
| Figma | System |
|---|---|
| Icon placed by typing 15 spaces into the text (`"Your               will"`) | Icon inline in the text run; reflows in every language and size |
| Medium and ExtraBold mixed in one run | `subheadline` medium with the duration in bold |
| Radius 46px at 3x | `radius-lg` 16pt |

## SwiftUI
```swift
HStack(spacing: 12) {
    Image(.tipBulb).resizable().scaledToFit()
        .frame(width: 28, height: 28)
        .frame(width: 40, height: 40)
        .background(Color.green700, in: Circle())
        .accessibilityHidden(true)
    Text("Your \\(Image(.star)) turn into rewards in **\\(timeLeft, format: .units(allowed: [.hours, .minutes], width: .narrow))**. The more stars, the higher the reward.")
        .font(.ds(.subheadline))
        .foregroundStyle(Color.ink)
}
.padding(.vertical, 12).padding(.horizontal, 16)
.background(Color.surfaceInfo, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
```
""")
C['Countdown']=("Cashout",250,"h('div',{className:'co-stack'},h(C.Countdown,{size:'card',seconds:11643,live:true}),h('div',null,'Next balance update ',h(C.Countdown,{size:'small',seconds:8707,live:true})))",
"""# Countdown

A live timer for the wait before stars convert or a balance updates.

**Figma source:** the "pre-conversion" frame (`03h:14m:03s` on a navy card, with the annotation "change the color to #000748") and "Next balance update 02h:25m:07s" on Home.

## Use
- `card` for the pending state of the cash-out sheet; `small` inline in running text; `large` on its own.
- Format is `3:14:03`, the iOS timer format. VoiceOver reads "3 hours, 14 minutes, 3 seconds".
- Digits are tabular so the text does not shift every second.

## Fixed from Figma
| Figma | System |
|---|---|
| `03h:14m:03s` (units and colons together, leading zero) | `3:14:03` |
| `#20262D` card, annotated to become `#000748` | `navy-900` |

## SwiftUI
```swift
// Updates itself without a Timer publisher.
Text(timerInterval: Date.now...unlockDate, countsDown: true)
    .font(.ds(.largeTitle))
    .monospacedDigit()
    .foregroundStyle(Color.onAccent)
```
""")
C['HistoryList']=("Cashout",250,"h('div',{className:'co-stack'},h(C.HistoryList,{currency:'USD',items:[{date:'April 26',amount:1.3},{date:'April 3',amount:0.32},{date:'March 22',amount:0.86,status:'pending'},{date:'March 14',amount:1.12,status:'failed'}]}))",
"""# HistoryList

An inset grouped list of past payouts: date, status and amount.

**Figma source:** the "history (prototype)" frames and `history 4` / `history 5`.

## Use
- Rows are read-only; tapping one may push a detail screen.
- Status is one of `success` (shown as "Paid"), `pending` or `failed`, with color as a second cue, never the only one.
- Amounts are right-aligned with tabular digits and formatted from `amount` + `currency`.

## Fixed from Figma
| Figma | System |
|---|---|
| Rows as separate floating cards with their own fills | One inset grouped list with hairline separators |
| Every row "Success" in green, no other states | Paid, Pending, Failed |

## SwiftUI
```swift
List(payouts) { payout in
    LabeledContent {
        Text(payout.amount, format: .currency(code: payout.currency))
            .font(.ds(.headline)).monospacedDigit()
    } label: {
        Text(payout.date, format: .dateTime.month(.wide).day())
            .font(.ds(.headline))
        Text(payout.status.label)
            .font(.ds(.footnote))
            .foregroundStyle(payout.status.color)
    }
}
.listStyle(.insetGrouped)
```
""")
C['StatTile']=("Home",110,"h('div',{className:'co-row',style:{maxWidth:'393px',boxSizing:'border-box',flexWrap:'nowrap'}},h(C.StatTile,{icon:'star',label:'Game coins',value:'66,378'}),h(C.StatTile,{label:'Ready to cash',value:C.format.money(5378.11,'USD','en-US')}))",
"""# StatTile

A compact label-and-value tile for the balances at the top of Home.

**Figma source:** the "Game Coins" and "Ready to cash" tiles on `Home` (17094:48749).

## Use
- Two side by side, equal width, `space-3` apart.
- Values use tabular digits. Coin counts are whole numbers (`66,378`, not `66,378.32`); money uses the currency format.

## Fixed from Figma
| Figma | System |
|---|---|
| 10.49pt and 21.35pt text | `caption` 12pt and `title3` 20pt |
| `#F2F2F2` tile on a blue header | `surface-grouped` |

## SwiftUI
```swift
HStack(spacing: 12) {
    Image(.star).resizable().frame(width: 32, height: 32)
    VStack(alignment: .leading, spacing: 0) {
        Text("Game coins").font(.ds(.caption)).foregroundStyle(Color.inkSecondary)
        Text(coins, format: .number).font(.ds(.title3)).monospacedDigit()
    }
}
.padding(12)
.frame(maxWidth: .infinity, alignment: .leading)
.background(Color.surfaceGrouped, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
```
""")
C['InlineMessage']=("Feedback",150,"h('div',{className:'co-stack'},h(C.InlineMessage,null,\"You've reached the maximum balance. Cash out to keep earning.\"),h(C.InlineMessage,{tone:'info'},'Payouts usually arrive within 24 hours.'))",
"""# InlineMessage

A tinted message inside a screen for limits, errors and short notices.

**Figma source:** the red "You've reached the maximum amount you can accumulate" text on the Home sheet.

## Use
- `danger` for limits and failures; `info` for neutral notices.
- Say what happened and what to do next in one or two sentences.
- An icon always accompanies the color.

## Fixed from Figma
| Figma | System |
|---|---|
| Pure `red` at 60% opacity on white (2.86:1) | `danger` on `danger-surface` (5.98:1) |
| Stray double space in "maximum  amount" | Copy cleaned up |

## SwiftUI
```swift
Label {
    Text("You've reached the maximum balance. Cash out to keep earning.")
} icon: {
    Image(systemName: "exclamationmark.circle")
}
.font(.ds(.subheadline))
.foregroundStyle(Color.danger)
.padding(.vertical, 12).padding(.horizontal, 16)
.frame(maxWidth: .infinity, alignment: .leading)
.background(Color.dangerSurface, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
```
""")
C['TabBar']=("Navigation",80,"h('div',{style:{maxWidth:'393px'}},h(C.TabBar,{selected:'cashout'}))",
"""# TabBar

The app's four root destinations: Home, Cash out, History and Profile.

**Figma source:** the bottom bar on `Home` (17094:48890).

## Use
- On device this is the system `TabView`; do not rebuild it. This component documents labels, icons and tint.
- Icons: SF Symbols `house`, `banknote`, `clock.arrow.circlepath`, `person.crop.circle`, filled when selected.
- Tint is `blue-500`.

## Fixed from Figma
| Figma | System |
|---|---|
| 83pt bar including a hand-drawn safe area | System tab bar, 49pt plus safe area |
| Selected state drawn with 50% opacity frames | `.tint(.blue500)` and filled symbol variants |
| "Cashout" | "Cash out" |

## SwiftUI
```swift
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Cash out", systemImage: "banknote") { CashoutView() }
    Tab("History", systemImage: "clock.arrow.circlepath") { HistoryView() }
    Tab("Profile", systemImage: "person.crop.circle") { ProfileView() }
}
.tint(.blue500)
```
""")
C['CashoutSheet']=("Cashout",1640,"h('div',{style:{display:'flex',flexDirection:'column',gap:'24px'}},h('div',{className:'co-stage'},h(C.CashoutSheet,{amount:0.32,secondsLeft:13500})),h('div',{className:'co-stage'},h(C.CashoutSheet,{state:'pending',seconds:11643,live:true,secondsLeft:11643})),h('div',{className:'co-stage'},h(C.CashoutSheet,{state:'empty',amount:0,limitReached:false})),h('div',{className:'co-stage'},h(C.CashoutSheet,{state:'success',amount:2.81})))",
"""# CashoutSheet

The cash-out screen, presented as a sheet, assembled from the system's components in each of its states.

**Figma source:** variants A, B, C and D, "< 0 cash", "= 0 cash already cashed out", "pre-conversion", "Cashout iOS counterpart" (23690:155027).

## Anatomy, top to bottom
1. System drag indicator.
2. `AmountHero` (or `Countdown` card when pending), with the History `Pill` on the earned state.
3. `InfoRow` explaining the conversion time.
4. `InlineMessage` only when the balance limit is reached.
5. One filled `Button` and one plain `Button`.

## States
| State | Primary | Secondary |
|---|---|---|
| earned | Cash out | Keep playing |
| pending | Play games | Back to home |
| empty | Play games | Back to home |
| success | Done | Back to home |

## Use
- Present with `.sheet` and `.presentationDetents([.large])`; let the system draw the grabber, corner radius and scrim.
- Keep the actions in a bottom safe-area inset so they never scroll away.
- The mascot illustration sits behind the sheet's top edge as decoration (`accessibilityHidden`).

## Fixed from Figma
| Figma | System |
|---|---|
| 25 frames at 1074 x 2394px, built from groups and rectangles | One component with a `state` prop, laid out in points |
| Grabber drawn as a 60 x 7pt rectangle | System drag indicator, 36 x 5pt |
| Side margins of 8, 9.4 and 6.5pt | `space-4` 16pt |
| Variants A to D each used a different hero color (blue, navy, green, gradient) | Green for money, navy for waiting |

## SwiftUI
```swift
.sheet(isPresented: $showCashout) {
    ScrollView {
        VStack(spacing: 24) {
            AmountHero(state: .earned, amount: balance) { HistoryPill() }
            InfoRow(timeLeft: conversionIn)
            if limitReached { InlineMessage(.danger, "You've reached the maximum balance. Cash out to keep earning.") }
        }
        .padding(.horizontal, 16)
    }
    .safeAreaInset(edge: .bottom) {
        VStack(spacing: 8) {
            Button("Cash out", action: cashOut).buttonStyle(PrimaryButtonStyle())
            Button("Keep playing") { showCashout = false }.font(.ds(.headline))
        }
        .padding(.horizontal, 16).padding(.bottom, 8)
    }
    .presentationDetents([.large])
    .presentationDragIndicator(.visible)
}
```
""")
for name,(group,height,body,readme) in C.items():
    d=os.path.join(P,'components',name); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'preview.html'),'w').write(prev(name,group,height,body))
    open(os.path.join(d,'README.md'),'w').write(readme)
print("ok", list(C))

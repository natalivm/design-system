import tokens from '../../design-system/tokens.json';

export { tokens };

export const swiftName = (name) => name.replace(/-([a-z0-9])/g, (_, c) => c.toUpperCase());

export const RULES = [
  ['Units', 'Points on a 393 × 852 canvas', '1074px frames'],
  ['Chrome', 'System sheet, tab bar, safe areas', 'Drawn status bars and grabbers'],
  ['Color', 'Green = money, navy = waiting, blue = action', 'A new hero color per variant'],
  ['Text', 'One family, iOS text styles, Dynamic Type', 'Three fonts, fixed 57px line height'],
  ['Shape', '5 radii + Capsule, continuous corners', '13 radii'],
  ['Touch', '44pt minimum tap area', '18pt text buttons'],
  ['Words', '"Cash out" (verb), sentence case, locale money', 'Cashout, Cash-out, "$30,00"'],
  ['Motion', 'System springs; crossfade under Reduce Motion', 'Custom timing per screen']
];

export const TYPE = [
  ['amount', '$0.32', 'Display/Amount', '54 / 60', 'ExtraBold', 'Text(amount, format: .currency(code: "USD"))\n    .font(.ds(.amount)).monospacedDigit()'],
  ['large-title', 'Cash out', 'Display/Large Title', '34 / 41', 'Bold', 'Text("Cash out").font(.ds(.largeTitle))'],
  ['title2', 'Cash out successful', 'Text/Title 2', '22 / 28', 'Bold', 'Text("Cash out successful").font(.ds(.title2))'],
  ['title3', 'Mission board', 'Text/Title 3', '20 / 25', 'SemiBold', 'Text("Mission board").font(.ds(.title3))'],
  ['headline', 'Keep playing', 'Text/Headline', '17 / 22', 'SemiBold', 'Text("Keep playing").font(.ds(.headline))'],
  ['body', 'Earned and ready to cash out.', 'Text/Body', '17 / 22', 'Regular', 'Text("Earned and ready to cash out.").font(.ds(.body))'],
  ['callout', 'Well done!', 'Text/Callout', '16 / 21', 'Medium', 'Text("Well done!").font(.ds(.callout))'],
  ['subheadline', 'Your stars turn into rewards in 3h 45m.', 'Text/Subheadline', '15 / 20', 'Medium', 'Text("Your stars turn into rewards in **3h 45m**.")\n    .font(.ds(.subheadline))'],
  ['footnote', 'April 26 · Paid', 'Text/Footnote', '13 / 18', 'Medium', 'Text("Paid").font(.ds(.footnote))'],
  ['caption', 'Game coins', 'Text/Caption', '12 / 16', 'SemiBold', 'Text("Game coins").font(.ds(.caption))']
];

export const SNIPPETS = {
  Button: 'Button("Cash out", action: cashOut)\n    .buttonStyle(PrimaryButtonStyle())',
  AmountHero: 'AmountHero(state: .earned, amount: 0.32) {\n    HistoryPill()\n}',
  Pill: 'Label("History", systemImage: "list.bullet.rectangle")\n    .font(.ds(.caption))\n    .padding(.horizontal, 12).frame(height: 32)\n    .background(Color.green700, in: Capsule())',
  InfoRow: 'Text("Your \\(Image(.star)) turn into rewards in **\\(timeLeft)**.")\n    .font(.ds(.subheadline))',
  Countdown: 'Text(timerInterval: .now...unlockDate, countsDown: true)\n    .font(.ds(.largeTitle)).monospacedDigit()',
  HistoryList: 'List(payouts) { p in PayoutRow(p) }\n    .listStyle(.insetGrouped)',
  InlineMessage: 'Label(message, systemImage: "exclamationmark.circle")\n    .foregroundStyle(Color.danger)\n    .background(Color.dangerSurface, in: .rect(cornerRadius: 12))',
  StatTile: 'StatTile(label: "Game coins", value: coins.formatted(), icon: Image(.star))'
};

export const MOTION = {
  press: { title: 'Press', tokens: ['150ms', 'snappy', 'scale 0.98'], code: '.scaleEffect(isPressed ? 0.98 : 1)\n.opacity(isPressed ? 0.7 : 1)\n.animation(.snappy(duration: 0.15), value: isPressed)' },
  count: { title: 'Count-up', tokens: ['600ms', 'snappy', '.numericText'], code: 'Text(balance, format: .currency(code: "USD"))\n    .contentTransition(.numericText(value: balance))\nwithAnimation(.snappy(duration: 0.6)) { balance = new }' },
  success: { title: 'Success pop', tokens: ['400ms', 'bouncy', 'haptic'], code: '.transition(.scale(scale: 0.85).combined(with: .opacity))\nwithAnimation(.bouncy) { didCashOut = true }\n.sensoryFeedback(.success, trigger: didCashOut)' },
  tick: { title: 'Countdown tick', tokens: ['250ms', 'snappy', 'countsDown'], code: 'Text(timerInterval: .now...end, countsDown: true)\n    .contentTransition(.numericText(countsDown: true))' },
  reveal: { title: 'Staggered reveal', tokens: ['250ms', 'smooth', '+50ms each'], code: '.opacity(appeared ? 1 : 0)\n.offset(y: appeared ? 0 : 12)\n.animation(.smooth.delay(Double(i) * 0.05), value: appeared)' }
};

export const LINKS = {
  figma: 'https://www.figma.com/design/xx3Wl01iiG5MWSoqtC0vz8/test?node-id=16671-42948',
  repo: 'https://github.com/natalivm/design-system'
};

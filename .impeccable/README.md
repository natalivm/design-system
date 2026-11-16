# Impeccable detector configuration

`config.json` turns off six rules and one rule/value pair. Each one was checked against the
rendered page before it was switched off, and each is here because this repository renders two
different kinds of thing on one page: the **website's own chrome**, which the rules apply to, and
**specimens of the iOS app**, which they mostly do not.

Nothing here is a blanket "we disagree". If you add a rule to this file, add the reason with it.

| Rule | Why it is off | What to watch |
|---|---|---|
| `undersized-ui-text` | The only remaining hits are the TabBar's four 10px labels. `type.tab-label` in `tokens.json` is 10px *because* the iOS system tab bar is, and the control carries the 44px `hit-target`. Raising it would make the design system wrong about the platform it documents. | This also silences genuinely tiny text in site chrome. The swatch labels that used to fire here were real and were fixed (10px → 11px), not ignored. Re-check by hand when adding site chrome. |
| `cramped-padding` | Fires on the TabBar specimen, whose children sit flush against the bottom of their container — which is what a tab bar does. | Site chrome panels are not exempt in spirit; check new ones by eye. |
| `nested-cards` | Fires where an app card (a pop-up, a mission card) is shown inside the website panel that frames it. The nesting is the gallery, not the app. | If the *website* starts nesting its own panels, that is a real finding this will hide. |
| `ai-color-palette` | The violet → indigo gradient is the game's mission art, documented as `violet-500` / `indigo-800` with contrast notes, and drawn with the fox mascot. It is brand, not a generated tell. | Any *new* purple gradient in site chrome would be the real thing. |
| `text-occlusion` | All nine hits are the pop-up scrims in the boost and onboarding prototypes, which open on load and are supposed to dim what is behind them. Verified by dismissing the modal: the strip underneath is exposed again. | — |
| `buried-raster` | One hit, the cash-out mascot at `opacity: 0`. That is its resting state before `mascot-in` runs; after the sheet opens it renders at full opacity with `naturalWidth` 560. | — |
| `overused-font` = *Plus Jakarta Sans* | The brand typeface, set in Figma and carried in `tokens.json` under `type.families.sans`. | — |

## Known findings that are left on, and why

These still report. They were checked and judged false, but suppressing them would cost more than
reading past them.

- **`low-contrast` on `p.sum` (Components).** Reported as 2.0:1 "gradient on body". The body carries
  decorative 1–1.8px radial specks; the sampler picked one as the background. The text is
  `--site-muted` over `--site-canvas`, which measures 5.54:1.
- **`low-contrast` on the boost pop-up body text.** Reported as 1.6:1. The copy is `--ink`
  (`#02266e`) on white, about 13:1. The sampler attributed the header's gradient to a body child.
- **`bounce-easing`** (advisory). `--bouncy` is `easing-bouncy` in `tokens.json`, mapped to SwiftUI's
  `.bouncy` and documented as "only the success moment". It is a platform spring, not decoration.
- **`straggler`** (advisory). Line-breaking is width-dependent; these come and go with the viewport.

## Re-running

```bash
python3 tools/build.py --site
```

```bash
python3 -m http.server 4177 --directory dist
```

```bash
.claude/skills/impeccable/scripts/impeccable detect --no-advisory http://localhost:4177/
```

Scan each route separately (`#foundations`, `#components`, `#prototype`, `#motion`, `#writing`) and
the three prototypes under `/prototype/`. The detector does not follow hash routes' content into
iframes, so `/prototype/index.html`, `onboarding.html` and `boost.html` need their own scans.

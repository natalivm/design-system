# Cashout — iOS

The design system as a real app, starting with one screen that exercises most of it.
Standalone for now, built so each screen can move into the game later without a rewrite.

## What is here

```
ios/Cashout/
  Assets.xcassets/          generated: 37 colorsets, 31 imagesets
  Info.plist                font registration, portrait only
  Sources/
    DesignTokens.swift      generated from design-system/tokens.json
    Components/             AdTag, TimePill, FlipTimer, Bokeh
    Screens/BoostPopup.swift   the 2x coins pop-up, four states
    CashoutApp.swift        the app, with a state picker and a running clock
```

`Assets.xcassets` and `DesignTokens.swift` are **generated** by `python3 tools/build.py`.
Edit `design-system/tokens.json` or the art in `tools/assets`, run the build, and they follow.
`tools/build.py --check` fails if someone changes a token without rebuilding.
The hand-written part of the Swift file lives in `tools/src/DesignTokens.swift`.

## Before it builds

**Fonts.** The repo has no font binaries — the prototypes pull Plus Jakarta Sans and Nunito
from Google at runtime, which an app cannot do. Both are SIL OFL, so download them, drop the
`.ttf` files next to `Info.plist`, and keep the licence file alongside. The names in
`UIAppFonts` must match the files, and `DSTextStyle.family` must match the fonts' PostScript
names — that enum is the one place to fix it if they differ.

**Art.** Nothing we have reaches 3x; see `tools/audit-assets.md`. Everything is declared at 2x,
which is the closest honest declaration, so it will look slightly soft on a current iPhone until
the coin pile, the 2x logo and the coins row are re-exported from source.

## Opening it

There is no `.xcodeproj` in the repo on purpose — a generated one I cannot compile here is worse
than thirty seconds of setup.

1. Xcode → File → New → Project → iOS → App. Name it `Cashout`, interface SwiftUI, language Swift.
2. Set the minimum deployment to **iOS 17** (the flip clock's digit roll and the blinking colons
   both use iOS 17 APIs).
3. Delete the `ContentView.swift` and `Assets.xcassets` Xcode made for you.
4. Drag `ios/Cashout/Sources` and `ios/Cashout/Assets.xcassets` into the project, with
   *Create folder references* off and *Copy items if needed* off, so the build keeps following
   the generated files.
5. Point the target's Info.plist at `ios/Cashout/Info.plist`, or copy the `UIAppFonts` array into
   the one Xcode generated.

Run it. You get the pop-up over the home backdrop and a segmented control to move between Offer,
Active, Progress and Time over. In Active the clock counts for real.

## What this screen proves

The card frame, the 184pt head and its curve, the clock pinned so Offer and Active open on it at
the same height, the earned block bottom-aligned so both amounts land 20 from the card bottom,
the ad chip trailing its label, the time pill without its icon, tap-outside-to-close, and the
bokeh field as a `Canvas` driven by `TimelineView`.

## Not done yet

- The cash-out sheet and history, onboarding, the 2x banner states.
- The rays and motes behind the coin piles — a Metal shader through `.colorEffect`, the one
  effect that is real work rather than a port.
- The coin-fly between the mission row and the balance.
- Three type sizes the pop-up uses (19/25, 22/28, 37/44) are written out by hand in
  `BoostPopup.swift` because the ramp does not carry them. Figma already has Popup Title and
  Button Large; `tokens.json` should get them so they generate like everything else.

Nothing in here has been compiled: the container this was written in has no Swift toolchain.
The first Xcode build is the first real check.

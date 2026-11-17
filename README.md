# BestPlay design system and prototypes

Design system and clickable prototype for the cash-out flow, rebuilt from the Figma page "Cashout Button Rework" with iOS fixes.

| Folder | What's in it |
|---|---|
| `prototype/cashout-prototype.html` | Clickable iPhone prototype of the flow. Open it in a browser; all art is embedded. |
| `prototype/onboarding-prototype.html` | Clickable prototype of the onboarding missions: coach marks, the welcome reward, coins flying to the balance, and the missions-complete card. Press Play to watch it run by itself; press Pause to tap through it yourself. |
| `prototype/boost-prototype.html` | Clickable prototype of the 2x coins boost: the offer pop-up, the home banner with a live timer, progress and the time-over summary. |
| `prototype/survey-prototype.html` | Clickable prototype of the Quick Survey, built from the Figma page "Survey System": the card on Home, two questions, the check-all-that-apply variation and collecting the 1,500 coins. |
| `design-system/` | Tokens (`tokens.json`, `tokens.css`), the rules (`README.md`), component previews and guidelines (`components/`), and `DesignTokens.swift` for the app. |
| `figma/variables-ledger.json` | IDs of the Cashout variable collections, modes and variables created in the Figma file. |
| `tools/` | Sources (`tools/src/`), art (`tools/assets/`) and the build (`tools/build.py`) that generates the files above. |
| `website/index.html` | The website's home page: the green BestPlay Design System page, with Overview, Foundations, Components, Prototype, Motion and Writing pages. Components is built from the `COMPONENTS` array in the page's script: each entry names its feature (Cash out, Onboarding, 2x coins, Core), which puts it under that feature in the list on the left and in the search, and lists the variants to draw. Screens used to be a separate page showing the same variants inside a phone frame; it was folded into Components. The prototype runs inside its Prototype page. |

## Website (GitHub Pages)

Live at **https://natalivm.github.io/design-system/** once Pages is turned on.

1. In the repo on GitHub, open **Settings → Pages** and set **Source** to **GitHub Actions**.
2. Merge into `main`. The workflow in `.github/workflows/pages.yml` first checks that the committed generated files match their sources (`python3 tools/build.py --check`), then writes the site to `dist/` and deploys it. You can also run it by hand from the **Actions** tab.

Run it locally:

```bash
python3 tools/build.py --site
```

```bash
python3 -m http.server 4177 --directory dist
```

Then open http://localhost:4177/.

## Live pages

- Design system: https://claude.ai/artifact/EhRwk5AimHab4UGYPqVcXM
- Prototype: https://claude.ai/artifact/VvYMocJkwSThXjzx56k6Un

Both pages are private until shared from their Share menu.

## Figma

- Source page: https://www.figma.com/design/xx3Wl01iiG5MWSoqtC0vz8/test?node-id=16671-42948
- The page "BestPlay Design System" in the same file holds the variables, text styles and components.

## Syncing from Figma

Figma is the source of truth for colours, spacing, radii, sizes and text styles (the `Cashout/*` variables and text styles on the "BestPlay Design System" page). After changing them in Figma, ask Claude to "sync from Figma". It will:

1. Run `tools/figma_snapshot.js` in the Figma file and save the result as `figma/snapshot.json`.
2. Run `python3 tools/figma_sync.py figma/snapshot.json` to list what differs, then the same with `--apply` to write it.

`--apply` updates `tokens.json`, `tokens.css`, `DesignTokens.swift` and the website, replaces old colour values in the prototype and component sources, and rebuilds everything. It reports what it cannot place on its own: a colour value still shared by another token, and sizes or font sizes the prototypes hard-code. Changes to how a component is laid out in Figma are applied by hand.

Add `--site` to also write the published site to `dist/`.

## Rebuilding

Edit the sources, never the generated files, then run:

```bash
python3 tools/build.py
```

| Source | Generated |
|---|---|
| `design-system/tokens.json` | `design-system/tokens.css` |
| `tools/src/bundle.src.js` and `tools/assets/icons/` | `design-system/components/bundle.js` |
| `tools/src/onboarding-components.src.js` and `tools/src/components.css` | `design-system/components/onboarding.js` and `.css` |
| `tools/src/proto.html`, `onboarding.html`, `boost.html`, `survey.html` and `tools/assets/` | `prototype/*.html` |
| `tools/src/popup.css` | copied into the onboarding and 2x coins prototypes and into `onboarding.css` |
| `tools/src/kit.js` | copied into all four prototypes: autoplay, the tap marker, coin flights, overlays, fitting the phone to the window |
| `design-system/DesignTokens.swift` | the SwiftTokens and Typography previews |
| all of the above | the blocks between `/* @gen … */` and `/* @end … */` in `website/index.html` |

`python3 tools/build.py --check` rebuilds and fails if a committed file changed; CI runs it on every push.

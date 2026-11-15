# BestPlay design system and prototypes

Design system and clickable prototype for the cash-out flow, rebuilt from the Figma page "Cashout Button Rework" with iOS fixes.

| Folder | What's in it |
|---|---|
| `prototype/cashout-prototype.html` | Clickable iPhone prototype of the flow. Open it in a browser; all art is embedded. |
| `prototype/onboarding-prototype.html` | Clickable prototype of the onboarding missions: coach marks, the welcome reward, coins flying to the balance, and the missions-complete card. Press Play to watch it run by itself; press Pause to tap through it yourself. |
| `prototype/boost-prototype.html` | Clickable prototype of the 2x coins boost: the offer pop-up, the home banner with a live timer, progress and the time-over summary. |
| `design-system/` | Tokens (`tokens.json`, `tokens.css`), the rules (`README.md`), component previews and guidelines (`components/`), and `DesignTokens.swift` for the app. |
| `figma/variables-ledger.json` | IDs of the Cashout variable collections, modes and variables created in the Figma file. |
| `tools/` | Scripts and source art used to generate the files above. |
| `website/index.html` | The website's home page: the green BestPlay Design System page, with Overview, Foundations, Components, Screens, Prototype, Motion and Writing pages. The prototype runs inside its Prototype page. |
| `site/` | Build for GitHub Pages. It publishes `website/index.html` as the home page, the prototype at `prototype/`, and an extra React + Three.js showcase at `showcase/`. |

## Website (GitHub Pages)

Live at **https://natalivm.github.io/design-system/** once Pages is turned on.

1. In the repo on GitHub, open **Settings → Pages** and set **Source** to **GitHub Actions**.
2. Merge this branch into `main`. The workflow in `.github/workflows/pages.yml` builds `site/` and deploys it on every push to `main`. You can also run it by hand from the **Actions** tab.

Run it locally:

```bash
cd site
npm install
npm run dev
```

Open the address Vite prints (it ends in `/design-system/`).

## Live pages

- Design system: https://claude.ai/artifact/EhRwk5AimHab4UGYPqVcXM
- Prototype: https://claude.ai/artifact/VvYMocJkwSThXjzx56k6Un

Both pages are private until shared from their Share menu.

## Figma

- Source page: https://www.figma.com/design/xx3Wl01iiG5MWSoqtC0vz8/test?node-id=16671-42948
- The page "BestPlay Design System" in the same file holds the variables, text styles and components.

## Rebuilding

`tools/css.py` regenerates `tokens.css` from `tokens.json`. `tools/build_boost.py`, `tools/build_onboarding.py` and `tools/build_onboarding_components.py` rebuild the onboarding prototype and its components from `tools/src/` and `tools/assets/onboarding/`. `tools/src/popup.css` holds the shared Popup styles; the onboarding and 2x coins builds copy it in, and the rules are in `design-system/components/Popup/README.md`. `tools/build_proto.py` embeds the art in `tools/assets/prototype/` into the prototype template `tools/src/proto.html`. The scripts were written for a temporary working folder, so update their paths before running them again.

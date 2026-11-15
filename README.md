# Cashout iOS design system and prototype

Design system and clickable prototype for the cash-out flow, rebuilt from the Figma page "Cashout Button Rework" with iOS fixes.

| Folder | What's in it |
|---|---|
| `prototype/cashout-prototype.html` | Clickable iPhone prototype of the flow. Open it in a browser; all art is embedded. |
| `design-system/` | Tokens (`tokens.json`, `tokens.css`), the rules (`README.md`), component previews and guidelines (`components/`), and `DesignTokens.swift` for the app. |
| `figma/variables-ledger.json` | IDs of the Cashout variable collections, modes and variables created in the Figma file. |
| `tools/` | Scripts and source art used to generate the files above. |

## Live pages

- Design system: https://claude.ai/artifact/EhRwk5AimHab4UGYPqVcXM
- Prototype: https://claude.ai/artifact/VvYMocJkwSThXjzx56k6Un

Both pages are private until shared from their Share menu.

## Figma

- Source page: https://www.figma.com/design/xx3Wl01iiG5MWSoqtC0vz8/test?node-id=16671-42948
- The page "Cashout iOS Design System" in the same file holds the variables, text styles and components.

## Rebuilding

`tools/css.py` regenerates `tokens.css` from `tokens.json`. `tools/build_proto.py` embeds the art in `tools/assets/prototype/` into the prototype template `tools/src/proto.html`. The scripts were written for a temporary working folder, so update their paths before running them again.

# Popup

The one frame for every centered pop-up: offers, rewards, summaries and confirmations. The cash-out sheet slides up from the bottom and is a separate component (`CashoutSheet`); it does not follow these rules.

Styles: `tools/src/popup.css` (copied into `design-system/components/onboarding.css` and both prototypes at build time).

## Fixed for every pop-up

| What | Value |
|---|---|
| Width | Screen width minus 32pt each side (329pt on a 393pt screen) |
| Corners | 24pt |
| Backdrop | `rgba(8, 10, 28, 0.84)` over the whole screen |
| Entrance | Scale 0.7 → 1 and rise 30pt, 500ms, bouncy easing; backdrop fades in 300ms |
| Body padding | 24pt top, 20pt sides and bottom |
| Slot order | Header art → title → body → one main button |
| Title | 22/28 bold; 28/34 in the hero size |
| Eyebrow | 15/20 semibold |
| Body text | 17/22 medium |
| Big number | 54/58 extra bold, tabular figures |
| Smallest text | 12pt |
| Main button | 50pt tall, full width of the body, pill shape, one per pop-up |
| Dismiss | One text link, 17pt, 44pt tall, centered 52pt above the bottom of the screen ("Skip", "Close", "Not now"). No X in the corner. Leave it out when the main button is the only sensible answer |

## Free per feature

- **Header**: colour or gradient (`--pp-head`), an illustration or logo, an optional curved bottom edge (`data-curve`).
- **Art above the card**: anything in `.pp-over` may poke out past the top edge (the coins on the 2x coins pop-up).
- **Effects**: rays, particles and confetti, behind the card or inside the header. Keep them slow and soft.
- **Card colour**: `--pp-bg`. On a dark card set `data-theme="dark"` so text turns white.
- **Body content**: a timer, a coin pile, an amount, a short list. It goes between the title and the button.

## Button tones

Pick the tone that fits the action and stands out from the card.

| Tone | Use for | Looks like |
|---|---|---|
| `claim` | Collecting or confirming something earned | Flat mint-400 (#0BDD66), dark green text |
| `boost` | Starting a multiplier, on light cards | Flat violet-400, white text |
| `offer` | An optional extra, on dark cards | Flat orange-500, dark brown text |

Buttons are flat: one solid colour, no gradient, no drop shadow. A button that plays an ad carries the "Watch ad" tag after its label.

## Sizes

| Size | Contains | Use for |
|---|---|---|
| `compact` | Title, one or two lines, button | Confirmations |
| `standard` | Header art, text, button | Offers (2x coins "Start ahead") |
| `hero` | Big art and a big number | Rewards, congrats, time over |

## Where it is used

- Onboarding: Welcome reward, Congrats, 2x boost offer.
- 2x coins: offer, "Bonus is active", progress, time over.

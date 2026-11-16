# Asset audit

Measured in the prototypes: the point size each image is actually drawn at, against the pixels we have.
Nothing in the set reaches 3x, so on a current iPhone every one of these is being upscaled a little.
The catalog puts each file in the 2x slot, which is the closest honest declaration.

| Asset | Pixels | Drawn at | Effective | 3x would need |
| --- | --- | --- | --- | --- |
| `prototype/home-body.jpg` | 514 x 800 | 393pt | 1.3x | 1179px wide |
| `prototype/fox-briefcase.png` | 560 x 472 | 284pt | 2.0x | 852px wide |
| `boost/banner.jpg` | 786 x 226 | 393pt | 2.0x | 1179px wide |
| `boost/body.jpg` | 786 x 1207 | 393pt | 2.0x | 1179px wide |
| `boost/tabbar.jpg` | 786 x 171 | 393pt | 2.0x | 1179px wide |
| `onboarding/banner.jpg` | 786 x 226 | 393pt | 2.0x | 1179px wide |
| `onboarding/below.jpg` | 786 x 896 | 393pt | 2.0x | 1179px wide |
| `onboarding/handshake.png` | 240 x 160 | 120pt | 2.0x | 360px wide |
| `onboarding/tabbar.jpg` | 786 x 174 | 393pt | 2.0x | 1179px wide |
| `prototype/home-top.jpg` | 800 x 369 | 393pt | 2.0x | 1179px wide |
| `prototype/success-art.jpg` | 800 x 521 | 393pt | 2.0x | 1179px wide |
| `prototype/tabbar.jpg` | 800 x 170 | 393pt | 2.0x | 1179px wide |
| `boost/pile.png` | 700 x 467 | 300pt | 2.3x | 900px wide |
| `onboarding/pile.png` | 700 x 467 | 300pt | 2.3x | 900px wide |
| `onboarding/fox.png` | 300 x 285 | 128pt | 2.3x | 384px wide |
| `onboarding/hand.png` | 160 x 160 | 64pt | 2.5x | 192px wide |
| `prototype/cash.png` | 124 x 80 | 46pt | 2.7x | 138px wide |
| `boost/logo.png` | 484 x 189 | 176pt | 2.8x | 528px wide |
| `boost/topcoins.png` | 749 x 103 | 271pt | 2.8x | 813px wide |
| `prototype/wallet.png` | 118 x 104 | 40pt | 3.0x | 120px wide |
| `icons/tip96.png` | 96 x 96 | not drawn in a prototype | - | - |
| `prototype/fox-think.png` | 560 x 410 | not drawn in a prototype | - | - |
| `prototype/fox-thumb.png` | 560 x 402 | not drawn in a prototype | - | - |
| `prototype/games.png` | 560 x 126 | not drawn in a prototype | - | - |
| `prototype/pattern.png` | 800 x 365 | not drawn in a prototype | - | - |
| `prototype/timer.png` | 138 x 160 | not drawn in a prototype | - | - |
| `prototype/transfer.png` | 600 x 120 | not drawn in a prototype | - | - |

The six backdrop JPEGs are screenshots of the host game standing in behind our screens, so they
only need re-exporting if they outlive the standalone build. The art we own - the coin pile, the
2x logo and coins row, the foxes, the hand - is what wants a 3x export from source.

// Cashout iOS Design System — the token sections are generated from design-system/tokens.json
// by tools/build.py. Edit the tokens, not the generated blocks; everything outside them is hand-written.
import SwiftUI

// MARK: Color — asset catalog names match token names
extension Color {
/* @gen colors */
    static let blue500        = Color("blue-500")
    static let onAccent       = Color("on-accent")
    static let green700       = Color("green-700")
    static let green500       = Color("green-500")
    static let green400       = Color("green-400")
    static let lime400        = Color("lime-400")
    static let navy900        = Color("navy-900")
    static let violet500      = Color("violet-500")
    static let indigo800      = Color("indigo-800")
    static let gold400        = Color("gold-400")
    static let mint400        = Color("mint-400")
    static let sky200         = Color("sky-200")
    static let orange500      = Color("orange-500")
    static let pink400        = Color("pink-400")
    static let pink600        = Color("pink-600")
    static let pink50         = Color("pink-50")
    static let pinkInk        = Color("pink-ink")
    static let pink800        = Color("pink-800")
    static let violet400      = Color("violet-400")
    static let violet600      = Color("violet-600")
    static let ink            = Color("ink")
    static let inkSecondary   = Color("ink-secondary")
    static let link           = Color("link")
    static let surface        = Color("surface")
    static let surfaceGrouped = Color("surface-grouped")
    static let surfaceInfo    = Color("surface-info")
    static let separator      = Color("separator")
    static let success        = Color("success")
    static let danger         = Color("danger")
    static let dangerSurface  = Color("danger-surface")
    static let grabber        = Color("grabber")
    static let scrim          = Color("scrim")
    static let scrimStrong    = Color("scrim-strong")
    static let chipDark       = Color("chip-dark")
    static let claimFill      = Color("claim-fill")
    static let claimInk       = Color("claim-ink")
    static let overlay        = Color("overlay")
/* @end colors */
}

extension ShapeStyle where Self == LinearGradient {
    /// AmountHero fill: green-400 at the top-right corner into green-500. Only large text sits on it.
    static var reward: LinearGradient {
        LinearGradient(colors: [.green400, .green500], startPoint: .topTrailing, endPoint: .bottom)
    }
}

extension ShapeStyle where Self == LinearGradient {
    /// MissionCard and Congrats card fill.
    static var mission: LinearGradient {
        LinearGradient(colors: [.violet500, .indigo800], startPoint: .top, endPoint: .bottom)
    }
}

// MARK: Type — Plus Jakarta Sans for UI, Nunito ExtraBold for titles, scaled like the system text styles
enum DSTextStyle {
/* @gen type-cases */
    case amount, largeTitle, popupTitle, title1, title2, title3, headline, body, callout, subheadline, footnote, caption, tabLabel, buttonLarge, popupBody
/* @end type-cases */

    var spec: (size: CGFloat, weight: Font.Weight, relativeTo: Font.TextStyle) {
        switch self {
/* @gen type-spec */
        case .amount:      (54, .heavy, .largeTitle)
        case .largeTitle:  (34, .heavy, .largeTitle)
        case .popupTitle:  (37, .heavy, .largeTitle)
        case .title1:      (28, .heavy, .title)
        case .title2:      (22, .heavy, .title2)
        case .title3:      (20, .heavy, .title3)
        case .headline:    (17, .semibold, .headline)
        case .body:        (17, .regular, .body)
        case .callout:     (16, .medium, .callout)
        case .subheadline: (15, .medium, .subheadline)
        case .footnote:    (13, .medium, .footnote)
        case .caption:     (12, .semibold, .caption)
        case .tabLabel:    (10, .semibold, .caption2)
        case .buttonLarge: (22, .bold, .title2)
        case .popupBody:   (19, .medium, .body)
/* @end type-spec */
        }
    }

    /// Titles are set in Nunito ExtraBold; everything else is Plus Jakarta Sans.
    var family: String {
        switch self {
/* @gen type-family */
        case .largeTitle, .popupTitle, .title1, .title2, .title3: "Nunito-ExtraBold"
        case .amount, .headline, .body, .callout, .subheadline, .footnote, .caption, .tabLabel, .buttonLarge, .popupBody: "PlusJakartaSans"
/* @end type-family */
        }
    }
}

extension Font {
    static func ds(_ style: DSTextStyle) -> Font {
        let s = style.spec
        return .custom(style.family, size: s.size, relativeTo: s.relativeTo).weight(s.weight)
    }
}

// MARK: Spacing, radius, size (points)
/* @gen metrics */
enum Space { static let s1: CGFloat = 4, s2: CGFloat = 8, s3: CGFloat = 12, s4: CGFloat = 16, s5: CGFloat = 20, s6: CGFloat = 24, s8: CGFloat = 32, s10: CGFloat = 40 }
enum Radius { static let sm: CGFloat = 8, md: CGFloat = 12, lg: CGFloat = 16, xl: CGFloat = 24, pill: CGFloat = 999 }
enum Size { static let controlHeight: CGFloat = 66, hitTarget: CGFloat = 44, pillHeight: CGFloat = 32, iconTile: CGFloat = 40, tabBarHeight: CGFloat = 49 }
/* @end metrics */

// MARK: Motion — the same durations and curves the prototypes run on
/* @gen motion */
enum Duration { static let fast: Double = 0.15, base: Double = 0.25, slow: Double = 0.4, count: Double = 0.6 }

enum Curve {
    /// SwiftUI .snappy. Presses, digit changes.
    static func snappy(_ d: Double = Duration.base) -> Animation { .timingCurve(0.2, 0.9, 0.3, 1, duration: d) }
    /// SwiftUI .smooth. Sheets, fades, layout changes.
    static func smooth(_ d: Double = Duration.base) -> Animation { .timingCurve(0.4, 0, 0.2, 1, duration: d) }
    /// SwiftUI .bouncy. Only the success moment.
    static func bouncy(_ d: Double = Duration.base) -> Animation { .timingCurve(0.34, 1.56, 0.64, 1, duration: d) }
}
/* @end motion */

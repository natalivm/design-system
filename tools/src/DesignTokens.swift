// Cashout iOS Design System — the token sections are generated from design-system/tokens.json
// by tools/build.py. Edit the tokens, not the generated blocks; everything outside them is hand-written.
import SwiftUI

// MARK: Color — asset catalog names match token names
extension Color {
/* @gen colors */
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
/* @end type-cases */

    var spec: (size: CGFloat, weight: Font.Weight, relativeTo: Font.TextStyle) {
        switch self {
/* @gen type-spec */
/* @end type-spec */
        }
    }

    /// Titles are set in Nunito ExtraBold; everything else is Plus Jakarta Sans.
    var family: String {
        switch self {
/* @gen type-family */
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
/* @end metrics */

// MARK: Motion — the same durations and curves the prototypes run on
/* @gen motion */
/* @end motion */

import SwiftUI

// MARK: Color — asset catalog names match token names
extension Color {
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

// MARK: Type — Plus Jakarta Sans, scaled like the system text styles
enum DSTextStyle {
    case amount, largeTitle, title1, title2, title3, headline, body, callout, subheadline, footnote, caption, tabLabel

    var spec: (size: CGFloat, weight: Font.Weight, relativeTo: Font.TextStyle) {
        switch self {
        case .amount:      (54, .heavy,    .largeTitle)
        case .largeTitle:  (34, .bold,     .largeTitle)
        case .title1:      (28, .bold,     .title)
        case .title2:      (22, .bold,     .title2)
        case .title3:      (20, .semibold, .title3)
        case .headline:    (17, .semibold, .headline)
        case .body:        (17, .regular,  .body)
        case .callout:     (16, .medium,   .callout)
        case .subheadline: (15, .medium,   .subheadline)
        case .footnote:    (13, .medium,   .footnote)
        case .caption:     (12, .semibold, .caption)
        case .tabLabel:    (10, .semibold, .caption2)
        }
    }
}

extension Font {
    static func ds(_ style: DSTextStyle) -> Font {
        let s = style.spec
        return .custom("PlusJakartaSans", size: s.size, relativeTo: s.relativeTo).weight(s.weight)
    }
}

// MARK: Spacing, radius, size (points)
enum Space { static let s1: CGFloat = 4, s2: CGFloat = 8, s3: CGFloat = 12, s4: CGFloat = 16, s5: CGFloat = 20, s6: CGFloat = 24, s8: CGFloat = 32, s10: CGFloat = 40 }
enum Radius { static let sm: CGFloat = 8, md: CGFloat = 12, lg: CGFloat = 16, xl: CGFloat = 24 }
enum Size { static let controlHeight: CGFloat = 50, hitTarget: CGFloat = 44, pillHeight: CGFloat = 32, iconTile: CGFloat = 40 }

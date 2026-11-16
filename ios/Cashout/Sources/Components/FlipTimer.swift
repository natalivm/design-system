import SwiftUI

/// The big counting clock: a tile per digit, split light over pink with a hairline across
/// the middle, and colons that blink. Digits roll with `.numericText()` rather than cutting.
struct FlipTimer: View {
    enum Scale {
        case large, small

        var tile: CGSize {
            switch self {
            case .large: CGSize(width: 38, height: 52)
            case .small: CGSize(width: 23, height: 34)
            }
        }
        var radius: CGFloat { self == .large ? 8 : 5 }
        var size: CGFloat { self == .large ? 34 : 21 }
        var colonWidth: CGFloat { self == .large ? 12 : 7 }
        var gap: CGFloat { self == .large ? 3 : 2 }
    }

    /// Six digits, HHMMSS. "240000" is a full day.
    let digits: String
    var scale: Scale = .large
    /// White on the violet card, pink on a light one.
    var colonColor: Color = .pinkInk

    var body: some View {
        HStack(spacing: scale.gap) {
            ForEach(cells, id: \.self) { cell in
                switch cell {
                case let .digit(character, _): tile(character)
                case .colon: colon
                }
            }
        }
        .accessibilityElement(children: .ignore)
        .accessibilityLabel(spoken)
        .accessibilityAddTraits(.updatesFrequently)
    }

    private enum Cell: Hashable {
        case digit(Character, Int)
        case colon(Int)
    }

    private var cells: [Cell] {
        var out: [Cell] = []
        for (index, character) in Array(digits).enumerated() {
            if index > 0, index.isMultiple(of: 2) { out.append(.colon(index)) }
            out.append(.digit(character, index))
        }
        return out
    }

    private func tile(_ character: Character) -> some View {
        Text(String(character))
            .font(.system(size: scale.size, weight: .bold))
            .monospacedDigit()
            .contentTransition(.numericText())
            .foregroundStyle(Color.pinkInk)
            .frame(width: scale.tile.width, height: scale.tile.height)
            .background {
                RoundedRectangle(cornerRadius: scale.radius, style: .continuous)
                    .fill(LinearGradient(stops: [
                        .init(color: Color.white, location: 0),
                        .init(color: Color.white, location: 0.5),
                        .init(color: Color.pink50, location: 0.5),
                        .init(color: Color.pink50, location: 1)
                    ], startPoint: .top, endPoint: .bottom))
                    .overlay { Rectangle().fill(Color.pinkInk.opacity(0.14)).frame(height: 1) }
                    .clipShape(RoundedRectangle(cornerRadius: scale.radius, style: .continuous))
                    .shadow(color: Color.pink800.opacity(0.25), radius: 2, y: 2)
            }
    }

    private var colon: some View {
        Text(":")
            .font(.system(size: scale.size, weight: .bold))
            .foregroundStyle(colonColor)
            .frame(width: scale.colonWidth)
            .phaseAnimator([1.0, 0.25], content: { view, opacity in
                view.opacity(opacity)
            }, animation: { _ in .linear(duration: 0.5) })
    }

    private var spoken: String {
        let parts = stride(from: 0, to: min(digits.count, 6), by: 2).map { start -> Int in
            let i = digits.index(digits.startIndex, offsetBy: start)
            let j = digits.index(i, offsetBy: 2)
            return Int(digits[i..<j]) ?? 0
        }
        guard parts.count == 3 else { return digits }
        return "\(parts[0]) hours, \(parts[1]) minutes, \(parts[2]) seconds"
    }
}

#Preview {
    VStack(spacing: 24) {
        FlipTimer(digits: "240000")
        FlipTimer(digits: "231400", scale: .small, colonColor: .white)
            .padding(8)
            .background(Color.pink600)
    }
    .padding()
}

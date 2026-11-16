import SwiftUI

enum PopupMetrics {
    static let width: CGFloat = 345
    static let height: CGFloat = 544
    static let corner: CGFloat = 26
    /// The pinned button and the 20 either side of it.
    static var buttonWell: CGFloat { Size.controlHeight + 40 }
}

/// The frame every pop-up shares: a scrim that closes on a tap, a 345x544 card on a 26pt corner,
/// the gold coins over its top edge, and the dismiss link under it. What goes inside differs;
/// this does not.
struct PopupScaffold<Content: View>: View {
    var cardFill: AnyShapeStyle = AnyShapeStyle(Color.surface)
    var showsCoins = true
    /// The word that floats above the card, as Time over has it.
    var aboveCard: String?
    var dismissLabel: String?
    var onDismiss: () -> Void = {}
    @ViewBuilder var content: Content

    var body: some View {
        ZStack {
            Color.scrimStrong
                .ignoresSafeArea()
                .contentShape(Rectangle())
                .onTapGesture(perform: onDismiss)

            if let aboveCard {
                Text(aboveCard)
                    .font(.ds(.popupTitle))
                    .foregroundStyle(Color.onAccent)
                    .shadow(color: .black.opacity(0.5), radius: 6, y: 2)
                    .offset(y: -(PopupMetrics.height / 2) - 42)
                    .allowsHitTesting(false)
            }

            content
                .frame(width: PopupMetrics.width, height: PopupMetrics.height)
                .background(cardFill)
                .clipShape(RoundedRectangle(cornerRadius: PopupMetrics.corner, style: .continuous))
                .shadow(color: .black.opacity(0.5), radius: 30, y: 20)
                .overlay(alignment: .top) {
                    if showsCoins {
                        Image("topcoins")
                            .resizable()
                            .scaledToFit()
                            .frame(width: 272)
                            .offset(y: -19)
                            .shadow(color: .black.opacity(0.25), radius: 3, y: 4)
                            .allowsHitTesting(false)
                    }
                }
        }
        .overlay(alignment: .bottom) {
            if let dismissLabel {
                Button(dismissLabel, action: onDismiss)
                    .font(.ds(.buttonLarge).weight(.semibold))
                    .foregroundStyle(Color.onAccent)
                    .underline()
                    .frame(minHeight: Size.hitTarget)
                    .padding(.bottom, 52)
            }
        }
    }
}

/// The 62pt primary inside a pop-up, pinned 20 from the card's bottom edge.
struct PopupButton: View {
    let title: String
    var tone: Color = .claimFill
    var showsAd = false
    var action: () -> Void = {}

    var body: some View {
        Button(action: action) {
            HStack(spacing: 10) {
                Text(title)
                if showsAd { AdTag() }
            }
            .font(.ds(.buttonLarge))
            .foregroundStyle(Color.onAccent)
            .frame(maxWidth: .infinity)
            .frame(height: Size.controlHeight)
            .background(tone, in: Capsule())
        }
        .buttonStyle(.plain)
        .padding(.horizontal, 20)
        .padding(.bottom, 20)
    }
}

import SwiftUI

/// The 2x coins pop-up, in the four states the prototype runs.
///
/// Geometry comes from the design system rather than from taste: one 184pt pink head in every
/// state, the clock pinned 230 from the card top so Offer and Active open on it at the same
/// height, and the earned block bottom-aligned on Progress and Time over so both amounts land
/// 20 from the card bottom. The card, the coins and the dismiss link come from PopupScaffold.
struct BoostPopup: View {
    enum BoostState: String, CaseIterable, Identifiable {
        case offer, active, progress, timeOver

        var id: String { rawValue }

        var label: String {
            switch self {
            case .offer: "Offer"
            case .active: "Active"
            case .progress: "Progress"
            case .timeOver: "Time over"
            }
        }

        var eyebrow: String {
            switch self {
            case .offer, .active: "Start ahead"
            case .progress: "Bonus active"
            case .timeOver: "Time is over"
            }
        }

        var dismissLabel: String {
            switch self {
            case .offer: "Skip"
            case .timeOver: "Tap to continue"
            case .active, .progress: "Close"
            }
        }
    }

    let state: BoostState
    var left: String = "235959"
    var onPrimary: () -> Void = {}
    var onDismiss: () -> Void = {}

    private let headHeight: CGFloat = 184
    /// The clock sits 230 from the card top in every state that shows one.
    private var bodyTopInset: CGFloat { 230 - headHeight }
    private var cardFill: Color { state == .active ? .violet400 : .surface }
    private var showsBokeh: Bool { state == .progress || state == .timeOver }

    var body: some View {
        PopupScaffold(cardFill: AnyShapeStyle(cardFill),
                      aboveCard: state == .timeOver ? "Congrats!" : nil,
                      dismissLabel: state.dismissLabel,
                      onDismiss: onDismiss) {
            ZStack(alignment: .top) {
                if showsBokeh { Bokeh() }
                VStack(spacing: 0) {
                    head
                    content
                }
                if state == .offer {
                    VStack(spacing: 0) {
                        Spacer(minLength: 0)
                        PopupButton(title: "Start now", tone: .violet400,
                                    showsAd: true, action: onPrimary)
                    }
                }
            }
        }
    }

    private var head: some View {
        ZStack(alignment: .top) {
            LinearGradient(colors: [.pink400, .pink600], startPoint: .top, endPoint: .bottom)
                .overlay(alignment: .top) {
                    RadialGradient(colors: [Color(red: 1, green: 0.478, blue: 0.608), .clear],
                                   center: .top, startRadius: 0, endRadius: 250)
                }

            VStack(spacing: 2) {
                Image("logo")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 176)
                    .accessibilityLabel("2x coins")
                Text(state.eyebrow)
                    .font(.system(size: 15, weight: .semibold))
                    .foregroundStyle(Color.onAccent)
                if state == .progress {
                    TimePill(clock: "23:59:59", spoken: "23 hours, 59 minutes, 59 seconds left")
                        .padding(.top, 8)
                }
            }
            .padding(.top, 22)
        }
        .frame(height: headHeight)
        // The card's own curve rises 30pt into the head: one ellipse, mostly below the fold.
        .overlay(alignment: .bottom) {
            Ellipse()
                .fill(cardFill)
                .frame(width: PopupMetrics.width * 1.9, height: 220)
                .offset(y: 190)
        }
    }

    @ViewBuilder private var content: some View {
        switch state {
        case .offer:
            VStack(spacing: 0) {
                FlipTimer(digits: "240000")
                Text("You have 24 hours to double all the coins you earn playing your favorite games.")
                    .font(.ds(.popupBody))
                    .foregroundStyle(Color.ink)
                    .multilineTextAlignment(.center)
                    .padding(.top, 20)
                Spacer(minLength: 0)
            }
            .padding(.top, bodyTopInset)
            .padding(.horizontal, 20)
            .padding(.bottom, PopupMetrics.buttonWell)

        case .active:
            VStack(spacing: 0) {
                FlipTimer(digits: left, colonColor: .white)
                Spacer(minLength: 0)
                // No button here, so the headline takes the place the button holds elsewhere.
                VStack(spacing: 4) {
                    Text("Bonus is active!")
                        .font(.ds(.buttonLarge))
                    Text("Play games to earn coins")
                        .font(.ds(.popupBody))
                }
                .foregroundStyle(Color.onAccent)
            }
            .padding(.top, bodyTopInset)
            .padding(.horizontal, 20)
            .padding(.bottom, Size.controlHeight + 20)

        case .progress, .timeOver:
            VStack(spacing: 0) {
                Spacer(minLength: 0)
                Image("pile")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 300)
                    .shadow(color: Color(red: 60 / 255, green: 10 / 255, blue: 0).opacity(0.35), radius: 9, y: 10)
                Text(state == .progress ? "So far you’ve earned" : "You’ve earned")
                    .font(.ds(.popupBody).weight(.semibold))
                    .padding(.top, 12)
                Text("5,000")
                    .font(.ds(.buttonLarge))
                    .strikethrough(true, color: .orange500)
                    .monospacedDigit()
                    .padding(.top, 4)
                Text("+10,000")
                    .font(.ds(.amount))
                    .monospacedDigit()
                    .foregroundStyle(Color.violet600)
            }
            .foregroundStyle(Color.ink)
            .padding(.horizontal, 20)
            .padding(.bottom, 20)
        }
    }
}

#Preview("Offer") { BoostPopup(state: .offer) }
#Preview("Active") { BoostPopup(state: .active) }
#Preview("Progress") { BoostPopup(state: .progress) }
#Preview("Time over") { BoostPopup(state: .timeOver) }

import SwiftUI

/// The three reward pop-ups: the welcome bonus, missions complete, and the 2x coins offer.
/// One card, one gradient, one pile — only the words, the amount and the button's tone differ.
struct RewardCard: View {
    enum Tone: String, CaseIterable, Identifiable {
        case welcome, congrats, boost
        var id: String { rawValue }

        var label: String {
            switch self {
            case .welcome: "Welcome reward"
            case .congrats: "Missions complete"
            case .boost: "2x boost"
            }
        }

        var title: String {
            switch self {
            case .welcome: "Welcome reward!"
            case .congrats, .boost: "Congrats!"
            }
        }

        var subtitle: String? {
            switch self {
            case .welcome: nil
            case .congrats: "Missions complete!"
            case .boost: "Get a 2x coins boost"
            }
        }

        var action: String {
            switch self {
            case .welcome: "Awesome!"
            case .congrats: "Get double"
            case .boost: "Boost now"
            }
        }

        /// Only the two that pay out in ad views carry the chip.
        var showsAd: Bool { self != .welcome }

        var buttonTone: Color {
            switch self {
            case .welcome, .congrats: .claimFill
            case .boost: .orange500
            }
        }

        var dismiss: String? {
            switch self {
            case .welcome: nil
            case .congrats: "Claim 1,500"
            case .boost: "Skip"
            }
        }
    }

    let tone: Tone
    var onAction: () -> Void = {}
    var onDismiss: () -> Void = {}

    var body: some View {
        PopupScaffold(cardFill: AnyShapeStyle(LinearGradient(stops: [
            .init(color: .violet500, location: 0.10),
            .init(color: .indigo800, location: 1)
        ], startPoint: .top, endPoint: .bottom)),
                      dismissLabel: tone.dismiss,
                      onDismiss: onDismiss) {
            ZStack(alignment: .bottom) {
                VStack(spacing: 0) {
                    Text(tone.title)
                        .font(.ds(.popupTitle))
                        .foregroundStyle(Color.gold400)
                    if let subtitle = tone.subtitle {
                        Text(subtitle)
                            .font(.ds(.popupBody))
                            .foregroundStyle(Color.onAccent)
                            .padding(.top, 8)
                    }

                    CoinPile()

                    switch tone {
                    case .welcome:
                        Text("+1,000")
                            .font(.ds(.amount))
                            .monospacedDigit()
                            .foregroundStyle(Color.onAccent)
                        Text("Start playing to earn even more!")
                            .font(.ds(.popupBody))
                            .foregroundStyle(Color.onAccent)
                            .multilineTextAlignment(.center)
                            .padding(.top, 8)
                    case .congrats:
                        Text("1,500")
                            .font(.ds(.amount))
                            .monospacedDigit()
                            .foregroundStyle(Color.onAccent)
                    case .boost:
                        Text("2x coins · 15 min")
                            .font(.ds(.buttonLarge))
                            .foregroundStyle(Color.gold400)
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .padding(.top, 24)
                .padding(.horizontal, 20)
                .padding(.bottom, PopupMetrics.buttonWell)

                PopupButton(title: tone.action, tone: tone.buttonTone,
                            showsAd: tone.showsAd, action: onAction)
            }
        }
    }
}

/// The pile and the glow behind it, at the size the whole system settled on.
struct CoinPile: View {
    var body: some View {
        ZStack {
            Circle()
                .fill(RadialGradient(colors: [Color.gold400.opacity(0.14), .clear],
                                     center: .center, startRadius: 0, endRadius: 130))
                .frame(width: 260, height: 260)
            Image("pile")
                .resizable()
                .scaledToFit()
                .frame(width: 300)
                .shadow(color: Color(red: 60 / 255, green: 10 / 255, blue: 0).opacity(0.45), radius: 9, y: 10)
        }
        .frame(height: 215)
        .accessibilityHidden(true)
    }
}

#Preview("Welcome") { RewardCard(tone: .welcome) }
#Preview("Congrats") { RewardCard(tone: .congrats) }
#Preview("Boost") { RewardCard(tone: .boost) }

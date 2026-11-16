import SwiftUI

@main
struct CashoutApp: App {
    var body: some Scene {
        WindowGroup { Gallery() }
    }
}

/// Every screen the design system covers, on the backdrops the prototypes use.
/// Tap one to open it full screen; tap the screen to come back.
struct Gallery: View {
    @State private var open: Screen?
    @State private var secondsLeft = 86_399

    private let tick = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    enum Screen: String, CaseIterable, Identifiable {
        case boostOffer, boostActive, boostProgress, boostTimeOver
        case bannerOffer, bannerActive
        case rewardWelcome, rewardCongrats, rewardBoost
        case missionCard, coachMark
        case terms, trustedBy
        case cashEarned, cashEmpty, cashLimit, cashLoading, cashPending, cashHistory, cashSuccess

        var id: String { rawValue }

        var group: String {
            switch self {
            case .boostOffer, .boostActive, .boostProgress, .boostTimeOver, .bannerOffer, .bannerActive:
                "2x coins"
            case .rewardWelcome, .rewardCongrats, .rewardBoost, .missionCard, .coachMark, .terms, .trustedBy:
                "Onboarding"
            default:
                "Cash out"
            }
        }

        var title: String {
            switch self {
            case .boostOffer: "Pop-up · Offer"
            case .boostActive: "Pop-up · Active"
            case .boostProgress: "Pop-up · Progress"
            case .boostTimeOver: "Pop-up · Time over"
            case .bannerOffer: "Banner · Offer"
            case .bannerActive: "Banner · Active"
            case .rewardWelcome: "Welcome reward"
            case .rewardCongrats: "Missions complete"
            case .rewardBoost: "2x boost reward"
            case .missionCard: "Missions card"
            case .coachMark: "Coach mark"
            case .terms: "Terms and conditions"
            case .trustedBy: "Trusted by"
            case .cashEarned: "Sheet · Earned"
            case .cashEmpty: "Sheet · Nothing yet"
            case .cashLimit: "Sheet · At the cap"
            case .cashLoading: "Sheet · Cashing out"
            case .cashPending: "Sheet · Converting"
            case .cashHistory: "History"
            case .cashSuccess: "Cash out successful"
            }
        }

        /// Which prototype backdrop this sits on, if any.
        var backdrop: String? {
            switch self {
            case .boostOffer, .boostActive, .boostProgress, .boostTimeOver, .bannerActive: "body"
            case .rewardWelcome, .rewardCongrats, .rewardBoost, .missionCard, .coachMark: "below"
            case .cashEarned, .cashEmpty, .cashLimit, .cashLoading, .cashPending, .cashHistory: "home-body"
            case .bannerOffer, .terms, .trustedBy, .cashSuccess: nil
            }
        }
    }

    var body: some View {
        NavigationStack {
            List {
                ForEach(["Cash out", "Onboarding", "2x coins"], id: \.self) { group in
                    Section(group) {
                        ForEach(Screen.allCases.filter { $0.group == group }) { screen in
                            Button(screen.title) { open = screen }
                                .foregroundStyle(Color.ink)
                        }
                    }
                }
            }
            .navigationTitle("Cashout")
        }
        .fullScreenCover(item: $open) { screen in
            ZStack {
                if let name = screen.backdrop {
                    Image(name)
                        .resizable()
                        .scaledToFill()
                        .ignoresSafeArea()
                        .accessibilityHidden(true)
                }
                view(for: screen)
            }
            .contentShape(Rectangle())
            .onTapGesture { open = nil }
        }
        .onReceive(tick) { _ in
            guard open == .boostActive || open == .bannerActive, secondsLeft > 0 else { return }
            secondsLeft -= 1
        }
    }

    @ViewBuilder private func view(for screen: Screen) -> some View {
        let clock = Self.digits(from: secondsLeft)
        switch screen {
        case .boostOffer: BoostPopup(state: .offer, onDismiss: { open = nil })
        case .boostActive: BoostPopup(state: .active, left: clock, onDismiss: { open = nil })
        case .boostProgress: BoostPopup(state: .progress, onDismiss: { open = nil })
        case .boostTimeOver: BoostPopup(state: .timeOver, onDismiss: { open = nil })

        case .bannerOffer:
            VStack { EventBanner(state: .offer); Spacer() }.ignoresSafeArea(edges: .top)
        case .bannerActive:
            VStack { EventBanner(state: .active, left: clock); Spacer() }.ignoresSafeArea(edges: .top)

        case .rewardWelcome: RewardCard(tone: .welcome, onDismiss: { open = nil })
        case .rewardCongrats: RewardCard(tone: .congrats, onDismiss: { open = nil })
        case .rewardBoost: RewardCard(tone: .boost, onDismiss: { open = nil })

        case .missionCard:
            MissionCard().padding(.horizontal, 7)
        case .coachMark:
            CoachMark(caption: AttributedString("First task:\nclaim your reward!"), onContinue: { open = nil }) {
                MissionRow(reward: "1,000", task: "Collect the welcome bonus", status: .claim)
            }

        case .terms: OnboardingStep(step: .terms)
        case .trustedBy: OnboardingStep(step: .trustedBy)

        case .cashEarned: sheet(.earned)
        case .cashEmpty: sheet(.empty)
        case .cashLimit: sheet(.limit)
        case .cashLoading: sheet(.loading)
        case .cashPending: sheet(.pending)
        case .cashHistory:
            VStack { Spacer(minLength: 232); CashoutHistory(onBack: { open = nil }) }.ignoresSafeArea()
        case .cashSuccess: CashoutSuccess(onDone: { open = nil })
        }
    }

    /// The sheet starts 232 down, as it does in the prototype.
    private func sheet(_ state: CashoutSheet.State) -> some View {
        VStack { Spacer(minLength: 232); CashoutSheet(state: state) }.ignoresSafeArea()
    }

    /// 86_399 -> "235959", the six digits the flip clock takes.
    static func digits(from seconds: Int) -> String {
        let s = max(0, seconds)
        return String(format: "%02d%02d%02d", s / 3600, (s % 3600) / 60, s % 60)
    }
}

#Preview { Gallery() }

import SwiftUI

/// The cash-out sheet, in the states the prototype runs. One sheet: the hero says where you
/// stand, the info row says what happens next, and the actions stay in the same place throughout
/// so the button never moves between states.
struct CashoutSheet: View {
    enum State: String, CaseIterable, Identifiable {
        case earned, empty, limit, loading, pending
        var id: String { rawValue }

        var label: String {
            switch self {
            case .earned: "Earned"
            case .empty: "Nothing yet"
            case .limit: "At the cap"
            case .loading: "Cashing out"
            case .pending: "Converting"
            }
        }

        var eyebrow: String {
            switch self {
            case .empty: "Oh no!"
            case .pending: "Your stars convert in"
            case .earned, .limit, .loading: "Well done!"
            }
        }

        var amount: String {
            switch self {
            case .empty: "$0.00"
            case .pending: "3:14:03"       // counting, so it reads as a clock
            case .earned, .limit, .loading: "$0.32"
            }
        }

        var sub: String? {
            switch self {
            case .empty: "Play more to earn your first reward."
            case .pending: nil
            case .earned, .limit, .loading: "Earned and ready to cash out."
            }
        }

        var note: String {
            self == .limit
                ? "You’ve reached the maximum balance. Cash out to keep earning."
                : "Your stars turn into rewards in 3h 45m. The more stars, the higher the reward."
        }

        var primary: String {
            switch self {
            case .empty, .pending: "Play games"
            case .loading: "Cashing out…"
            case .earned, .limit: "Cash out"
            }
        }

        var secondary: String {
            switch self {
            case .empty, .pending: "Back to home"
            case .earned, .limit, .loading: "Keep playing"
            }
        }

        var showsHistory: Bool { self != .empty }
    }

    let state: State
    var onPrimary: () -> Void = {}
    var onSecondary: () -> Void = {}
    var onHistory: () -> Void = {}

    var body: some View {
        VStack(spacing: 16) {
            hero
            InfoRow(text: state.note)
            Spacer(minLength: 0)
            VStack(spacing: 4) {
                Button(action: onPrimary) {
                    HStack(spacing: 8) {
                        if state == .loading { ProgressView().tint(.white) }
                        Text(state.primary)
                    }
                    .font(.ds(.headline))
                    .foregroundStyle(Color.onAccent)
                    .frame(maxWidth: .infinity)
                    .frame(height: Size.controlHeight)
                    .background(Color.blue500, in: Capsule())
                }
                .buttonStyle(.plain)
                .disabled(state == .loading)

                Button(state.secondary, action: onSecondary)
                    .font(.ds(.headline))
                    .foregroundStyle(Color.link)
                    .frame(maxWidth: .infinity, minHeight: Size.hitTarget)
                    .buttonStyle(.plain)
            }
        }
        .padding(.top, 52)
        .padding(.horizontal, 16)
        .padding(.bottom, 34)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
        .background(Color.surface)
        .clipShape(UnevenRoundedRectangle(topLeadingRadius: 32, topTrailingRadius: 32, style: .continuous))
        .overlay(alignment: .top) {
            Capsule()
                .fill(Color.ink.opacity(0.22))
                .frame(width: 36, height: 5)
                .padding(.top, 6)
        }
    }

    private var hero: some View {
        VStack(spacing: 8) {
            Text(state.eyebrow)
                .font(.ds(.callout))
            Text(state.amount)
                .font(.ds(.amount))
                .monospacedDigit()
                .contentTransition(.numericText())
            if let sub = state.sub {
                Text(sub)
                    .font(.ds(.subheadline))
                    .opacity(0.92)
            }
            if state.showsHistory {
                Button(action: onHistory) {
                    HStack(spacing: 6) {
                        Image("history")
                            .resizable()
                            .scaledToFit()
                            .frame(width: 16, height: 16)
                        Text("History")
                    }
                    .font(.system(size: 13, weight: .semibold))
                    .frame(height: Size.pillHeight)
                    .padding(.horizontal, 14)
                    .background(Color.green700, in: Capsule())
                }
                .buttonStyle(.plain)
                .padding(.top, 2)
            }
        }
        .foregroundStyle(Color.onAccent)
        .multilineTextAlignment(.center)
        .frame(maxWidth: .infinity)
        .padding(.vertical, 30)
        .padding(.horizontal, 20)
        .background(.reward, in: RoundedRectangle(cornerRadius: Radius.xl, style: .continuous))
    }
}

struct InfoRow: View {
    let text: String

    var body: some View {
        HStack(spacing: 12) {
            Circle()
                .fill(Color.green700)
                .frame(width: Size.iconTile, height: Size.iconTile)
                .overlay {
                    Image("icons-coin")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 22, height: 22)
                }
            Text(text)
                .font(.ds(.subheadline))
                .foregroundStyle(Color.ink)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.vertical, 12)
        .padding(.horizontal, 16)
        .background(Color.surfaceInfo, in: RoundedRectangle(cornerRadius: Radius.lg, style: .continuous))
    }
}

/// What the sheet shows behind the History pill.
struct CashoutHistory: View {
    struct Entry: Identifiable {
        let id = UUID()
        let date: String
        let status: String
        let amount: String
        var tint: Color {
            switch status {
            case "Paid": .success
            case "Failed": .danger
            default: .inkSecondary
            }
        }
    }

    var entries: [Entry] = [
        .init(date: "April 26", status: "Paid", amount: "$1.30"),
        .init(date: "April 3", status: "Paid", amount: "$0.32"),
        .init(date: "March 22", status: "Pending", amount: "$0.86"),
        .init(date: "March 14", status: "Failed", amount: "$1.12")
    ]
    var onBack: () -> Void = {}

    var body: some View {
        VStack(spacing: 16) {
            ZStack {
                Text("History").font(.ds(.headline).weight(.bold)).foregroundStyle(Color.ink)
                HStack {
                    Button("Back", action: onBack)
                        .font(.system(size: 13, weight: .semibold))
                        .foregroundStyle(Color.ink)
                        .frame(height: Size.pillHeight)
                        .padding(.horizontal, 14)
                        .background(Color.surfaceGrouped, in: Capsule())
                        .buttonStyle(.plain)
                    Spacer()
                }
            }
            .frame(minHeight: Size.hitTarget)

            VStack(spacing: 0) {
                ForEach(Array(entries.enumerated()), id: \.element.id) { index, entry in
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(entry.date).font(.ds(.subheadline)).foregroundStyle(Color.ink)
                            Text(entry.status).font(.ds(.caption)).foregroundStyle(entry.tint)
                        }
                        Spacer()
                        Text(entry.amount)
                            .font(.ds(.headline))
                            .monospacedDigit()
                            .foregroundStyle(Color.ink)
                    }
                    .padding(.vertical, 12)
                    if index < entries.count - 1 {
                        Rectangle().fill(Color.separator).frame(height: 1)
                    }
                }
            }
            .padding(.horizontal, 16)
            .background(Color.surfaceGrouped, in: RoundedRectangle(cornerRadius: Radius.lg, style: .continuous))

            Spacer(minLength: 0)
        }
        .padding(.top, 52)
        .padding(.horizontal, 16)
        .padding(.bottom, 34)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
        .background(Color.surface)
        .clipShape(UnevenRoundedRectangle(topLeadingRadius: 32, topTrailingRadius: 32, style: .continuous))
    }
}

/// The end of the flow: the money is on its way.
struct CashoutSuccess: View {
    var amount: String = "$2.81"
    var onDone: () -> Void = {}

    var body: some View {
        ZStack {
            Color(red: 0.26, green: 0.26, blue: 0.26).ignoresSafeArea()
            VStack(spacing: 0) {
                Image("success-art")
                    .resizable()
                    .scaledToFit()
                    .accessibilityLabel("The fox relaxing on a beach")
                VStack(spacing: 14) {
                    Text("Cash out successful!")
                        .font(.ds(.title2))
                        .foregroundStyle(Color.green700)
                        .multilineTextAlignment(.center)
                    Text("Your \(amount) is on the way.")
                        .font(.ds(.subheadline))
                        .foregroundStyle(Color.ink)
                    Button("Done", action: onDone)
                        .font(.ds(.headline))
                        .foregroundStyle(Color.onAccent)
                        .frame(maxWidth: .infinity)
                        .frame(height: Size.controlHeight)
                        .background(Color.blue500, in: Capsule())
                        .buttonStyle(.plain)
                }
                .padding(.top, 8)
                .padding(.horizontal, 20)
                .padding(.bottom, 24)
                .background(Color.surface)
                .clipShape(UnevenRoundedRectangle(bottomLeadingRadius: Radius.xl,
                                                  bottomTrailingRadius: Radius.xl, style: .continuous))
                .padding(.horizontal, 22)
            }
        }
    }
}

#Preview("Earned") { CashoutSheet(state: .earned) }
#Preview("Converting") { CashoutSheet(state: .pending) }
#Preview("History") { CashoutHistory() }
#Preview("Success") { CashoutSuccess() }

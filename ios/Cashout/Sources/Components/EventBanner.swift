import SwiftUI

/// The 2x coins strip across the top of the home screen. Before the boost starts it offers it and
/// counts down to the deadline; once it is running it shows the time left on the big clock.
struct EventBanner: View {
    enum State: String, CaseIterable, Identifiable {
        case offer, active
        var id: String { rawValue }
        var label: String { self == .offer ? "Offer" : "Active" }
    }

    let state: State
    /// Six digits, HHMMSS — the time left on the boost.
    var left: String = "235842"
    var endsIn: String = "23:14:00"
    var onStart: () -> Void = {}

    var body: some View {
        ZStack(alignment: .topLeading) {
            LinearGradient(colors: [.pink400, .pink600], startPoint: .top, endPoint: .bottom)
                .overlay(alignment: .top) {
                    RadialGradient(colors: [Color(red: 1, green: 0.478, blue: 0.608), .clear],
                                   center: .top, startRadius: 0, endRadius: 250)
                }

            VStack(alignment: .trailing, spacing: 2) {
                Text("LIMITED EVENT")
                    .font(.system(size: 12, weight: .bold))
                    .tracking(1.2)
                    .opacity(0.85)
                Image("logo")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 158)
                    .accessibilityLabel("2x coins")
            }
            .foregroundStyle(Color.onAccent)
            .frame(maxWidth: .infinity, alignment: .trailing)
            .padding(.trailing, 14)
            .padding(.top, 72)

            VStack(alignment: .leading, spacing: 6) {
                switch state {
                case .offer:
                    Button(action: onStart) {
                        HStack(spacing: 8) {
                            Text("Start now")
                            AdTag()
                        }
                        .font(.system(size: 15, weight: .bold))
                        .foregroundStyle(Color.onAccent)
                        .frame(minHeight: Size.hitTarget)
                        .padding(.horizontal, 14)
                        .background(Color.violet400, in: Capsule())
                    }
                    .buttonStyle(.plain)

                    Text("Ends in \(endsIn)")
                        .font(.system(size: 12, weight: .semibold))
                        .monospacedDigit()
                        .foregroundStyle(Color.onAccent)
                        .frame(height: 22)
                        .padding(.horizontal, 10)
                        .background(Color.pink800.opacity(0.75), in: Capsule())
                        .accessibilityLabel("Offer ends in \(endsIn)")

                case .active:
                    FlipTimer(digits: left, scale: .small, colonColor: .white)
                }
            }
            .padding(.leading, 14)
            .padding(.top, 108)
        }
        .frame(height: 190)
        .clipped()
        .accessibilityElement(children: .contain)
        .accessibilityLabel("2x coins, limited event")
    }
}

#Preview("Offer") { EventBanner(state: .offer) }
#Preview("Active") { EventBanner(state: .active) }

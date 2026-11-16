import SwiftUI

@main
struct CashoutApp: App {
    var body: some Scene {
        WindowGroup { PopupGallery() }
    }
}

/// The same four states the 2x coins prototype runs, on the same backdrop, with the clock
/// actually counting so the digit roll and the blinking colons are real rather than described.
struct PopupGallery: View {
    @State private var state: BoostPopup.BoostState = .offer
    @State private var secondsLeft = 86_399

    private let tick = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    var body: some View {
        ZStack {
            Image("body")
                .resizable()
                .scaledToFill()
                .ignoresSafeArea()
                .accessibilityHidden(true)

            BoostPopup(state: state,
                       left: Self.digits(from: secondsLeft),
                       onPrimary: { state = .active },
                       onDismiss: { state = .offer })

            VStack {
                Spacer()
                picker
            }
        }
        .onReceive(tick) { _ in
            guard state == .active, secondsLeft > 0 else { return }
            secondsLeft -= 1
        }
    }

    private var picker: some View {
        Picker("State", selection: $state) {
            ForEach(BoostPopup.BoostState.allCases) { Text($0.label).tag($0) }
        }
        .pickerStyle(.segmented)
        .padding(.horizontal, 16)
        .padding(.bottom, 8)
    }

    /// 86_399 -> "235959", the six digits the flip clock takes.
    static func digits(from seconds: Int) -> String {
        let s = max(0, seconds)
        return String(format: "%02d%02d%02d", s / 3600, (s % 3600) / 60, s % 60)
    }
}

#Preview { PopupGallery() }

import SwiftUI

/// The time left, on the pink head of the 2x coins pop-up. No icon: the numbers carry it.
/// Solid pink-800 rather than a translucent fill, so it reads the same wherever it lands
/// on the gradient instead of turning dusty over the white curve.
struct TimePill: View {
    /// Counting, so it is written as a clock: 3:14:03.
    let clock: String
    var spoken: String?

    var body: some View {
        Text(clock)
            .font(.system(size: 18, weight: .semibold))
            .monospacedDigit()
            .contentTransition(.numericText())
            .foregroundStyle(Color.onAccent)
            .frame(height: 32)
            .padding(.horizontal, 14)
            .background(Color.pink800, in: Capsule())
            .accessibilityElement(children: .ignore)
            .accessibilityLabel(spoken ?? clock)
            .accessibilityAddTraits(.updatesFrequently)
    }
}

#Preview {
    TimePill(clock: "23:59:59", spoken: "23 hours, 59 minutes left")
        .padding()
        .background(Color.pink600)
}

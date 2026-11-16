import SwiftUI

/// Marks a button as paid for by a rewarded video. 32x22, and it follows the label
/// rather than leading it — see the ad chip note in the design system.
struct AdTag: View {
    var body: some View {
        RoundedRectangle(cornerRadius: 7, style: .continuous)
            .fill(Color.chipDark)
            .frame(width: 32, height: 22)
            .overlay {
                Image(systemName: "play.fill")
                    .font(.system(size: 10))
                    .foregroundStyle(Color.onAccent)
            }
            .accessibilityElement(children: .ignore)
            .accessibilityLabel("Watch ad")
    }
}

#Preview {
    AdTag().padding().background(Color.violet400)
}

import SwiftUI

/// The two full-screen steps before the game: the terms, then the proof.
/// Both end in a footer whose primary sits at the same height — a footer with no link under the
/// button reserves the room one would take, rather than dropping 48pt lower.
struct OnboardingStep: View {
    enum Step: String, CaseIterable, Identifiable {
        case terms, trustedBy
        var id: String { rawValue }
        var label: String { self == .terms ? "Terms" : "Trusted by" }
    }

    let step: Step
    var onPrimary: () -> Void = {}
    var onSkip: () -> Void = {}

    var body: some View {
        VStack(spacing: 0) {
            switch step {
            case .terms: terms
            case .trustedBy: trusted
            }
            footer
        }
        .background(Color.surface)
    }

    private var terms: some View {
        VStack(spacing: 20) {
            Image("handshake")
                .resizable()
                .scaledToFit()
                .frame(width: 200)
                .accessibilityHidden(true)
            Text("Terms and conditions")
                .font(.ds(.title1))
                .foregroundStyle(Color.ink)
            Text(termsCopy)
                .font(.ds(.body))
                .foregroundStyle(Color.inkSecondary)
                .multilineTextAlignment(.center)
        }
        .padding(.horizontal, 24)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private var termsCopy: AttributedString {
        var s = AttributedString("To continue playing, confirm that you agree to our Terms of Service and have read our Privacy Policy.")
        for phrase in ["Terms of Service", "Privacy Policy"] {
            if let r = s.range(of: phrase) {
                s[r].foregroundColor = .link
                s[r].font = .ds(.body).weight(.semibold)
            }
        }
        return s
    }

    private var trusted: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Trusted by\n10M+ users")
                .font(.ds(.title1))
                .foregroundStyle(Color.ink)
                .multilineTextAlignment(.center)
                .frame(maxWidth: .infinity)

            HStack(spacing: 12) {
                ratingCard(source: "Google reviews", score: "4.6", note: "Based on 123 reviews")
                ratingCard(source: "Trustpilot", score: "4.8 / 5", note: "Based on 456 reviews")
            }

            Text("Don’t believe us? Check our reviews")
                .font(.ds(.headline))
                .foregroundStyle(Color.ink)
                .frame(maxWidth: .infinity)

            VStack(spacing: 12) {
                review("Player review · placed 2 days ago", "Cashed out twice already. Took about a day both times, no fuss.")
                review("Player review · placed a week ago", "The missions make it worth opening every day.")
            }
            Spacer(minLength: 0)
        }
        .padding(.horizontal, 16)
        .padding(.top, 48)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
    }

    private func ratingCard(source: String, score: String, note: String) -> some View {
        VStack(spacing: 2) {
            Text(source).font(.ds(.caption)).foregroundStyle(Color.inkSecondary)
            Text(score).font(.ds(.title1).weight(.bold)).foregroundStyle(Color.ink)
            Stars()
            Text(note).font(.ds(.caption).weight(.medium)).foregroundStyle(Color.inkSecondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 16)
        .padding(.horizontal, 12)
        .background(Color.surfaceGrouped, in: RoundedRectangle(cornerRadius: Radius.lg, style: .continuous))
    }

    private func review(_ meta: String, _ body: String) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(meta).font(.ds(.caption)).foregroundStyle(Color.inkSecondary)
            Stars()
            Text(body).font(.ds(.subheadline)).foregroundStyle(Color.ink)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(16)
        .background(Color.surfaceGrouped, in: RoundedRectangle(cornerRadius: Radius.lg, style: .continuous))
    }

    private var footer: some View {
        VStack(spacing: 4) {
            Button(step == .terms ? "Accept" : "Continue", action: onPrimary)
                .font(.ds(.headline))
                .foregroundStyle(Color.onAccent)
                .frame(maxWidth: .infinity)
                .frame(height: Size.controlHeight)
                .background(Color.blue500, in: Capsule())
                .buttonStyle(.plain)

            if step == .trustedBy {
                Button("Skip", action: onSkip)
                    .font(.ds(.headline))
                    .foregroundStyle(Color.link)
                    .frame(maxWidth: .infinity, minHeight: Size.hitTarget)
                    .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 16)
        .padding(.top, 16)
        // With no link under it the button would sit 48 lower than every other primary,
        // so the footer keeps that room either way.
        .padding(.bottom, step == .terms ? 34 + Size.hitTarget + 4 : 34)
    }
}

private struct Stars: View {
    var body: some View {
        HStack(spacing: 1) {
            ForEach(0..<5, id: \.self) { _ in
                Image(systemName: "star.fill")
                    .font(.system(size: 13))
                    .foregroundStyle(Color.gold400)
            }
        }
        .accessibilityHidden(true)
    }
}

#Preview("Terms") { OnboardingStep(step: .terms) }
#Preview("Trusted by") { OnboardingStep(step: .trustedBy) }

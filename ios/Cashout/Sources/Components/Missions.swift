import SwiftUI

/// One task on the missions card. The reward sits in its own cell on the left, so the row reads
/// reward first, then what earns it, then the control.
struct MissionRow: View {
    enum Status {
        case claim          // earned, waiting to be collected
        case go             // not started
        case claimed        // done

        var isDone: Bool { self == .claimed }
    }

    let reward: String
    let task: String
    let status: Status
    var onTap: () -> Void = {}

    var body: some View {
        HStack(spacing: 0) {
            VStack(spacing: 2) {
                Image("icons-coin")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 22, height: 22)
                Text(reward)
                    .font(.system(size: 13, weight: .bold))
            }
            .frame(width: 66)
            .padding(.vertical, 8)
            .background(status.isDone ? Color.clear : Color.sky200)
            .foregroundStyle(status.isDone ? Color.onAccent : Color.ink)

            HStack(spacing: 8) {
                Text(task)
                    .font(.system(size: 13, weight: .bold))
                    .foregroundStyle(status.isDone ? Color.onAccent : Color.ink)
                    .frame(maxWidth: .infinity, alignment: .leading)

                switch status {
                case .claim:
                    control("Claim", fill: .claimFill)
                case .go:
                    control("Go", fill: .blue500)
                case .claimed:
                    HStack(spacing: 4) {
                        Image(systemName: "checkmark")
                        Text("Claimed")
                    }
                    .font(.system(size: 14, weight: .heavy))
                    .foregroundStyle(Color.onAccent)
                }
            }
            .padding(.leading, 12)
            .padding(.trailing, 10)
            .padding(.vertical, 8)
        }
        .background(status.isDone ? Color.green700 : Color.surfaceInfo)
        .clipShape(RoundedRectangle(cornerRadius: Radius.md, style: .continuous))
        .overlay {
            if status.isDone {
                RoundedRectangle(cornerRadius: Radius.md, style: .continuous)
                    .strokeBorder(Color.mint400, lineWidth: 2)
            }
        }
    }

    private func control(_ title: String, fill: Color) -> some View {
        Button(title, action: onTap)
            .font(.system(size: 15, weight: .heavy))
            .foregroundStyle(Color.onAccent)
            .frame(height: 36)
            .padding(.horizontal, title == "Go" ? 24 : 20)
            .background(fill, in: Capsule())
            .buttonStyle(.plain)
    }
}

/// The card the rows live on: the event art, the time left, and how far along you are.
struct MissionCard: View {
    var timeLeft: String = "3d 8h"
    var done: Int = 1
    var total: Int = 3

    var body: some View {
        VStack(spacing: 10) {
            ZStack(alignment: .topLeading) {
                Image("fox")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 108)
                    .accessibilityHidden(true)

                VStack(spacing: 8) {
                    HStack(spacing: 4) {
                        Image("clock")
                            .resizable()
                            .scaledToFit()
                            .frame(width: 22, height: 22)
                        // A span, not a countdown, so it reads 3d 8h rather than as a clock.
                        Text(timeLeft)
                            .font(.system(size: 15, weight: .bold))
                            .monospacedDigit()
                    }
                    .foregroundStyle(Color.gold400)
                    .frame(height: 24)
                    .padding(.horizontal, 12)
                    .background(Color.chipDark, in: Capsule())

                    Text("Fast track to max earnings!")
                        .font(.system(size: 17, weight: .heavy))
                        .foregroundStyle(Color.onAccent)

                    HStack(spacing: 8) {
                        ForEach(0..<total, id: \.self) { i in
                            Circle()
                                .strokeBorder(Color.mint400, lineWidth: 2)
                                .background(Circle().fill(i < done ? Color.mint400 : .clear))
                                .frame(width: 24, height: 24)
                                .overlay {
                                    if i < done {
                                        Image(systemName: "checkmark")
                                            .font(.system(size: 11, weight: .bold))
                                            .foregroundStyle(Color.green700)
                                    }
                                }
                        }
                    }
                    .accessibilityLabel("\(done) of \(total) done")
                }
                .frame(maxWidth: .infinity)
                .padding(.leading, 92)
            }
            .padding(.top, 12)
            .padding(.horizontal, 16)

            VStack(spacing: 8) {
                MissionRow(reward: "1,000", task: "Collect the welcome bonus", status: .claimed)
                MissionRow(reward: "1,000", task: "Win 1 regular level", status: .claim)
                MissionRow(reward: "1,500", task: "Play 10 levels in Kitchen Ninja", status: .go)
            }
            .padding(.horizontal, 10)
            .padding(.bottom, 10)
        }
        .background(LinearGradient(stops: [
            .init(color: .violet500, location: 0.24),
            .init(color: .indigo800, location: 1)
        ], startPoint: .top, endPoint: .bottom))
        .clipShape(RoundedRectangle(cornerRadius: Radius.lg, style: .continuous))
        .shadow(color: .black.opacity(0.4), radius: 2, y: 2)
    }
}

/// The teaching moment: the screen dims, one thing stays lit, and a line of copy explains it.
/// Tapping anywhere moves on, so the scrim carries the gesture rather than a button.
struct CoachMark<Target: View>: View {
    let caption: AttributedString
    var onContinue: () -> Void = {}
    @ViewBuilder var target: Target

    var body: some View {
        ZStack {
            Color.scrimStrong
                .ignoresSafeArea()
                .contentShape(Rectangle())
                .onTapGesture(perform: onContinue)
                .accessibilityAddTraits(.isButton)
                .accessibilityLabel("Continue")

            VStack(spacing: 44) {
                target
                Text(caption)
                    .font(.ds(.title2))
                    .foregroundStyle(Color.onAccent)
                    .multilineTextAlignment(.center)
            }
            .padding(.horizontal, 16)
            .allowsHitTesting(false)
        }
    }
}

#Preview("Missions card") {
    MissionCard().padding(8).background(Color.surfaceGrouped)
}

#Preview("Coach mark") {
    CoachMark(caption: AttributedString("First task:\nclaim your reward!")) {
        MissionRow(reward: "1,000", task: "Collect the welcome bonus", status: .claim)
    }
}

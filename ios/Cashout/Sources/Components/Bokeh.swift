import SwiftUI

/// The soft field of light that drifts up behind the earned states. The prototype draws this
/// on a 2D canvas; here it is a `Canvas` driven by `TimelineView`, which costs one redraw per
/// frame and nothing else. Motion stops when the device asks for reduced motion.
struct Bokeh: View {
    var count: Int = 18
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 30.0, paused: reduceMotion)) { context in
            Canvas { canvas, size in
                let t = context.date.timeIntervalSinceReferenceDate
                for i in 0..<count {
                    let seed = Double(i)
                    let radius = 18 + (seed * 7).truncatingRemainder(dividingBy: 26)
                    let drift = sin(t * 0.07 + seed) * 0.5 + 0.5
                    let x = drift * size.width
                    let rise = (t * (8 + seed.truncatingRemainder(dividingBy: 5)) + seed * 60)
                        .truncatingRemainder(dividingBy: size.height + 160)
                    let y = size.height + 80 - rise
                    let rect = CGRect(x: x - radius, y: y - radius, width: radius * 2, height: radius * 2)
                    canvas.fill(Circle().path(in: rect), with: .color(.white.opacity(0.10)))
                }
            }
        }
        .blur(radius: 8)
        .allowsHitTesting(false)
        .accessibilityHidden(true)
    }
}

#Preview {
    Bokeh().background(Color.violet500)
}

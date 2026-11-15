/* Onboarding components for the Cashout design system: MissionRow, MissionCard, CoachMark, RewardCard, Popup, and the 2x coins set (FlipTimer, TimePill, AdTag, BoostTag, BoostButton, EventBanner, BoostPopup).
   Built by tools/build.py. Adds to window.Cashout. */
(function () {
  var React = window.React, h = React.createElement;
  var A = { coin: "__COIN__", fox: "__FOX__", hand: "__HAND__", pile: "__PILE__", clock: "__CLOCK__", logo: "__LOGO__", topcoins: "__TOPCOINS__" };
  var nf = new Intl.NumberFormat("en-US");
  var check = function (color) { return h("svg", { viewBox: "0 0 14 14", width: 14, height: 14, fill: "none", stroke: color || "#fff", strokeWidth: 2.6, strokeLinecap: "round", strokeLinejoin: "round", "aria-hidden": "true" }, h("path", { d: "M2.5 7.5 5.8 10.5 11.5 4" })); };

  // state: "go" | "progress" | "claim" | "claimed"
  function MissionRow(props) {
    var st = props.state || "go", total = props.total || 0, p = props.progress || 0;
    var label = st === "claimed" ? "Claimed" : st === "claim" ? "Claim" : "Go";
    return h("div", { className: "ob mr " + st },
      h("div", { className: "mr-coin" }, h("img", { src: A.coin, alt: "" }), nf.format(props.coins || 0)),
      h("div", { className: "mr-main" }, h("div", { className: "mr-title" }, props.title),
        h("div", { className: "mr-bar" }, h("i", { style: { width: (total ? p / total * 100 : 0) + "%" } }), h("span", null, p + "/" + total))),
      h("button", { type: "button", className: "mr-btn", disabled: st === "claimed" || st === "progress", onClick: props.onAction },
        st === "claimed" ? h("span", { style: { marginRight: 4, verticalAlign: -2, display: "inline-block" } }, check("#fff")) : null, label));
  }

  function MissionCard(props) {
    var s = React.useState(!!props.collapsed), collapsed = s[0], set = s[1], done = props.done || 0;
    React.useEffect(function () { set(!!props.collapsed); }, [props.collapsed]);
    return h("section", { className: "ob mc" + (collapsed ? " collapsed" : "") + (props.finished ? " finished" : ""), "aria-label": "Missions" },
      h("div", { className: "mc-head" },
        h("img", { className: "mc-fox", src: A.fox, alt: "" }),
        h("span", { className: "mc-timer" }, h("img", { src: A.clock, alt: "" }), props.timer || "3d 8h"),
        h("div", { className: "mc-title" }, props.finished ? "" : (props.title || "Fast track to max earnings!")),
        h("div", { className: "mc-dots" }, [0, 1, 2].map(function (i) { return h("span", { key: i, className: "mc-dot" + (i < done ? " done" : "") }, check()); })),
        h("div", { className: "mc-done" }, h("img", { src: A.coin, alt: "" }), "Missions complete"),
        h("button", { type: "button", className: "mc-toggle", "aria-label": "Show or hide missions", onClick: function () { set(!collapsed); } }, h("i"))),
      h("div", { className: "mc-rows" }, props.children));
  }

  function CoachMark(props) {
    return h("div", { className: "ob ob-coach" },
      h("div", { className: "ob-coach-target" }, props.target, h("img", { className: "ob-coach-hand", src: A.hand, alt: "" })),
      h("div", { className: "ob-coach-text" }, props.children));
  }

__GLOW__
  // The reward moment, as a Popup (hero size, violet card) with a glowing coin pile.
  // tone: "welcome" | "congrats" | "boost" (orange action, 2x offer)
  function RewardCard(props) {
    var tone = props.tone || "welcome", pile = React.useRef(null);
    React.useEffect(function () {
      var el = pile.current, seen = false; if (!el || !window.IntersectionObserver) return;
      var fx = makeGlow(el, function () { return seen; }, tone === "boost" ? [1.0, 0.62, 0.22] : tone === "congrats" ? [1.0, 0.78, 0.30] : [1.0, 0.82, 0.18]);
      var io = new IntersectionObserver(function (es) { seen = es[0].isIntersecting; if (seen) fx.start(); });
      io.observe(el);
      return function () { seen = false; io.disconnect(); };
    }, [tone]);
    var welcome = tone === "welcome", boost = tone === "boost";
    var amount = props.amount || (welcome ? "+1,000" : boost ? "2x coins · 15 min" : "1,500");
    return h(Popup, {
      size: "hero", card: "dark", bg: "linear-gradient(180deg, var(--violet-500) 10%, var(--indigo-800) 100%)",
      over: h("img", { className: "bx-coins", src: A.topcoins, alt: "" }),
      title: props.title || (welcome ? "Welcome reward!" : "Congrats!"),
      text: welcome ? null : (props.subtitle || (boost ? "Get a 2x coins boost" : "Missions complete!")),
      action: props.cta || (welcome ? "Awesome!" : boost ? "Boost now" : "Get double"), tone: boost ? "offer" : "claim", ad: !welcome,
      onAction: props.onAction, dismiss: props.dismiss || (welcome ? null : boost ? "Skip" : "Claim 1,500"), onDismiss: props.onDismiss,
      className: "ob ob-reward"
    },
      h("div", { className: "ob-pile", ref: pile }, h("img", { src: A.pile, alt: "" })),
      h("div", { className: boost ? "pp-title ob-boost-amount" : "pp-amount" }, amount),
      welcome ? h("p", { className: "pp-text" }, props.subtitle || "Start playing to earn even more!") : null);
  }

  // Popup: the one frame for centered pop-ups. Fixed frame, free header art and body content.
  // size: "compact" | "standard" | "hero" · card: "light" | "dark" · tone: "claim" | "boost" | "offer"
  function Popup(props) {
    var style = {}; if (props.bg) style["--pp-bg"] = props.bg; if (props.headBg) style["--pp-head"] = props.headBg;
    var hasHead = props.head != null || props.eyebrow != null;
    return h("div", { className: "pp-demo" + (props.dismiss ? " has-dismiss" : "") + (props.className ? " " + props.className : "") },
      h("div", { className: "pp", "data-size": props.size || "standard", "data-card": props.card || props.theme || "light", style: style },
        props.over ? h("div", { className: "pp-over" }, props.over) : null,
        h("div", { className: "pp-card" },
          hasHead ? h("div", { className: "pp-head", "data-curve": props.curve ? "" : undefined }, props.head, props.eyebrow ? h("div", { className: "pp-eyebrow" }, props.eyebrow) : null) : null,
          h("div", { className: "pp-body" },
            props.title ? h("h4", { className: "pp-title" }, props.title) : null,
            props.text ? h("p", { className: "pp-text" }, props.text) : null,
            props.children,
            props.amount ? h("div", { className: "pp-amount" }, props.amount) : null,
            props.action ? h("button", { type: "button", className: "pp-btn", "data-tone": props.tone || "claim", onClick: props.onAction }, props.ad ? h(AdTag, { key: "ad" }) : null, props.action) : null))),
      props.dismiss ? h("button", { type: "button", className: "pp-dismiss", onClick: props.onDismiss }, props.dismiss) : null);
  }
  Popup.art = A;
  /* ---------- 2x coins ---------- */
  // value: seconds left (a number) or six digits "hhmmss" · size: "large" | "small"
  function FlipTimer(props) {
    var raw = props.value == null ? "235959" : props.value, v;
    if (typeof raw === "number") { var t = Math.max(0, Math.floor(raw)), p = function (n) { return (n < 10 ? "0" : "") + n; }; v = p(Math.min(99, Math.floor(t / 3600))) + p(Math.floor(t % 3600 / 60)) + p(t % 60); }
    else v = (String(raw).replace(/\D/g, "") + "000000").slice(0, 6);
    var kids = [];
    for (var k = 0; k < 6; k++) { if (k === 2 || k === 4) kids.push(h("em", { key: "c" + k }, ":")); kids.push(h("i", { key: k }, v.charAt(k))); }
    return h("span", { className: "bx-flip" + (props.size === "small" ? " small" : ""), role: "timer", "aria-label": +v.slice(0, 2) + " hours " + +v.slice(2, 4) + " minutes " + +v.slice(4) + " seconds left" }, kids);
  }
  // A running clock, so it carries the format and the role Countdown uses.
  function TimePill(props) { return h("span", { className: "bx-pill", role: "timer", "aria-label": props.spoken }, h("img", { src: A.clock, alt: "" }), props.children || "23:59:59"); }
  function AdTag() { return h("span", { className: "pp-adtag", role: "img", "aria-label": "Watch ad", title: "Watch ad" }); }
  function BoostTag() { return h("span", { className: "bx-tag" }, "2x"); }
  // size: "popup" (50pt, fills the body) | "banner" (44pt, hugs its label)
  function BoostButton(props) {
    var label = props.children || "Start now";
    if (props.size === "banner") return h("button", { type: "button", className: "bx-ev-start bx-reset", onClick: props.onAction }, h(AdTag), label);
    return h("button", { type: "button", className: "pp-btn", "data-tone": "boost", onClick: props.onAction }, h(AdTag), label);
  }
  // state: "offer" (Start now plays the ad: onAction) | "active" (tapping opens progress: onOpen)
  function EventBanner(props) {
    var active = props.state === "active";
    return h("div", { className: "bx" }, h("div", { className: "bx-ev", role: "group", "aria-label": "2x coins, limited event", onClick: active ? props.onOpen : undefined, style: active && props.onOpen ? { cursor: "pointer" } : undefined },
      h("span", { className: "bx-ev-left" },
        active ? h(FlipTimer, { size: "small", value: props.value == null ? "235842" : props.value }) : h(BoostButton, { size: "banner", onAction: props.onAction }, props.label || "Start now"),
        active ? null : h("span", { className: "bx-ev-ends" }, h("img", { src: A.clock, alt: "" }), props.endsIn || "Ends in 23h 14m")),
      h("span", { className: "bx-ev-right" }, h("span", null, "Limited event"), h("img", { src: A.logo, alt: "2x coins" }))));
  }
  // state: "offer" | "active" | "progress" | "over" · onAction starts the boost, onDismiss closes
  function BoostPopup(props) {
    var st = props.state || "offer", mode = st === "offer" ? "intro" : st;
    var dismiss = props.dismiss || (st === "offer" ? "Skip" : st === "over" ? "Tap to continue" : "Close");
    return h("div", { className: "bx pp-demo has-dismiss" + (st === "over" ? " bx-over" : "") },
      h("div", { className: "pp bpop", "data-size": "standard", "data-mode": mode },
        h("div", { className: "bx-over-title" }, "Congrats!"),
        h("div", { className: "bx-rays", "aria-hidden": "true" }),
        h("div", { className: "pp-over" }, h("img", { className: "bx-coins", src: A.topcoins, alt: "" })),
        h("div", { className: "pp-card" },
          h("div", { className: "pp-head", "data-curve": "" },
            h("img", { src: A.logo, alt: "2x coins" }),
            h("div", { className: "pp-eyebrow" }, st === "progress" ? "Bonus active" : st === "over" ? "Time is over" : "Start ahead"),
            h(TimePill, null, props.left)),
          h("div", { className: "pp-body" },
            h(FlipTimer, { value: props.value != null ? props.value : st === "offer" ? "240000" : "235959" }),
            h("p", { className: "pp-text" }, "You have 24 hours to double all the coins you earn playing your favorite games."),
            h("div", { className: "bx-active" }, h("b", { className: "pp-title" }, "Bonus is active!"), h("span", { className: "pp-text", style: { margin: 0, display: "block" } }, "Play games to earn coins")),
            h("div", { className: "bx-earn" }, h("img", { src: A.pile, alt: "" }), h("span", { className: "pp-eyebrow" }, st === "over" ? "You\u2019ve earned" : "So far you\u2019ve earned"), h("s", null, props.base || "5,000"), h("b", { className: "pp-amount" }, props.total || "+10,000")),
            h(BoostButton, { onAction: props.onAction }, props.label)))),
      h("button", { type: "button", className: "pp-dismiss", onClick: props.onDismiss }, dismiss));
  }
  window.Cashout = Object.assign(window.Cashout || {}, { MissionRow: MissionRow, MissionCard: MissionCard, CoachMark: CoachMark, RewardCard: RewardCard, Popup: Popup, FlipTimer: FlipTimer, TimePill: TimePill, AdTag: AdTag, BoostTag: BoostTag, BoostButton: BoostButton, EventBanner: EventBanner, BoostPopup: BoostPopup });
})();

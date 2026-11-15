/* @ds-bundle: {"format":4,"namespace":"Cashout","components":[{"name":"Button"},{"name":"AmountHero"},{"name":"Pill"},{"name":"InfoRow"},{"name":"Countdown"},{"name":"HistoryList"},{"name":"StatTile"},{"name":"InlineMessage"},{"name":"TabBar"},{"name":"CashoutSheet"}]} */
(function () {
  var React = window.React, h = React.createElement;
  var ASSET = { history: "__HISTORY__", star: "__STAR__", tip: "__TIP__" };
  function cx() { return Array.prototype.filter.call(arguments, Boolean).join(" "); }

  function money(amount, currency, locale) {
    try { return new Intl.NumberFormat(locale || "en-US", { style: "currency", currency: currency || "USD" }).format(amount); }
    catch (e) { return String(amount); }
  }
  function clock(sec) {
    sec = Math.max(0, Math.floor(sec));
    var hh = Math.floor(sec / 3600), mm = Math.floor(sec % 3600 / 60), ss = sec % 60;
    var p = function (n) { return (n < 10 ? "0" : "") + n; };
    return { text: (hh ? hh + ":" + p(mm) : mm) + ":" + p(ss), spoken: [hh && hh + " hours", mm && mm + " minutes", ss + " seconds"].filter(Boolean).join(", ") };
  }
  function shortDuration(sec) { var hh = Math.floor(sec / 3600), mm = Math.floor(sec % 3600 / 60); return (hh ? hh + "h " : "") + mm + "m"; }

  // Copy text from inside a sandboxed preview frame: Clipboard API, then execCommand, then select.
  function copyText(text, el) {
    function fallback() {
      var ta = document.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", "");
      ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select();
      var ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
      if (!ok && el) { var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); }
      return ok;
    }
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text).then(function () { return true; }, fallback);
    } catch (e) {}
    return Promise.resolve(fallback());
  }

  function Copy(props) {
    var st = React.useState(""), msg = st[0], set = st[1];
    var ref = React.useRef(null);
    function go() { copyText(props.code, ref.current).then(function (ok) { set(ok ? "Copied" : "Selected"); setTimeout(function () { set(""); }, 1400); }); }
    return h("div", { className: cx("co-code", props.inline && "co-code-inline") },
      props.label ? h("span", { className: "co-code-label" }, props.label) : null,
      h("pre", { ref: ref }, props.code),
      h("button", { type: "button", className: "co-copy", onClick: go, "aria-label": "Copy " + (props.label || "code") }, msg || "Copy"));
  }

  function Demo(props) {
    return h("figure", { className: "co-demo" }, h("div", { className: "co-demo-stage" }, props.children), props.caption ? h("figcaption", null, props.caption) : null);
  }

  function Button(props) {
    var variant = props.variant || "filled";
    return h("button", {
      type: "button",
      className: cx("co-btn", variant === "filled" && "co-btn-filled", props.fullWidth && "co-btn-full", props.className),
      disabled: props.disabled || props.loading, "aria-busy": props.loading ? "true" : undefined, onClick: props.onClick, style: props.style
    }, props.loading ? h("span", { className: "co-spinner", "aria-hidden": "true" }) : null, props.loading ? (props.loadingLabel || "Cashing out…") : props.children);
  }

  var HERO_COPY = {
    earned: { eyebrow: "Well done!", sub: "Earned and ready to cash out." },
    empty: { eyebrow: "Oh no!", sub: "Play more to earn your first reward." },
    pending: { eyebrow: "Almost there", sub: "Your stars are being converted." },
    success: { eyebrow: "Cash out successful", sub: "Your money is on the way." }
  };
  function AmountHero(props) {
    var state = HERO_COPY[props.state] ? props.state : "earned", copy = HERO_COPY[state];
    var value = props.display != null ? props.display : money(props.amount || 0, props.currency, props.locale);
    return h("section", { className: cx("co-hero", "co-hero-" + state, props.className), "aria-label": (props.eyebrow || copy.eyebrow) + " " + value },
      h("div", { className: "co-hero-eyebrow" }, props.eyebrow || copy.eyebrow),
      h("div", { className: "co-hero-amount" }, value),
      h("div", { className: "co-hero-sub" }, props.subtitle || copy.sub),
      props.children ? h("div", { className: "co-hero-slot" }, props.children) : null);
  }

  function Pill(props) {
    return h("button", { type: "button", className: cx("co-pill", props.glass && "co-pill-glass"), onClick: props.onClick },
      h("img", { src: props.icon || ASSET.history, alt: "" }), props.children || "History");
  }

  function InfoRow(props) {
    var dur = shortDuration(props.secondsLeft == null ? 13500 : props.secondsLeft);
    return h("div", { className: "co-info", role: "note" },
      h("div", { className: "co-info-tile", "aria-hidden": "true" }, h("img", { src: ASSET.tip, alt: "" })),
      h("p", { className: "co-info-text" }, props.children || [
        "Your ", h("img", { key: "i", className: "co-inline-icon", src: ASSET.star, alt: "stars" }),
        " turn into rewards in ", h("b", { key: "b" }, dur + "."), " The more stars, the higher the reward."]));
  }

  function Countdown(props) {
    var start = props.seconds == null ? 11643 : props.seconds;
    var st = React.useState(start), left = st[0], set = st[1];
    React.useEffect(function () { set(start); }, [start]);
    React.useEffect(function () {
      if (!props.live) return;
      var id = setInterval(function () { set(function (s) { return s > 0 ? s - 1 : 0; }); }, 1000);
      return function () { clearInterval(id); };
    }, [props.live]);
    var c = clock(left), size = props.size || "large";
    var digits = c.text.split("").map(function (ch, i) { return h("span", { key: i + ch, className: /\d/.test(ch) ? "co-digit" : "co-colon" }, ch); });
    var value = h("time", { className: "co-count-value", dateTime: "PT" + left + "S", "aria-label": c.spoken }, digits);
    if (size === "card") return h("div", { className: "co-count co-count-card", role: "timer" }, h("div", { className: "co-count-caption" }, props.label || "Your stars convert in"), value);
    return h("span", { className: cx("co-count", size === "small" && "co-count-sm"), role: "timer" }, value);
  }

  function HistoryList(props) {
    return h("div", { className: "co-list", role: "list" }, (props.items || []).map(function (r, i) {
      var status = r.status || "success";
      return h("div", { key: i, className: "co-list-row", role: "listitem" },
        h("div", { className: "co-list-main" }, h("span", { className: "co-list-title" }, r.date),
          h("span", { className: "co-list-meta is-" + status }, { success: "Paid", pending: "Pending", failed: "Failed" }[status])),
        h("span", { className: "co-list-amount" }, money(r.amount, r.currency || props.currency, props.locale)));
    }));
  }

  function StatTile(props) {
    return h("div", { className: "co-stat" },
      props.icon ? h("img", { src: props.icon === "star" ? ASSET.star : props.icon, alt: "" }) : null,
      h("div", null, h("div", { className: "co-stat-label" }, props.label), h("div", { className: "co-stat-value" }, props.value)));
  }

  var ICON_ALERT = h("svg", { viewBox: "0 0 20 20", fill: "none", "aria-hidden": "true" },
    h("circle", { cx: 10, cy: 10, r: 8.25, stroke: "currentColor", strokeWidth: 1.5 }),
    h("path", { d: "M10 5.5v5.5", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round" }),
    h("circle", { cx: 10, cy: 14, r: 1.1, fill: "currentColor" }));
  function InlineMessage(props) {
    var tone = props.tone || "danger";
    return h("div", { className: "co-msg co-msg-" + tone, role: tone === "danger" ? "alert" : "status" }, ICON_ALERT, h("span", null, props.children));
  }

  function tabIcon(name) {
    var p = { stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", fill: "none" };
    var parts = {
      home: [h("path", Object.assign({ key: 1, d: "M4 10.5 12 4l8 6.5V20h-5v-5h-6v5H4z" }, p))],
      cashout: [h("rect", Object.assign({ key: 1, x: 3, y: 6, width: 18, height: 12, rx: 2.5 }, p)), h("circle", Object.assign({ key: 2, cx: 12, cy: 12, r: 2.5 }, p))],
      history: [h("circle", Object.assign({ key: 1, cx: 12, cy: 12, r: 8.5 }, p)), h("path", Object.assign({ key: 2, d: "M12 7.5V12l3 2" }, p))],
      profile: [h("circle", Object.assign({ key: 1, cx: 12, cy: 8.5, r: 3.5 }, p)), h("path", Object.assign({ key: 2, d: "M5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5" }, p))]
    };
    return h("svg", { viewBox: "0 0 24 24", "aria-hidden": "true" }, parts[name]);
  }
  function TabBar(props) {
    var tabs = props.tabs || [{ id: "home", label: "Home" }, { id: "cashout", label: "Cash out" }, { id: "history", label: "History" }, { id: "profile", label: "Profile" }];
    var st = React.useState(props.selected || "home"), sel = st[0], set = st[1];
    React.useEffect(function () { if (props.selected) set(props.selected); }, [props.selected]);
    return h("nav", { className: "co-tabbar", role: "tablist" }, tabs.map(function (t) {
      return h("button", { key: t.id, type: "button", role: "tab", className: "co-tab", "aria-selected": sel === t.id ? "true" : "false", onClick: function () { set(t.id); if (props.onSelect) props.onSelect(t.id); } }, tabIcon(t.id), t.label);
    }));
  }

  function CashoutSheet(props) {
    var state = props.state || "earned", canCash = state === "earned";
    return h("div", { className: "co-sheet", role: "dialog", "aria-label": "Cash out" },
      h("div", { className: "co-grabber", "aria-hidden": "true" }),
      state === "pending" ? h(Countdown, { size: "card", seconds: props.seconds, live: props.live })
        : h(AmountHero, { state: state, amount: props.amount, currency: props.currency, locale: props.locale }, canCash ? h(Pill, { glass: true }) : null),
      state === "success" ? null : h(InfoRow, { secondsLeft: props.secondsLeft }),
      props.limitReached ? h(InlineMessage, null, "You've reached the maximum balance. Cash out to keep earning.") : null,
      h("div", { className: "co-sheet-actions" },
        h(Button, { fullWidth: true, loading: props.loading }, canCash ? "Cash out" : state === "success" ? "Done" : "Play games"),
        h(Button, { variant: "plain" }, canCash ? "Keep playing" : "Back to home")));
  }

  window.Cashout = Object.assign(window.Cashout || {}, {
    Button: Button, AmountHero: AmountHero, Pill: Pill, InfoRow: InfoRow, Countdown: Countdown,
    HistoryList: HistoryList, StatTile: StatTile, InlineMessage: InlineMessage, TabBar: TabBar, CashoutSheet: CashoutSheet,
    Copy: Copy, Demo: Demo, format: { money: money, clock: clock }, assets: ASSET
  });
})();

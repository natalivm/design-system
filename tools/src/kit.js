/* Shared by the three prototypes: autoplay, the tap marker, coin flights, counting, overlays and fitting the
   phone to the window. Source: tools/src/kit.js, copied into each prototype by tools/build.py. */
var KIT = (function () {
  var $ = function (id) { return document.getElementById(id); };
  var K = { runId: 0, playing: false };
  // Inside the website's frame, the prototype has no background of its own, so the page reads as one colour.
  if (window.self !== window.top) document.documentElement.style.setProperty("--page", "transparent");
  K.reduce = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  K.sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  K.scale = function () { var s = $("screen"); return s.getBoundingClientRect().width / s.offsetWidth; };
  K.local = function (el) {
    var sr = $("screen").getBoundingClientRect(), k = K.scale(), r = el.getBoundingClientRect();
    return { x: (r.left - sr.left) / k, y: (r.top - sr.top) / k, w: r.width / k, h: r.height / k };
  };

  /* ---------- Play / Pause ---------- */
  K.setPlaying = function (on) {
    K.playing = on;
    $("playBtn").setAttribute("aria-pressed", on ? "true" : "false");
    $("pauseBtn").setAttribute("aria-pressed", on ? "false" : "true");
    if (!on) { $("tap").classList.remove("show", "down"); $("ring").classList.remove("show"); }
  };
  K.stopPlay = function () { K.runId++; K.setPlaying(false); };

  // Scroll any scrolling area inside the phone so the control is visible.
  function reveal(el) {
    var scr = $("screen"), p = el.parentElement, k = K.scale();
    for (; p && p !== scr; p = p.parentElement) {
      if (!/(auto|scroll)/.test(getComputedStyle(p).overflowY) || p.scrollHeight <= p.clientHeight) continue;
      var r = el.getBoundingClientRect(), pr = p.getBoundingClientRect();
      if (r.top < pr.top) p.scrollTop -= (pr.top - r.top) / k + 16;
      else if (r.bottom > pr.bottom) p.scrollTop += (r.bottom - pr.bottom) / k + 16;
    }
  }
  // Put the tap marker on the control and the ring around it. Measured again before the press, so controls
  // that are still sliding in are ringed where they end up.
  function place(el) {
    var tap = $("tap"), ring = $("ring"), r = K.local(el), pad = 5, rad = parseFloat(getComputedStyle(el).borderTopLeftRadius) || 12;
    tap.style.left = (r.x + r.w / 2) + "px"; tap.style.top = (r.y + r.h / 2) + "px";
    ring.style.left = (r.x - pad) + "px"; ring.style.top = (r.y - pad) + "px";
    ring.style.width = (r.w + pad * 2) + "px"; ring.style.height = (r.h + pad * 2) + "px";
    ring.style.borderRadius = Math.min(rad + pad, (r.h + pad * 2) / 2) + "px";
  }
  K.tapOn = function (el, id) {
    if (!el || id !== K.runId) return Promise.resolve();
    var tap = $("tap"), ring = $("ring");
    reveal(el); place(el); tap.classList.add("show");
    setTimeout(function () { if (id === K.runId) { place(el); ring.classList.add("show"); } }, 350);
    return K.sleep(950).then(function () { if (id !== K.runId) return; place(el); tap.classList.add("down"); return K.sleep(220); })
      .then(function () { if (id !== K.runId) return; tap.classList.remove("down"); ring.classList.remove("show"); el.click(); return K.sleep(300); })
      .then(function () { if (id === K.runId) tap.classList.remove("show"); });
  };
  // next() returns the control to tap now, null to wait, or "done" to stop.
  K.autoplay = function (next) {
    var id = ++K.runId, idle = 0; K.setPlaying(true);
    (function step() {
      if (id !== K.runId) return;
      var t = next();
      if (t === "done" || idle > 80) { K.setPlaying(false); return; }
      if (!t) { idle++; K.sleep(300).then(step); return; }
      idle = 0; K.tapOn(t, id).then(function () { return K.sleep(900); }).then(step);
    })();
  };
  K.wire = function (start, reset) {
    $("playBtn").onclick = function () { if (!K.playing) start(); };
    $("pauseBtn").onclick = function () { if (K.playing) K.stopPlay(); };
    $("reset").onclick = reset;
    $("screen").addEventListener("pointerdown", function (e) { if (e.isTrusted) K.stopPlay(); }, true);
  };

  /* ---------- fit the phone to the window (also inside the site's iframe) ---------- */
  K.fit = function () {
    var availH = window.innerHeight - 48, availW = Math.min(window.innerWidth - 32, 417);
    var s = Math.max(0.25, Math.min(1, availW / 417, availH / 876));
    $("device").style.transform = "scale(" + s + ")";
    $("deviceWrap").style.width = (417 * s) + "px"; $("deviceWrap").style.height = (876 * s) + "px";
  };
  window.addEventListener("resize", K.fit);

  /* ---------- numbers and coins ---------- */
  // Animate a number into el. Stops as soon as alive() is false, so a reset can't be overwritten.
  K.countTo = function (el, from, to, ms, format, alive) {
    var t0 = null;
    function f(ts) {
      if (alive && !alive()) return;
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / ms);
      el.textContent = format(from + (to - from) * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(f);
    }
    requestAnimationFrame(f);
  };
  // Coins fly from one element to another; resolves after the last one lands.
  K.flyCoins = function (fromEl, toEl, n, src) {
    var a = K.local(fromEl), t = K.local(toEl), scr = $("screen");
    var sx = a.x + a.w / 2 - 15, sy = a.y + a.h / 2 - 15, tx = t.x + t.w / 2 - 15, ty = t.y + t.h / 2 - 15;
    for (var i = 0; i < n; i++) (function (i) {
      var c = document.createElement("img"); c.src = src; c.className = "fly"; c.alt = "";
      var ox = (Math.random() - .5) * 120, oy = (Math.random() - .5) * 70;
      c.style.left = sx + "px"; c.style.top = sy + "px"; scr.appendChild(c);
      var mx = (tx - sx) * 0.35 + ox * 1.6 - 60, my = (ty - sy) * 0.45 + oy;
      var an = c.animate([
        { transform: "translate(0,0) scale(.3) rotate(0deg)", opacity: 0 },
        { transform: "translate(" + ox + "px," + oy + "px) scale(1.15) rotate(120deg)", opacity: 1, offset: .22, easing: "cubic-bezier(.3,0,.4,1)" },
        { transform: "translate(" + mx + "px," + my + "px) scale(1) rotate(300deg)", opacity: 1, offset: .62, easing: "cubic-bezier(.5,0,.8,.6)" },
        { transform: "translate(" + (tx - sx) + "px," + (ty - sy) + "px) scale(.55) rotate(540deg)", opacity: 1 }
      ], { duration: K.reduce ? 1 : 900 + Math.random() * 250, delay: K.reduce ? 0 : i * 45, fill: "both" });
      an.onfinish = function () { c.remove(); toEl.classList.remove("bump"); void toEl.offsetWidth; toEl.classList.add("bump"); };
    })(i);
    return K.sleep(K.reduce ? 300 : 1000 + n * 45 + 450);
  };
  K.clearCoins = function () { Array.prototype.forEach.call(document.querySelectorAll(".fly"), function (c) { c.remove(); }); };

  /* ---------- overlays ---------- */
  // A closed overlay is inert: no tab stops, not read out, can't be pressed. An open one takes focus when
  // the person is using the prototype (not when it opens on its own in a page they are scrolling).
  K.overlays = function (ids, opts) {
    var noFocus = (opts && opts.noFocus) || [];
    ids.forEach(function (id) {
      var el = $(id); if (!el) return;
      function sync() {
        var open = el.classList.contains("on");
        el.inert = !open;
        if (el.getAttribute("role") === "dialog") { if (open) el.setAttribute("aria-modal", "true"); else el.removeAttribute("aria-modal"); }
        if (open && noFocus.indexOf(id) < 0 && document.hasFocus()) setTimeout(function () {
          if (!el.classList.contains("on") || el.contains(document.activeElement)) return;
          var f = el.querySelector("button:not([disabled]):not([hidden])"); if (f) f.focus({ preventScroll: true });
        }, 80);
      }
      new MutationObserver(sync).observe(el, { attributes: true, attributeFilter: ["class"] });
      sync();
    });
  };
  return K;
})();

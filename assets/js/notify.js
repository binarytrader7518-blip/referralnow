/*!
 * InfoNotify — reusable bottom-left informational notification card.
 * Shows rotating, factual messages only (no fake purchases, names or ratings).
 *
 * Usage:
 *   InfoNotify.init({
 *     messages: [{ title: "…", text: "…", href: "…" }],
 *     firstDelay: 5000, duration: 6000, intervalMin: 18000, intervalMax: 26000,
 *     linkLabel: "View offer", linkRel: "sponsored nofollow noopener"
 *   });
 * Pauses while a page modal is open (body.modal-open) and waits for
 * the "promomodal:closed" event when window.__promoPending is true.
 */
(function (global) {
  "use strict";

  var css = "" +
    ".inotify{position:fixed;left:20px;bottom:20px;z-index:60;width:340px;max-width:calc(100vw - 32px);" +
    "background:#fff;border:1px solid #e3e8f4;border-radius:16px;box-shadow:0 18px 44px rgba(14,23,48,.16),0 2px 6px rgba(14,23,48,.06);" +
    "padding:14px 40px 14px 14px;display:flex;gap:12px;align-items:flex-start;font-family:var(--font-body,system-ui,sans-serif);" +
    "opacity:0;transform:translateY(14px) scale(.98);pointer-events:none;transition:opacity .45s cubic-bezier(.2,.7,.2,1),transform .45s cubic-bezier(.2,.7,.2,1)}" +
    ".inotify.show{opacity:1;transform:none;pointer-events:auto}" +
    ".inotify-ic{flex:none;width:36px;height:36px;border-radius:50%;background:#e9f9ef;color:#16a34a;display:grid;place-items:center}" +
    ".inotify-ic svg{width:18px;height:18px}" +
    ".inotify-title{font-family:var(--font-head,system-ui,sans-serif);font-weight:700;color:#0e1730;font-size:.95rem;line-height:1.3;margin:1px 0 3px}" +
    ".inotify-text{font-size:.88rem;line-height:1.45;color:#4a5573;margin:0}" +
    ".inotify-link{display:inline-block;margin-top:6px;font-family:var(--font-head,system-ui,sans-serif);font-weight:700;font-size:.85rem;color:var(--blue,#1f5eff)}" +
    ".inotify-x{position:absolute;top:8px;right:8px;width:26px;height:26px;border:0;border-radius:50%;background:transparent;color:#8a93ad;cursor:pointer;display:grid;place-items:center;font-size:18px;line-height:1}" +
    ".inotify-x:hover{background:#f1f4fb;color:#0e1730}" +
    ".inotify-bar{position:absolute;left:14px;right:14px;bottom:0;height:3px;border-radius:3px;background:linear-gradient(90deg,var(--pink,#f032c8),var(--coral,#f2554b));transform-origin:left;transform:scaleX(0)}" +
    ".inotify.show .inotify-bar{animation:inotifyBar var(--inotify-dur,6s) linear forwards}" +
    "@keyframes inotifyBar{from{transform:scaleX(1)}to{transform:scaleX(0)}}" +
    "@media (max-width:560px){.inotify{left:12px;bottom:12px;width:auto;right:12px;max-width:none}}" +
    "@media (prefers-reduced-motion:reduce){.inotify{transition:opacity .2s linear;transform:none}.inotify.show .inotify-bar{animation:none}}";

  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7"/></svg>';

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  var InfoNotify = {
    init: function (opts) {
      var o = Object.assign({
        messages: [], firstDelay: 5000, duration: 6000, intervalMin: 18000, intervalMax: 26000,
        linkLabel: "View offer", linkRel: "sponsored nofollow noopener", storageKey: "inotify_dismissed"
      }, opts || {});
      if (!o.messages.length) return;
      try { if (sessionStorage.getItem(o.storageKey) === "1") return; } catch (e) {}

      var style = document.createElement("style");
      style.textContent = css;
      document.head.appendChild(style);

      var el = document.createElement("div");
      el.className = "inotify";
      el.setAttribute("role", "status");
      el.setAttribute("aria-live", "polite");
      el.style.setProperty("--inotify-dur", (o.duration / 1000) + "s");
      el.innerHTML = '<div class="inotify-ic">' + CHECK + '</div><div class="inotify-body"></div>' +
        '<button class="inotify-x" type="button" aria-label="Close notification">&times;</button><div class="inotify-bar"></div>';
      document.body.appendChild(el);

      var body = el.querySelector(".inotify-body");
      var idx = 0, hideT = null, nextT = null, stopped = false, visible = false;

      function modalOpen() { return document.body.classList.contains("modal-open"); }
      function rand() { return o.intervalMin + Math.random() * (o.intervalMax - o.intervalMin); }

      function render(m) {
        body.innerHTML = '<p class="inotify-title">' + esc(m.title) + '</p><p class="inotify-text">' + esc(m.text) + '</p>' +
          (m.href ? '<a class="inotify-link" href="' + esc(m.href) + '"' +
            (/^https?:/i.test(m.href) && m.href.indexOf(location.host) === -1 ? ' target="_blank" rel="' + esc(o.linkRel) + '"' : "") +
            '>' + esc(m.linkLabel || o.linkLabel) + ' &rarr;</a>' : "");
      }
      function hide() {
        clearTimeout(hideT);
        if (!visible) return;
        visible = false;
        el.classList.remove("show");
      }
      function schedule(ms) {
        clearTimeout(nextT);
        if (!stopped) nextT = setTimeout(show, ms);
      }
      function show() {
        if (stopped) return;
        if (modalOpen() || global.__promoPending) { schedule(4000); return; } // never overlap the modal
        if (visible) return; // never stack
        render(o.messages[idx % o.messages.length]);
        idx++;
        // restart progress bar animation
        var bar = el.querySelector(".inotify-bar"); bar.style.animation = "none"; void bar.offsetWidth; bar.style.animation = "";
        visible = true;
        el.classList.add("show");
        hideT = setTimeout(function () { hide(); schedule(rand()); }, o.duration);
      }

      el.querySelector(".inotify-x").addEventListener("click", function () {
        stopped = true; hide(); clearTimeout(nextT);
        try { sessionStorage.setItem(o.storageKey, "1"); } catch (e) {}
      });
      document.addEventListener("promomodal:opened", hide);
      el.addEventListener("mouseenter", function () { clearTimeout(hideT); });
      el.addEventListener("mouseleave", function () { if (visible) hideT = setTimeout(function () { hide(); schedule(rand()); }, 2500); });

      schedule(o.firstDelay);
      InfoNotify._debug = { show: show, hide: hide, el: el };
    }
  };
  global.InfoNotify = InfoNotify;
})(window);

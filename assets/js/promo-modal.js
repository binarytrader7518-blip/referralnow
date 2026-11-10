/*!
 * PromoModal — reusable centered promotional modal.
 * - Dark overlay, centered card, fade + scale entrance/exit
 * - Close button, overlay click, Escape; focus trap; background scroll lock
 * - Cooldown (default 24h) so it never re-interrupts a visitor
 * - Optional countdown ONLY when a real seller deadline is supplied; hides once passed
 *
 * PromoModal.init({
 *   delay: 6500, cooldownHours: 24, storageKey: "promo_seen",
 *   image: "…", imageAlt: "…", name: "…", headline: "…",
 *   priceHtml: "…", priceNote: "…", points: ["…"],
 *   ctaLabel: "…", ctaHref: "…", ctaRel: "sponsored nofollow noopener",
 *   deadlineISO: "2026-11-15T04:59:00Z", deadlineLabel: "…", note: "…"
 * });
 */
(function (global) {
  "use strict";

  var css = "" +
    ".pm-overlay{position:fixed;inset:0;z-index:100;background:rgba(9,14,32,.62);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);" +
    "display:flex;align-items:center;justify-content:center;padding:16px;opacity:0;transition:opacity .35s ease;overflow-y:auto}" +
    ".pm-overlay.show{opacity:1}" +
    ".pm-card{position:relative;width:100%;max-width:440px;margin:auto;background:#fff;border-radius:24px;box-shadow:0 40px 90px rgba(0,0,0,.35);" +
    "padding:30px 28px 24px;text-align:center;transform:translateY(12px) scale(.94);opacity:0;transition:transform .45s cubic-bezier(.2,.8,.2,1.1),opacity .35s ease;font-family:var(--font-body,system-ui,sans-serif)}" +
    ".pm-overlay.show .pm-card{transform:none;opacity:1}" +
    ".pm-x{position:absolute;top:12px;right:12px;width:38px;height:38px;border-radius:50%;border:0;background:#f1f4fb;color:#0e1730;cursor:pointer;display:grid;place-items:center;font-size:22px;line-height:1}" +
    ".pm-x:hover{background:#e3e8f4}" +
    ".pm-img{display:block;width:100%;max-width:300px;margin:4px auto 14px;filter:drop-shadow(0 16px 20px rgba(14,23,48,.2))}" +
    ".pm-name{display:inline-block;font-family:var(--font-head,system-ui,sans-serif);font-weight:700;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--blue,#1f5eff);background:var(--blue-50,#eef3ff);padding:5px 12px;border-radius:999px;margin-bottom:10px}" +
    ".pm-h{font-family:var(--font-head,system-ui,sans-serif);font-weight:800;color:#0e1730;font-size:1.5rem;line-height:1.2;letter-spacing:-.02em;margin:0 0 12px}" +
    ".pm-price{font-family:var(--font-head,system-ui,sans-serif);font-weight:800;color:#0e1730;font-size:2.3rem;line-height:1;letter-spacing:-.03em;margin:6px 0 6px}" +
    ".pm-price small{font-size:1rem;color:#6b7591;font-weight:700;letter-spacing:0}" +
    ".pm-pnote{color:#5a6482;font-size:.92rem;margin:0 0 12px}" +
    ".pm-points{list-style:none;padding:0;margin:0 auto 18px;display:grid;gap:6px;text-align:left;max-width:320px;font-size:.93rem;color:#3a4560}" +
    ".pm-points li{display:flex;gap:8px}.pm-points li::before{content:'';flex:none;width:18px;height:18px;margin-top:2px;border-radius:50%;background:#e9f9ef url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2316a34a' stroke-width='3.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12.5l4.2 4.2L19 7'/%3E%3C/svg%3E\") center/11px no-repeat}" +
    ".pm-cd{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:8px;margin:0 0 16px;font-size:.85rem;color:#0e1730}" +
    ".pm-cd[hidden]{display:none}.pm-cd b{font-weight:600}" +
    ".pm-cd .t{display:inline-flex;gap:5px}.pm-cd .t span{background:#0e1730;color:#fff;border-radius:7px;padding:3px 7px;font-family:var(--font-head,system-ui,sans-serif);font-weight:700;font-size:.82rem;min-width:36px}" +
    ".pm-cta{display:flex;width:100%;align-items:center;justify-content:center;gap:8px;padding:16px 22px;border-radius:999px;color:#fff !important;text-decoration:none !important;" +
    "font-family:var(--font-head,system-ui,sans-serif);font-weight:800;font-size:1.08rem;background:linear-gradient(90deg,var(--pink,#f032c8),var(--coral,#f2554b));box-shadow:0 12px 26px rgba(240,50,140,.32);transition:transform .25s,box-shadow .25s}" +
    ".pm-cta:hover{transform:translateY(-2px);box-shadow:0 16px 32px rgba(240,50,140,.4)}.pm-cta:active{transform:scale(.98)}" +
    ".pm-note{font-size:.78rem;color:#7b84a0;margin:10px 0 0}" +
    ".pm-later{background:none;border:0;color:#6b7591;font-size:.88rem;margin-top:8px;cursor:pointer;text-decoration:underline}" +
    "body.modal-open{overflow:hidden}" +
    ".pm-img{height:auto}" +
    "@media (max-width:480px){.pm-card{padding:22px 18px 16px;border-radius:20px}.pm-h{font-size:1.25rem;margin-bottom:8px}.pm-price{font-size:2rem}.pm-img{max-width:200px;margin-bottom:8px}.pm-points{display:none}.pm-pnote{font-size:.88rem;margin-bottom:10px}.pm-cd{margin-bottom:12px}.pm-later{margin-top:4px}}" +
    "@media (max-height:760px){.pm-img{max-width:180px;margin-bottom:8px}.pm-points{display:none}}" +
    "@media (prefers-reduced-motion:reduce){.pm-overlay,.pm-card{transition:opacity .15s linear}.pm-card{transform:none}}";

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function pad(n) { return (n < 10 ? "0" : "") + n; }

  var PromoModal = {
    init: function (opts) {
      var o = Object.assign({
        delay: 6500, cooldownHours: 24, storageKey: "promo_seen",
        ctaRel: "sponsored nofollow noopener", points: [], force: false
      }, opts || {});

      var forced = o.force || /[?&]showpromo=1/.test(location.search);
      var seen = 0;
      try { seen = parseInt(localStorage.getItem(o.storageKey) || "0", 10) || 0; } catch (e) {}
      if (!forced && seen && Date.now() - seen < o.cooldownHours * 3600 * 1000) return;

      global.__promoPending = true;
      var style = document.createElement("style");
      style.textContent = css;
      document.head.appendChild(style);

      var lastFocus = null, overlay = null, cdTimer = null;

      function markSeen() { try { localStorage.setItem(o.storageKey, String(Date.now())); } catch (e) {} }

      function build() {
        overlay = document.createElement("div");
        overlay.className = "pm-overlay";
        overlay.innerHTML =
          '<div class="pm-card" role="dialog" aria-modal="true" aria-labelledby="pm-title" aria-describedby="pm-desc">' +
          '<button type="button" class="pm-x" aria-label="Close">&times;</button>' +
          (o.image ? '<img class="pm-img" src="' + esc(o.image) + '" alt="' + esc(o.imageAlt) + '" width="690" height="528" decoding="async" referrerpolicy="no-referrer">' : "") +
          '<span class="pm-name">' + esc(o.name) + '</span>' +
          '<h2 class="pm-h" id="pm-title">' + esc(o.headline) + '</h2>' +
          (o.priceHtml ? '<div class="pm-price">' + o.priceHtml + '</div>' : "") +
          (o.priceNote ? '<p class="pm-pnote" id="pm-desc">' + o.priceNote + '</p>' : '<p id="pm-desc" hidden></p>') +
          (o.points.length ? '<ul class="pm-points">' + o.points.map(function (p) { return "<li>" + esc(p) + "</li>"; }).join("") + "</ul>" : "") +
          (o.deadlineISO ? '<div class="pm-cd" hidden><b>' + esc(o.deadlineLabel || "Ends in") + '</b><span class="t"><span data-d>0d</span><span data-h>00h</span><span data-m>00m</span><span data-s>00s</span></span></div>' : "") +
          '<a class="pm-cta" href="' + esc(o.ctaHref) + '" target="_blank" rel="' + esc(o.ctaRel) + '">' + esc(o.ctaLabel) + ' &rarr;</a>' +
          (o.note ? '<p class="pm-note">' + esc(o.note) + "</p>" : "") +
          '<button type="button" class="pm-later">No thanks</button>' +
          "</div>";
        document.body.appendChild(overlay);

        overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
        overlay.querySelector(".pm-x").addEventListener("click", close);
        overlay.querySelector(".pm-later").addEventListener("click", close);
        overlay.querySelector(".pm-cta").addEventListener("click", function () { markSeen(); });
        overlay.addEventListener("keydown", trap);
        if (o.deadlineISO) startCountdown();
      }

      function startCountdown() {
        var end = Date.parse(o.deadlineISO);
        var box = overlay.querySelector(".pm-cd");
        if (isNaN(end)) return;
        function tick() {
          var diff = end - Date.now();
          if (diff <= 0) { box.hidden = true; clearInterval(cdTimer); return; }
          box.hidden = false;
          var s = Math.floor(diff / 1000);
          box.querySelector("[data-d]").textContent = Math.floor(s / 86400) + "d";
          box.querySelector("[data-h]").textContent = pad(Math.floor(s % 86400 / 3600)) + "h";
          box.querySelector("[data-m]").textContent = pad(Math.floor(s % 3600 / 60)) + "m";
          box.querySelector("[data-s]").textContent = pad(s % 60) + "s";
        }
        tick();
        cdTimer = setInterval(tick, 1000);
      }

      function focusables() {
        return [].slice.call(overlay.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])'));
      }
      function trap(e) {
        if (e.key === "Escape") { e.preventDefault(); close(); return; }
        if (e.key !== "Tab") return;
        var f = focusables(), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
      function onDocKey(e) { if (e.key === "Escape" && overlay && overlay.classList.contains("show")) close(); }

      function open() {
        if (document.querySelector(".pm-overlay")) return;
        build();
        lastFocus = document.activeElement;
        document.body.classList.add("modal-open");
        document.addEventListener("keydown", onDocKey);
        requestAnimationFrame(function () { requestAnimationFrame(function () { overlay.classList.add("show"); }); });
        setTimeout(function () { var c = overlay.querySelector(".pm-cta"); if (c) c.focus({ preventScroll: true }); }, 60);
        markSeen();
        document.dispatchEvent(new CustomEvent("promomodal:opened"));
      }
      function close() {
        if (!overlay) return;
        overlay.classList.remove("show");
        document.removeEventListener("keydown", onDocKey);
        clearInterval(cdTimer);
        var ov = overlay; overlay = null;
        setTimeout(function () { if (ov.parentNode) ov.parentNode.removeChild(ov); }, 380);
        document.body.classList.remove("modal-open");
        if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
        global.__promoPending = false;
        document.dispatchEvent(new CustomEvent("promomodal:closed"));
      }

      function arm() { setTimeout(open, o.delay); }
      if (document.readyState === "complete") arm();
      else global.addEventListener("load", arm);

      PromoModal._debug = { open: open, close: close };
    }
  };
  global.PromoModal = PromoModal;
})(window);

/* Referral Now Bundle — site behaviour */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");

  var AFF = "https://jvz7.com/c/1834263/456459/";
  var IMG = "https://referralnow.co/partners/assets/img/s17/mon-bundle.feb69d8b.png";
  var DEADLINE = "2026-11-15T04:59:00Z"; // published on the seller's page (Date.UTC(2026,10,15,4,59))
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Mobile navigation */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); toggle.focus(); }
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1100) { nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); } });
  }

  /* FAQ accordion */
  document.querySelectorAll(".faq-q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq-item");
      var open = !item.classList.contains("open");
      item.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  /* Scroll reveal */
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add("in"); }); }

  /* Hero product: gentle pointer perspective */
  var stage = document.querySelector("[data-tilt]");
  if (stage && !reduce && window.matchMedia("(hover: hover)").matches) {
    var inner = stage.querySelector(".product-tilt");
    stage.addEventListener("pointermove", function (e) {
      var r = stage.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      inner.style.transform = "rotateY(" + (x * 10).toFixed(2) + "deg) rotateX(" + (-y * 8).toFixed(2) + "deg)";
    });
    stage.addEventListener("pointerleave", function () { inner.style.transform = ""; });
  }

  /* On-page countdown (seller deadline only; hides itself once passed) */
  document.querySelectorAll("[data-deadline]").forEach(function (box) {
    var end = Date.parse(box.getAttribute("data-deadline"));
    if (isNaN(end)) return;
    function p(n) { return (n < 10 ? "0" : "") + n; }
    function tick() {
      var d = end - Date.now();
      if (d <= 0) { box.hidden = true; clearInterval(t); return; }
      box.hidden = false;
      var s = Math.floor(d / 1000);
      box.querySelector("[data-d]").textContent = Math.floor(s / 86400) + "d";
      box.querySelector("[data-h]").textContent = p(Math.floor(s % 86400 / 3600)) + "h";
      box.querySelector("[data-m]").textContent = p(Math.floor(s % 3600 / 60)) + "m";
      box.querySelector("[data-s]").textContent = p(s % 60) + "s";
    }
    var t = setInterval(tick, 1000); tick();
  });

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Centered promotional modal (verified seller pricing) */
  if (window.PromoModal) {
    PromoModal.init({
      delay: 6500,
      cooldownHours: 24,
      storageKey: "rnb_promo_seen",
      image: IMG,
      imageAlt: "Referral Now Bundle shown on screen (seller's product image)",
      name: "Referral Now Bundle",
      headline: "All five ReferralNow plans on one login",
      priceHtml: "$397<small> / year</small>",
      priceNote: "With seller code <b>FRIEND100</b> (list price $497/year). Or split it into 2 payments of $199.",
      points: ["Premium, Pro, Unlimited, Agency and Reseller", "All 16 launch bonuses", "14-day money-back guarantee from the seller"],
      deadlineISO: DEADLINE,
      deadlineLabel: "Seller's launch price ends in",
      ctaLabel: "View the Bundle Offer",
      ctaHref: AFF,
      note: "Affiliate link: we may be paid a commission if you buy."
    });
  }

  /* Bottom-left informational notifications (no fake purchase activity) */
  if (window.InfoNotify) {
    InfoNotify.init({
      firstDelay: 5000, duration: 6000, intervalMin: 18000, intervalMax: 26000,
      storageKey: "rnb_notify_off",
      messages: [
        { title: "Five plans, one account", text: "The Referral Now Bundle includes Premium, Pro, Unlimited, Agency and Reseller.", href: AFF, linkLabel: "Compare the offer" },
        { title: "Seller guarantee", text: "The seller offers a 14-day money-back guarantee on the Bundle.", href: "/reviews.html#guarantee", linkLabel: "Read the terms" },
        { title: "Two ways to pay", text: "$397/year with code FRIEND100, or 2 payments of $199.", href: AFF, linkLabel: "See both options" },
        { title: "No app for your customers", text: "Advocates and friends use links and codes on their phones, no app or password needed.", href: "/how-it-works.html", linkLabel: "How it works" }
      ]
    });
  }
})();

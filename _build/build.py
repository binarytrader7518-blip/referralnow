#!/usr/bin/env python3
"""Static site generator for referralnow.vercel.app.

Run:  python3 _build/build.py
Writes every page, sitemap.xml and robots.txt into the project root.
Shared header/footer/head live here so all pages stay consistent.
"""
import os, json, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://referralnow.vercel.app"
BRAND = "Referral Now Bundle"
AFF = "https://jvz7.com/c/1834263/456459/"
REL = 'target="_blank" rel="sponsored nofollow noopener"'
LASTMOD = "2026-11-10"           # date this content was written and verified
DEADLINE = "2026-11-15T04:59:00Z"  # seller-published launch-price deadline
AFFNOTE = "Affiliate link: we may be paid a commission if you buy."

IMGBASE = "https://referralnow.co/partners/assets/img/"
IMG = {  # seller's original product images, used unaltered: (path, w, h)
    "bundle": ("s17/mon-bundle.feb69d8b.png", 690, 528),
    "premium": ("s17/mon-premium.d99f6fbf.webp", 596, 398),
    "unlimited": ("s17/mon-unlimited.ae77feea.webp", 594, 408),
    "agency": ("s17/mon-agency.2c6f1abe.webp", 592, 392),
    "dashboard": ("s08/dashboard.f9498f47.webp", 1448, 1052),
    "recruiter": ("s09/recruiter.7253103b.webp", 742, 706),
    "nudge": ("s09/nudge.c68030ba.webp", 502, 588),
    "verifier": ("s09/verifier.4b7c43c4.webp", 504, 588),
    "fraud": ("s09/fraud.2555ebfc.webp", 502, 588),
    "payout": ("s09/payout.26e6c222.webp", 502, 588),
    "report": ("s09/report.c6f5cc10.webp", 632, 536),
    "step1": ("s10/step1-analyze.a0b80c92.webp", 1062, 580),
    "step2": ("s10/step2-builder.9704d8e2.webp", 874, 516),
    "step3": ("s10/step3-agents.c749a8ee.webp", 880, 920),
    "step4": ("s10/step4-report.d906d2e7.webp", 1000, 732),
    "rewards": ("s11/f2-reward-types.153b8dbe.webp", 1022, 1174),
    "instore": ("s11/f7-in-store.e23e3860.webp", 1022, 812),
    "online": ("s11/f8-online.c6593210.webp", 1022, 952),
    "agencyconsole": ("s11/f10-agency-console.e089340a.webp", 1022, 1200),
    "advocates": ("s11/f9-advocates.3f563a4a.webp", 1022, 800),
}

LOCAL_DIR = os.path.join(ROOT, "assets", "img", "product")

def img_src(key, here=""):
    """Use a local copy if _build/fetch-images.sh has been run, else the seller's original URL."""
    p = IMG[key][0]
    name = p.split("/")[-1]
    if os.path.exists(os.path.join(LOCAL_DIR, name)):
        return rel("assets/img/product/" + name, here) if here else "/assets/img/product/" + name
    return IMGBASE + p

def img(key, alt, cls="", eager=False):
    p, w, h = IMG[key]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{img_src(key)}" alt="{html.escape(alt)}" width="{w}" height="{h}" {load} decoding="async" referrerpolicy="no-referrer">'

# ---------------------------------------------------------------- icons
def ic(name):
    P = {
        "check": '<path d="M5 12.5l4.2 4.2L19 7"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "play": '<path d="M8 5v14l11-7z"/>',
        "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        "card": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h4"/>',
        "store": '<path d="M4 9l1.5-5h13L20 9"/><path d="M4 9h16v2a3 3 0 01-6 0 3 3 0 01-4 0 3 3 0 01-6 0z"/><path d="M5 13v7h14v-7"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
        "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M3 4h2l2.5 11h11L21 8H7"/>',
        "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M3 13h18"/>',
        "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 010 6.8M18 14.7c1.9.7 3.1 2.5 3.5 5.3"/>',
        "link": '<path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/>',
        "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v8h14v-8M12 8v12M12 8c-1.5-3-5-3.5-5-1s3 1 5 1zm0 0c1.5-3 5-3.5 5-1s-3 1-5 1z"/>',
        "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        "bot": '<rect x="4" y="8" width="16" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 17h6"/>',
        "bell": '<path d="M6 16V11a6 6 0 0112 0v5l2 2H4z"/><path d="M10 20a2 2 0 004 0"/>',
        "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "qr": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM20 14v1M14 20h1M18 18h3v3"/>',
        "repeat": '<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 013-3h15M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 01-3 3H3"/>',
        "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
        "book": '<path d="M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2z"/><path d="M4 21V5M9 7h6"/>',
        "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
        "phone": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
        "brush": '<path d="M19 3l-9 9M14 4l6 6"/><path d="M9 13c-3 0-4 2-4 4s-1 3-2 4c4 0 8-1 8-5z"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "plus": '<path d="M12 5v14M5 12h14"/>',
        "scale": '<path d="M12 3v18M5 21h14M6 7h12M6 7l-3 7a3 3 0 006 0zM18 7l-3 7a3 3 0 006 0z"/>',
    }[name]
    fill = ' fill="currentColor" stroke="none"' if name == "play" else ' fill="none" stroke="currentColor"'
    return f'<svg viewBox="0 0 24 24"{fill} stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P}</svg>'

CHECK = f'<span class="check">{ic("check")}</span>'

def checklist(items, cls="check-list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{CHECK}<span>{i}</span></li>" for i in items) + "</ul>"

def cta(label="Get the Bundle", cls="btn btn-cta", note=True, big=False):
    b = f'<a class="{cls}{" btn-lg" if big else ""}" href="{AFF}" {REL}>{label} {ic("arrow")}</a>'
    return b

def affnote():
    return f'<p class="aff-note">{AFFNOTE}</p>'

# ---------------------------------------------------------------- navigation
NAV = [
    ("What Is It", "product-overview.html"),
    ("How It Works", "how-it-works.html"),
    ("Benefits", "benefits.html"),
    ("Focus Areas", "focus-areas/index.html"),
    ("Reviews", "reviews.html"),
    ("Blog", "blog/index.html"),
    ("FAQ", "faq.html"),
]
LEGAL = [
    ("Affiliate Disclosure", "affiliate-disclosure.html"),
    ("Privacy Policy", "privacy-policy.html"),
    ("Terms and Conditions", "terms.html"),
    ("Earnings Disclaimer", "earnings-disclaimer.html"),
    ("Software Disclaimer", "software-disclaimer.html"),
]

def rel(path, here):
    """relative URL from page `here` to site path `path`."""
    depth = here.count("/")
    pre = "../" * depth
    if path == "":
        return pre or "./"
    return pre + path

def canon(path):
    if path == "index.html":
        return DOMAIN + "/"
    if path.endswith("/index.html"):
        return DOMAIN + "/" + path[: -len("index.html")]
    return DOMAIN + "/" + path

CUR = ' aria-current="page"'

def header(here, section):
    items = "".join(
        f'<li><a href="{rel(u, here)}"{CUR if section == u else ""}>{t}</a></li>' for t, u in NAV
    )
    return f'''<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="{rel("", here)}" aria-label="{BRAND} home"><span class="logo-mark" aria-hidden="true">R</span><span class="logo-text">{BRAND}</span></a>
    <nav class="main-nav" id="main-nav" aria-label="Main"><ul>{items}</ul></nav>
    <div class="header-actions">
      <a class="btn btn-cta header-cta" href="{AFF}" {REL}>Order Now</a>
      <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu">{ic("menu")}</button>
    </div>
  </div>
</header>'''

def footer(here):
    nav = "".join(f'<li><a href="{rel(u, here)}">{t}</a></li>' for t, u in NAV)
    learn = "".join(f'<li><a href="{rel(u, here)}">{t}</a></li>' for t, u in [
        ("Local Businesses", "focus-areas/local-businesses.html"),
        ("Online Stores & Funnels", "focus-areas/online-stores-and-funnels.html"),
        ("Referral Agency Services", "focus-areas/referral-agency.html"),
        ("Reselling Accounts", "focus-areas/reselling-accounts.html"),
        ("Pricing & Plans", "index.html#pricing"),
    ])
    legal = "".join(f'<li><a href="{rel(u, here)}">{t}</a></li>' for t, u in LEGAL)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="logo" href="{rel("", here)}"><span class="logo-mark" aria-hidden="true">R</span><span class="logo-text">{BRAND}</span></a>
        <p>Plain-English information about the {BRAND}: all five ReferralNow plans for running self-running referral programs in your own businesses, for clients, and as resold accounts.</p>
        <a class="btn btn-cta" href="{AFF}" {REL}>Order Now</a>
      </div>
      <div><h4>Explore</h4><ul>{nav}</ul></div>
      <div><h4>Focus Areas</h4><ul>{learn}</ul></div>
      <div><h4>Legal</h4><ul>{legal}</ul></div>
    </div>
    <div class="footer-bottom">
      <p>This is an independent information site. The {BRAND} is created and sold by its vendor, with JVZoo acting as the retailer. Purchase buttons are affiliate links; see our <a href="{rel("affiliate-disclosure.html", here)}">Affiliate Disclosure</a>.</p>
      <p>No software can guarantee referrals, customers, sales or income. Any client fees mentioned are the seller's example prices, not typical results. Shopify, WooCommerce, BigCommerce, Wix, Squarespace, Stripe, Twilio and JVZoo are trademarks of their respective owners.</p>
      <p>&copy; <span data-year>2026</span> {BRAND} information site.</p>
    </div>
  </div>
</footer>'''

def page(path, title, desc, body, section="", schema=None, og_image=None):
    depth_pre = rel("", path) if path.count("/") else ""
    css = rel("assets/css/style.css", path)
    js = [rel("assets/js/notify.js", path), rel("assets/js/promo-modal.js", path), rel("assets/js/main.js", path)]
    og = og_image or IMGBASE + IMG["bundle"][0]
    ld = ""
    for s in (schema or []):
        ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    doc = f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon(path)}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#1f5eff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon(path)}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel("assets/img/favicon.svg", path)}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://referralnow.co">
<link href="https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600&family=Urbanist:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
{ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(path, section)}
<main id="main">
{body}
</main>
{footer(path)}
<script src="{js[0]}" defer></script>
<script src="{js[1]}" defer></script>
<script src="{js[2]}" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES.append(path)

PAGES = []

def section_head(eyebrow, h, lead=None, tag="h2"):
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="section-head reveal"><span class="eyebrow">{eyebrow}</span><{tag}>{h}</{tag}>{l}</div>'

def crumbs(here, items):
    parts = [f'<a href="{rel("", here)}">Home</a>']
    for t, u in items:
        parts.append(f'<a href="{rel(u, here)}">{t}</a>' if u else f'<span aria-current="page" style="margin:0">{t}</span>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"

def crumb_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def page_hero(here, crumb_items, eyebrow, h1, lead, visual, buttons=True):
    btns = f'<div class="btn-row">{cta("Get the Bundle")}<a class="btn btn-ghost" href="{rel("index.html#pricing", here)}">See pricing</a></div>{affnote()}' if buttons else ""
    return f'''<section class="page-hero"><div class="container page-hero-grid">
  <div class="reveal">{crumbs(here, crumb_items)}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p>{btns}</div>
  <div class="reveal">{visual}</div>
</div></section>'''

def stage(key="bundle", alt="Referral Now Bundle shown on screen (seller's original product image)", eager=True):
    return f'''<div class="product-stage" data-tilt><div class="product-glow"></div>
  <div class="product-tilt"><div class="product-float">{img(key, alt, "product-img", eager)}</div></div>
  <div class="product-shadow"></div></div>'''

def frame(key, alt):
    return f'<div class="media-frame">{img(key, alt)}</div>'

def faq_html(items):
    out = []
    for i, (q, a) in enumerate(items):
        out.append(f'''<div class="faq-item"><button class="faq-q" type="button" aria-expanded="false" aria-controls="fa{i}" id="fq{i}">{q}<span class="pm">{ic("plus")}</span></button>
<div class="faq-a" id="fa{i}" role="region" aria-labelledby="fq{i}"><div><div class="inner">{a}</div></div></div></div>''')
    return '<div class="faq reveal">' + "".join(out) + "</div>"

def faq_schema(items):
    import re
    def strip(s): return re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}

def deadline_box():
    return f'''<div class="center"><div class="deadline" data-deadline="{DEADLINE}" hidden>
  <span>The seller's launch price is listed until 15 Nov 2026</span>
  <span class="cd" aria-hidden="true"><span data-d>0d</span><span data-h>00h</span><span data-m>00m</span><span data-s>00s</span></span>
</div></div>'''

def pricing_cards(here):
    return f'''{deadline_box()}
<div class="pricing">
  <div class="price-card featured reveal">
    <span class="badge">Lowest yearly price</span>
    <h3>Yearly Plan</h3>
    <p class="sub">All five plans and all 16 launch bonuses</p>
    {img("bundle", "Referral Now Bundle on screen (seller's original image)")}
    <div class="price-amount">$397<small> / year</small></div>
    <p class="price-was">List price <s>$497/year</s> &minus; $100 with code <span class="code-pill">FRIEND100</span></p>
    <ul>
      <li>{CHECK}<span>Premium, Pro, Unlimited, Agency and Reseller on one login</span></li>
      <li>{CHECK}<span>Renews yearly until you cancel; the code applies each year, per the seller</span></li>
      <li>{CHECK}<span>14-day money-back guarantee from the seller</span></li>
    </ul>
    {cta("Get the Yearly Plan", "btn btn-cta btn-block")}
    <p class="price-foot">Enter the code at the seller's checkout.</p>
  </div>
  <div class="price-card reveal">
    <span class="badge" style="background:var(--navy)">Split payment</span>
    <h3>2-Payment Option</h3>
    <p class="sub">The same Bundle, paid in two parts</p>
    {img("bundle", "Referral Now Bundle on screen (seller's original image)")}
    <div class="price-amount">$199<small> &times; 2</small></div>
    <p class="price-was">$398 in total &middot; no code needed</p>
    <ul>
      <li>{CHECK}<span>Same five plans and 16 launch bonuses</span></li>
      <li>{CHECK}<span>Login arrives by email right after purchase</span></li>
      <li>{CHECK}<span>14-day money-back guarantee from the seller</span></li>
    </ul>
    {cta("Choose 2 Payments", "btn btn-ghost btn-block")}
    <p class="price-foot">Pick "2 payments of $199" on the seller's page.</p>
  </div>
</div>
<p class="aff-note center" style="margin-top:22px">{AFFNOTE} Prices verified on the seller's page on 10 Nov 2026.</p>'''

def guarantee_block(here):
    return f'''<div class="guarantee reveal" id="guarantee">
  <div class="seal" aria-hidden="true"><div><b>14</b><span>Day money-back</span></div></div>
  <div>
    <span class="eyebrow">Seller guarantee</span>
    <h2>Try every plan for 14 days</h2>
    <p>The seller offers a 14-day money-back guarantee on the Bundle. If it isn't right for you, the seller asks you to email their support team at <b>support@referralnow.online</b> within that window for a full refund. That address belongs to the seller, not to this site.</p>
    <p class="small muted">Refunds are handled by the seller and JVZoo under their own <a href="https://referralnow.co/bundle_split/" target="_blank" rel="nofollow noopener">refund policy</a>. Check it before you buy.</p>
  </div>
</div>'''

def final_cta(here, h="Put word of mouth on autopilot", text=None):
    text = text or f"One purchase gives you every ReferralNow plan, every upgrade and all 16 launch bonuses on a single account."
    return f'''<section class="section"><div class="container"><div class="cta-band reveal">
  <div>
    <span class="eyebrow">{BRAND}</span>
    <h2>{h}</h2>
    <p>{text}</p>
    <ul><li>{CHECK}<span>$397/year with code FRIEND100, or 2 payments of $199</span></li><li>{CHECK}<span>Five plans and 16 bonuses on one login</span></li><li>{CHECK}<span>14-day money-back guarantee from the seller</span></li></ul>
    <div class="btn-row">{cta("Order Now", big=True)}</div>
    {affnote()}
  </div>
  <div>{stage(eager=False)}</div>
</div></div></section>'''

PLANS = [
    ("Premium", "$49", "The complete referral loop for a single business: guided setup, AI drafting from one sentence, a five-step builder with live preview, advocate links and codes, till confirmations, fraud scoring, print kit, website widget and store connections."),
    ("Pro", "$67/yr", "Four businesses on one account; cash, gift-card and commission rewards with bank payouts through Stripe; monthly reports, the Advocate Finder, win-back messages and all 37 trade packs. Cash rewards always need a person's approval."),
    ("Unlimited", "$297/yr", "No caps on businesses you own or run, live campaigns, advocates or AI drafts, plus 20 tills so every counter in every location can confirm sales."),
    ("Agency", "$147/yr", "An HQ for client work: unlimited client workspaces, a team of 10 with role-based access, your agency's name and colour on client-facing pages and reports, a reports centre and a margins screen."),
    ("Reseller", "$497/yr", "A reseller console with up to 50 customer accounts (each the full front-end plan), accounts created from a name and email or automatically from your own JVZoo product, your support email inside each account, and a sales kit."),
]

def plan_table():
    rows = "".join(f'<tr><th>{n}</th><td>{d}</td><td class="price">{p}</td></tr>' for n, p, d in PLANS)
    return f'''<div class="table-wrap reveal"><table class="spec">
<thead><tr><th>Plan</th><td><b>What it adds</b></td><td class="price">Sold alone</td></tr></thead>
<tbody>{rows}<tr><th>Bought one by one</th><td>Seller's stated total for all five plans</td><td class="price">$1,057</td></tr>
<tr><th>In the Bundle</th><td>All five, plus all 16 launch bonuses</td><td class="price">$397/yr with FRIEND100</td></tr></tbody></table></div>'''

BONUSES = [
    ("Premium", "Referral Ask Swipe Vault: 60 ready-to-send messages across 20 trades"),
    ("Premium", "Counter-To-Checkout Print Templates: posters, table tents, receipt slips and cards"),
    ("Premium", "Reward Sizing Calculator: a suggested reward plus a safe budget ceiling"),
    ("Premium", "30-Day Referral Launch Playbook: a day-by-day first-month plan"),
    ("Pro", "Commission Rate Planner: spreadsheet and guide"),
    ("Pro", "Multi-Business Rollout Kit: playbook and checklists"),
    ("Pro", "VIP Advocate Blueprint: tiers and 12 scripts"),
    ("Pro", "Referral Report Decoder: guide and worksheet"),
    ("Unlimited", "Big List Launch Playbook: checklist and 6 scripts"),
    ("Unlimited", "52-Week Campaign Calendar: spreadsheet calendar"),
    ("Unlimited", "Till Team Training Kit: briefing and counter cards"),
    ("Unlimited", "Multi-Business Scorecard: spreadsheet and guide"),
    ("Agency", "Sign Your First Referral Clients: agency training playbook"),
    ("Agency", "Client Proposal & Report Kit: templates and scripts"),
    ("Reseller", "The First 10 Customers Sales Playbook: 14-day plan and scripts"),
    ("Reseller", "Reseller Pricing & Packaging Toolkit"),
]

HOME_FAQ = [
    ("What exactly is the Referral Now Bundle?", "It's the all-in-one package of ReferralNow, an AI-assisted referral marketing web app sold through JVZoo. The Bundle puts all five plans (Premium, Pro, Unlimited, Agency and Reseller) and all 16 launch bonuses on one account and one login. See the <a href=\"product-overview.html\">full overview</a>."),
    ("How much does it cost?", "On the seller's page the Bundle is $497 a year, renewing yearly until you cancel. Seller code FRIEND100 takes $100 off each year, making it $397 a year. There is also a split option of 2 payments of $199. Always confirm your total at checkout."),
    ("Do I need to buy the front-end product first?", "No. According to the seller, the Bundle creates your account on its own and your login is emailed as soon as you buy."),
    ("Do my customers need to download an app?", "No. Advocates and their friends use personal links and codes on their phones, with no app, account or password."),
    ("Are there any ongoing costs besides the Bundle?", "The seller notes that text messages are sent from each business's own Twilio number, so Twilio's normal message charges apply. Stripe is used for cash payouts on Pro."),
    ("Is there a money-back guarantee?", "Yes. The seller offers a 14-day money-back guarantee; refunds are requested from the seller's support team. Details are on the <a href=\"reviews.html#guarantee\">Reviews</a> page."),
    ("Will it guarantee me referrals or income?", "No. The seller states that it doesn't guarantee referrals, customers, sales or income, and its client fees are example prices only. Results depend on the business, the offer and your effort."),
    ("Why do purchase buttons go to JVZoo?", "This is an independent information site. Order buttons are affiliate links to the seller's official page, where checkout happens through JVZoo. We may earn a commission at no extra cost to you. Read our <a href=\"affiliate-disclosure.html\">Affiliate Disclosure</a>."),
]

# =================================================================== HOME
def build_home():
    here = "index.html"
    body = f'''
<section class="hero">
  <div class="container hero-grid">
    <div class="reveal">
      <span class="eyebrow">AI referral software &middot; All five plans</span>
      <h1>Turn word of mouth into a <span class="accent">referral system that runs itself</span></h1>
      <p class="lead">The {BRAND} puts every ReferralNow plan on one login: self-running referral programs for your own businesses, an agency HQ for client work, and 50 accounts you can resell.</p>
      <ul class="hero-points">
        <li>{CHECK}<span>Premium, Pro, Unlimited, Agency and Reseller in one purchase</span></li>
        <li>{CHECK}<span>Six AI agents recruit, nudge, verify, fraud-check, pay out and report</span></li>
        <li>{CHECK}<span>Works at the counter, on web pages, in funnels and in online stores</span></li>
        <li>{CHECK}<span>From $397/year with code FRIEND100, or 2 payments of $199</span></li>
      </ul>
      <div class="btn-row">{cta("Get the Bundle", big=True)}<a class="btn btn-ghost btn-lg" href="how-it-works.html">{ic("play")} See How It Works</a></div>
      <div class="trust-row"><span>{ic("mail")}Login emailed on purchase</span><span>{ic("shield")}14-day seller guarantee</span><span>{ic("card")}Checkout via JVZoo</span></div>
      {affnote()}
    </div>
    <div>{stage()}</div>
  </div>
</section>

<section class="section" id="overview">
  <div class="container split">
    <div class="reveal">{frame("premium", "ReferralNow Premium shown on screen (seller's product image)")}</div>
    <div class="reveal">
      <span class="eyebrow">What it is</span>
      <h2>A complete referral program, built and run for you</h2>
      <p>ReferralNow is a web app that finds the customers already recommending a business, gives each of them a personal link and code, confirms which referred friends actually bought, and pays the reward. Then it invites every new customer to become the next advocate.</p>
      <p>The Bundle is the package that unlocks everything. Instead of buying the front end and four upgrades one at a time, you get all five plans and the 16 launch bonuses together on one account.</p>
      <div class="btn-row"><a class="btn btn-ghost" href="product-overview.html">Read the full overview {ic("arrow")}</a></div>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    {section_head("Where it fits", "One system that works wherever customers buy", "Referrals happen at the till, in a text, on a product page. ReferralNow is designed to catch them in each of those places.")}
    <div class="grid grid-4">
      <div class="card card-3d reveal"><div class="icon">{ic("store")}</div><h3>At the counter</h3><p>Staff confirm a referred sale with a quick tap at the till, plus QR codes, table tents and receipt slips from the print kit.</p></div>
      <div class="card card-3d reveal"><div class="icon icon-pink">{ic("globe")}</div><h3>On web pages</h3><p>A one-line website widget and hosted offer pages in the business's colours let friends claim in seconds.</p></div>
      <div class="card card-3d reveal"><div class="icon icon-green">{ic("cart")}</div><h3>In online stores</h3><p>Paid orders from Shopify, WooCommerce, BigCommerce, Wix and Squarespace can confirm the referral automatically.</p></div>
      <div class="card card-3d reveal"><div class="icon icon-coral">{ic("briefcase")}</div><h3>For clients</h3><p>Agency gives each client a separate workspace under your brand, with a monthly report that shows what referrals earned.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Focus areas", "Four ways people use the Bundle", "Pick the path that matches your situation. Each one has its own guide.")}
    <div class="grid grid-4">
      {focus_cards(here)}
    </div>
  </div>
</section>

<section class="section section-tint" id="details">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Product details</span>
      <h2>What you're actually buying</h2>
      <p>Here are the verified specifics from the seller's page, so you know exactly what arrives after checkout.</p>
      <div class="btn-row"><a class="btn btn-ghost" href="product-overview.html#plans">Compare every plan {ic("arrow")}</a></div>
    </div>
    <div class="table-wrap reveal"><table class="spec"><tbody>
      <tr><th>Product</th><td>{BRAND}</td></tr>
      <tr><th>Format</th><td>Web-based software (online app), one account and one login</td></tr>
      <tr><th>Includes</th><td>Premium, Pro, Unlimited, Agency and Reseller, plus 16 launch bonuses</td></tr>
      <tr><th>Access</th><td>Login sent by email right after purchase</td></tr>
      <tr><th>Price</th><td>$497/year list; $397/year with code FRIEND100; or 2 payments of $199</td></tr>
      <tr><th>Integrations</th><td>Shopify, WooCommerce, BigCommerce, Wix, Squarespace; Stripe payouts; Twilio texts</td></tr>
      <tr><th>Extra costs</th><td>Twilio's normal message charges for texts</td></tr>
      <tr><th>Guarantee</th><td>14-day money-back guarantee from the seller</td></tr>
      <tr><th>Retailer</th><td>JVZoo</td></tr>
    </tbody></table></div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Benefits", "Why a referral system beats &ldquo;tell a friend&rdquo;", "Most businesses already get recommendations. Very few track them, reward them or repeat them on purpose.")}
    <div class="grid grid-3">
      {benefit_cards()}
    </div>
    <div class="center" style="margin-top:36px"><a class="btn btn-ghost" href="benefits.html">Explore all benefits {ic("arrow")}</a></div>
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    {section_head("How it works", "From a business name to a live program in four steps", "Steps one and two take minutes. After that, the agents handle the daily work and the owner approves what matters.")}
    <div class="steps">
      {step_cards()}
    </div>
    <div class="center" style="margin-top:36px"><a class="btn btn-ghost" href="how-it-works.html">See the full walkthrough {ic("arrow")}</a></div>
  </div>
</section>

<section class="section">
  <div class="container split reverse">
    <div class="reveal">{frame("dashboard", "ReferralNow dashboard with referred revenue and rewards (seller's product image)")}</div>
    <div class="reveal">
      <span class="eyebrow">Good habits</span>
      <h2>Software amplifies referrals. It can't create them.</h2>
      <p>People recommend businesses that treat them well. ReferralNow makes it easy to ask, track and reward, but the best results come from pairing it with a few simple habits:</p>
      {checklist(["Ask right after a good experience, not weeks later", "Offer a reward that fits your margins and your customers", "Thank advocates quickly once a sale is confirmed", "Review the monthly report and adjust the offer, not just the budget"])}
      <a href="blog/index.html">Read our referral guides {ic("arrow")}</a>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="container narrow center reveal">
    <span class="eyebrow">Reviews</span>
    <h2>We only publish reviews we can verify</h2>
    <p class="lead">We haven't found verifiable customer reviews of the {BRAND} yet, so you won't see star ratings or testimonials here. Instead, our Reviews page sets out what's confirmed, what to weigh up, and how the guarantee works.</p>
    <div class="btn-row"><a class="btn btn-ghost" href="reviews.html">Read our product assessment {ic("arrow")}</a></div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Every plan included", "Five plans that would cost $1,057 one by one", "Prices below are what the seller lists for each plan on its own.")}
    {plan_table()}
  </div>
</section>

<section class="section section-tint" id="pricing">
  <div class="container">
    {section_head("Pricing", "Choose how you'd like to pay", "Both options unlock the same Bundle. You'll pick one on the seller's order page.")}
    {pricing_cards(here)}
  </div>
</section>

<section class="section"><div class="container">{guarantee_block(here)}</div></section>

<section class="section section-tint">
  <div class="container">
    {section_head("From the blog", "Learn to run referrals well", "Practical guides for anyone setting up a referral program, with or without software.")}
    <div class="grid grid-3">{blog_cards(here)}</div>
  </div>
</section>

<section class="section" id="faq">
  <div class="container">
    {section_head("FAQ", "Questions people ask before buying")}
    {faq_html(HOME_FAQ)}
    <div class="center" style="margin-top:30px"><a class="btn btn-ghost" href="faq.html">See all questions {ic("arrow")}</a></div>
  </div>
</section>

{final_cta(here)}
'''
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": DOMAIN + "/"},
        {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": BRAND,
         "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
         "image": IMGBASE + IMG["bundle"][0],
         "offers": {"@type": "Offer", "price": "497.00", "priceCurrency": "USD", "url": AFF}},
        faq_schema(HOME_FAQ),
    ]
    page(here, f"{BRAND}: All Five ReferralNow Plans, Pricing & Features",
         "Referral Now Bundle explained: all five ReferralNow plans, 16 bonuses, verified pricing ($397/yr with FRIEND100 or 2 x $199), features and the 14-day guarantee.",
         body, "", schema)

# ---------------------------------------------------------------- shared blocks
FOCUS = [
    ("local-businesses.html", "Local Businesses", "store", "", "Salons, dentists, gyms, restaurants and home services: confirm referred sales at the till and reward regulars."),
    ("online-stores-and-funnels.html", "Online Stores & Funnels", "cart", "icon-green", "Confirm referrals from paid orders or the thank-you page in stores, funnels, courses and coaching."),
    ("referral-agency.html", "Referral Agency Services", "briefcase", "icon-pink", "Set up and manage referral programs for clients under your own brand with Agency HQ."),
    ("reselling-accounts.html", "Reselling Accounts", "tag", "icon-coral", "Sell up to 50 ReferralNow accounts through the Reseller console and set your own price."),
]

def focus_cards(here):
    out = ""
    for f, t, i, c, d in FOCUS:
        out += f'<a class="card card-3d card-link reveal" href="{rel("focus-areas/" + f, here)}"><div class="icon {c}">{ic(i)}</div><h3>{t}</h3><p>{d}</p><span class="more">Explore {ic("arrow")}</span></a>'
    return out

def benefit_cards():
    items = [
        ("search", "", "Finds your existing fans", "The Recruiter agent looks through the customer list, Google reviews and Instagram and Facebook mentions to spot people already talking the business up."),
        ("link", "icon-pink", "Every advocate gets a link", "Each advocate receives a personal link, code and QR, so every friend they send is tracked back to them."),
        ("shield", "icon-green", "Fraud checks before payouts", "Every claim gets a 0 to 100 risk score with a plain-English reason, and rewards are held through the refund window."),
        ("gift", "icon-coral", "Rewards people want", "Store credit, discounts, points, a free service, cash, gift cards or commission, with double-sided and tiered options."),
        ("repeat", "", "It keeps compounding", "Every friend who buys is invited to become an advocate with their own link, so one recommendation leads to the next."),
        ("chart", "icon-pink", "Proof in a monthly report", "Referred revenue, top advocates and cost per referred customer, in a report the Report agent writes from real numbers."),
    ]
    return "".join(f'<div class="card card-3d reveal"><div class="icon {c}">{ic(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i, c, t, d in items)

STEPS = [
    ("Point it at a business", "Type a name, paste a website or choose one of 37 trade packs. The seller says it works out what's sold and what a customer is worth in about 15 seconds."),
    ("Let the program draft itself", "It drafts the friend's offer, the advocate's reward, the messages, the offer page and the QR kit. Everything is editable, and nothing goes live until you press Launch."),
    ("The agents go to work", "The Recruiter signs up advocates, the Nudge agent prompts them to share at the right moment, and the Verifier confirms who actually bought."),
    ("Rewards pay, results report", "The Fraud agent scores each claim, the Payout agent releases rewards, and the Report agent sends the month's results."),
]

def step_cards():
    return "".join(f'<div class="card card-3d reveal"><div class="num">{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS))

POSTS = [
    ("referral-reward-ideas.html", "How to Choose a Referral Reward Customers Actually Want", "t1", "gift",
     "Store credit, cash or a free service? A practical framework for picking rewards that motivate sharing without eating your margin.", "7 min read"),
    ("double-sided-referral-program-guide.html", "Double-Sided Referral Programs: A Plain-English Setup Guide", "t2", "users",
     "Why rewarding both the advocate and the friend works, and how to set the offer, the timing and the rules.", "8 min read"),
    ("referral-fraud-prevention.html", "Referral Fraud: Practical Safeguards for Small Businesses", "t3", "lock",
     "Self-referrals, recycled codes and refunded orders. The common abuse patterns and the simple rules that stop them.", "7 min read"),
]

def blog_cards(here):
    out = ""
    for f, t, th, i, d, rt in POSTS:
        out += f'''<a class="card card-3d card-link post-card reveal" href="{rel("blog/" + f, here)}">
  <div class="post-thumb {th}">{ic(i)}</div>
  <p class="post-meta">Guide &middot; {rt}</p><h3>{t}</h3><p>{d}</p><span class="more" style="margin-top:auto">Read article {ic("arrow")}</span></a>'''
    return out

# =================================================================== WHAT IS IT
def build_overview():
    here = "product-overview.html"
    plan_imgs = {"Premium": "premium", "Unlimited": "unlimited", "Agency": "agency"}
    plan_cards = ""
    for n, p, d in PLANS:
        k = plan_imgs.get(n)
        im = f'<div class="card-img">{img(k, f"ReferralNow {n} on screen (seller image)")}</div>' if k else ""
        plan_cards += f'<div class="card card-3d reveal">{im}<span class="eyebrow">Sold alone: {p}</span><h3>{n}</h3><p>{d}</p></div>'
    bon = "".join(f"<tr><th>{p}</th><td>{b}</td></tr>" for p, b in BONUSES)
    body = f'''
{page_hero(here, [("What Is It", None)], "What is it", f"What is the {BRAND}?",
  "An AI-assisted referral marketing system sold as one package: every ReferralNow plan, every upgrade and all 16 launch bonuses, on one account.",
  stage())}

<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Introduction</span>
      <h2>The short version</h2>
      <p>ReferralNow is web-based software for running a referral program. You point it at a business, it drafts the offer and messages, and a set of AI agents handle the routine work: finding likely advocates, reminding them to share, confirming real purchases, scoring claims for fraud, releasing rewards and reporting results.</p>
      <p>The <strong>{BRAND}</strong> is the package that includes all of it. The front end (Premium) and the four upgrades (Pro, Unlimited, Agency and Reseller) normally sell separately. The Bundle combines them on one login, so you can run referral programs in your own businesses, for clients, and as accounts you sell.</p>
      <p>Want to know what that means day to day? Read <a href="benefits.html">the benefits</a> or <a href="how-it-works.html">how it works</a>.</p>
    </div>
    <div class="reveal">{frame("dashboard", "ReferralNow owner dashboard (seller's product image)")}</div>
  </div>
</section>

<section class="section section-tint">
  <div class="container">
    {section_head("Who it's for", "Built for three kinds of buyers")}
    <div class="grid grid-3">
      <div class="card card-3d reveal"><div class="icon">{ic("store")}</div><h3>Business owners</h3><p>Run referral programs in every business you own or manage, with unlimited businesses on the Unlimited plan.</p></div>
      <div class="card card-3d reveal"><div class="icon icon-pink">{ic("briefcase")}</div><h3>Marketers and agencies</h3><p>Offer referral programs as a client service, each client in its own branded workspace. See <a href="focus-areas/referral-agency.html">agency use</a>.</p></div>
      <div class="card card-3d reveal"><div class="icon icon-coral">{ic("tag")}</div><h3>Resellers</h3><p>Sell up to 50 ReferralNow accounts at a price you set. See <a href="focus-areas/reselling-accounts.html">reselling</a>.</p></div>
    </div>
  </div>
</section>

<section class="section" id="plans">
  <div class="container">
    {section_head("Inside the Bundle", "The five plans, explained", "Each plan's stand-alone price is what the seller lists for it on its own.")}
    <div class="grid grid-3">{plan_cards}</div>
  </div>
</section>

<section class="section section-tint">
  <div class="container narrow">
    {section_head("Specifications", "Product specifications")}
    <div class="table-wrap reveal"><table class="spec"><tbody>
      <tr><th>Product name</th><td>{BRAND}</td></tr>
      <tr><th>Vendor</th><td>ReferralNow (founder: Godswill Okoyomon)</td></tr>
      <tr><th>Format</th><td>Online software (web app). Advocates and friends use links and codes in a phone browser; no app required.</td></tr>
      <tr><th>Plans included</th><td>Premium, Pro, Unlimited, Agency, Reseller</td></tr>
      <tr><th>AI agents</th><td>Recruiter, Nudge, Verifier, Fraud, Payout, Report</td></tr>
      <tr><th>Trade packs</th><td>37 ready-made packs with offers, rewards and wording</td></tr>
      <tr><th>Sale confirmation</th><td>Staff tap at the till, unique codes, paid store orders, or the thank-you page</td></tr>
      <tr><th>Reward types</th><td>Store credit, discount, points, free service, cash, gift cards, commission</td></tr>
      <tr><th>Store connections</th><td>Shopify, WooCommerce, BigCommerce, Wix, Squarespace</td></tr>
      <tr><th>Messaging</th><td>Texts via each business's own Twilio number; quiet hours 9pm to 9am in the business's time zone; opt-in only, STOP honoured</td></tr>
      <tr><th>Running costs</th><td>Twilio's normal message charges</td></tr>
      <tr><th>Price</th><td>$497/year (renews until cancelled); $397/year with FRIEND100; or 2 payments of $199</td></tr>
      <tr><th>Guarantee</th><td>14-day money-back guarantee from the seller</td></tr>
    </tbody></table></div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    {section_head("Launch bonuses", "All 16 bonuses included", "Templates, playbooks and planners that come with each plan, listed by the plan they belong to.")}
    <div class="table-wrap reveal"><table class="spec"><thead><tr><th>Plan</th><td><b>Bonus</b></td></tr></thead><tbody>{bon}</tbody></table></div>
  </div>
</section>

<section class="section section-tint">
  <div class="container narrow reveal">
    <div class="callout">
      <h3>Before you buy</h3>
      <p>The Bundle is a yearly subscription that renews until you cancel (unless you choose the 2-payment option on the seller's page). Text messages cost extra through Twilio. And like any marketing tool, it can't guarantee referrals or income. The seller says so too.</p>
      <p>Next: see <a href="benefits.html">what it does well</a>, or go straight to <a href="index.html#pricing">pricing</a>.</p>
    </div>
  </div>
</section>

{final_cta(here)}
'''
    page(here, f"What Is the {BRAND}? Plans, Specs & Bonuses",
         "What the Referral Now Bundle includes: all five ReferralNow plans, six AI agents, 37 trade packs, 16 launch bonuses, specifications and verified pricing.",
         body, "product-overview.html", [crumb_schema([("Home", DOMAIN + "/"), ("What Is It", canon(here))])])

# =================================================================== HOW IT WORKS
def build_how():
    here = "how-it-works.html"
    step_imgs = ["step1", "step2", "step3", "step4"]
    rows = ""
    for i, ((t, d), k) in enumerate(zip(STEPS, step_imgs)):
        rows += f'''<div class="split{" reverse" if i % 2 else ""}" style="margin-bottom:72px">
  <div class="reveal"><div class="num">{i+1}</div><span class="eyebrow">Step {i+1}</span><h2>{t}</h2><p>{d}</p></div>
  <div class="reveal">{frame(k, f"ReferralNow step {i+1}: {t} (seller's product image)")}</div></div>'''
    agents = [
        ("recruiter", "Recruiter", "Reviews the customer list, Google reviews and social mentions, then invites likely advocates with their own link, code and QR."),
        ("nudge", "Nudge", "Times each ask for when an advocate is most likely to act, follows up with quiet ones, and never texts between 9pm and 9am."),
        ("verifier", "Verifier", "Confirms who really bought: a staff tap at the till, a unique code, a paid store order or the thank-you page."),
        ("fraud", "Fraud", "Scores every claim from 0 to 100 with a plain-English reason. Clean claims clear; risky ones wait for one tap."),
        ("payout", "Payout", "Releases the reward, from store credit to cash or a gift card, after the refund window. Cash always waits for a person."),
        ("report", "Report", "Writes the monthly report from real numbers: new customers, referred revenue and cost per customer."),
    ]
    agent_cards = "".join(f'<div class="card card-3d reveal"><div class="card-img">{img(k, f"{n} agent (seller image)")}</div><h3>{n} agent</h3><p>{d}</p></div>' for k, n, d in agents)
    body = f'''
{page_hero(here, [("How It Works", None)], "How it works", "How the referral system runs itself",
  "You set a business up once. After that, six AI agents do the routine work, and a person only steps in to approve what matters.",
  frame("step3", "ReferralNow agents at work (seller's product image)"))}

<section class="section"><div class="container">
  {section_head("The four steps", "From &ldquo;tell a friend&rdquo; to a working program")}
  {rows}
</div></section>

<section class="section section-tint"><div class="container">
  {section_head("Behind the scenes", "Six agents, six jobs", "These are the roles the seller describes. AI drafts and explains; fixed rules, real confirmations and a person's approval decide who gets paid.")}
  <div class="grid grid-3">{agent_cards}</div>
</div></section>

<section class="section"><div class="container split">
  <div class="reveal">
    <span class="eyebrow">Daily routine</span>
    <h2>What the owner actually does</h2>
    <p>Once a campaign is live, the hands-on work is small and predictable:</p>
    {checklist(["Glance at the digest of anything waiting for approval", "Approve or block flagged claims with one tap", "Approve cash rewards, which always need a person", "Read the monthly report and tweak the offer if needed"])}
    <p>Running more than one business or client? See the <a href="focus-areas/index.html">focus areas</a> for how each setup works.</p>
  </div>
  <div class="reveal">
    <h3>Built-in safeguards</h3>
    {checklist(["Opt-in only, with STOP honoured immediately", "Quiet hours from 9pm to 9am in each business's time zone", "Every claim fraud-scored with a reason", "Rewards held through the refund window; no payouts on refunded sales", "A budget ceiling that pauses the campaign when it's reached"])}
  </div>
</div></section>

<section class="section section-tint"><div class="container narrow reveal">
  <div class="callout callout-warn">
    <h3>Good to know</h3>
    <p>Texts are sent from each business's own Twilio number, so Twilio's normal charges apply. Cash and gift-card payouts with Stripe are part of the Pro plan, which the Bundle includes.</p>
  </div>
</div></section>

{final_cta(here, "Ready to see it in your own business?")}
'''
    page(here, f"How the {BRAND} Works: 4 Steps and 6 AI Agents",
         "How ReferralNow runs a referral program: point it at a business, let it draft the campaign, and six AI agents recruit, nudge, verify, fraud-check, pay and report.",
         body, "how-it-works.html", [crumb_schema([("Home", DOMAIN + "/"), ("How It Works", canon(here))])])

# =================================================================== BENEFITS
def build_benefits():
    here = "benefits.html"
    blocks = [
        ("advocates", "Find advocates", "Start with the people who already like you", "Most businesses have customers who recommend them without being asked. The Recruiter agent looks for them in your customer list, reviews and social mentions, then invites them to join with their own link.", "Local businesses benefit most from this", "focus-areas/local-businesses.html"),
        ("instore", "Confirm real sales", "Pay only for referrals that turn into purchases", "Referred sales are confirmed with a staff tap at the till, a unique code, a paid online order or the thank-you page. Advocates are rewarded after a confirmed purchase, not for clicks.", "See how online confirmation works", "focus-areas/online-stores-and-funnels.html"),
        ("rewards", "Flexible rewards", "Reward people in ways that suit your margins", "Choose store credit, a discount, points, a free service, cash, gift cards or commission. Set double-sided or tiered rewards, and a budget ceiling that pauses the campaign when it's reached.", "Read: choosing a reward", "blog/referral-reward-ideas.html"),
        ("fraud", "Fraud protection", "Stop self-referrals and recycled codes", "Each claim is scored from 0 to 100 with a plain-English explanation before any reward moves. Rewards wait out the refund window, and cheats can be blocked with one tap.", "Read: referral fraud safeguards", "blog/referral-fraud-prevention.html"),
        ("agencyconsole", "Client-ready", "Run it for clients under your own brand", "Agency HQ gives every client a separate workspace with your agency's name and colour, a team of up to 10, a reports centre and a margins screen.", "Explore agency use", "focus-areas/referral-agency.html"),
        ("report", "Clear reporting", "See what word of mouth is really worth", "The monthly report shows new customers, referred revenue and cost per referred customer, so owners can judge the program on real numbers.", "Explore reselling", "focus-areas/reselling-accounts.html"),
    ]
    out = ""
    for i, (k, ey, h, p, lt, lu) in enumerate(blocks):
        out += f'''<section class="section{" section-tint" if i % 2 else ""}"><div class="container split{" reverse" if i % 2 else ""}">
  <div class="reveal">{frame(k, f"{ey} in ReferralNow (seller's product image)")}</div>
  <div class="reveal"><span class="eyebrow">{ey}</span><h2>{h}</h2><p>{p}</p><a href="{lu}">{lt} {ic("arrow")}</a></div>
</div></section>'''
    body = f'''
{page_hero(here, [("Benefits", None)], "Benefits", f"Benefits of the {BRAND}",
  "What a systematic referral program adds over hoping customers spread the word, and what the Bundle adds over buying plans one at a time.",
  stage())}
<section class="section"><div class="container">
  {section_head("At a glance", "Six reasons buyers choose a referral system")}
  <div class="grid grid-3">{benefit_cards()}</div>
</div></section>
{out}
<section class="section"><div class="container">
  {section_head("Bundle value", "Why buy the Bundle instead of single plans?")}
  <div class="grid grid-3">
    <div class="card card-3d reveal"><div class="icon">{ic("users")}</div><h3>One account</h3><p>Every plan sits on a single login, so you don't juggle separate upgrades.</p></div>
    <div class="card card-3d reveal"><div class="icon icon-green">{ic("tag")}</div><h3>Lower total cost</h3><p>Bought one by one, the seller prices the five plans at $1,057. The Bundle is $397/year with code FRIEND100.</p></div>
    <div class="card card-3d reveal"><div class="icon icon-pink">{ic("book")}</div><h3>All 16 bonuses</h3><p>Swipe messages, print templates, playbooks and planners from every tier. <a href="product-overview.html">See the list</a>.</p></div>
  </div>
</div></section>
{final_cta(here)}
'''
    page(here, f"{BRAND} Benefits: Advocates, Verified Sales, Rewards & Reports",
         "The benefits of the Referral Now Bundle: find existing advocates, confirm real sales, flexible rewards, fraud scoring, client-ready agency tools and clear reports.",
         body, "benefits.html", [crumb_schema([("Home", DOMAIN + "/"), ("Benefits", canon(here))])])

# =================================================================== FOCUS AREAS
FOCUS_DETAIL = {
    "local-businesses.html": dict(
        img="instore", title="Local Businesses",
        h1="Referral programs for local businesses",
        lead="For salons, dentists, gyms, restaurants and home services, most new customers already arrive through someone who said good things. ReferralNow helps you catch those moments at the counter.",
        why="Local referrals usually happen offline: a friend asks where you got your hair done, or which plumber you used. Without a system, the business never learns who sent whom and the advocate is never thanked.",
        feats=["Staff confirm referred sales with a tap at the till (up to 20 tills on Unlimited)", "Printable QR posters, table tents, receipt slips and cards", "Hosted offer pages in the business's colours, no website needed", "37 trade packs with ready-written offers, rewards and wording", "Texts follow quiet hours, 9pm to 9am in the business's time zone"],
        trades=["Salons and spas", "Dentists and clinics", "Gyms and studios", "Restaurants and cafés", "Home services", "Auto and car wash", "Vets and pet care", "Photographers", "Tutors and lessons", "Boutiques and retail", "Wellness and physio", "Florists and bakers"],
        setup=["Pick the business's trade pack or paste its website", "Choose a friend offer and an advocate reward that fit your margins", "Print the QR kit and brief staff on the till confirmation", "Invite your best existing customers first"],
        consider="Train counter staff on the confirmation step; it's what makes the tracking accurate. Budget for Twilio text charges if you message advocates by SMS.",
        related=[("How the till confirmation fits in", "how-it-works.html"), ("Double-sided referral setup guide", "blog/double-sided-referral-program-guide.html")]),
    "online-stores-and-funnels.html": dict(
        img="online", title="Online Stores & Funnels",
        h1="Referrals for online stores, funnels and courses",
        lead="For e-commerce, info products, coaches and course creators, ReferralNow can confirm a referred sale from the paid order itself, without manual checks.",
        why="Online referrals are easy to share but just as easy to abuse. Confirming against real paid orders, holding rewards through the refund window and scoring claims keeps the program honest.",
        feats=["Store connections for Shopify, WooCommerce, BigCommerce, Wix and Squarespace", "Thank-you page confirmation for funnels and info products", "One-line website widget for any site", "Advocate Finder to spot past buyers who already recommend you (Pro)", "Commission-style rewards with Stripe payouts (Pro)"],
        trades=["Online stores", "Sales funnels", "Info products", "Online courses", "Coaches and consultants", "Freelancers and agencies"],
        setup=["Connect the store or add the thank-you page snippet", "Set the friend's offer and the advocate's reward", "Add the widget to product or account pages", "Invite past buyers and let new buyers join automatically"],
        consider="Pick a reward that still makes sense after refunds and fees. Rewards are held through the refund window, so set that window to match your refund policy.",
        related=[("Referral fraud safeguards", "blog/referral-fraud-prevention.html"), ("Choosing a referral reward", "blog/referral-reward-ideas.html")]),
    "referral-agency.html": dict(
        img="agencyconsole", title="Referral Agency Services",
        h1="Run referral programs as a client service",
        lead="The Agency plan in the Bundle lets you set up and manage referral programs for clients, each in its own workspace and under your own brand.",
        why="Many owners believe in word of mouth but won't build a system themselves. Agency HQ is designed so one person can manage many clients, with a monthly report that shows each client what referrals produced.",
        feats=["Agency HQ with unlimited client workspaces and a daily digest", "Each client separate, with its own campaigns, advocates and till", "Your agency's name and colour on offer pages, advocate pages, reports and client screens", "A team of 10: admin, account managers who see only their clients, read-only client viewers", "A reports centre and a margins screen"],
        trades=["Local service businesses", "Retail and hospitality", "Clinics and wellness", "E-commerce brands"],
        setup=["Create a client workspace and pick their trade pack", "Agree the offer and reward with the client", "Launch, then let the agents handle the routine work", "Send the monthly report under your brand"],
        consider="The seller's agency page gives example prices of $297 to $997 to set up and $300 to $1,000 a month to manage. These are examples, not typical earnings; what you charge and earn depends on you, your market and your clients. Read our <a href=\"../earnings-disclaimer.html\">Earnings Disclaimer</a>.",
        related=[("Agency and Reseller FAQ", "faq.html"), ("How the agents work", "how-it-works.html")]),
    "reselling-accounts.html": dict(
        img="agency", title="Reselling Accounts",
        h1="Resell ReferralNow accounts at your own price",
        lead="The Reseller plan in the Bundle includes a console for up to 50 customer accounts, each with the full front-end plan, and you keep what you charge.",
        why="If you already serve business owners, such as through a membership, a newsletter or a service, ReferralNow accounts can be offered as a product of your own.",
        feats=["Reseller console with up to 50 customer accounts", "Each account includes the full front-end (Premium) plan", "Create accounts from a name and email, or automatically from your own JVZoo product", "Your support email inside every customer account", "A sales kit with page copy, email swipes and banners"],
        trades=["Course and membership owners", "Marketing consultants", "Business coaches", "Local marketing agencies"],
        setup=["Decide your price and what support you'll provide", "Set your support email in the console", "Connect your JVZoo product or create accounts manually", "Use the sales kit to announce the offer"],
        consider="You'll be the first point of support for the customers you sell to, so plan for that. The Reseller plan is sold alone at $497/year; the Bundle includes it.",
        related=[("What's in each plan", "product-overview.html#plans"), ("Earnings disclaimer", "earnings-disclaimer.html")]),
}

def build_focus():
    here = "focus-areas/index.html"
    body = f'''
{page_hero(here, [("Focus Areas", None)], "Focus areas", "Where the Referral Now Bundle fits best",
  "Four ways to use the Bundle, depending on whether you're growing your own business, serving clients, or selling accounts.",
  stage(), buttons=False)}
<section class="section"><div class="container">
  {section_head("Choose your path", "Four focus areas, each with its own guide")}
  <div class="grid grid-2">{focus_cards(here)}</div>
</div></section>
<section class="section section-tint"><div class="container narrow reveal">
  <div class="callout"><h3>Not sure which applies?</h3><p>Most buyers start with their own business, then add clients or resold accounts later. The Bundle covers all four on one login. Read <a href="../how-it-works.html">how it works</a> or check the <a href="../faq.html">FAQ</a>.</p></div>
</div></section>
{final_cta(here)}
'''
    page(here, f"{BRAND} Focus Areas: Local, Online, Agency & Reseller",
         "How the Referral Now Bundle fits local businesses, online stores and funnels, referral agency services and reselling ReferralNow accounts.",
         body, "focus-areas/index.html", [crumb_schema([("Home", DOMAIN + "/"), ("Focus Areas", canon(here))])])

    for f, d in FOCUS_DETAIL.items():
        here = "focus-areas/" + f
        trades = "".join(f'<span class="eyebrow" style="margin:0">{t}</span>' for t in d["trades"])
        setup = "".join(f'<div class="card card-3d reveal"><div class="num">{i+1}</div><p style="margin:0;color:var(--navy);font-weight:500">{s}</p></div>' for i, s in enumerate(d["setup"]))
        related = "".join(f'<li><a href="{rel(u, here)}">{t}</a></li>' for t, u in d["related"])
        others = "".join(f'<li><a href="{x[0]}">{x[1]}</a></li>' for x in FOCUS if x[0] != f)
        body = f'''
{page_hero(here, [("Focus Areas", "focus-areas/index.html"), (d["title"], None)], "Focus area", d["h1"], d["lead"], frame(d["img"], d["title"] + " in ReferralNow (seller's product image)"))}
<section class="section"><div class="container split">
  <div class="reveal"><span class="eyebrow">Why it matters</span><h2>The problem it solves</h2><p>{d["why"]}</p>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:18px">{trades}</div></div>
  <div class="reveal"><h3>What the Bundle gives you here</h3>{checklist(d["feats"])}</div>
</div></section>
<section class="section section-tint"><div class="container">
  {section_head("Getting started", "A simple setup path")}
  <div class="steps">{setup}</div>
</div></section>
<section class="section"><div class="container split">
  <div class="reveal"><div class="callout callout-warn"><h3>Things to consider</h3><p>{d["consider"]}</p></div></div>
  <div class="reveal"><h3>Related reading</h3><ul>{related}</ul><h3 style="margin-top:22px">Other focus areas</h3><ul>{others}</ul></div>
</div></section>
{final_cta(here)}
'''
        page(here, f"{d['title']}: Using the {BRAND}",
             (d["lead"][:150].rsplit(" ", 1)[0] + "…") if len(d["lead"]) > 155 else d["lead"],
             body, "focus-areas/index.html",
             [crumb_schema([("Home", DOMAIN + "/"), ("Focus Areas", canon("focus-areas/index.html")), (d["title"], canon(here))])])

# =================================================================== REVIEWS
def build_reviews():
    here = "reviews.html"
    body = f'''
{page_hero(here, [("Reviews", None)], "Reviews", f"{BRAND} review: what's verified and what to weigh",
  "We don't publish ratings or testimonials we can't verify. Here's an honest assessment built from the seller's published details.",
  stage())}
<section class="section"><div class="container narrow reveal">
  <div class="callout"><h3>About customer reviews</h3><p>At the time of writing (10 Nov 2026) we haven't found independent, verifiable customer reviews of the {BRAND}, so this page has no star ratings, scores or customer quotes. If genuine reviews from an authorized source become available, we'll add them with a link to the source.</p></div>
</div></section>
<section class="section section-tint"><div class="container">
  {section_head("Verified facts", "What we confirmed on the seller's page")}
  <div class="grid grid-2">
    <div class="card reveal"><h3>Included</h3>{checklist(["All five plans: Premium, Pro, Unlimited, Agency, Reseller", "All 16 launch bonuses", "One account and one login, emailed after purchase", "37 trade packs and six AI agents"])}</div>
    <div class="card reveal"><h3>Commercial terms</h3>{checklist(["$497/year, renewing until cancelled", "$397/year with code FRIEND100", "Or 2 payments of $199 ($398 in total)", "14-day money-back guarantee; JVZoo is the retailer"])}</div>
  </div>
</div></section>
<section class="section"><div class="container">
  {section_head("Our assessment", "Strengths and things to weigh", "This is our editorial view based on the published feature set. It isn't a customer rating.")}
  <div class="grid grid-2">
    <div class="card card-3d reveal"><div class="icon icon-green">{ic("check")}</div><h3>Strengths</h3>{checklist(["Covers the whole loop: recruiting, sharing, confirming, fraud checks, payouts and reports", "Works offline (till, QR, print) and online (stores, funnels, widget)", "Sensible safeguards: refund-window holds, human approval for cash, quiet hours", "Agency and Reseller tools included, not sold as extra upgrades"])}</div>
    <div class="card card-3d reveal"><div class="icon icon-coral">{ic("scale")}</div><h3>Things to weigh</h3>{checklist(["It's a yearly subscription unless you choose the 2-payment option", "Twilio text charges are extra", "Results depend on the business, the offer and how well staff use it", "Agency and reseller income isn't guaranteed; the fees shown are the seller's examples"])}</div>
  </div>
</div></section>
<section class="section section-tint"><div class="container">{guarantee_block(here)}</div></section>
<section class="section"><div class="container narrow reveal">
  <span class="eyebrow">How to judge it</span>
  <h2>Testing it during the guarantee window</h2>
  <p>Fourteen days is enough to find out whether the software fits how you work. A practical plan:</p>
  <ol><li>Set up one real business using its trade pack and launch a small campaign.</li><li>Try the till confirmation, the QR kit and a test claim from a friend's phone.</li><li>Check how fraud scoring and reward holds behave.</li><li>If you plan agency work, create one client workspace and preview the branded report.</li></ol>
  <p>Questions still open? The <a href="faq.html">FAQ</a> covers pricing, running costs and refunds.</p>
</div></section>
{final_cta(here)}
'''
    page(here, f"{BRAND} Review: Verified Facts, Pros, Cons & Guarantee",
         "An honest Referral Now Bundle review: verified features and pricing, strengths, things to weigh, and how the 14-day seller guarantee works. No fake ratings.",
         body, "reviews.html", [crumb_schema([("Home", DOMAIN + "/"), ("Reviews", canon(here))])])

# =================================================================== FAQ
FULL_FAQ = [
    ("What is the Referral Now Bundle?", "It's the complete package of ReferralNow referral marketing software: all five plans (Premium, Pro, Unlimited, Agency and Reseller) plus 16 launch bonuses on one account. <a href=\"product-overview.html\">Read the overview</a>."),
    ("What does &ldquo;self-running&rdquo; mean here?", "You set a business up once, and the software handles the routine work: drafting, inviting, messaging, confirming sales, catching cheats and handling rewards. Cash rewards always wait for a person's approval. <a href=\"how-it-works.html\">See how it works</a>."),
    ("How much does it cost?", "The seller lists the Bundle at $497 a year, renewing yearly until you cancel. Code FRIEND100 takes $100 off each year ($397/year). A split option of 2 payments of $199 is also offered. Confirm the final total at checkout."),
    ("Is it a subscription?", "The yearly option is: it renews each year until you cancel. The seller presents the 2-payment option ($199 twice) separately; check its terms on the order page before you buy."),
    ("Do I need to buy the front end first?", "No. The seller says the Bundle creates your account by itself, and your login is emailed when you buy."),
    ("Do customers or advocates need an app?", "No. They use links and codes on their phones, with no app, account or password."),
    ("Will it work without a website or online shop?", "Yes. Hosted offer pages, counter QR codes, printed cards and the till confirmation cover the whole loop without a website. <a href=\"focus-areas/local-businesses.html\">See local business use</a>."),
    ("Which online platforms does it connect to?", "The seller lists Shopify, WooCommerce, BigCommerce, Wix and Squarespace, plus thank-you page confirmation for funnels. <a href=\"focus-areas/online-stores-and-funnels.html\">More on online use</a>."),
    ("How does it stop people cheating?", "Every claim is scored for fraud before a reward moves, rewards are held through the refund window, cash always needs a person's approval, and cheats can be blocked in one tap. <a href=\"blog/referral-fraud-prevention.html\">Read our fraud guide</a>."),
    ("Does AI decide who gets paid?", "No. According to the seller, AI drafts campaigns and writes explanations, while fixed rules, real purchase confirmations and a person's approval decide payouts."),
    ("Are there running costs?", "Yes, Twilio's normal message charges for texts sent from each business's own Twilio number."),
    ("Can I use it for clients or resell it?", "Yes. Agency (unlimited client workspaces under your brand) and Reseller (50 accounts to sell at your own price) are both included. <a href=\"focus-areas/referral-agency.html\">Agency</a> &middot; <a href=\"focus-areas/reselling-accounts.html\">Reseller</a>."),
    ("Can I expect to earn money from it?", "There's no guarantee. The seller's client fees ($297 to $997 setup, $300 to $1,000 a month) are example prices only. <a href=\"earnings-disclaimer.html\">Read our Earnings Disclaimer</a>."),
    ("What's the refund policy?", "The seller offers a 14-day money-back guarantee. To request a refund, contact the seller's support at support@referralnow.online within 14 days. This site can't process refunds."),
    ("Who sells it, and why do links go to JVZoo?", "ReferralNow sells it, with JVZoo as the retailer. This is an independent site; our buttons are affiliate links and we may earn a commission. <a href=\"affiliate-disclosure.html\">Affiliate Disclosure</a>."),
]

def build_faq():
    here = "faq.html"
    body = f'''
{page_hero(here, [("FAQ", None)], "FAQ", f"{BRAND} FAQ",
  "Straight answers about plans, pricing, running costs, refunds and how the software works, based on the seller's published information.",
  stage())}
<section class="section"><div class="container">{faq_html(FULL_FAQ)}</div></section>
<section class="section section-tint"><div class="container narrow reveal center">
  <h2>Still deciding?</h2><p class="lead">Compare <a href="product-overview.html#plans">every plan</a>, read <a href="reviews.html">our assessment</a>, or browse <a href="blog/index.html">the blog</a>.</p>
</div></section>
{final_cta(here)}
'''
    page(here, f"{BRAND} FAQ: Pricing, Plans, Costs & Refunds",
         "Answers about the Referral Now Bundle: what's included, $397/yr with FRIEND100 or 2 x $199, Twilio costs, fraud protection, agency and reseller use, and refunds.",
         body, "faq.html", [faq_schema(FULL_FAQ), crumb_schema([("Home", DOMAIN + "/"), ("FAQ", canon(here))])])

# =================================================================== BLOG
ARTICLES = {
"referral-reward-ideas.html": '''
<p>The reward is the part of a referral program people notice first, and the part most businesses get wrong. Too small and nobody bothers. Too generous and the program quietly loses money. Here's a simple way to pick one that works.</p>
<h2>Start from what a new customer is worth</h2>
<p>Before choosing a reward, estimate what a typical new customer spends with you in their first few months, then decide what share of that you're comfortable giving away to win them. That number is your reward budget per referred customer. Everything else is about how you spend it.</p>
<h2>Match the reward to the relationship</h2>
<ul>
<li><strong>Store credit or a discount</strong> suits businesses people visit repeatedly, like salons, cafés and gyms. It brings the advocate back, and the real cost to you is lower than its face value.</li>
<li><strong>A free service or product</strong> feels generous and personal, and works well where you have spare capacity.</li>
<li><strong>Points</strong> fit businesses with an existing loyalty habit.</li>
<li><strong>Cash or gift cards</strong> are the strongest motivators, but they cost exactly what they say. Keep them for high-value sales.</li>
<li><strong>Commission</strong> suits online products and affiliates who refer often.</li>
</ul>
<h2>Reward both sides</h2>
<p>A welcome offer for the friend gives the advocate something to share that isn't just a favour to you. We cover this in detail in our <a href="double-sided-referral-program-guide.html">double-sided program guide</a>.</p>
<h2>Protect the budget</h2>
<p>Pay only after a confirmed purchase, hold rewards until your refund window has passed, and set a monthly ceiling. Tiered rewards, where the reward grows after the third or fifth referral, keep your best advocates engaged without raising the cost of every single referral.</p>
<h2>Where software helps</h2>
<p>Tools like the Referral Now Bundle let you choose between these reward types, set double-sided and tiered rewards, and pause a campaign automatically when it reaches its budget ceiling. See the <a href="../benefits.html">benefits page</a> for details.</p>
''',
"double-sided-referral-program-guide.html": '''
<p>A double-sided referral program rewards two people: the customer who makes the recommendation and the friend who acts on it. It's one of the most common structures because it makes the ask feel like a gift rather than a favour.</p>
<h2>Why it works</h2>
<p>When an advocate can say &ldquo;use my link and you'll get 20% off your first visit,&rdquo; they're helping their friend, not just the business. The friend has a reason to act now, and the advocate has a reason to share.</p>
<h2>Step 1: Set the friend's offer</h2>
<p>Make it simple and immediate: a first-visit discount, a free add-on, or credit on the first order. Avoid complicated conditions. Friends should understand the offer at a glance.</p>
<h2>Step 2: Set the advocate's reward</h2>
<p>Pay it only after the friend's purchase is confirmed. Choose a reward that brings the advocate back too; our <a href="referral-reward-ideas.html">reward guide</a> walks through the options.</p>
<h2>Step 3: Choose when to ask</h2>
<p>The best moment is right after a good experience: at checkout, when a service is finished, or when an order arrives. A follow-up a few days later catches people who meant to share but forgot. Respect quiet hours and only message people who have opted in.</p>
<h2>Step 4: Make claiming effortless</h2>
<p>Friends should be able to claim with a name and phone number on a simple page, with no app and no password. Every extra step loses people.</p>
<h2>Step 5: Confirm, then reward</h2>
<p>Decide how a referred sale is confirmed: a staff check at the till, a unique code, or the online order itself. Reward promptly once it's confirmed; a fast thank-you encourages the next referral.</p>
<h2>Step 6: Review monthly</h2>
<p>Track referred customers, referred revenue and the cost per referred customer. If people join but don't share, improve the friend's offer. If friends claim but don't buy, simplify the claim step.</p>
<p>Want to see how this structure is automated? Read <a href="../how-it-works.html">how the Referral Now Bundle works</a>.</p>
''',
"referral-fraud-prevention.html": '''
<p>Any program that pays people can attract people who game it. The good news is that most referral fraud follows a few predictable patterns, and simple rules stop the majority of it.</p>
<h2>The common patterns</h2>
<ul>
<li><strong>Self-referral:</strong> a customer refers themselves using a second email or phone number to claim both rewards.</li>
<li><strong>Code sharing:</strong> a discount code ends up on coupon sites, so &ldquo;referrals&rdquo; come from strangers.</li>
<li><strong>Buy-and-refund:</strong> a friend buys to trigger the reward, then asks for a refund.</li>
<li><strong>Existing customers:</strong> people who already shop with you claim a new-customer offer.</li>
</ul>
<h2>Rules that stop most of it</h2>
<ol>
<li><strong>Reward confirmed purchases only,</strong> never clicks or sign-ups.</li>
<li><strong>Hold rewards through your refund window,</strong> and cancel rewards for refunded sales.</li>
<li><strong>Use personal links and codes,</strong> so every claim traces back to one advocate.</li>
<li><strong>Check for matching details,</strong> such as the same surname, device or address as the advocate.</li>
<li><strong>Require a person to approve cash rewards,</strong> which are the most attractive to abuse.</li>
<li><strong>Set a budget ceiling</strong> so an unexpected spike can't run up a large bill.</li>
</ol>
<h2>Keep it friendly</h2>
<p>Most of your advocates are honest. Write your terms in plain English, explain why a claim was declined, and give genuine customers an easy way to ask questions.</p>
<h2>How software can help</h2>
<p>The Referral Now Bundle scores each claim from 0 to 100 with a plain-English reason, holds rewards through the refund window, and keeps cash rewards waiting for human approval. Learn more on the <a href="../benefits.html">benefits page</a> or in the <a href="../faq.html">FAQ</a>.</p>
''',
}

def build_blog():
    here = "blog/index.html"
    body = f'''
{page_hero(here, [("Blog", None)], "Blog", "Referral marketing guides",
  "Practical, original articles on running referral programs well: rewards, structure and keeping things fair.",
  frame("rewards", "Reward types in ReferralNow (seller's product image)"), buttons=False)}
<section class="section"><div class="container">
  <div class="grid grid-3">{blog_cards(here)}</div>
</div></section>
{final_cta(here)}
'''
    page(here, f"Referral Marketing Guides | {BRAND} Blog",
         "Original guides on referral rewards, double-sided referral programs and preventing referral fraud, from the Referral Now Bundle information site.",
         body, "blog/index.html", [crumb_schema([("Home", DOMAIN + "/"), ("Blog", canon(here))])])

    for f, t, th, i, d, rt in POSTS:
        here = "blog/" + f
        others = "".join(f'<li><a href="{x[0]}">{x[1]}</a></li>' for x in POSTS if x[0] != f)
        body = f'''
<section class="page-hero"><div class="container narrow">
  {crumbs(here, [("Blog", "blog/index.html"), (t, None)])}
  <span class="eyebrow">Guide &middot; {rt}</span>
  <h1>{t}</h1>
  <p class="lead">{d}</p>
  <p class="post-meta">Published 10 November 2026</p>
</div></section>
<section class="section"><div class="container">
  <article class="article reveal">{ARTICLES[f]}
    <div class="callout" style="margin-top:40px"><h3>Related reading</h3><ul>{others}<li><a href="../product-overview.html">What is the {BRAND}?</a></li></ul></div>
  </article>
</div></section>
{final_cta(here, "Put these ideas into practice")}
'''
        schema = [{"@context": "https://schema.org", "@type": "Article", "headline": t, "description": d,
                   "datePublished": LASTMOD, "dateModified": LASTMOD, "mainEntityOfPage": canon(here),
                   "author": {"@type": "Organization", "name": BRAND + " information site"}},
                  crumb_schema([("Home", DOMAIN + "/"), ("Blog", canon("blog/index.html")), (t, canon(here))])]
        page(here, f"{t} | {BRAND} Blog", d, body, "blog/index.html", schema)

# =================================================================== LEGAL
def legal(path, title, desc, content):
    body = f'''<section class="page-hero"><div class="container narrow">{crumbs(path, [(title, None)])}<h1>{title}</h1><p class="post-meta">Last updated 10 November 2026</p></div></section>
<section class="section"><div class="container"><article class="article">{content}</article></div></section>'''
    page(path, f"{title} | {BRAND}", desc, body, "")

def build_legal():
    legal("affiliate-disclosure.html", "Affiliate Disclosure",
          "How this Referral Now Bundle information site earns money through affiliate links.", f'''
<p>This website is an independent information site about the {BRAND}. It is not owned or operated by ReferralNow, its founder, or JVZoo.</p>
<h2>How we earn money</h2>
<p>Buttons such as &ldquo;Order Now&rdquo;, &ldquo;Get the Bundle&rdquo; and &ldquo;View the Bundle Offer&rdquo; are affiliate links. If you click one and buy, we may receive a commission from the seller through JVZoo. You don't pay anything extra because of it.</p>
<h2>Our approach to content</h2>
<p>Product facts on this site come from the seller's published sales page and were checked on 10 November 2026. We don't publish invented reviews, ratings, purchase notifications, discounts or deadlines. Opinions on the <a href="reviews.html">Reviews</a> page are our own editorial assessment.</p>
<h2>Prices and offers</h2>
<p>The seller controls pricing, checkout and refunds and can change them at any time. Your final price is the one shown at checkout.</p>''')
    legal("privacy-policy.html", "Privacy Policy",
          "Privacy policy for the Referral Now Bundle information site.", '''
<p>This is a static information website. We don't run user accounts, contact forms, comments or analytics, and we don't collect personal information directly.</p>
<h2>Information stored in your browser</h2>
<p>To avoid showing the promotional pop-up repeatedly, the site stores a timestamp in your browser's local storage, and a session flag if you close the notification card. Nothing is sent to us.</p>
<h2>Third-party services</h2>
<ul>
<li><strong>Google Fonts</strong> delivers the site's typefaces, which means your browser connects to Google's servers.</li>
<li><strong>Product images</strong> load from the seller's website (referralnow.co).</li>
<li><strong>Hosting</strong> is provided by Vercel, which may keep standard server logs.</li>
<li><strong>Affiliate links</strong> lead to JVZoo and the seller's site, which use their own cookies and tracking under their own privacy policies.</li>
</ul>
<h2>Your choices</h2>
<p>You can clear local storage in your browser settings at any time, and block third-party cookies if you prefer.</p>''')
    legal("terms.html", "Terms and Conditions",
          "Terms of use for the Referral Now Bundle information site.", '''
<p>By using this website you agree to these terms.</p>
<h2>Information only</h2>
<p>Content here is general information about third-party software. It isn't legal, financial or business advice. Check the seller's own page and terms before you buy.</p>
<h2>No sales on this site</h2>
<p>We don't sell the product. Purchases, payments, accounts, support and refunds are handled by the seller and JVZoo under their terms.</p>
<h2>Accuracy</h2>
<p>We try to keep product details accurate as of the date shown, but the seller may change features, prices or offers without notice.</p>
<h2>Trademarks</h2>
<p>ReferralNow, JVZoo, Shopify, WooCommerce, BigCommerce, Wix, Squarespace, Stripe and Twilio are trademarks of their respective owners. Product images belong to the seller.</p>
<h2>Liability</h2>
<p>To the extent permitted by law, we aren't liable for any loss arising from use of this site or of any third-party product described here.</p>''')
    legal("earnings-disclaimer.html", "Earnings Disclaimer",
          "No income guarantees: earnings disclaimer for the Referral Now Bundle information site.", '''
<p>Nothing on this site is a promise or guarantee of income, clients, referrals or sales.</p>
<p>Where we mention client fees, such as $297 to $997 to set up a client or $300 to $1,000 a month to manage one, these are the seller's own example prices. They aren't typical or expected earnings. The seller itself states that it does not guarantee any number of referrals, customers, sales or income.</p>
<p>Results from any marketing software depend on many factors, including your skills, effort, market, the businesses involved, and their offers and service. Many people who buy business software earn little or nothing from it.</p>''')
    legal("software-disclaimer.html", "Software Disclaimer",
          "Software disclaimer for the Referral Now Bundle information site.", '''
<p>The Referral Now Bundle is third-party software. This site doesn't develop, host, support or warrant it.</p>
<h2>Compliance is the user's responsibility</h2>
<p>Referral programs that send texts or emails and pay rewards are subject to marketing, consumer-protection, privacy and tax rules that vary by country. Anyone using the software is responsible for consent, opt-outs, reward terms and record-keeping in their market.</p>
<h2>Third-party costs</h2>
<p>Some features rely on other services, such as Twilio for text messages and Stripe for payouts, which may charge their own fees.</p>''')

def build_404():
    body = f'''<section class="section"><div class="container narrow center">
<span class="eyebrow">404</span><h1>Page not found</h1><p class="lead">That page doesn't exist. Try one of these instead.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn-ghost" href="/">Home</a><a class="btn btn-ghost" href="/product-overview.html">What Is It</a><a class="btn btn-ghost" href="/faq.html">FAQ</a></div></div></section>'''
    # 404 is served from any depth, so it uses root-absolute asset paths
    page("404.html", f"Page not found | {BRAND}", "Page not found.", body, "")
    p = os.path.join(ROOT, "404.html")
    s = open(p).read()
    s = s.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
    s = s.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex">')
    s = s.replace('<link rel="canonical" href="https://referralnow.vercel.app/404.html">\n', "")
    import re
    s = re.sub(r'href="(?!https?:|/|#|mailto:)([^"]+)"', r'href="/\1"', s)
    s = s.replace('href="/./"', 'href="/"')
    open(p, "w").write(s)
    PAGES.remove("404.html")

def build_seo():
    urls = ""
    for p in PAGES:
        prio = "1.0" if p == "index.html" else ("0.8" if p.count("/") == 0 and p not in [x[1] for x in LEGAL] else "0.6")
        if p in [x[1] for x in LEGAL]:
            prio = "0.3"
        urls += f"  <url>\n    <loc>{canon(p)}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n    <priority>{prio}</priority>\n  </url>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {DOMAIN}/sitemap.xml\n")

if __name__ == "__main__":
    build_home(); build_overview(); build_how(); build_benefits(); build_focus()
    build_reviews(); build_faq(); build_blog(); build_legal(); build_404(); build_seo()
    print(len(PAGES), "pages:", *PAGES, sep="\n  ")

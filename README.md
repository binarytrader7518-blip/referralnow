# Referral Now Bundle — affiliate site

Static multi-page site for https://referralnow.vercel.app (plain HTML/CSS/JS, no framework, no build step needed to deploy).

## Deploy to Vercel
1. Put this folder in a Git repo (or drag it into vercel.com/new).
2. Framework preset: **Other**. Build command: none. Output directory: `.` (root).
3. Assign the domain `referralnow.vercel.app`.
4. In Google Search Console / Bing Webmaster Tools, submit `https://referralnow.vercel.app/sitemap.xml`.

## Edit content
All pages are generated from `_build/build.py` (shared header, footer, prices, copy).
Edit it, then run `python3 _build/build.py` to regenerate every page, `sitemap.xml` and `robots.txt`.
Key constants at the top: `AFF` (affiliate URL), `LASTMOD`, `DEADLINE` (seller's launch-price end).

## Product images
Images are the seller's original files, loaded unaltered from referralnow.co.
To host them yourself instead, run `sh _build/fetch-images.sh` (downloads them to `assets/img/product/` and rebuilds).

## Reusable components
- `assets/js/notify.js` — bottom-left informational notification (`InfoNotify.init({...})`)
- `assets/js/promo-modal.js` — centered promo modal with 24h cooldown (`PromoModal.init({...})`); add `?showpromo=1` to any URL to preview it
- Both are configured in `assets/js/main.js`.

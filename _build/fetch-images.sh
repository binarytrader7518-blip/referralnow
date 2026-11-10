#!/usr/bin/env sh
# Optional: download the seller's original product images into the site so it
# doesn't depend on referralnow.co. Images are saved byte-for-byte (unaltered),
# then the pages are rebuilt to point at the local copies.
set -e
cd "$(dirname "$0")/.."
mkdir -p assets/img/product
for p in s17/mon-bundle.feb69d8b.png s17/mon-premium.d99f6fbf.webp s17/mon-unlimited.ae77feea.webp \
  s17/mon-agency.2c6f1abe.webp s08/dashboard.f9498f47.webp s09/recruiter.7253103b.webp \
  s09/nudge.c68030ba.webp s09/verifier.4b7c43c4.webp s09/fraud.2555ebfc.webp s09/payout.26e6c222.webp \
  s09/report.c6f5cc10.webp s10/step1-analyze.a0b80c92.webp s10/step2-builder.9704d8e2.webp \
  s10/step3-agents.c749a8ee.webp s10/step4-report.d906d2e7.webp s11/f2-reward-types.153b8dbe.webp \
  s11/f7-in-store.e23e3860.webp s11/f8-online.c6593210.webp s11/f10-agency-console.e089340a.webp \
  s11/f9-advocates.3f563a4a.webp; do
  curl -fsSL "https://referralnow.co/partners/assets/img/$p" -o "assets/img/product/$(basename "$p")"
done
sed -i.bak 's#"https://referralnow.co/partners/assets/img/s17/mon-bundle.feb69d8b.png"#"/assets/img/product/mon-bundle.feb69d8b.png"#' assets/js/main.js && rm -f assets/js/main.js.bak
python3 _build/build.py
echo "Done: images saved to assets/img/product and pages rebuilt."

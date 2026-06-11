#!/usr/bin/env python3
"""Remove hardcoded gtag/fbq tracking calls from the duplicated trackLead()
function across all pages. All tracking is now handled via Google Tag Manager,
which listens for the `w13_form_submit` dataLayer event pushed below."""
import glob
import os

OLD = """    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);

    if (typeof window.gtag === 'function') {
        window.gtag('event', 'generate_lead', {
            send_to: window.W13_GOOGLE_ADS_ID || undefined,
            form_type: formType,
            page_path: window.location.pathname
        });
    }
    if (typeof window.fbq === 'function') {
        window.fbq('track', 'Lead', {
            form_type: formType,
            page_path: window.location.pathname
        });
    }
}"""

NEW = """    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
    // Tracking (GA4 / Meta / Clarity etc.) is handled entirely in Google Tag
    // Manager, which listens for the w13_form_submit event pushed above.
}"""

files = []
for pattern in ("*.html", "services/*.html", "sectors/*.html"):
    files.extend(glob.glob(pattern))

changed = 0
for f in sorted(set(files)):
    if f.endswith(".backup"):
        continue
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    if OLD in content:
        count = content.count(OLD)
        content = content.replace(OLD, NEW)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(content)
        changed += 1
        print(f"updated ({count}x): {f}")

print(f"\nTotal files updated: {changed}")

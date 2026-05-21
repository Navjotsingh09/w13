#!/usr/bin/env python3
"""
Accessibility fixes for W13 UK site.
Issues:
1. Skip link #main target missing on pages without <main id="main"> — first content section needs id="main" tabindex="-1"
2. Form inputs/selects in project register-interest forms missing aria-label
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

def fix_file(rel_path, replacements):
    path = os.path.join(ROOT, rel_path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)  # replace first occurrence only
        else:
            print(f"  WARNING: pattern not found in {rel_path}: {old[:60]!r}")
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  FIXED: {rel_path}")
    else:
        print(f"  UNCHANGED: {rel_path}")

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE 1: Add id="main" tabindex="-1" to first content section
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== FIX 1: Skip link #main target ===")

# services.html  →  <section class="page-hero">
fix_file('services.html', [
    ('<section class="page-hero">',
     '<section class="page-hero" id="main" tabindex="-1">'),
])

# about.html  →  <section class="about-hero">
fix_file('about.html', [
    ('<section class="about-hero">',
     '<section class="about-hero" id="main" tabindex="-1">'),
])

# projects.html  →  <section class="projects-hero">
fix_file('projects.html', [
    ('<section class="projects-hero">',
     '<section class="projects-hero" id="main" tabindex="-1">'),
])

# project pages  →  <section class="project-hero">
for fname in [
    'project-willenhall-gurdwara.html',
    'project-hilston-park.html',
    'project-pear-tree-lane.html',
    'project-thornley-street.html',
    'project-walsall-road.html',
    'project-oldbury-gurdwara.html',
    'project-showell-lane.html',
]:
    fix_file(fname, [
        ('<section class="project-hero">',
         '<section class="project-hero" id="main" tabindex="-1">'),
    ])

# sectors/*.html  →  <section class="sector-hero">
for fname in [
    'sectors/architects-planning.html',
    'sectors/commercial.html',
    'sectors/residential.html',
    'sectors/urban-regeneration.html',
]:
    fix_file(fname, [
        ('<section class="sector-hero">',
         '<section class="sector-hero" id="main" tabindex="-1">'),
    ])

# services/*.html  →  <div class="hero">
for fname in [
    'services/asset-management.html',
    'services/architecture-design.html',
    'services/consultancy.html',
    'services/land-development.html',
    'services/master-developer.html',
]:
    fix_file(fname, [
        ('<div class="hero">',
         '<div class="hero" id="main" tabindex="-1">'),
    ])

# news.html, terms.html, privacy-policy.html  →  <div class="page-hero">
for fname in ['news.html', 'terms.html', 'privacy-policy.html']:
    fix_file(fname, [
        ('<div class="page-hero">',
         '<div class="page-hero" id="main" tabindex="-1">'),
    ])

# news-*.html  →  <div class="article-hero">
for fname in [
    'news-housing-market-outlook.html',
    'news-rise-of-btr.html',
    'news-delivering-net-zero.html',
]:
    fix_file(fname, [
        ('<div class="article-hero">',
         '<div class="article-hero" id="main" tabindex="-1">'),
    ])

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE 2: Form inputs in project register-interest forms — add aria-label
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== FIX 2: Form input aria-labels on project register forms ===")

FORM_FIXES = [
    # name input
    ('<input type="text" name="name" placeholder="Full name" required>',
     '<input type="text" name="name" placeholder="Full name" required aria-label="Full name">'),
    # email input
    ('<input type="email" name="email" placeholder="Email address" required>',
     '<input type="email" name="email" placeholder="Email address" required aria-label="Email address">'),
    # phone input
    ('<input type="tel" name="phone" placeholder="Phone number">',
     '<input type="tel" name="phone" placeholder="Phone number" aria-label="Phone number">'),
    # interest select  (first occurrence — the register form, not any other select)
    ('<select name="interest">',
     '<select name="interest" aria-label="Your interest">'),
]

for fname in [
    'project-willenhall-gurdwara.html',
    'project-hilston-park.html',
    'project-pear-tree-lane.html',
    'project-thornley-street.html',
    'project-walsall-road.html',
    'project-oldbury-gurdwara.html',
    'project-showell-lane.html',
]:
    fix_file(fname, FORM_FIXES)

print("\nDone.")

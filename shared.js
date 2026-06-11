/* W13 — Shared navbar interactions (used by every page) */
(function () {
    'use strict';

    // ===== ANTI-FLASH: fix navbar state + BFCache on every page load =====
    (function () {
        // 1. Set navbar scroll state immediately (no waiting for a scroll event).
        //    This stops the navbar from appearing transparent when the browser
        //    restores scroll position after a hard refresh.
        var navbar = document.getElementById('navbar');
        if (navbar && window.pageYOffset > 100) {
            // Disable transition first so there is no animated "flash"
            navbar.style.transition = 'none';
            navbar.classList.add('scrolled');
            // Re-enable after the browser has painted the correct state
            requestAnimationFrame(function () {
                requestAnimationFrame(function () {
                    navbar.style.transition = '';
                });
            });
        }

        // 2. BFCache restore handler — fires when the user navigates back/forward.
        //    CSS animations restart on BFCache restore, which makes the preloader
        //    reappear and reveal-* elements go blank.
        window.addEventListener('pageshow', function (e) {
            if (!e.persisted) return; // normal load — nothing to fix here

            // 2a. Instantly kill the preloader (no fade, no animation)
            var preloader = document.getElementById('preloader');
            if (preloader) {
                preloader.style.cssText += ';transition:none!important;animation:none!important;opacity:0!important;visibility:hidden!important;pointer-events:none!important';
            }

            // 2b. Sync navbar state instantly (no transition)
            var nav = document.getElementById('navbar');
            if (nav) {
                nav.style.transition = 'none';
                if (window.pageYOffset > 100) {
                    nav.classList.add('scrolled');
                } else {
                    nav.classList.remove('scrolled');
                }
                requestAnimationFrame(function () {
                    requestAnimationFrame(function () {
                        nav.style.transition = '';
                    });
                });
            }

            // 2c. Re-mark any reveal elements that should already be visible
            document.querySelectorAll('.reveal-up, .reveal-scale, .reveal-right').forEach(function (el) {
                el.classList.add('visible');
            });

            // 2d. Force GSAP-animated hero elements visible on BFCache restore
            //     (handles pages like services.html that use gsap.to() with CSS-hidden start state)
            document.querySelectorAll('.page-hero-title, .page-hero-bottom').forEach(function (el) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            });
        });
    }());

    // ===== Mega-menu image swap (scoped to current dropdown) =====
    document.querySelectorAll('.mega-menu-link').forEach(function (link) {
        link.addEventListener('mouseenter', function () {
            var sector = this.dataset.sector;
            if (!sector) return;
            var menu = this.closest('.mega-menu');
            if (!menu) return;
            menu.querySelectorAll('.mega-menu-image-container').forEach(function (c) {
                c.classList.remove('active');
            });
            var target = menu.querySelector('.mega-menu-image-container[data-sector="' + sector + '"]');
            if (target) target.classList.add('active');
        });
    });

    // ===== Restore default image when leaving link list =====
    document.querySelectorAll('.mega-menu-links').forEach(function (group) {
        group.addEventListener('mouseleave', function () {
            var menu = this.closest('.mega-menu');
            if (!menu) return;
            var containers = menu.querySelectorAll('.mega-menu-image-container');
            containers.forEach(function (c) { c.classList.remove('active'); });
            if (containers[0]) containers[0].classList.add('active');
        });
    });

    // ===== Close dropdown on click (so anchor jumps don't leave panel open) =====
    function closeAllDropdowns() {
        document.querySelectorAll('.nav-dropdown').forEach(function (d) {
            d.classList.add('nav-dropdown--closing');
            setTimeout(function () { d.classList.remove('nav-dropdown--closing'); }, 400);
        });
    }
    document.querySelectorAll('.mega-menu a, .nav-dropdown > .nav-link').forEach(function (a) {
        a.addEventListener('click', function () {
            // briefly hide the panel so the user gets feedback even on same-page anchor jumps
            closeAllDropdowns();
        });
    });

    // When the user lands on an anchor section from the dropdown, the hash change
    // also triggers a close (covers the case where the click handler races the hover).
    window.addEventListener('hashchange', closeAllDropdowns);
})();


/* =====================================================================
   W13 — Consent management + Google Tag Manager bootstrap
   ---------------------------------------------------------------------
   ALL analytics / marketing / behaviour tracking (GA4, Microsoft Clarity,
   Meta Pixel, Google Ads, etc.) is configured INSIDE Google Tag Manager —
   nothing is hardcoded into the page source. To activate tracking, set
   the container ID below (one place only) and configure the tags in GTM.

   This module:
     1. Sets Google Consent Mode v2 defaults to "denied" before GTM loads.
     2. Re-applies any previously stored consent choice.
     3. Loads the GTM container.
     4. Renders the cookie banner + preference centre + floating settings
        button, and lets the user Accept / Decline / Manage preferences at
        any time (also linked from the footer).
   ===================================================================== */
(function () {
    'use strict';

    /* ----- Single source of truth for the GTM container ID ----- */
    /* Replace GTM-XXXXXXX with your real container ID to go live. */
    var GTM_ID = 'GTM-XXXXXXX';

    var CONSENT_COOKIE = 'w13_consent';
    var CONSENT_VERSION = 1;
    var CONSENT_MAX_AGE_DAYS = 365;

    /* ===== Consent Mode (v2) ===== */
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = window.gtag || gtag;

    // Default everything (except security) to denied until the user chooses.
    gtag('consent', 'default', {
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
        analytics_storage: 'denied',
        functionality_storage: 'denied',
        personalization_storage: 'denied',
        security_storage: 'granted',
        wait_for_update: 500
    });

    /* ===== Stored consent helpers ===== */
    function readConsent() {
        try {
            var m = document.cookie.match(new RegExp('(?:^|; )' + CONSENT_COOKIE + '=([^;]*)'));
            var raw = m ? decodeURIComponent(m[1]) : (window.localStorage ? localStorage.getItem(CONSENT_COOKIE) : null);
            if (!raw) return null;
            var data = JSON.parse(raw);
            if (!data || data.v !== CONSENT_VERSION) return null;
            return data;
        } catch (e) { return null; }
    }

    function writeConsent(prefs) {
        var data = {
            v: CONSENT_VERSION,
            analytics: !!prefs.analytics,
            advertising: !!prefs.advertising,
            functional: !!prefs.functional,
            ts: Date.now()
        };
        var json = JSON.stringify(data);
        try {
            var expires = new Date(Date.now() + CONSENT_MAX_AGE_DAYS * 864e5).toUTCString();
            document.cookie = CONSENT_COOKIE + '=' + encodeURIComponent(json) + ';expires=' + expires + ';path=/;SameSite=Lax';
            if (window.localStorage) localStorage.setItem(CONSENT_COOKIE, json);
        } catch (e) { /* storage blocked — consent stays for this session only */ }
        return data;
    }

    function applyConsent(prefs) {
        gtag('consent', 'update', {
            ad_storage: prefs.advertising ? 'granted' : 'denied',
            ad_user_data: prefs.advertising ? 'granted' : 'denied',
            ad_personalization: prefs.advertising ? 'granted' : 'denied',
            analytics_storage: prefs.analytics ? 'granted' : 'denied',
            functionality_storage: prefs.functional ? 'granted' : 'denied',
            personalization_storage: prefs.functional ? 'granted' : 'denied',
            security_storage: 'granted'
        });
        window.dataLayer.push({
            event: 'w13_consent_update',
            consent_analytics: !!prefs.analytics,
            consent_advertising: !!prefs.advertising,
            consent_functional: !!prefs.functional
        });
    }

    /* ===== Load Google Tag Manager ===== */
    function loadGTM(id) {
        if (!id || id.indexOf('GTM-') !== 0 || id === 'GTM-XXXXXXX') return; // not configured yet
        if (window.__w13GtmLoaded) return;
        window.__w13GtmLoaded = true;
        window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
        var f = document.getElementsByTagName('script')[0];
        var j = document.createElement('script');
        j.async = true;
        j.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(id);
        f.parentNode.insertBefore(j, f);
        // <noscript> iframe fallback
        var ns = document.createElement('noscript');
        var iframe = document.createElement('iframe');
        iframe.src = 'https://www.googletagmanager.com/ns.html?id=' + encodeURIComponent(id);
        iframe.height = '0';
        iframe.width = '0';
        iframe.style.display = 'none';
        iframe.style.visibility = 'hidden';
        ns.appendChild(iframe);
        document.body.insertBefore(ns, document.body.firstChild);
    }

    /* ===== UI styles (injected so it works with the minified CSS bundle) ===== */
    function injectStyles() {
        if (document.getElementById('w13-consent-styles')) return;
        var css = ''
            + '.w13-cc-banner,.w13-cc-modal-overlay{font-family:"Graphie",sans-serif;box-sizing:border-box}'
            + '.w13-cc-banner *,.w13-cc-modal-overlay *{box-sizing:border-box}'
            + '.w13-cc-banner{position:fixed;left:0;right:0;bottom:0;z-index:100050;background:#091c33;border-top:3px solid #44C0C0;color:#EAEAEA;padding:22px 24px;box-shadow:0 -10px 40px rgba(0,0,0,.35);transform:translateY(110%);transition:transform .45s cubic-bezier(.16,1,.3,1)}'
            + '.w13-cc-banner.is-visible{transform:translateY(0)}'
            + '.w13-cc-banner-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:28px;flex-wrap:wrap}'
            + '.w13-cc-banner-text{flex:1;min-width:260px}'
            + '.w13-cc-banner-text h2{font-size:16px;font-weight:700;color:#fff;margin:0 0 6px}'
            + '.w13-cc-banner-text p{font-size:13.5px;line-height:1.6;color:rgba(234,234,234,.72);margin:0}'
            + '.w13-cc-banner-text a{color:#44C0C0;text-decoration:underline}'
            + '.w13-cc-actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center}'
            + '.w13-cc-btn{font-family:"Graphie",sans-serif;font-size:13px;font-weight:600;letter-spacing:.3px;padding:12px 22px;border-radius:8px;cursor:pointer;border:1px solid transparent;transition:all .25s;white-space:nowrap}'
            + '.w13-cc-btn--primary{background:#44C0C0;color:#0C233F}'
            + '.w13-cc-btn--primary:hover{background:#5ad4d4}'
            + '.w13-cc-btn--ghost{background:transparent;color:#EAEAEA;border-color:rgba(234,234,234,.3)}'
            + '.w13-cc-btn--ghost:hover{border-color:#44C0C0;color:#44C0C0}'
            + '.w13-cc-btn--link{background:transparent;color:rgba(234,234,234,.7);border:none;text-decoration:underline;padding:12px 8px}'
            + '.w13-cc-btn--link:hover{color:#44C0C0}'
            + '.w13-cc-modal-overlay{position:fixed;inset:0;z-index:100060;background:rgba(9,28,51,.82);backdrop-filter:blur(4px);display:none;align-items:center;justify-content:center;padding:24px}'
            + '.w13-cc-modal-overlay.is-visible{display:flex}'
            + '.w13-cc-modal{background:#0C233F;border:1px solid rgba(68,192,192,.25);border-radius:16px;max-width:560px;width:100%;max-height:88vh;overflow-y:auto;box-shadow:0 24px 80px rgba(0,0,0,.5)}'
            + '.w13-cc-modal-head{padding:28px 32px 18px;border-bottom:1px solid rgba(234,234,234,.1);position:relative}'
            + '.w13-cc-modal-head h2{font-size:21px;font-weight:700;color:#fff;margin:0 0 8px}'
            + '.w13-cc-modal-head p{font-size:13.5px;line-height:1.6;color:rgba(234,234,234,.7);margin:0}'
            + '.w13-cc-modal-head p a{color:#44C0C0;text-decoration:underline}'
            + '.w13-cc-close{position:absolute;top:18px;right:20px;background:none;border:none;color:rgba(234,234,234,.5);font-size:26px;line-height:1;cursor:pointer}'
            + '.w13-cc-close:hover{color:#44C0C0}'
            + '.w13-cc-modal-body{padding:8px 32px 4px}'
            + '.w13-cc-cat{padding:20px 0;border-bottom:1px solid rgba(234,234,234,.08)}'
            + '.w13-cc-cat-top{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}'
            + '.w13-cc-cat-top h3{font-size:15px;font-weight:600;color:#fff;margin:0}'
            + '.w13-cc-cat p{font-size:13px;line-height:1.6;color:rgba(234,234,234,.62);margin:8px 0 0}'
            + '.w13-cc-switch{position:relative;width:46px;height:26px;flex:0 0 auto}'
            + '.w13-cc-switch input{opacity:0;width:0;height:0;position:absolute}'
            + '.w13-cc-slider{position:absolute;inset:0;background:rgba(234,234,234,.18);border-radius:26px;transition:.3s;cursor:pointer}'
            + '.w13-cc-slider:before{content:"";position:absolute;height:18px;width:18px;left:4px;top:4px;background:#fff;border-radius:50%;transition:.3s}'
            + '.w13-cc-switch input:checked+.w13-cc-slider{background:#44C0C0}'
            + '.w13-cc-switch input:checked+.w13-cc-slider:before{transform:translateX(20px)}'
            + '.w13-cc-switch input:disabled+.w13-cc-slider{background:#44C0C0;opacity:.5;cursor:not-allowed}'
            + '.w13-cc-locked{font-size:11px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;color:#44C0C0}'
            + '.w13-cc-modal-foot{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;padding:20px 32px 28px}'
            + '.w13-cc-fab{position:fixed;left:20px;bottom:20px;z-index:100040;width:46px;height:46px;border-radius:50%;background:#091c33;border:1px solid rgba(68,192,192,.4);color:#44C0C0;font-size:18px;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;transition:all .25s}'
            + '.w13-cc-fab:hover{background:#44C0C0;color:#0C233F}'
            + '@media (max-width:768px){.w13-cc-banner{padding:18px 16px}.w13-cc-banner-inner{gap:16px}.w13-cc-actions{width:100%}.w13-cc-actions .w13-cc-btn{flex:1;text-align:center}.w13-cc-fab{bottom:84px;left:16px}}';
        var style = document.createElement('style');
        style.id = 'w13-consent-styles';
        style.textContent = css;
        document.head.appendChild(style);
    }

    /* ===== Resolve relative path to site root (root vs /services, /sectors) ===== */
    function rootPrefix() {
        var legalLink = document.querySelector('.footer-legal-links a[href*="privacy-policy.html"]');
        if (legalLink) {
            var href = legalLink.getAttribute('href') || '';
            return href.slice(0, href.indexOf('privacy-policy.html'));
        }
        // Fallback: count path depth below the domain root.
        var segs = window.location.pathname.split('/').filter(Boolean);
        // last segment is the file name
        var depth = Math.max(0, segs.length - 1);
        return depth > 0 ? new Array(depth + 1).join('../') : '';
    }

    /* ===== Build & manage the UI ===== */
    var elBanner, elModal, inputs = {};

    function setSwitches(prefs) {
        if (inputs.analytics) inputs.analytics.checked = !!prefs.analytics;
        if (inputs.advertising) inputs.advertising.checked = !!prefs.advertising;
        if (inputs.functional) inputs.functional.checked = !!prefs.functional;
    }

    function hideBanner() { if (elBanner) elBanner.classList.remove('is-visible'); }
    function openModal() {
        setSwitches(readConsent() || { analytics: false, advertising: false, functional: false });
        if (elModal) elModal.classList.add('is-visible');
    }
    function closeModal() { if (elModal) elModal.classList.remove('is-visible'); }

    function saveAndApply(prefs) {
        var data = writeConsent(prefs);
        applyConsent(data);
        hideBanner();
        closeModal();
    }

    function buildUI() {
        injectStyles();
        var prefix = rootPrefix();
        var cookieHref = prefix + 'cookie-policy.html';
        var privacyHref = prefix + 'privacy-policy.html';

        /* ---- Banner ---- */
        elBanner = document.createElement('div');
        elBanner.className = 'w13-cc-banner';
        elBanner.setAttribute('role', 'dialog');
        elBanner.setAttribute('aria-label', 'Cookie consent');
        elBanner.innerHTML =
            '<div class="w13-cc-banner-inner">'
            + '<div class="w13-cc-banner-text">'
            + '<h2>We value your privacy</h2>'
            + '<p>We use cookies to keep our site secure, understand how it is used and improve your experience. '
            + 'Non-essential cookies are only set with your consent. Read our '
            + '<a href="' + cookieHref + '">Cookie Policy</a> and <a href="' + privacyHref + '">Privacy Policy</a>.</p>'
            + '</div>'
            + '<div class="w13-cc-actions">'
            + '<button type="button" class="w13-cc-btn w13-cc-btn--link" data-w13="manage">Manage Preferences</button>'
            + '<button type="button" class="w13-cc-btn w13-cc-btn--ghost" data-w13="decline">Decline</button>'
            + '<button type="button" class="w13-cc-btn w13-cc-btn--primary" data-w13="accept">Accept All</button>'
            + '</div>'
            + '</div>';
        document.body.appendChild(elBanner);

        /* ---- Preferences modal ---- */
        elModal = document.createElement('div');
        elModal.className = 'w13-cc-modal-overlay';
        elModal.innerHTML =
            '<div class="w13-cc-modal" role="dialog" aria-modal="true" aria-label="Cookie preferences">'
            + '<div class="w13-cc-modal-head">'
            + '<button type="button" class="w13-cc-close" data-w13="close" aria-label="Close">&times;</button>'
            + '<h2>Cookie Preferences</h2>'
            + '<p>Manage how W13UK uses cookies. Strictly necessary cookies are always on. '
            + 'See our <a href="' + cookieHref + '">Cookie Policy</a> for full details.</p>'
            + '</div>'
            + '<div class="w13-cc-modal-body">'
            + cat('Strictly Necessary', 'Required for the website to function securely and to remember your consent choices. These cannot be switched off.', null, true)
            + cat('Analytics &amp; Performance', 'Help us understand how visitors use the site (e.g. Microsoft Clarity, Google Analytics 4) so we can improve performance. Aggregated and anonymous.', 'analytics', false)
            + cat('Functional', 'Allow the site to remember choices you make to provide enhanced, personalised features.', 'functional', false)
            + cat('Advertising &amp; Targeting', 'Used by marketing partners to measure campaign performance and show relevant ads. Only set with your explicit consent.', 'advertising', false)
            + '</div>'
            + '<div class="w13-cc-modal-foot">'
            + '<button type="button" class="w13-cc-btn w13-cc-btn--ghost" data-w13="reject-all">Reject All</button>'
            + '<button type="button" class="w13-cc-btn w13-cc-btn--ghost" data-w13="save">Save Preferences</button>'
            + '<button type="button" class="w13-cc-btn w13-cc-btn--primary" data-w13="accept-all">Accept All</button>'
            + '</div>'
            + '</div>';
        document.body.appendChild(elModal);

        inputs.analytics = elModal.querySelector('#w13-cc-analytics');
        inputs.advertising = elModal.querySelector('#w13-cc-advertising');
        inputs.functional = elModal.querySelector('#w13-cc-functional');

        /* ---- Floating settings button ---- */
        var fab = document.createElement('button');
        fab.type = 'button';
        fab.className = 'w13-cc-fab';
        fab.setAttribute('aria-label', 'Cookie settings');
        fab.setAttribute('title', 'Cookie settings');
        fab.innerHTML = '<i class="fas fa-cookie-bite" aria-hidden="true"></i>';
        fab.addEventListener('click', openModal);
        document.body.appendChild(fab);

        /* ---- Footer links (Cookie Policy + Cookie Settings) ---- */
        var legal = document.querySelector('.footer-legal-links');
        if (legal) {
            if (!legal.querySelector('a[href*="cookie-policy.html"]')) {
                var cp = document.createElement('a');
                cp.href = cookieHref;
                cp.textContent = 'Cookie Policy';
                legal.appendChild(cp);
            }
            if (!legal.querySelector('[data-w13="manage"]')) {
                var cs = document.createElement('a');
                cs.href = '#';
                cs.setAttribute('data-w13', 'manage');
                cs.textContent = 'Cookie Settings';
                legal.appendChild(cs);
            }
        }

        /* ---- Wire up all controls (event delegation) ---- */
        document.addEventListener('click', function (e) {
            var t = e.target.closest('[data-w13]');
            if (!t) return;
            var action = t.getAttribute('data-w13');
            if (action === 'manage') { e.preventDefault(); openModal(); }
            else if (action === 'close') { closeModal(); }
            else if (action === 'accept' || action === 'accept-all') { saveAndApply({ analytics: true, advertising: true, functional: true }); }
            else if (action === 'decline' || action === 'reject-all') { saveAndApply({ analytics: false, advertising: false, functional: false }); }
            else if (action === 'save') {
                saveAndApply({
                    analytics: inputs.analytics && inputs.analytics.checked,
                    advertising: inputs.advertising && inputs.advertising.checked,
                    functional: inputs.functional && inputs.functional.checked
                });
            }
        });
        elModal.addEventListener('click', function (e) { if (e.target === elModal) closeModal(); });

        function cat(title, desc, key, locked) {
            var control = locked
                ? '<span class="w13-cc-locked">Always On</span>'
                : '<label class="w13-cc-switch"><input type="checkbox" id="w13-cc-' + key + '"><span class="w13-cc-slider"></span></label>';
            return '<div class="w13-cc-cat"><div class="w13-cc-cat-top"><h3>' + title + '</h3>' + control + '</div><p>' + desc + '</p></div>';
        }
    }

    /* ===== Init ===== */
    function init() {
        var stored = readConsent();
        if (stored) applyConsent(stored); // re-affirm before GTM evaluates triggers
        loadGTM(GTM_ID);
        buildUI();
        if (!stored) {
            // Show the banner shortly after load so it doesn't fight the preloader.
            setTimeout(function () { if (elBanner) elBanner.classList.add('is-visible'); }, 600);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

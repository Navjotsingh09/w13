/* W13 — Cookie Consent & Google Consent Mode v2 */
(function () {
    "use strict";

    var KEY = "w13_consent";
    var VER = 1;

    /* 1. Google Consent Mode v2 defaults — must fire before GTM loads */
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    gtag("consent", "default", {
        analytics_storage: "denied",
        ad_storage: "denied",
        ad_user_data: "denied",
        ad_personalization: "denied",
        wait_for_update: 500
    });

    /* 2. Helpers */
    function readPrefs() {
        try {
            var raw = localStorage.getItem(KEY);
            if (raw) {
                var p = JSON.parse(raw);
                if (p && p.v === VER) return p;
            }
        } catch (e) {}
        return null;
    }

    function writePrefs(analytics, marketing) {
        var p = { v: VER, analytics: analytics, marketing: marketing, ts: Date.now() };
        try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {}
        return p;
    }

    function applyConsent(p) {
        gtag("consent", "update", {
            analytics_storage: p.analytics ? "granted" : "denied",
            ad_storage:         p.marketing ? "granted" : "denied",
            ad_user_data:       p.marketing ? "granted" : "denied",
            ad_personalization: p.marketing ? "granted" : "denied"
        });
        window.dataLayer.push({
            event: "consent_update",
            analytics_consent: p.analytics,
            marketing_consent: p.marketing
        });
    }

    function tog(btn, val) {
        btn.className = val ? "w13cm-tgl on" : "w13cm-tgl";
        btn.setAttribute("aria-checked", val ? "true" : "false");
    }

    /* 3. Expose global open function (footer link + FAB) */
    window.w13OpenConsent = function () {
        var m = document.getElementById("w13cm");
        var tA = document.getElementById("w13cm-a");
        var tM = document.getElementById("w13cm-m");
        if (m && tA && tM) {
            var prefs = readPrefs();
            if (prefs) { tog(tA, prefs.analytics); tog(tM, prefs.marketing); }
            m.classList.add("open");
        }
    };

    /* 4. Apply stored prefs immediately (returning visitor) */
    var storedOnLoad = readPrefs();
    if (storedOnLoad) applyConsent(storedOnLoad);

    /* 5. Build UI after DOM is ready */
    document.addEventListener("DOMContentLoaded", function () {

        var st = document.createElement("style");
        st.textContent = [
            "#w13cb{position:fixed;bottom:0;left:0;right:0;z-index:99999;background:rgba(12,35,63,0.97);backdrop-filter:blur(12px);border-top:1px solid rgba(68,192,192,0.2);padding:18px 24px;font-family:inherit;animation:w13cb-up .4s cubic-bezier(.16,1,.3,1)}",
            "@keyframes w13cb-up{from{transform:translateY(100%);opacity:0}to{transform:translateY(0);opacity:1}}",
            "#w13cb *{box-sizing:border-box;margin:0;padding:0}",
            "#w13cb-inner{max-width:1400px;margin:0 auto;display:flex;align-items:center;gap:20px;flex-wrap:wrap}",
            "#w13cb-text{flex:1;min-width:200px;font-size:13px;color:rgba(234,234,234,0.75);line-height:1.6}",
            "#w13cb-text a{color:#44C0C0;text-decoration:underline}",
            "#w13cb-btns{display:flex;gap:10px;flex-wrap:wrap;align-items:center}",
            ".w13cb-b{display:inline-block;padding:10px 20px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid rgba(68,192,192,0.5);background:none;color:#EAEAEA;transition:all .25s;font-family:inherit;letter-spacing:.5px;white-space:nowrap}",
            ".w13cb-b-yes{background:#44C0C0;color:#0C233F;border-color:#44C0C0}",
            ".w13cb-b-yes:hover{background:#3aadad}",
            ".w13cb-b-no:hover{background:rgba(68,192,192,0.1)}",
            ".w13cb-b-mgr{border:none;background:none;color:rgba(234,234,234,0.55);text-decoration:underline;font-size:12px;padding:10px 6px;font-family:inherit;cursor:pointer}",
            ".w13cb-b-mgr:hover{color:#44C0C0}",
            "#w13cm{display:none;position:fixed;inset:0;z-index:100000;background:rgba(12,35,63,0.88);backdrop-filter:blur(6px);align-items:center;justify-content:center}",
            "#w13cm.open{display:flex}",
            "#w13cm-box{background:#0C233F;border:1px solid rgba(68,192,192,0.22);max-width:480px;width:calc(100% - 40px);padding:36px;position:relative}",
            "#w13cm-box h3{font-size:18px;font-weight:700;color:#EAEAEA;margin-bottom:8px}",
            "#w13cm-box > p{font-size:13px;color:rgba(234,234,234,0.6);line-height:1.6;margin-bottom:24px}",
            "#w13cm-close{position:absolute;top:16px;right:16px;background:none;border:none;color:rgba(234,234,234,0.45);font-size:22px;cursor:pointer;line-height:1;padding:4px;font-family:inherit}",
            "#w13cm-close:hover{color:#EAEAEA}",
            ".w13cm-row{display:flex;justify-content:space-between;align-items:flex-start;padding:16px 0;border-bottom:1px solid rgba(68,192,192,0.1);gap:16px}",
            ".w13cm-row:last-of-type{border-bottom:none}",
            ".w13cm-info strong{font-size:14px;color:#EAEAEA;display:block;margin-bottom:4px}",
            ".w13cm-info span{font-size:12px;color:rgba(234,234,234,0.5);line-height:1.5}",
            ".w13cm-tgl{flex-shrink:0;width:44px;height:24px;background:rgba(68,192,192,0.2);border-radius:12px;position:relative;cursor:pointer;transition:background .25s;border:none;outline:none;font-family:inherit}",
            ".w13cm-tgl.on{background:#44C0C0}",
            ".w13cm-tgl::after{content:'';position:absolute;top:3px;left:3px;width:18px;height:18px;background:#EAEAEA;border-radius:50%;transition:transform .25s}",
            ".w13cm-tgl.on::after{transform:translateX(20px)}",
            ".w13cm-tgl[disabled]{opacity:0.5;cursor:not-allowed}",
            ".w13cm-actions{display:flex;gap:10px;margin-top:24px;flex-wrap:wrap}",
            ".w13cm-actions .w13cb-b{flex:1;text-align:center}",
            "#w13-fab{display:none;position:fixed;bottom:20px;left:20px;z-index:99998;width:44px;height:44px;background:#0C233F;border:1px solid rgba(68,192,192,0.4);border-radius:50%;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,0.4);transition:all .25s}",
            "#w13-fab:hover{border-color:#44C0C0}",
            "#w13-fab svg{width:22px;height:22px;fill:#44C0C0;display:block}",
            ".w13-manage-cookies-btn{background:none;border:none;color:inherit;font:inherit;cursor:pointer;padding:0;line-height:inherit;text-decoration:none}",
            ".w13-manage-cookies-btn:hover{color:#44C0C0}",
            "@media(max-width:640px){#w13cb-inner{flex-direction:column;align-items:flex-start}#w13cb-btns{width:100%}.w13cb-b{flex:1;text-align:center}}"
        ].join("\n");
        document.head.appendChild(st);

        var banner = document.createElement("div");
        banner.id = "w13cb";
        banner.setAttribute("role", "dialog");
        banner.setAttribute("aria-label", "Cookie consent");
        banner.innerHTML = '<div id="w13cb-inner">'
            + '<p id="w13cb-text">We use cookies to improve your experience, analyse site usage and support marketing. You choose which types to allow. <a href="/cookie-policy.html">Cookie Policy</a></p>'
            + '<div id="w13cb-btns">'
            + '<button class="w13cb-b w13cb-b-yes" id="w13cb-accept">Accept All</button>'
            + '<button class="w13cb-b w13cb-b-no" id="w13cb-decline">Decline All</button>'
            + '<button class="w13cb-b w13cb-b-mgr" id="w13cb-manage">Manage Preferences</button>'
            + '</div></div>';

        var modal = document.createElement("div");
        modal.id = "w13cm";
        modal.setAttribute("role", "dialog");
        modal.setAttribute("aria-modal", "true");
        modal.setAttribute("aria-label", "Cookie preferences");
        modal.innerHTML = '<div id="w13cm-box">'
            + '<button id="w13cm-close" aria-label="Close">&#215;</button>'
            + '<h3>Cookie Preferences</h3>'
            + '<p>Choose which cookies you allow. Necessary cookies are always active as they keep the site working.</p>'
            + '<div class="w13cm-row"><div class="w13cm-info"><strong>Necessary</strong><span>Login, security and core site functionality. Cannot be disabled.</span></div>'
            +   '<button class="w13cm-tgl on" disabled aria-checked="true" role="switch" aria-label="Necessary — always on"></button></div>'
            + '<div class="w13cm-row"><div class="w13cm-info"><strong>Analytics</strong><span>Helps us understand how visitors use the site (Google Analytics, Microsoft Clarity).</span></div>'
            +   '<button class="w13cm-tgl" id="w13cm-a" aria-checked="false" role="switch" aria-label="Analytics cookies"></button></div>'
            + '<div class="w13cm-row"><div class="w13cm-info"><strong>Marketing</strong><span>Used to deliver relevant ads and measure campaign effectiveness (Meta Pixel).</span></div>'
            +   '<button class="w13cm-tgl" id="w13cm-m" aria-checked="false" role="switch" aria-label="Marketing cookies"></button></div>'
            + '<div class="w13cm-actions">'
            +   '<button class="w13cb-b w13cb-b-no" id="w13cm-decline">Decline All</button>'
            +   '<button class="w13cb-b w13cb-b-yes" id="w13cm-save">Save Preferences</button>'
            + '</div></div>';

        var fab = document.createElement("div");
        fab.id = "w13-fab";
        fab.setAttribute("role", "button");
        fab.setAttribute("tabindex", "0");
        fab.setAttribute("aria-label", "Manage cookie settings");
        fab.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M21.97 12.18A10 10 0 1 1 11.8 2.03a1 1 0 0 1 .94 1.35 2.5 2.5 0 0 0 3.27 3.27 1 1 0 0 1 1.35.93 5 5 0 0 0 4.61 4.6zM12 20a8 8 0 1 0-7.52-10.73 4.5 4.5 0 0 1-1.22 8.83A8 8 0 0 0 12 20zm-3-8a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm4 3a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm3-2a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/></svg>';

        document.body.appendChild(banner);
        document.body.appendChild(modal);
        document.body.appendChild(fab);

        var tA = document.getElementById("w13cm-a");
        var tM = document.getElementById("w13cm-m");

        var prefs = readPrefs();
        if (prefs) {
            tog(tA, prefs.analytics);
            tog(tM, prefs.marketing);
            banner.style.display = "none";
            fab.style.display = "flex";
        }

        function hideBanner() {
            banner.style.animation = "w13cb-up .3s reverse";
            setTimeout(function () { banner.style.display = "none"; fab.style.display = "flex"; }, 280);
        }
        function closeModal() { modal.classList.remove("open"); }
        function acceptAll()  { applyConsent(writePrefs(true, true));   hideBanner(); closeModal(); }
        function declineAll() { applyConsent(writePrefs(false, false)); hideBanner(); closeModal(); }

        document.getElementById("w13cb-accept").addEventListener("click", acceptAll);
        document.getElementById("w13cb-decline").addEventListener("click", declineAll);
        document.getElementById("w13cb-manage").addEventListener("click", function () { modal.classList.add("open"); });

        tA.addEventListener("click", function () { tog(tA, tA.getAttribute("aria-checked") === "false"); });
        tM.addEventListener("click", function () { tog(tM, tM.getAttribute("aria-checked") === "false"); });

        document.getElementById("w13cm-close").addEventListener("click", closeModal);
        document.getElementById("w13cm-decline").addEventListener("click", declineAll);
        document.getElementById("w13cm-save").addEventListener("click", function () {
            var a = tA.getAttribute("aria-checked") === "true";
            var m = tM.getAttribute("aria-checked") === "true";
            applyConsent(writePrefs(a, m));
            hideBanner();
            closeModal();
        });

        fab.addEventListener("click", function () { window.w13OpenConsent(); });
        fab.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") { e.preventDefault(); window.w13OpenConsent(); }
        });

        modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && modal.classList.contains("open")) closeModal();
        });
    });

}());

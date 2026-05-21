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

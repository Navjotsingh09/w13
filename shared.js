/* W13 — Shared navbar interactions (used by every page) */
(function () {
    'use strict';

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

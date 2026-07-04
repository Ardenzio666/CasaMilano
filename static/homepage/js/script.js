/* =========================
   CASA MILANO - GLOBAL JS
========================= */

document.addEventListener('DOMContentLoaded', function () {
    initTooltips();
    initRevealSections();
});

/* =========================
   BOOTSTRAP TOOLTIPS
========================= */

function initTooltips() {
    if (window.jQuery && typeof $('[data-toggle="tooltip"]').tooltip === 'function') {
        $('[data-toggle="tooltip"]').tooltip();
    }
}

/* =========================
   REVEAL ON SCROLL
========================= */

function initRevealSections() {
    const revealElements = document.querySelectorAll('.reveal-section, .reveal');

    if (!revealElements.length) return;

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (reduceMotion || !('IntersectionObserver' in window)) {
        revealElements.forEach(function (el) {
            el.classList.add('is-visible');
        });
        return;
    }

    const observer = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(function (el) {
        observer.observe(el);
    });
}
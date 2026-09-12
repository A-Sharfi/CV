// Scroll-reveal: add .in-view when a .reveal element enters the viewport.
(function () {
    function wire() {
        var els = document.querySelectorAll(".reveal:not(.wired)");
        if (!("IntersectionObserver" in window)) {
            els.forEach(function (el) { el.classList.add("in-view", "wired"); });
            return;
        }
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.classList.add("in-view");
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.12 });
        els.forEach(function (el) { el.classList.add("wired"); io.observe(el); });
    }

    document.addEventListener("DOMContentLoaded", wire);
    var tries = 0;
    var iv = setInterval(function () {
        wire();
        if (++tries > 20) clearInterval(iv);
    }, 300);
})();

// Anchor navigation. Dash renders the page after the initial HTML, so the
// browser's native "#section" jump misses. Handle clicks ourselves, and honour
// a hash present on first load once the target exists.
(function () {
    var NAV_OFFSET = 72;  // clear the sticky bar

    function scrollToId(id, behavior) {
        var el = document.getElementById(id);
        if (!el) return false;
        var y = el.getBoundingClientRect().top + window.pageYOffset - NAV_OFFSET;
        window.scrollTo({ top: y, behavior: behavior || "smooth" });
        return true;
    }

    document.addEventListener("click", function (event) {
        var link = event.target && event.target.closest
            ? event.target.closest('a[href^="#"]')
            : null;
        if (!link) return;
        var id = link.getAttribute("href").slice(1);
        if (id && scrollToId(id, "smooth")) {
            event.preventDefault();
            history.replaceState(null, "", "#" + id);
        }
    });

    if (window.location.hash.length > 1) {
        var target = window.location.hash.slice(1);
        var attempts = 0;
        var timer = setInterval(function () {
            if (scrollToId(target, "auto") || ++attempts > 40) clearInterval(timer);
        }, 150);
    }
})();

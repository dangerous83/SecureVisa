/* =====================================================================
   SecureVisa Group — interactions
   Vanilla JS, no dependencies. Mirrors what Webflow Interactions (IX2)
   and a small custom code embed would handle.
   ===================================================================== */
(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Sticky navbar shadow on scroll ---------- */
  var nav = document.querySelector("[data-nav]");
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle("is-scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Mobile menu ---------- */
  var burger = document.querySelector("[data-burger]");
  var mobileMenu = document.querySelector("[data-mobile-menu]");
  if (burger && mobileMenu) {
    var toggleMenu = function (open) {
      var expanded = open != null ? open : burger.getAttribute("aria-expanded") !== "true";
      burger.setAttribute("aria-expanded", String(expanded));
      mobileMenu.hidden = !expanded;
      document.body.style.overflow = expanded ? "hidden" : "";
    };
    burger.addEventListener("click", function () { toggleMenu(); });
    mobileMenu.addEventListener("click", function (e) {
      if (e.target.tagName === "A") toggleMenu(false);
    });
    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !mobileMenu.hidden) toggleMenu(false);
    });
  }

  /* ---------- Regulator tabs ---------- */
  var tabsRoot = document.querySelector("[data-tabs]");
  if (tabsRoot) {
    var tabs = Array.prototype.slice.call(tabsRoot.querySelectorAll(".reg_tab"));
    var panels = Array.prototype.slice.call(tabsRoot.querySelectorAll(".regulator-card"));
    var activate = function (key) {
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-tab") === key;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", String(on));
      });
      panels.forEach(function (p) {
        p.hidden = p.getAttribute("data-panel") !== key;
      });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { activate(t.getAttribute("data-tab")); });
      // Roving keyboard navigation
      t.addEventListener("keydown", function (e) {
        if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
        e.preventDefault();
        var next = e.key === "ArrowRight" ? (i + 1) % tabs.length : (i - 1 + tabs.length) % tabs.length;
        tabs[next].focus();
        activate(tabs[next].getAttribute("data-tab"));
      });
    });
  }

  /* ---------- FAQ: single-open accordion ---------- */
  var faq = document.querySelector("[data-faq]");
  if (faq) {
    var items = Array.prototype.slice.call(faq.querySelectorAll("details"));
    items.forEach(function (item) {
      item.addEventListener("toggle", function () {
        if (item.open) {
          items.forEach(function (other) { if (other !== item) other.open = false; });
        }
      });
    });
  }

  /* ---------- Reveal + animate dashboard metrics ---------- */
  var animateDash = function (root) {
    // Audit readiness gauge
    var gauge = root.querySelector("[data-gauge]");
    if (gauge) {
      var pct = parseInt(gauge.getAttribute("data-gauge"), 10) || 0;
      var ring = gauge.querySelector("[data-gauge-ring]");
      var C = 2 * Math.PI * 50; // r=50
      if (ring) {
        ring.style.strokeDasharray = C;
        ring.style.strokeDashoffset = reduceMotion ? C * (1 - pct / 100)
          : C; // start empty, then fill
        if (!reduceMotion) {
          requestAnimationFrame(function () {
            ring.style.strokeDashoffset = C * (1 - pct / 100);
          });
        }
      }
      var counter = gauge.querySelector("[data-count]");
      if (counter) countUp(counter, pct);
    }
    // Progress bars
    root.querySelectorAll("[data-progress]").forEach(function (bar) {
      var v = parseInt(bar.getAttribute("data-progress"), 10) || 0;
      bar.style.width = v + "%";
    });
  };

  function countUp(el, target) {
    if (reduceMotion) { el.textContent = target; return; }
    var start = null, dur = 1200;
    var step = function (ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(target * easeOut(p));
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = target;
    };
    requestAnimationFrame(step);
  }
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

  var dash = document.querySelector(".compliance-dashboard");
  if (dash) {
    if ("IntersectionObserver" in window && !reduceMotion) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { animateDash(dash); io.disconnect(); }
        });
      }, { threshold: 0.3 });
      io.observe(dash);
    } else {
      animateDash(dash);
    }
  }

  /* ---------- Generic on-scroll reveal for cards ---------- */
  if ("IntersectionObserver" in window && !reduceMotion) {
    var revealEls = document.querySelectorAll(
      ".ind_card, .proc_step, .case_card, .eco_nodes li, .regulator-card"
    );
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.style.opacity = "1";
          en.target.style.transform = "none";
          ro.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el, i) {
      el.style.opacity = "0";
      el.style.transform = "translateY(16px)";
      el.style.transition = "opacity .5s ease " + (i % 6 * 0.05) + "s, transform .5s ease " + (i % 6 * 0.05) + "s";
      ro.observe(el);
    });
  }

  /* ---------- Class-based reveal for [data-reveal] (heroes, NEXUS, etc.) ---------- */
  if ("IntersectionObserver" in window && !reduceMotion) {
    var dro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-visible"); dro.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -10% 0px" });
    Array.prototype.forEach.call(document.querySelectorAll("[data-reveal]"), function (el) {
      // stagger siblings that share a parent
      var sibs = el.parentElement ? el.parentElement.querySelectorAll(":scope > [data-reveal]") : [el];
      var idx = Array.prototype.indexOf.call(sibs, el);
      if (idx > 0) el.style.transitionDelay = (Math.min(idx, 6) * 0.07).toFixed(2) + "s";
      dro.observe(el);
    });
  } else {
    Array.prototype.forEach.call(document.querySelectorAll("[data-reveal]"), function (el) {
      el.classList.add("is-visible");
    });
  }

  /* ---------- Subtle parallax on photographic backdrops ---------- */
  if (!reduceMotion && window.matchMedia("(min-width: 768px)").matches) {
    var pxImgs = Array.prototype.slice.call(document.querySelectorAll("[data-parallax] img"));
    if (pxImgs.length) {
      var ticking = false;
      var updatePx = function () {
        pxImgs.forEach(function (img) {
          var host = img.parentElement;
          var r = host.getBoundingClientRect();
          if (r.bottom < 0 || r.top > window.innerHeight) return;
          var prog = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
          img.style.transform = "scale(1.12) translateY(" + (prog * 22).toFixed(1) + "px)";
        });
        ticking = false;
      };
      window.addEventListener("scroll", function () {
        if (!ticking) { ticking = true; requestAnimationFrame(updatePx); }
      }, { passive: true });
      updatePx();
    }
  }
})();

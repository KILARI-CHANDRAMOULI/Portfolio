/* Portfolio interactions: typing hero, scroll reveal, nav state, counters. */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initNavbar();
    initScrollProgress();
    initTyping();
    initReveal();
    initSkillBars();
    initCounters();
    initScrollSpy();
    initSmoothAnchors();
  });

  /* ---- Navbar background on scroll ---- */
  function initNavbar() {
    var nav = document.querySelector(".navbar-portfolio");
    if (!nav) return;
    var apply = function () {
      nav.classList.toggle("scrolled", window.scrollY > 24);
    };
    apply();
    window.addEventListener("scroll", apply, { passive: true });
  }

  /* ---- Thin progress bar at the top of the page ---- */
  function initScrollProgress() {
    var bar = document.getElementById("scroll-progress");
    if (!bar) return;
    window.addEventListener(
      "scroll",
      function () {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = h > 0 ? (window.scrollY / h) * 100 + "%" : "0%";
      },
      { passive: true }
    );
  }

  /* ---- Hero typing animation ---- */
  function initTyping() {
    var el = document.getElementById("typed-text");
    if (!el) return;

    var roles;
    try {
      roles = JSON.parse(el.dataset.roles || "[]");
    } catch (e) {
      roles = [];
    }
    if (!roles.length) return;

    var roleIndex = 0;
    var charIndex = 0;
    var deleting = false;

    function tick() {
      var current = roles[roleIndex];
      el.textContent = current.substring(0, charIndex);

      var delay = deleting ? 45 : 85;

      if (!deleting && charIndex === current.length) {
        delay = 1700;
        deleting = true;
      } else if (deleting && charIndex === 0) {
        deleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
        delay = 350;
      } else {
        charIndex += deleting ? -1 : 1;
      }
      setTimeout(tick, delay);
    }
    tick();
  }

  /* ---- Reveal elements as they enter the viewport ---- */
  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    if (!("IntersectionObserver" in window)) {
      items.forEach(function (i) {
        i.classList.add("visible");
      });
      return;
    }

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var delay = parseInt(entry.target.dataset.delay || "0", 10);
            setTimeout(function () {
              entry.target.classList.add("visible");
            }, delay);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    items.forEach(function (item) {
      io.observe(item);
    });
  }

  /* ---- Animate skill proficiency bars into place ---- */
  function initSkillBars() {
    var bars = document.querySelectorAll(".skill-bar > span");
    if (!bars.length || !("IntersectionObserver" in window)) {
      bars.forEach(function (b) {
        b.style.width = (b.dataset.value || 0) + "%";
      });
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.style.width = (entry.target.dataset.value || 0) + "%";
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    bars.forEach(function (b) {
      io.observe(b);
    });
  }

  /* ---- Count-up for the stats strip ---- */
  function initCounters() {
    var counters = document.querySelectorAll("[data-count]");
    if (!counters.length) return;

    var run = function (el) {
      var target = parseFloat(el.dataset.count);
      var suffix = el.dataset.suffix || "";
      var decimals = (el.dataset.count.split(".")[1] || "").length;
      var started = null;
      var duration = 1400;

      function step(ts) {
        if (!started) started = ts;
        var progress = Math.min((ts - started) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = (target * eased).toFixed(decimals) + suffix;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    };

    if (!("IntersectionObserver" in window)) {
      counters.forEach(run);
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            run(entry.target);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach(function (c) {
      io.observe(c);
    });
  }

  /* ---- Highlight the nav link for the section in view ---- */
  function initScrollSpy() {
    var sections = document.querySelectorAll("section[id]");
    var links = document.querySelectorAll(".navbar-portfolio .nav-link[href^='#']");
    if (!sections.length || !links.length) return;

    window.addEventListener(
      "scroll",
      function () {
        var pos = window.scrollY + 140;
        var currentId = "";
        sections.forEach(function (section) {
          if (pos >= section.offsetTop) currentId = section.id;
        });
        links.forEach(function (link) {
          link.classList.toggle("active", link.getAttribute("href") === "#" + currentId);
        });
      },
      { passive: true }
    );
  }

  /* ---- Close the mobile menu after clicking an in-page link ---- */
  function initSmoothAnchors() {
    var collapse = document.getElementById("navMenu");
    document.querySelectorAll(".navbar-portfolio .nav-link[href*='#']").forEach(function (link) {
      link.addEventListener("click", function () {
        if (collapse && collapse.classList.contains("show") && window.bootstrap) {
          window.bootstrap.Collapse.getOrCreateInstance(collapse).hide();
        }
      });
    });
  }
})();

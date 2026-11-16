// رفتارهای عمومی: منوی موبایل، فوکوس، ورود بخش‌ها و پارالاکس ملایم هرو.
(function () {

  "use strict";

  // تصویر ثابت تا شروع پخش، بعد ویدیوی ابرها.
    // ویدیوی ابرها: فقط بعد از نمایش عکس و اگر کاربر حرکت کمتر نخواسته باشد.
    var heroVideo = document.querySelector(".hero-media__video");
    if (heroVideo && heroVideo.dataset.src) {
      var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!reduceMotion) {
        var startHeroVideo = function () {
          if (heroVideo.dataset.started === "true") {
            return;
          }
          heroVideo.dataset.started = "true";
          heroVideo.addEventListener("playing", function () {
            heroVideo.classList.add("is-playing");
          }, { once: true });
          heroVideo.addEventListener("error", function () {
            heroVideo.classList.remove("is-playing");
          }, { once: true });
          heroVideo.src = heroVideo.dataset.src;
          var attempt = heroVideo.play();
          if (attempt && typeof attempt.catch === "function") {
            attempt.catch(function () {});
          }
        };
        if (document.readyState === "complete") {
          startHeroVideo();
        } else {
          window.addEventListener("load", startHeroVideo);
        }
      }
    }


  var header = document.querySelector("[data-site-header]");
  var menu = document.querySelector("[data-menu]");
  var openButton = document.querySelector("[data-menu-open]");
  var closeButton = document.querySelector("[data-menu-close]");
  var lastFocused = null;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // ورود نرم بخش‌ها؛ فقط عناصری که با .reveal علامت خورده‌اند.
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window && !reduceMotion) {
    document.documentElement.classList.add("has-reveal");
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -10% 0px", threshold: 0.08 }
    );
    Array.prototype.forEach.call(reveals, function (element) {
      observer.observe(element);
    });
  }

  // منوی کشویی خدمات: با هاور و کلیک باز می‌شود، با خروج ماوس نرم محو می‌شود.
  var dropdown = document.querySelector("[data-nav-dd]");
  if (dropdown) {
    var ddToggle = dropdown.querySelector("[data-nav-dd-toggle]");
    var ddMenu = dropdown.querySelector("[data-nav-dd-menu]");
    var ddOpen = false;
    var ddOpenedByHover = false;
    var ddHoverTimer = null;
    var ddCloseTimer = null;

    var clearDropdownTimers = function () {
      if (ddHoverTimer) {
        window.clearTimeout(ddHoverTimer);
        ddHoverTimer = null;
      }
      if (ddCloseTimer) {
        window.clearTimeout(ddCloseTimer);
        ddCloseTimer = null;
      }
    };

    var openDropdown = function (byHover) {
      clearDropdownTimers();
      ddOpenedByHover = Boolean(byHover);
      if (ddOpen) {
        return;
      }
      ddOpen = true;
      dropdown.removeAttribute("data-closing");
      dropdown.setAttribute("data-open", "true");
      ddToggle.setAttribute("aria-expanded", "true");
    };

    var closeDropdown = function () {
      if (!ddOpen) {
        return;
      }
      ddOpen = false;
      clearDropdownTimers();
      ddToggle.setAttribute("aria-expanded", "false");
      // محو نرم؛ بعد از پایان انیمیشن از چیدمان و از دسترس صفحه‌خوان خارج می‌شود.
      dropdown.setAttribute("data-closing", "true");
      ddCloseTimer = window.setTimeout(function () {
        dropdown.removeAttribute("data-open");
        dropdown.removeAttribute("data-closing");
        ddCloseTimer = null;
      }, 240);
    };

    dropdown.addEventListener("pointerenter", function () {
      openDropdown(true);
    });

    dropdown.addEventListener("pointerleave", function () {
      ddHoverTimer = window.setTimeout(function () {
        if (dropdown.contains(document.activeElement)) {
          return;
        }
        closeDropdown();
        ddOpenedByHover = false;
      }, 220);
    });

    ddToggle.addEventListener("click", function () {
      if (ddOpen) {
        if (ddOpenedByHover) {
          ddOpenedByHover = false;
          return;
        }
        closeDropdown();
      } else {
        openDropdown(false);
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && ddOpen) {
        closeDropdown();
        ddToggle.focus();
      }
    });

    document.addEventListener("click", function (event) {
      if (ddOpen && !dropdown.contains(event.target)) {
        closeDropdown();
      }
    });

    ddMenu.addEventListener("focusout", function (event) {
      if (!dropdown.contains(event.relatedTarget)) {
        closeDropdown();
      }
    });
  }

  // حرکت لوگوها و گرافیک‌ها فقط وقتی در دید هستند.
  var motionTargets = document.querySelectorAll(".service-logo, .feature-graphic");
  if (motionTargets.length) {
    if ("IntersectionObserver" in window) {
      var motionObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            entry.target.setAttribute("data-in-view", entry.isIntersecting ? "true" : "false");
          });
        },
        { rootMargin: "120px 0px" }
      );
      Array.prototype.forEach.call(motionTargets, function (target) {
        motionObserver.observe(target);
      });
    } else {
      Array.prototype.forEach.call(motionTargets, function (target) {
        target.setAttribute("data-in-view", "true");
      });
    }
  }

  if (!menu || !openButton) {
    return;
  }

  var focusable = function () {
    return Array.prototype.slice.call(
      menu.querySelectorAll('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])')
    );
  };

  var open = function () {
    lastFocused = document.activeElement;
    menu.hidden = false;
    document.body.classList.add("has-overlay");
    openButton.setAttribute("aria-expanded", "true");
    var first = focusable()[0];
    if (first) {
      first.focus();
    }
    document.addEventListener("keydown", onKeydown);
  };

  var close = function (restoreFocus) {
    menu.hidden = true;
    document.body.classList.remove("has-overlay");
    openButton.setAttribute("aria-expanded", "false");
    document.removeEventListener("keydown", onKeydown);
    if (restoreFocus && lastFocused) {
      lastFocused.focus();
    }
  };

  var onKeydown = function (event) {
    if (event.key === "Escape") {
      event.preventDefault();
      close(true);
      return;
    }
    if (event.key !== "Tab") {
      return;
    }
    var items = focusable();
    if (!items.length) {
      return;
    }
    var first = items[0];
    var last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };

  openButton.addEventListener("click", open);
  if (closeButton) {
    closeButton.addEventListener("click", close.bind(null, true));
  }

  menu.addEventListener("click", function (event) {
    var link = event.target.closest("a[href]");
    if (link && !link.getAttribute("href").startsWith("#")) {
      close(false);
    }
  });

  window.addEventListener("resize", function () {
    if (!menu.hidden && window.innerWidth >= 900) {
      close(false);
    }
  });


  // احترام به کاهش حرکت برای انیمیشن‌های SMIL داخل هیرو.
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.querySelectorAll(".hero-media__motion").forEach(function (svg) {
      if (typeof svg.pauseAnimations === "function") {
        svg.pauseAnimations();
      }
    });
  }
})();

// رفتارهای عمومی: منوی موبایل، فوکوس، ورود بخش‌ها و پارالاکس ملایم هرو.
(function () {
  "use strict";

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

  // پارالاکس ملایم تصویر هرو روی ماوس؛ در لمس و کاهش حرکت غیرفعال است.
  var art = document.querySelector("[data-hero-art]");
  var hero = art ? art.closest(".hero") : null;
  if (art && hero && !reduceMotion && window.matchMedia("(pointer: fine)").matches) {
    hero.addEventListener("pointermove", function (event) {
      var rect = hero.getBoundingClientRect();
      var dx = (event.clientX - rect.left) / rect.width - 0.5;
      var dy = (event.clientY - rect.top) / rect.height - 0.5;
      art.style.transform = "translate3d(" + (dx * 18).toFixed(1) + "px," + (dy * 12).toFixed(1) + "px,0)";
    });
    hero.addEventListener("pointerleave", function () {
      art.style.transform = "";
    });
  }

  // پیش‌نمایش تصویر دسته هنگام حرکت ماوس روی ردیف‌ها؛ روی لمس وجود ندارد.
  var previewRows = document.querySelectorAll("[data-preview]");
  if (
    previewRows.length &&
    !reduceMotion &&
    window.matchMedia("(pointer: fine)").matches
  ) {
    var preview = null;

    var ensurePreview = function () {
      if (!preview) {
        preview = document.createElement("img");
        preview.className = "row-preview";
        preview.alt = "";
        preview.setAttribute("aria-hidden", "true");
        document.body.appendChild(preview);
      }
      return preview;
    };

    Array.prototype.forEach.call(previewRows, function (row) {
      row.addEventListener("pointerenter", function () {
        var element = ensurePreview();
        element.src = row.getAttribute("data-preview");
        element.classList.add("is-on");
      });
      row.addEventListener("pointermove", function (event) {
        if (!preview) {
          return;
        }
        preview.style.transform =
          "translate3d(" + (event.clientX + 26) + "px," + (event.clientY - 110) + "px, 0)";
      });
      row.addEventListener("pointerleave", function () {
        if (preview) {
          preview.classList.remove("is-on");
        }
      });
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

  // نقشهٔ مسیر تأمین: هاور روی هر ایستگاه، همان بخش مسیر را روشن می‌کند.
  var routeFigure = document.querySelector("[data-route]");
  if (routeFigure) {
    var routeItems = routeFigure.querySelectorAll(".route__item");
    Array.prototype.forEach.call(routeItems, function (item) {
      var focus = function () {
        routeFigure.setAttribute("data-focus", item.getAttribute("data-stop"));
      };
      var blur = function () {
        routeFigure.removeAttribute("data-focus");
      };
      item.addEventListener("pointerenter", focus);
      item.addEventListener("pointerleave", blur);
      item.addEventListener("focusin", focus);
      item.addEventListener("focusout", blur);
    });
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
})();

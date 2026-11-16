// جلوگیری از پرش صفحه به محل اسکرول قبلی هنگام رفرش.
// این فایل باید در <head> و بدون defer بارگذاری شود تا پیش از بازیابی مرورگر اجرا شود.
(function () {
  "use strict";

  var entry = performance.getEntriesByType ? performance.getEntriesByType("navigation")[0] : null;
  var isReload = entry && entry.type === "reload";

  if (!isReload || window.location.hash) {
    return;
  }

  if ("scrollRestoration" in history) {
    history.scrollRestoration = "manual";
  }

  // فقط ورودی واقعی کاربر باعث می‌شود دست از بالا بردن صفحه برداریم؛
  // بازیابی خودکار مرورگر نباید «اسکرول کاربر» حساب شود.
  var userMoved = false;
  var markMoved = function () {
    userMoved = true;
  };
  ["wheel", "touchstart", "touchmove", "pointerdown", "keydown"].forEach(function (name) {
    window.addEventListener(name, markMoved, { passive: true, once: true });
  });

  var toTop = function () {
    if (!userMoved) {
      window.scrollTo(0, 0);
    }
  };

  toTop();
  document.addEventListener("DOMContentLoaded", toTop, { once: true });
  window.addEventListener("load", toTop, { once: true });
})();

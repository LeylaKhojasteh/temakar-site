// جلوگیری از پرش صفحه به محل اسکرول قبلی هنگام رفرش.
// این فایل باید در <head> و بدون defer بارگذاری شود تا پیش از بازیابی مرورگر اجرا شود.
(function () {
  "use strict";

  var entry = performance.getEntriesByType ? performance.getEntriesByType("navigation")[0] : null;
  var isReload = entry && entry.type === "reload";

  if (isReload && !window.location.hash) {
    if ("scrollRestoration" in history) {
      history.scrollRestoration = "manual";
    }

    var toTop = function () {
      window.scrollTo(0, 0);
    };

    toTop();

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", toTop);
    }

    window.addEventListener("load", toTop);
  }
})();

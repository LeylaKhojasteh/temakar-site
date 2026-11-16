// تم اولیه پیش از رنگ‌آمیزی صفحه، تا پرش رنگ دیده نشود.
(function () {
  "use strict";

  try {
    var stored = window.localStorage.getItem("temakar-theme");
    var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    var dark = stored ? stored === "dark" : prefersDark;
    if (dark) {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  } catch (error) {
    /* دسترسی به حافظه ممکن نیست؛ تم روشن می‌ماند. */
  }
})();

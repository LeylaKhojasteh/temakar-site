// تم اولیه پیش از رنگ‌آمیزی صفحه، تا پرش رنگ دیده نشود.
// پیش‌فرض روشن است؛ فقط اگر کاربر خودش تیره را انتخاب کرده باشد، تیره می‌شود.
(function () {
  "use strict";

  try {
    if (window.localStorage.getItem("temakar-theme") === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  } catch (error) {
    /* دسترسی به حافظه ممکن نیست؛ تم روشن می‌ماند. */
  }
})();

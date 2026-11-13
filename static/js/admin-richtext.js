// ویرایشگر متن غنی در پنل ادمین: Quill روی textarea سوار می‌شود.
(function () {
  "use strict";

  function init() {
    if (typeof Quill === "undefined") {
      return;
    }

    var editors = document.querySelectorAll("textarea[data-richtext]");

    Array.prototype.forEach.call(editors, function (textarea) {
      var holder = document.createElement("div");
      holder.className = "rich-editor";
      textarea.parentNode.insertBefore(holder, textarea);
      textarea.classList.add("visually-hidden");

      var quill = new Quill(holder, {
        theme: "snow",
        modules: {
          toolbar: [
            [{ header: [2, 3, false] }],
            ["bold", "italic", "underline"],
            [{ list: "ordered" }, { list: "bullet" }],
            ["blockquote", "link"],
            ["clean"],
          ],
        },
      });

      quill.clipboard.dangerouslyPasteHTML(textarea.value || "");

      // Quill منوهای خودش را بدون نام دسترس‌پذیر می‌سازد.
      Array.prototype.forEach.call(
        document.querySelectorAll(".ql-picker-label[aria-controls]"),
        function (control) {
          control.setAttribute("aria-label", "سطح سرتیتر");
        }
      );

      var sync = function () {
        textarea.value = quill.root.innerHTML;
      };

      quill.on("text-change", sync);
      if (textarea.form) {
        textarea.form.addEventListener("submit", sync);
      }
    });
  }

  // اسکریپت‌های ادمین در head بارگذاری می‌شوند، پس تا آماده‌شدن DOM صبر می‌کنیم.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

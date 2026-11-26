// ویرایشگر متن غنی: Quill با درج مستقیم عکس.
(function () {
  "use strict";

  function init() {
    if (typeof Quill === "undefined") return;

    var editors = document.querySelectorAll("textarea[data-richtext]");
    Array.prototype.forEach.call(editors, function (textarea) {
      var holder = document.createElement("div");
      holder.className = "rich-editor";
      textarea.parentNode.insertBefore(holder, textarea);
      textarea.classList.add("visually-hidden");

      var quill = new Quill(holder, {
        theme: "snow",
        modules: {
          toolbar: {
            container: [
              [{ header: [2, 3, false] }],
              ["bold", "italic", "underline"],
              [{ list: "ordered" }, { list: "bullet" }],
              ["blockquote", "link", "image"],
              ["clean"],
            ],
            handlers: {
              image: function () {
                var input = document.createElement("input");
                input.type = "file";
                input.accept = "image/*";
                input.addEventListener("change", function () {
                  if (!input.files || !input.files[0]) return;
                  var data = new FormData();
                  data.append("image", input.files[0]);
                  var csrf = document.querySelector('[name=csrfmiddlewaretoken]');
                  fetch(window.TEMAKAR_UPLOAD_URL || "/manage/upload-image/", {
                    method: "POST",
                    body: data,
                    credentials: "same-origin",
                    headers: csrf ? { "X-CSRFToken": csrf.value } : {},
                  })
                    .then(function (r) { return r.json(); })
                    .then(function (res) {
                      if (!res.url) return;
                      var range = quill.getSelection(true);
                      quill.insertEmbed(range.index, "image", res.url, "user");
                      quill.setSelection(range.index + 1, 0);
                    })
                    .catch(function () {});
                });
                input.click();
              },
            },
          },
        },
      });

      quill.clipboard.dangerouslyPasteHTML(textarea.value || "");

      var sync = function () { textarea.value = quill.root.innerHTML; };
      quill.on("text-change", sync);
      if (textarea.form) textarea.form.addEventListener("submit", sync);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

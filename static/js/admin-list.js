// ورودی‌های ویرایش درون‌خطی فهرست ادمین برچسب دسترس‌پذیر ندارند.
(function () {
  "use strict";

  var labels = {
    "field-order": "ترتیب نمایش",
    "field-is_active": "فعال",
    "field-is_featured": "منتخب برای صفحهٔ اصلی",
  };

  function labelEditableCells() {
    var rows = document.querySelectorAll("#result_list tbody tr");
    Array.prototype.forEach.call(rows, function (row) {
      var cells = row.querySelectorAll("td");
      Array.prototype.forEach.call(cells, function (cell) {
        var field = null;
        for (var index = 0; index < cell.classList.length; index += 1) {
          if (cell.classList[index].indexOf("field-") === 0) {
            field = cell.classList[index];
            break;
          }
        }
        if (!field || !labels[field]) {
          return;
        }
        var input = cell.querySelector("input, select, textarea");
        if (input && !input.getAttribute("aria-label")) {
          input.setAttribute("aria-label", labels[field]);
        }
      });
    });
  }

  // اسکریپت‌های ادمین در head بارگذاری می‌شوند.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", labelEditableCells);
  } else {
    labelEditableCells();
  }
})();

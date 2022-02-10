document.addEventListener("DOMContentLoaded", function () {
  const CLASSNAME_HIDDEN = "hidden";
  document
    .querySelector("[data-reveal='pass']")
    .addEventListener("click", (e) => {
      const attr = e.target.getAttribute("data-reveal");
      if (e.target.checked) {
        document
          .querySelectorAll(`[data-revealed="${attr}"]`)
          .forEach((el) => (el.type = "text"));
      } else {
        document
          .querySelectorAll(`[data-revealed="${attr}"]`)
          .forEach((el) => (el.type = "password"));
      }
    });

  const edit_els = document.querySelectorAll("a[data-edit]");
  for (let i = 0; i < edit_els.length; i++) {
    edit_els[i].addEventListener("click", (e) => {
      document
        .querySelector(
          `div[data-reveal="${e.target.getAttribute("data-edit")}"]`
        )
        .classList.toggle(CLASSNAME_HIDDEN);
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const CLASSNAME_HIDDEN = "hidden";
  document.getElementById("reveal").addEventListener("click", () => {
    if (document.getElementById("reveal").checked) {
      document.getElementById("password").type = "text";
      document.getElementById("confirm").type = "text";
    } else {
      document.getElementById("password").type = "password";
      document.getElementById("confirm").type = "password";
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

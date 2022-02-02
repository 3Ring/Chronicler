const HIDDEN = "hidden";

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("select").forEach((sel) => set_select_title(sel));
  set_reveals();
});

/**
 * Creates an unselectable title card select element
 * @param sel - the select element to modify
 */
function set_select_title(sel) {
  let opt = document.createElement("option");
  opt.setAttribute("selected", true);
  opt.setAttribute("hidden", true);
  opt.setAttribute("value", "");
  opt.innerHTML = "Choose Your Character";
  sel.insertAdjacentElement("afterbegin", opt);
}


/**
 * reveals form associated with clicked button and resets all forms
 */
function set_reveals() {
  document.querySelectorAll("[data-reveal]").forEach((el) =>
    el.addEventListener("click", (e) => {
      document
        .querySelectorAll("[data-revealed]")
        .forEach((el) =>
          check_and_reveal(el, e.target.getAttribute("data-reveal"))
        );
      document.querySelectorAll("form").forEach((el) => el.reset());
    })
  );
}

/**
  hides and reveals correct element os that only one form is visible at a time
 * @param el - The element to check.
 * @param attr - The attribute that will be checked.
 */
function check_and_reveal(el, attr) {
  el.getAttribute("data-revealed") == attr
    ? el.classList.toggle(HIDDEN)
    : el.classList.add(HIDDEN);
}

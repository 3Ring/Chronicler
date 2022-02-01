const HIDDEN = "hidden";

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("select").forEach((sel) => set_select_title(sel));
  set_reveals();
});

function set_select_title(sel) {
  let opt = document.createElement("option");
  opt.setAttribute("selected", true);
  opt.setAttribute("hidden", true);
  opt.setAttribute("value", "");
  opt.innerHTML = "Choose Your Character";
  sel.insertAdjacentElement("afterbegin", opt);
}

function set_reveals() {
  document.querySelectorAll("[data-reveal]").forEach((el) =>
    el.addEventListener("click", (e) => {
      document
        .querySelectorAll("[data-revealed]")
        .forEach((el) =>
          check_and_reveal(el, e.target.getAttribute("data-reveal"))
        );
    })
  );
}

function check_and_reveal(el, attr) {
  el.getAttribute("data-revealed") == attr
    ? el.classList.remove(HIDDEN)
    : el.classList.add(HIDDEN);
}

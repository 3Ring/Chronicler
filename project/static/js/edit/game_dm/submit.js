document.addEventListener("DOMContentLoaded", () => {
  confirmation_listeners();
  final_confirmation_listeners();
});

function confirmation_listeners() {
  const els = document.querySelectorAll("form[data-remove='submit']");
  els.forEach((el) =>
    el.addEventListener("submit", (e) => {
      e.preventDefault();
      const select = e.target.querySelector("select");
      const i = select.selectedIndex;
      const attr = el.getAttribute("data-flag");
      if (i > 0) {
        e.target.classList.add(HIDDEN);
        const confirm = document.querySelector(`form[data-confirm="${attr}"]`);
        confirm.querySelector(
          `h2[data-flag="header"]`
        ).innerHTML = `Do you wish to remove ${select.childNodes[i].innerHTML} and all of their characters from ${game_name}?`;
        confirm.classList.remove(HIDDEN);
      }
    })
  );
}
function final_confirmation_listeners() {
  const confirms = document.querySelectorAll(`form[data-cancel]`);
  for (let i = 0; i < confirms.length; i++) {
    confirm(confirms[i]);
    cancel(confirms[i]);
  }
}
function confirm(confirms) {
  const el = confirms.querySelector(`a[data-confirm]`);
  if (el) {
    const attr = el.getAttribute("data-confirm");
    el.addEventListener("click", () => {
      const form = document.querySelector(`form[data-flag="${attr}"`);
      form.submit();
    });
  }
}
function cancel(confirms) {
  const el = confirms.querySelector(`a[data-cancel="cancel"]`);
  if (el) {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      hide_rms();
      hide_confirms();
    });
  }
}

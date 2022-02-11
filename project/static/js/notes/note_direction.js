document.addEventListener("DOMContentLoaded", function () {
    set_direction();
});

function set_direction() {
    const button = document.querySelector(`button[data-flag="note_direction"`);
    if (button) {
      button.addEventListener("click", () => {
        const els = document.querySelectorAll(`ul[data-flag="note_list"]`);
        for (let i = 0; i < els.length; i++) {
          els[i].classList.toggle("reverse");
          button.classList.toggle("fa-sort-numeric-down");
          button.classList.toggle("fa-sort-numeric-up-alt");
        }
      });
    }
}

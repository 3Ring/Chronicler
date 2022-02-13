const HIDDEN = "hidden";
/* 
functions to reveal/hide forms
*/
document.addEventListener("DOMContentLoaded", () => {
  reveal_form_if_errors();
  document.querySelectorAll(`div[data-form]`).forEach((form) => reveal(form));
  final_confirmation_listeners();
});

/**
 * If there are errors, reveal the corresponding form
 */
function reveal_form_if_errors() {
  if (error_target) {
    document
      .querySelector(`form[data-form="${error_target}"]`)
      .classList.remove(HIDDEN);
  }
}

/**
 * Reveal the hidden content of a page when a user clicks on a link
 * @param el - the parent element that contains the links
 */
function reveal(el) {
  const els = el.querySelectorAll("a[data-reveal]");
  for (let i = 0; i < els.length; i++) {
    const attr = els[i].getAttribute("data-reveal");
    els[i].addEventListener("click", (e) => {
      e.preventDefault();
      el.querySelectorAll(`[data-flag="${attr}"]`).forEach((r) =>
        r.classList.toggle(HIDDEN)
      );
      hide_confirms();
      hide_rms(attr);
      document.querySelectorAll("form").forEach((form) => form.reset());
    });
  }
}
/**
 * Hide all the forms that have a `data-confirm` attribute
 */
function hide_confirms() {
  document
    .querySelectorAll(`form[data-confirm]`)
    .forEach((el) => el.classList.add(HIDDEN));
}
/**
 * Hide all the forms with the `data-remove` attribute that don't have the `data-flag` attribute set to
 * the value of `attr`
 * @param [attr=null] - The `data-remove` value that you want to exclude.
 */
function hide_rms(attr = null) {
  const rms = document.querySelectorAll(`form[data-remove]`);
  for (let i = 0; i < rms.length; i++) {
    if (rms[i].getAttribute("data-flag") != attr) {
      rms[i].classList.add(HIDDEN);
    }
  }
}




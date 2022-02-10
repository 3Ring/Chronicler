/*
 functions to set correct form values and information 
*/
document.addEventListener("DOMContentLoaded", () => {
  init_published_checkbox_value();
  if (players) {
    create_select_element_title_cards();
  }
});

/**
 * set published checkbox in game_edit form to its correct value
 */
function init_published_checkbox_value() {
  const pub = document.querySelector("input[data-published]");
  pub.getAttribute("data-published") == "True"
    ? (pub.checked = true)
    : (pub.checked = false);
}

/**
 * Create and insert a title card as the top option for each select element
 */
function create_select_element_title_cards() {
  const el = document.querySelectorAll("select");
  for (let i = 0; i < el.length; i++) {
    let title = document.createElement("option");
    title.setAttribute("selected", true);
    title.setAttribute("hidden", true);
    title.setAttribute("value", "");
    title.innerHTML = `Choose ${el[i].getAttribute("data-type")} to remove`;
    el[i].insertAdjacentElement("afterbegin", title);
  }
}

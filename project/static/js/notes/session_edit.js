var session_menu_deployed = false;
var session_edit_form_deployed = false;
var session_edit_hidden_class = className__hidden;

/*
Main function
*/
function Session_Editor() {
  if (user_is_dm) {
    session_add_contextual_listeners();
    session_edit_add_submit_listeners();
    session_add_cancel_listener();
  }
}

/*
Event Listeners
*/
function session_add_contextual_listeners() {
  document.addEventListener("click", function (e) {
    session_context_menu(e);
  });
}
function session_add_cancel_listener() {
  document.addEventListener("click", function (e) {
    if (click_from_session_form_cancel()) {
      let id_num = e.target.getAttribute("data-formEditSession_buttonCancel");
      toggle_session_edit_off(id_num);
    }
  });
}
function session_edit_add_submit_listeners() {
  var session_edit_forms = document.querySelectorAll(
    `form[data-flag='formEditSession_form']`
  );
  for (let i = 0; i < session_edit_forms.length; i++) {
    session_edit_forms[i].addEventListener("submit", function (e) {
      edit_session_func(e);
    });
  }
}

/*
Event Logic
*/
function session_context_menu(e) {
  if (!session_edit_form_deployed) {
    if (!session_menu_deployed) {
      if (click_from_session_edit_button(e)) {
        session_context_menu_deployment(e);
      }
    }
    // check if the click happened within the contextual form
    else if (click_from_session_menu(e)) {
      session_context_menu_interior(e);
    } else {
      toggle_session_menus_off();
    }
  }
}
function session_context_menu_deployment(e) {
  // deploy session context menu
  // if statement is because the user can click the container which would throw an error otherwise
  if (e.target.getAttribute("data-id_editSessionImage")) {
    let target_id = e.target.getAttribute("data-id_editSessionImage");
    let target_element = document.querySelector(
      `div[data-sessionContextMenuId="${target_id}"]`
    );
    toggle_session_menu_on(target_element);
  }
}
function session_context_menu_interior(e) {
  if (session_menu_deployed) {
    // check if the click happened within the edit menu
    if (click_from_session_context_button()) {
      let id_num = e.target.getAttribute("data-editMenuId");
      // if the edit button was clicked
      if (e.target.getAttribute("data-action") == "edit") {
        e.preventDefault();
        toggle_session_edit_on(id_num);
        toggle_session_menus_off();
        // if the delete button was clicked
      } else {
        toggle_session_menus_off();
        delete_session(id_num);
      }
    }
  }
}

/*
Context menu and edit form actions
*/
function delete_session(id_num) {
  // TODO
  console.log("delete", id_num);
}
function edit_session_func(event) {
  let id_num = event.target.getAttribute("data-sid");
  event.preventDefault();
  let number = document.querySelector(
    `input[data-session_edit_number="${id_num}"]`
  );
  let title = document.querySelector(
    `input[data-session_edit_title="${id_num}"]`
  );
  socket.emit("edit_session", id_num, number.value, title.value);
  toggle_session_edit_off(id_num);
}

/*
Context menu deployment functions
*/
function toggle_session_menu_on(element) {
  if (element.classList.contains(className__active)) {
  } else {
    session_edit_reveal_element(element);
    session_menu_deployed = true;
  }
}
function toggle_session_menus_off() {
  let sessionMenus = document.querySelectorAll(
    `div[data-flag='sessionContextMenu']`
  );
  for (let i = 0; i < sessionMenus.length; i++) {
    if (!sessionMenus[i].classList.contains(className__hidden)) {
      sessionMenus[i].classList.add(className__hidden);
    }
    if (sessionMenus[i].classList.contains(className__active)) {
      sessionMenus[i].classList.remove(className__active);
    }
  }
  session_menu_deployed = false;
}

/*
Session edit form deployment functions
*/
function toggle_session_edit_on(id_num) {
  let el = document.querySelector(
    `div[data-session_edit_form_container="${id_num}"]`
  );
  session_edit_reveal_element(el);
  session_edit_form_deployed = true;
}
function toggle_session_edit_off(id_num) {
  let el = document.querySelector(
    `div[data-session_edit_form_container="${id_num}"]`
  );
  session_edit_hide_element(el);
  session_edit_form_deployed = false;
}

/*
Hide/reveal helper functions
*/
function session_edit_hide_element(element) {
  add_hidden_class(element);
  remove_active_class(element);
}
function session_edit_reveal_element(element) {
  remove_hidden_class(element);
  add_active_class(element);
}
function add_hidden_class(element) {
  if (!element.classList.contains(session_edit_hidden_class)) {
    element.classList.add(session_edit_hidden_class);
  }
}
function remove_hidden_class(element) {
  if (element.classList.contains(session_edit_hidden_class)) {
    element.classList.remove(session_edit_hidden_class);
  }
}
function add_active_class(element) {
  if (!element.classList.contains(className__active)) {
    element.classList.add(className__active);
  }
}
function remove_active_class(element) {
  if (element.classList.contains(className__active)) {
    element.classList.remove(className__active);
  }
}

/*
Click event location finders
*/
function click_from_session_edit_button(e) {
  if (click_inside_element(e, "data-sessionEditNumber")) {
    return true;
  }
  return false;
}
function click_from_session_menu(e) {
  if (click_inside_element(e, "data-sessionContextMenuId")) {
    return true;
  }
  return false;
}
function click_from_session_form(e) {
  if (click_inside_element(e, "data-session_edit_form_container")) {
    return true;
  }
  return false;
}
function click_from_session_form_cancel(e) {
  if (click_inside_element(e, "data-formEditSession_buttonCancel")) {
    return true;
  }
  return false;
}
function click_from_session_context_button(e) {
  if (click_inside_element(e, "data-editMenuId")) {
    return true;
  }
  return false;
}

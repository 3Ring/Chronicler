// Note Editor functions
//
//
// //

// Edit button and contextual menu functions
//
// check if element or any of its parents contain the edit button
function click_inside_element(e, attribute) {
  // Local Variables
  let el = e.target;

  // check if element clicked has attribute
  if (el.hasAttribute(attribute)) {
    return el;
  } else {
    // check if any of the parentNodes have the attribute
    while ((el = el.parentNode)) {
      if (el.hasAttribute(attribute)) {
        return el;

        // break before final loop otherwise it will throw an error
      } else if (el.parentNode == document) {
        break;
      }
    }
  }
  return false;
}
// hide all open contextual menues
function toggle_menues_off() {
  // find all context menus
  let contextMenus = document.querySelectorAll("div[data-flag='contextMenu']");

  // check to see if there are any yet
  if (contextMenus.length != 0) {
    // iterate through each element, remove active class name if it exists and hide it
    for (let i = 0; i < contextMenus.length; i++) {
      // remove active class
      if (contextMenus[i].classList.contains(className__active)) {
        contextMenus[i].classList.remove(className__active);
      }
      // add hidden class if not already applied
      if (!contextMenus[i].classList.contains(className__hidden)) {
        contextMenus[i].classList.add(className__hidden);
      }

      // update menu flag
      menu_deployed = false;
    }
  }
}
// deploy context menu
function toggle_menu_on(element) {
  if (element.classList.contains(className__active)) {
  } else {
    element.classList.add(className__active);
    element.classList.remove(className__hidden);
    menu_deployed = true;
  }
}
// Set click events to trigger contextual menu and deploy edit form
function click_listener() {
  document.addEventListener("click", function (e) {
    // check if edit button was clicked
    if (click_inside_element(e, attribute__editButtons)) {
      // check if context  menu is already deployed
      if (menu_deployed == false) {
        // deploy context menu
        // if statement is because the user can click the container which would throw an error otherwise
        if (e.target.getAttribute("data-id_editImage")) {
          let target_id = e.target.getAttribute("data-id_editImage");
          let target_element = document.querySelector(
            `div[data-contextMenuId="${target_id}"]`
          );
          toggle_menu_on(target_element);
        }
      }
    }
    // check if the click happened within the contextual form
    else if (click_inside_element(e, attribute__contextForm)) {
      // check if the click happened within the edit menu
      if (click_inside_element(e, attribute__editMenu)) {
        // if the edit button was clicked
        if (e.target.getAttribute("data-action") == "edit") {
          let id_num = e.target.getAttribute("data-id_note");

          e.preventDefault();
          toggle_form_on(id_num);
          toggle_menues_off();

          // if the delete button was clicked
        } else {
          let id_num = e.target.getAttribute("data-id_note");
          delete_note(id_num);
          menu_deployed = false;
        }
      }
    } else {
      toggle_menues_off();
    }
  });
}

// Note editting form functions
// }
// deploy note editting form
function toggle_form_on(id_num) {
  let quill_edit = new Quill("#QuillEdit_" + id_num, {
    modules: {
      toolbar: [
        ["bold", "italic"],
        [{ size: ["small", false, "large", "huge"] }],
        [{ list: "ordered" }, { list: "bullet" }],
      ],
    },
    placeholder: "A note about this session.",
    theme: "snow",
  });

  // Local variables
  let flag__formEdit = "form[data-id_formEdit='" + id_num + "']",
    flag__notes_noteText = "span[data-id_noteText='" + id_num + "']",
    flag__notes_editImage = "a[data-editButtonAnchorId='" + id_num + "']",
    element__formEdit = document.querySelector(flag__formEdit),
    element__notes_noteText = document.querySelector(flag__notes_noteText),
    element__notes_editImage = document.querySelector(flag__notes_editImage);

  // hide original note
  element__notes_noteText.classList.add(className__hidden);
  element__notes_editImage.remove();
  // element__notes_editImage.classList.add(className__hidden);

  // display edit form
  element__formEdit.classList.remove(className__hidden);

  // insert text into Quill
  let old_html = element__notes_noteText.innerHTML,
    delta = quill_edit.clipboard.convert(old_html);
  quill_edit.setContents(delta, "silent");
}

// hide note editting form
function toggle_form_off(id_num) {
  // Local Variables
  let flag__formEdit = "form[data-id_formEdit='" + id_num + "']",
    form_element = document.querySelector(flag__formEdit);

  // hide form
  form_element.classList.add(className__hidden);
}

// Note edit: capture form data and send data to server
function edit_note_func(id_num, event) {
  // local variables
  // let element__notes_editImage = document.querySelector(`span[data-id_editImage='${id_num}']`);

  // stop page reload
  event.preventDefault();
  // find element and capture data
  // text
  let element__editorParent = document.querySelector(
      `div[data-crumb="${id_num}"]`
    ),
    element__newQuill_speaking_as = document.querySelector(
      `select[name="speaking_as"]`
    ),
    element__formEdit_Editor = element__editorParent.firstElementChild;
  let note_text = element__formEdit_Editor.innerHTML,
    speaking_as = element__newQuill_speaking_as.value;
  // private
  let element__notes_checkboxPrivate = document.querySelector(
    `input[data-id_noteCheckboxPrivate="${id_num}"]`
  );
  if (element__notes_checkboxPrivate) {
    note_private = element__notes_checkboxPrivate.value;
  } else {
    note_private = false;
  }
  // if the note isn't from the dm: the to dm value
  if (user_id != dm_id) {
    let element__notes_checkboxToDm = document.querySelector(
      `input[data-id_noteCheckboxToDm="${id_num}"]`
    );
    var note_to_dm = element__notes_checkboxToDm.value;
  } else {
    var note_to_dm = false;
  }

  // send to server
  socket.emit(
    "edit_note",
    note_text,
    note_private,
    note_to_dm,
    dm_id,
    speaking_as,
    game_id,
    user_id,
    id_num
  );

  // remove form
  toggle_form_off(id_num);
  let element__notes_noteText = document.querySelector(
    `span[data-id_noteText="${id_num}"]`
  );
  element__notes_noteText.classList.remove(className__hidden);
  return false;
}

// Note Delete: hide note element from page and emit delete event to server.
function delete_note(id_num) {
  // Local Variables
  let element__containerNote = document.querySelector(
    `li[data-id_noteCont='${id_num}']`
  );

  // add hidden class to note element
  element__containerNote.classList.add(className__hidden);

  // emit delete event to server
  socket.emit("delete_note", id_num);
}

// Set listener for note edit forms
function submit_listener() {
  // Local Variables
  let elements__formEdit_form = document.querySelectorAll(flag__formEdit_form);

  // set listeners on all note editting forms in document
  for (let i = 0; i < elements__formEdit_form.length; i++) {
    elements__formEdit_form[i].addEventListener("submit", function (event) {
      let id_num = event.target.getAttribute("data-id_formEdit");

      // set function on form that handles the data
      edit_note_func(id_num, event);
    });
  }
}

// tie functions together for init()
function Note_Editor() {
  click_listener();
  submit_listener();
}

// socket.on Functions
//
//
// //

// this is to add logic to notes populated throuck websocket
function filled_note_logic(note_id_number) {
  let socket_inserted_element_note_edit_form = document.querySelector(
    `form[data-id_formedit='${note_id_number}']`
  );
  socket_inserted_element_note_edit_form.addEventListener(
    "submit",
    function (event) {
      let note_id = event.target.getAttribute("data-id_formedit");
      edit_note_func(note_id, event);
    }
  );

  // set_true_checkboxes_to_checked() found in general
  set_true_checkboxes_to_checked();
  new_check_box_logic(note_id_number);
}

// add checkbox logic to new or edittied checkboxes
function new_check_box_logic(note_id_number) {
  let checkbox_draft = document.querySelector(
      `input[data-id_notecheckboxprivate="${note_id_number}"]`
    ),
    checkbox_to_dm = document.querySelector(
      `input[data-id_notecheckboxToDm="${note_id_number}"]`
    );

  checkbox_draft.addEventListener("click", function (event) {
    // find event origin
    let clicked = event.target;
    // change value to opposite of current
    if (clicked.value == "True") {
      clicked.value = "False";
    } else {
      clicked.value = "True";
    }
  });
  if (user_id != dm_id && checkbox_to_dm) {
    checkbox_to_dm.addEventListener("click", function (event) {
      // find event origin
      let clicked = event.target;
      // change value to opposite of current
      if (clicked.value == "True") {
        clicked.value = "False";
      } else {
        clicked.value = "True";
      }
    });
  }
}

socket.on(
  "edit_session",
  function (new_card, new_list, session_number, old_number) {
    if (session_number > current__session_number) {
      current__session_number = session_number;
    }
    replace_session(old_number, new_card, new_list);
    display_editted_session(session_number);
    add_session_listener(session_number);
  }
);

function add_session_listener(session_number) {
  let el = document.querySelector(
    `form[data-snum='${session_number}']`
  );
  el.addEventListener("submit", function (e) {
    edit_session_func(e);
  });
}

function display_editted_session(session_number) {
  let el = document.querySelector(
    `li[data-number_sessionList='${session_number}']`
  );
  display_sessionCont(el);
}
function replace_session(old_number, new_card, new_list) {
  replace_session_list(old_number, new_list);
  replace_session_card(old_number, new_card);
}

function replace_session_list(old_number, new_list) {
  let old_sl = document.querySelector(
    `li[data-number_sessionList='${old_number}']`
  );
  old_sl.insertAdjacentHTML("afterend", new_list);
  old_sl.remove();
}

function replace_session_card(old_number, new_card) {
  let old_sc = document.querySelector(
    `div[data-number_sessionCont='${old_number}']`
  );
  old_sc.insertAdjacentHTML("afterend", new_card);
  old_sc.remove();
}

// Display new Session
socket.on("fill_new_session", function (new_session, new_list, session_number) {
  // remove filler session title if first session
  let filler_session = document.querySelector(
    `li[data-number_sessionList="set_up"]`
  );
  if (filler_session) {
    filler_session.remove();
  }
  // Local Variables

  let element__sessionsContainer = document.querySelector(
      flag__sessionContainer
    ),
    element__sessionsList = document.querySelector(
      "ul[data-flag='sessions_list']"
    );

  remove_activeFlags_sessionList();
  if (session_number > current__session_number) {
    current__session_number = session_number;
  }

  // Insert into document
  element__sessionsContainer.insertAdjacentHTML("afterbegin", new_session);
  element__sessionsList.insertAdjacentHTML("afterbegin", new_list);

  // update "New Session form's default number logic"
  if (session_number > current__session_number) {
    set_new_session_form_highest(session_number);
  }

  element__new_list = document.querySelector(
    "li[data-number_sessionList='" + session_number + "']"
  );
  // hide all elements except the newest
  display_sessionCont(element__new_list);
  element__new_list.classList.add(className__active_sessionList);

  // apply logic

  element__new_list.addEventListener("click", function () {
    apply_sessionHighlightLogic_fromElement(element__new_list);
    // session container
    element__new_session = document.querySelector(
      "div[data-number_sessionCont='" + session_number + "']"
    );
    display_sessionCont(element__new_list);
    set_currentSessionVariable_fromElement(element__new_list);
  });
});

function fill_new_note(new_note, session_number, note_id_number, note_text) {
  // local Variables
  element = document.querySelector(`ul[data-idSession='${session_number}']`);

  // Insert into document
  element.insertAdjacentHTML("beforeend", new_note);

  // apply logic
  filled_note_logic(note_id_number);

  // insert note body
  let element__notes_body = document.querySelector(
    `span[data-id_noteText="${note_id_number}"]`
  );
  element__notes_body.innerHTML = note_text;
}

// display new note
socket.on(
  "fill_new_note",
  function (new_note, note_text, draft, to_dm, note_id, session_number, u_id) {
    let origin_index = 0,
      dm_index = 1,
      other_index = 2;

    if (user_id == u_id) {
      fill_new_note(new_note[origin_index], session_number, note_id, note_text);
    } else if (user_id == dm_id) {
      if (!draft) {
        fill_new_note(new_note[dm_index], session_number, note_id, note_text);
      }
    } else {
      if (!draft && !to_dm) {
        fill_new_note(
          new_note[other_index],
          session_number,
          note_id,
          note_text
        );
      }
    }
  }
);

function insert_socket(editted_note, note_id_number, note_text) {
  // find location of old note and insert new note in its place
  var old_note_location = document.querySelector(
    `li[data-id_notecont="${note_id_number}"]`
  );
  old_note_location.insertAdjacentHTML("afterend", editted_note);
  old_note_location.remove();

  // insert note body
  var element__notes_body = document.querySelector(
    `span[data-id_noteText="${note_id_number}"]`
  );
  element__notes_body.innerHTML = note_text;

  // apply logic
  filled_note_logic(note_id_number);
}

function remove_socket(note_id_number) {
  var old_note_location = document.querySelector(
    `li[data-id_notecont="${note_id_number}"]`
  );
  if (old_note_location) {
    old_note_location.remove();
  }
}

// display note edit
socket.on(
  "fill_note_edit",
  function (
    editted_note,
    note_text,
    draft,
    to_dm,
    note_id_number,
    u_id,
    changed,
    was_not_private,
    was_draft
  ) {
    let origin_index = 0,
      dm_index = 1,
      other_index = 2;
    // user is note origin
    if (user_id == u_id) {
      // note privacy has been changed
      if (changed) {
        // note is now draft
        if (draft) {
          // insert new socket
          insert_socket(editted_note[origin_index], note_id_number, note_text);
          // note is now to dm
        } else if (to_dm) {
          // insert new socket
          insert_socket(editted_note[origin_index], note_id_number, note_text);
          // note is no longer draft
        } else {
          // insert new socket
          insert_socket(editted_note[origin_index], note_id_number, note_text);
        }
        // privacy is the same
      } else {
        // insert new socket
        insert_socket(editted_note[origin_index], note_id_number, note_text);
      }
      // user is game master
    } else if (user_id == dm_id) {
      // note privacy has been changed
      if (changed) {
        // note was draft
        if (was_draft) {
          // went from being draft to being for dm_only
          if (to_dm && !draft) {
            // fill dm socket
            fill_note_made_public(
              editted_note[dm_index],
              note_id_number,
              note_text
            );
            // went from being draft to being open
          } else if (!draft) {
            // fill socket
            fill_note_made_public(
              editted_note[dm_index],
              note_id_number,
              note_text
            );
          }
          // note was not draft
        } else {
          // is now draft
          if (draft) {
            // remove socket
            remove_socket(note_id_number);
            // was open. is now to_dm
          } else if (was_not_private) {
            // insert socket
            insert_socket(editted_note[dm_index], note_id_number, note_text);
            // was to_dm now open
          } else {
            // insert socket
            insert_socket(editted_note[dm_index], note_id_number, note_text);
          }
        }
        // note privacy hasn't changed
      } else {
        if (draft) {
          // do nothing
        } else if (to_dm) {
          // insert dm socket
          insert_socket(editted_note[dm_index], note_id_number, note_text);
        } else {
          // insert socket
          insert_socket(editted_note[dm_index], note_id_number, note_text);
        }
      }
      // user is neither orgin or game master
    } else {
      if (changed) {
        // note changed to draft or to_dm
        if (draft || to_dm) {
          // remove note
          remove_socket(note_id_number);
        } else {
          fill_note_made_public(
            editted_note[other_index],
            note_id_number,
            note_text
          );
        }
        // wasn't changed and isn't private
      } else if (!draft && !to_dm) {
        insert_socket(editted_note[other_index], note_id_number, note_text);
      }
    }
  }
);

// Remove deleted note for all users without reloading page
socket.on("remove_deleted_note", function (note_id_number) {
  let el_to_remove = get_note_element(note_id_number);
  el_to_remove.remove();
});
// this is to replace the hidden placeholder element with the new note
function fill_note_made_public(new_note, note_id_number, note_text) {
  let element__placeholder = document.querySelector(
    `span[data-placeholder_flag_id="${note_id_number}"]`
  );
  element__placeholder.insertAdjacentHTML("afterend", new_note);
  element__placeholder.remove();

  // apply logic
  filled_note_logic(note_id_number);

  // insert note body
  var element__notes_body = document.querySelector(
    `span[data-id_noteText="${note_id_number}"]`
  );
  element__notes_body.innerHTML = note_text;
}

// make and insert temp element into DOM as placeholder for other users if changing to from private to not private
socket.on(
  "make_filler",
  function (
    note_id_number,
    ordered_session_note_list,
    list_location,
    session_number,
    text,
    is_draft,
    to_dm,
    dm_id,
    game_id,
    user_id,
    note_id
  ) {
    let found = false;
    let top_of_session_flag = false;
    while (!found) {
      if (list_location == 0) {
        found = document.querySelector(
          `ul[data-idSession='${session_number}']`
        );
        top_of_session_flag = true;
      } else {
        let previous_note_id = ordered_session_note_list[list_location - 1];
        let element__previous = document.querySelector(
          `li[data-id_notecont="${previous_note_id}"]`
        );
        if (element__previous) {
          found = element__previous;
        } else {
          list_location += -1;
        }
      }
    }

    placeholder = `<span data-placeholder_flag_id="${note_id_number}" class="hidden"></span>`;
    if (top_of_session_flag) {
      found.insertAdjacentHTML("beforeend", placeholder);
    } else {
      found.insertAdjacentHTML("beforebegin", placeholder);
    }
    socket.emit(
      "filled",
      text,
      is_draft,
      to_dm,
      dm_id,
      game_id,
      user_id,
      note_id
    );
  }
);

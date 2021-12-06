// New Note form functions:
//
//
// //

function NewQuill(event, quill) {
  // Local Variables
  let element__newQuill_private = document.querySelector(flag__newQuillPrivate),
    element__newQuill_to_dm = document.querySelector(
      `input[data-flag="newQuillDm"]`
    ),
    element__newQuill_speaking_as = document.querySelector(
      `select[name="speaking_as"]`
    );
  // capture data
  let new_note_html = quill.root.innerHTML,
    new_note_private = element__newQuill_private.value,
    new_note_to_dm = false,
    speaking_as = element__newQuill_speaking_as.value;

  if (element__newQuill_to_dm) {
    new_note_to_dm = element__newQuill_to_dm.value;
  }

  // check to make sure note isn't empty
  if (quill.getText() == "\n") {
    alert("note cannot be empty");
    return false;

    // send data to server
  } else {
    socket.emit(
      "send_new_note",
      user_id,
      game_id,
      dm_id,
      speaking_as,
      current__session_number,
      new_note_html,
      new_note_private,
      new_note_to_dm
    );

    // clear editor
    quill.root.innerHTML = "";
    return false;
  }
}

// capture and send new note to server
function NewQuill_submitListener(quill) {
  // Local Variables
  var element__newQuill_formSession = document.querySelector(
    flag__newQuill_formSession
  );

  // Listener
  element__newQuill_formSession.addEventListener("submit", function (event) {
    // prevent page reload
    event.preventDefault();
    NewQuill(event, quill);
  });
}

// set new notes to populate after page load Function
// We do it this because wysiwig fomatting doesn't work otherwise
function insert_rich_note(note_session) {
  // Local Variables

  let index__noteText = 1,
    index__noteId = 0;

  for (let i = 0; i < js_dict[note_session].length; i++) {
    // set the attributes of each rich note
    let id__note = js_dict[note_session][i][index__noteId],
      note_rich = js_dict[note_session][i][index__noteText],
      element__notes_noteText = document.querySelector(
        `span[data-id_noteText="${id__note}"]`
      );

    // insert rich note
    if (element__notes_noteText) {
      element__notes_noteText.innerHTML = note_rich;
    } else {
    }
  }
}

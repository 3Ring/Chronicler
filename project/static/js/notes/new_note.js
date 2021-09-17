// New Note form functions:
// 
// 
// //

function NewQuill(event) {

    // Local Variables
    let element__newQuill_private = document.querySelector(flag__newQuillPrivate);

    console.log("here")
    // capture data
    let new_note_html = quill.root.innerHTML
    , new_note_private = element__newQuill_private.value

    // check to make sure note isn't empty
    if (quill.getText() == '\n') {
        alert("note cannot be empty");
        return false

    // send data to server
    } else {
        socket.emit('send_new_note'
            , user_id
            , game_id
            , new_note_html
            , new_note_private
        )
        return false
    }

}

// capture and send new note to server
function NewQuill_submitListener() {

    // Local Variables
    var element__newQuill_formSession = document.querySelector(flag__newQuill_formSession);

    // Listener
    element__newQuill_formSession.addEventListener("submit", function (event) {
        // prevent page reload
        event.preventDefault();
        NewQuill(event);
    })
}

// set new notes to populate after page load Function 
// We do it this because wysiwig fomatting doesn't work otherwise
function insert_rich_note(note_session) {

    // Local Variables

    let index__noteText = 1
    , index__noteId = 0;

    for (let i = 0; i < js_dict[note_session].length; i++) {

        // set the attributes of each rich note
        let id__note = ( js_dict[note_session][i][index__noteId])
        , note_rich = js_dict[note_session][i][index__noteText]
        , flag__notes_noteText = "span[data-id_noteText='"+id__note+"']"
        , element__notes_noteText = document.querySelector(flag__notes_noteText);

        // insert rich note
        element__notes_noteText.innerHTML = note_rich;
    }
}
// socket.on Functions
// 
// 
// //

// Display new Session
socket.on('fill_new_session', function(new_card) {
    // Local Variables
    let element__sessionsContainer = document.querySelector(flag__sessionContainer);

    // Insert into document
    element__sessionsContainer.insertAdjacentHTML('afterbegin', new_card);
});


// display new note
socket.on('fill_new_note', function(new_note, priv, session_number) {
    // local Variables
    element = get_session_element(session_number);

    // Insert into document
    element.insertAdjacentHTML('beforeend', new_note);
});

// display note edit
socket.on('fill_note_edit', function(editted_note, is_private, session_number, note_id_number) {
    // local Variables
    note_location = get_note_element(note_id_number);

    // Insert into document
    note_location.innerHTML = editted_note;
});

// Remove deleted note for all users without reloading page
socket.on('remove_deleted_note', function(note_id_number) {
    let el_to_remove = get_note_element(note_id_number);
    el_to_remove.remove();
})

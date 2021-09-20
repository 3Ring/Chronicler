// socket.on Functions
// 
// 
// //

// Display new Session
socket.on('fill_new_session', function(new_session, new_list, session_number) {
    // Local Variables
    let element__sessionsContainer = document.querySelector(flag__sessionContainer)
    , element__sessionsList = document.querySelector("ul[data-flag='sessions_list']");

    remove_activeFlags_sessionList();
    
    

    // Insert into document
    element__sessionsContainer.insertAdjacentHTML('afterbegin', new_session);
    element__sessionsList.insertAdjacentHTML('afterbegin', new_list);

    // apply logic
    element__new_list = document.querySelector("li[data-number_sessionList='" + session_number + "']")
    element__new_list.addEventListener("click", function () {
    apply_sessionHighlightLogic_fromElement(element__new_list);
    // session container
    element__new_session = document.querySelector("div[data-number_sessionCont='" + session_number +"']");
    display_sessionCont(element__new_list);
    set_currentSessionVariable_fromElement(element__new_session);
    // session list

    })
});


// display new note
socket.on('fill_new_note', function(new_note, priv, session_number) {
    // local Variables
    element = get_session_element(session_number);

    // Insert into document
    element.insertAdjacentHTML('afterbegin', new_note);
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

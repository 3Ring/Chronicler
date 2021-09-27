// socket.on Functions
// 
// 
// //

// this is to add logic to notes populated throuck websocket
function filled_note_logic (note_id) {
    let socket_inserted_element_note_edit_form = document.querySelector(`form[data-id_formedit='${note_id}']`);
        socket_inserted_element_note_edit_form.addEventListener("submit", function (event) {
            let note_id = event.target.getAttribute("data-id_formedit")
            edit_note_func(note_id, event);
    })
}

// Display new Session
socket.on('fill_new_session', function(new_session, new_list, session_number) {

    // remove filler session title if first session
    let filler_session = document.querySelector(`li[data-number_sessionList="set_up"]`)
    if ( filler_session) {
        filler_session.remove();
    }
    // Local Variables
    let element__sessionsContainer = document.querySelector(flag__sessionContainer)
    , element__sessionsList = document.querySelector("ul[data-flag='sessions_list']");

    remove_activeFlags_sessionList();
    
    

    // Insert into document
    element__sessionsContainer.insertAdjacentHTML('afterbegin', new_session);
    element__sessionsList.insertAdjacentHTML('afterbegin', new_list);

    // update "New Session form's default number logic"
    if ( session_number > current__session_number ) {
        set_new_session_form_highest ( session_number );
    }

    // apply logic
    element__new_list = document.querySelector("li[data-number_sessionList='" + session_number + "']")
    element__new_list.addEventListener("click", function () {

        apply_sessionHighlightLogic_fromElement(element__new_list);
        // session container
        element__new_session = document.querySelector("div[data-number_sessionCont='" + session_number +"']");
        display_sessionCont(element__new_list);
        set_currentSessionVariable_fromElement(element__new_list);
    })
});


// display new note
socket.on('fill_new_note', function(new_note, private, to_dm, note_id, session_number) {
    // local Variables
    element = get_session_element(session_number);

    // Insert into document
    element.insertAdjacentHTML('afterbegin', new_note);

    // apply logic
    filled_note_logic(note_id);

});

// display note edit
socket.on('fill_note_edit', function(editted_note, is_private, session_number, note_id_number) {
    // find location of old note and insert new note in its place
    old_note_location = document.querySelector(`li[data-id_notecont="${note_id_number}"]`);
    old_note_location.insertAdjacentHTML("afterend", editted_note);
    old_note_location.remove();

    // apply logic
    filled_note_logic(note_id_number);
    
});

// Remove deleted note for all users without reloading page
socket.on('remove_deleted_note', function(note_id_number) {
    let el_to_remove = get_note_element(note_id_number);
    el_to_remove.remove();
})

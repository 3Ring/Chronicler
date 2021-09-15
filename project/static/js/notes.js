// Variables
var context_menu_class_name = "note_edit_menu_link"
, context_menu_prefix = "note_edit_menu_"
, context_menu_name = "note_edit_menu"

, edit_form_class_name = "edit_form"
, edit_form_prefix = "edit_form_"
, edit_form_text_prefix = "form_text_"
, edit_form_private_prefix = "change_private_"

, className__hidden = "hidden"
, active_class_name = "active"
, inner_id_prefix = "inner_"
, image_class_name = "note_edit_button"
, new_session_form_game_id = "new_session_form_game_id"
, menu_deployed = false

, flag__formEdit_form = "form[data-flag='formEdit']"

, flag__formNewSession_container = "div[data-flag='formNewSession_container']"
, flag__button_newSessionDisplay = "button[data-flag='button_newSessionDisplay']"
, flag__formNewSession_form = "form[data-flag='formNewSession_form']"
, flag__formNewSession_inputSessionNumber = "input[data-flag='formNewSession_inputSessionNumber']"
, flag__formNewSession_inputSessionTitle = "input[data-flag='formNewSession_inputSessionTitle']"
, flag__formNewSession_inputSessionSynopsis = "input[data-flag='formNewSession_inputSessionSynopsis"
, flag__formNewSession_buttonCancel = "input[data-flag='formNewSession_buttonCancel']"
, flag__formNewSession_idGame = "input[data-flag='formNewSession_idGame']"
, flag__newQuill_formSession = "form[data-flag='newQuill_FormSession']"

, flag__newQuillPrivate = "input[data-flag='newQuillPrivate']";





// socket.on Functions
// 
// 
// //

// Display new Session
socket.on('fill_new_session', function(new_card) {
    // Local Variables
    let flag__sessionContainer = "div[data-flag='sessionsContainer"
    , element__sessionsContainer = document.querySelector(flag__sessionContainer);

    // Insert into document
    element__sessionsContainer.insertAdjacentHTML('beforeend', new_card);
});


// display new note
socket.on('fill_new_note', function(new_note, priv, session_number) {
    // local Variables
    let flag__newNoteContainer = "ul[data-idSession='" + session_number + "']"
    , element__newNoteContainer = document.querySelector(flag__newNoteContainer);

    // Insert into document
    element__newNoteContainer.insertAdjacentHTML('beforeend', new_note);
});

// display note edit
socket.on('fill_note_edit', function(editted_note, is_private, session_number, note_id) {
    note_location = document.getElementById("inner_" + note_id);
    note_location.innerHTML = editted_note;
});

// Remove deleted note for all users
socket.on('remove_deleted_note', function(id_num) {
    let el_to_remove = document.getElementById("note_line_" + id_num)
    el_to_remove.remove();
})




// Note Edittor functions
//
//
// //

var attribute__editButtons = "data-editButtonAnchorId"
, attribute__editMenu = "data-editMenuId"
, attribute__contextForm = "data-contextMenuId";


// check if element or any of its parents contain the edit button
function click_inside_element( e, attribute ) {

    // Local Variables
    let el = e.target;

    // check if element clicked has attribute
    if ( el.hasAttribute(attribute) ) {
        return el;
    } else {

        // check if any of the parentNodes have the attribute
        while ( el = el.parentNode ) {
            if ( el.hasAttribute(attribute) ) {
                return el;
            
            // break before final loop otherwise it will throw an error
            } else if (el.parentNode == document) {
                break;
            }
        }
    }
    return false;
}

// hide all open menues
function toggle_menues_off() {

    // there should only be one, but this just makes sure
    actives = document.getElementsByClassName(active_class_name)
    for (let i = 0; i < actives.length; i++) {
        actives[i].classList.add(className__hidden);
        actives[i].classList.remove(active_class_name);
        menu_deployed = false;
    }
}

// deploy menu
function toggle_menu_on(element) {
    if (element.classList.contains(active_class_name)) {} else {
        element.classList.add(active_class_name);
        element.classList.remove(className__hidden);
        menu_deployed = true;
    }
}

// deploy note editting form
function toggle_form_on(id_num) {

    // Local variables
    let flag__formEdit = "form[data-id_formEdit='"+id_num+"']"
    , flag__notes_noteText = "span[data-id_noteText='"+id_num+"']"
    , flag__notes_editImage = "span[data-id_editImage='"+id_num+"']"
    , flag__formEdit_textArea = "input[data-id_formText='"+id_num+"']"

    , element__formEdit = document.querySelector(flag__formEdit)
    , element__notes_noteText = document.querySelector(flag__notes_noteText)
    , element__notes_editImage = document.querySelector(flag__notes_editImage)
    , element__formEdit_textArea = document.querySelector(flag__formEdit_textArea);


    // hide original note
    element__notes_noteText.classList.add(className__hidden);
    element__notes_editImage.classList.add(className__hidden);

    // display edit form
    element__formEdit.classList.remove(className__hidden);

    // highlight text to edit
    element__formEdit_textArea.select();
}

// hide note editting form
function toggle_form_off(id_num) {

    // Local Variables
    let flag__formEdit = "form[data-id_formEdit='"+id_num+"']" 
    , form_element = document.querySelector(flag__formEdit)

    // hide form
    form_element.classList.add(className__hidden);
}

// capture form data and send data to server
function edit_note_func(id_num) {

    // local variables
    let flag__notes_noteText = "span[data-id_noteText='"+id_num+"']"
    , flag__formEdit_form = "form[data-id_formEdit='"+id_num+"']"
    , flag__formEdit_private = "input[data-id_noteCheckboxPrivate='"+id_num+"']"
    , flag__notes_editImage = "span[data-id_editImage='"+id_num+"']"

    , element__formEdit_form = document.querySelector(flag__formEdit_form)
    , element__notes_editImage = document.querySelector(flag__notes_editImage)
    , element__notes_noteText = document.querySelector(flag__notes_noteText)
    , element__notes_checkboxPrivate = document.querySelector(flag__formEdit_private)

    // capture data
    , note_text = element__notes_noteText.innerHTML
    , note_private = element__notes_checkboxPrivate.value;

    // send to server
    socket.emit("edit_note", note_text, note_private, game_id, user_id, id_num);

    // remove form
    toggle_form_off(id_num);
    element__notes_noteText.classList.remove(className__hidden);
    element__notes_editImage.classList.remove(className__hidden);
    return false;
};


// Set click events to trigger contextual menu and deploy edit form
function click_listener() {

    document.addEventListener( "click", function( e ) {

        // check if edit button was clicked
        if ( click_inside_element( e, attribute__editButtons ) ) {

            // check if context  menu is already deployed
            if ( menu_deployed == false ) {

                // deploy context menu
                let flag__contextMenu = "div[data-contextMenuId='"+e.target.getAttribute("data-id_editImage")+"']"
                , element__contextMenu = document.querySelector( flag__contextMenu );
                toggle_menu_on( element__contextMenu );
            }
        } 
        // check if the click happened within the contextual form
        else if ( click_inside_element( e, attribute__contextForm ) ) {
            // check if the click happened within the edit menu
            if (click_inside_element( e, attribute__editMenu )) {

                // if the edit button was clicked
                if ( e.target.getAttribute("data-action") == "edit" ) {
                    
                    let id_num = e.target.getAttribute("data-id_note");

                    toggle_form_on(id_num);
                    toggle_menues_off();

                // if the delete button was clicked
                } else {
                    let id_num = e.target.getAttribute("data-id_note");
                    socket.emit("delete_note", id_num)
                }
            }
        } else {
            toggle_menues_off();
        }
    })
}

function submit_listener() {

    // Local Variables
    let elements__formEdit_form = document.querySelectorAll(flag__formEdit_form);

    // set listeners on all note editting forms in document
    for (let i = 0; i < elements__formEdit_form.length; i++) {
        elements__formEdit_form[i].addEventListener("submit", function (event) {

            // stop page reload
            event.preventDefault();
            let id_num = event.target.getAttribute("data-id_formEdit")

            // set function on form that handles the data
            edit_note_func(id_num);
        })
    }
}



// New Session form functions:
// 
// 
// //

// display form for making new session card
function newSessionForm_clickListener() {

    // Local Variables 
    let element__button_newSessionDisplay = document.querySelector(flag__button_newSessionDisplay)
    , element__formNewSession_container = document.querySelector(flag__formNewSession_container);

    element__button_newSessionDisplay.onclick = function() {

        element__formNewSession_container.classList.remove(className__hidden);
        element__button_newSessionDisplay.classList.add(className__hidden);
    }
}

// adds listener for cancel button click
function cancel_button_listener() {
    
    // Local Variables 
    let element__formNewSession_buttonCancel = document.querySelector(flag__formNewSession_buttonCancel);

    element__formNewSession_buttonCancel.onclick = cancel_new_session_func()
}

// function to remove new session form and add the edit button back
function cancel_new_session_func() {

    // Local Variables
    let element__button_newSessionDisplay = document.querySelector(flag__button_newSessionDisplay)
    , element__formNewSession_container = document.querySelector(flag__formNewSession_container);

    // add and removes hidden class
    element__formNewSession_container.classList.add(className__hidden);
    element__button_newSessionDisplay.classList.remove(className__hidden);
}

// check that all required data is there
function new_session_form_is_incomplete() {

    // Local Variables
    let element__formNewSession_inputNumber = document.querySelector(flag__formNewSession_inputSessionNumber)
    , element__formNewSession_inputTitle = document.querySelector(flag__formNewSession_inputSessionTitle);

    // check each field to see if it's empty
    // Session Title
    if ( element__formNewSession_inputTitle.value == '' || element__formNewSession_inputTitle.value == null ) {
        return true;

    // check to make sure the number isn't zero which will mess up the rest of the algo's logic
    } else if ( element__formNewSession_inputNumber.value == 0 ) {

        // skip child conditionals if session zero
    } else {

        // Session Number
        if ( element__formNewSession_inputNumber.value == '' || element__formNewSession_inputNumber.value == null ) {
            return true;

        // Check if the number field contains an integer
        } else if ( parseInt( element__formNewSession_inputNumber.value ) == '' || parseInt( element__formNewSession_inputNumber.value ) == null ) {
            return true;
        } 
    }
    return false;
}

// check to make sure the session doesn't already exist
function new_session_form_is_not_unique() {

    // Local Variables
    let element__formNewSession_inputNumber = document.querySelector(flag__formNewSession_inputSessionNumber);

    if ( document.querySelector( "ul[data-idSession='"+element__formNewSession_inputNumber.value+"']" ) ) {
        return true;
    } else {
        return false;
    }
}


// Validation of new session
function newSession__validateFormError() {

    if ( new_session_form_is_incomplete() ) { 
        alert("Must fill out required fields");
        return true;

    } else if ( new_session_form_is_not_unique() ) {
        alert("Session number must be unique");
        return true;

    } else {
        return false;
    }
}

// capture and send new session to server
function newSession__submitListener() {

    // Local Variables
    let element__formNewSession_form = document.querySelector(flag__formNewSession_form)
    , element__formNewSession_inputTitle = document.querySelector(flag__formNewSession_inputSessionTitle)
    , element__formNewSession_inputNumber = document.querySelector(flag__formNewSession_inputSessionNumber)
    , element__formNewSession_inputSynopsis = document.querySelector(flag__formNewSession_inputSessionSynopsis);

    element__formNewSession_form.addEventListener( "submit", function( event ) {
        
        // stop page from reloading
        event.preventDefault();

        // ensure that form is filled out correctly
        newSession__validateFormError()

        // send new session data to server through socket.io
        socket.emit('send_new_session', game_id, element__formNewSession_inputNumber.value, element__formNewSession_inputTitle.value, element__formNewSession_inputSynopsis.value);
        
        // remove new session form
        cancel_new_session_func();
        return false;
    })
}

function NewSessionMaker() {
    newSessionForm_clickListener();
    newSession__submitListener();
    cancel_button_listener();
}


// Checkbox functions
// 
//
// //

function set_true_checkboxes_to_checked() {
    // find all checkboxes
    let checkboxes = document.querySelectorAll("input[type='checkbox']");
    
    // make a list of the checkboxes that have a value of "True"
    let checkboxes__true = [];
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].value == "True") {
            checkboxes__true.push(checkboxes[i])
        }
    }


    // Set Checkboxes with a value of "True" to checked
    for (let i = 0; i < checkboxes__true.length; i++) {
        checkboxes__true[i].checked = true;
    }
}
function change_checkbox_value_onClick() {
    // find all checkboxes
    let checkboxes = document.querySelectorAll("input[type='checkbox']");

    // set click events
    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].addEventListener("click", function(event) {
            // find event origin
            let clicked = event.target;

            // change value to opposite of current
            if (clicked.value == "True") {
                clicked.value = "False";
            } else {
                clicked.value = "True";
            }
        })
    }
}
function apply_checkbox_value_logic() {
    // run subprograms
    set_true_checkboxes_to_checked();
    change_checkbox_value_onClick();
}



// New Note form functions:
// 
// 
// //

function NewQuill(event) {

    // Local Variables
    let element__newQuill_private = document.querySelector(flag__newQuillPrivate);

    // prevent page reload
    event.preventDefault();

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
        NewQuill(event);
    })
}

// set new notes to populate after page load Function 
// We do it this because wysiwig fomatting doesn't work otherwise
function insert_rich_note(note_session) {

    // Local Variables

    let note_id_index = 0
    , index__noteText = 1
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



// Main Function
// 
// 
// //

// Start app
function init() {

// note editting functions
click_listener();
submit_listener();

// general functions
apply_checkbox_value_logic();

// newSession functions
NewSessionMaker();

// Quill functions
NewQuill_submitListener();
}


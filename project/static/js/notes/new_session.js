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

    element__formNewSession_buttonCancel.addEventListener("click", function () {
        cancel_new_session_func();
    })
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
        return false;

    } else if ( new_session_form_is_not_unique() ) {
        alert("Session number must be unique");
        return false;

    } else {
        return true;
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
        validated = newSession__validateFormError()

        if ( validated ) {
            // send new session data to server through socket.io
            socket.emit('send_new_session'
                , game_id
                , element__formNewSession_inputNumber.value
                , element__formNewSession_inputTitle.value
                , element__formNewSession_inputSynopsis.value);
        }
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

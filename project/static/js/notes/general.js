// Helper functions
//
//
// //

// return correct note element when passed its ID
function get_note_element(note_id_number) {
    let flag = "span[data-id_noteText='"+note_id_number+"']"
    , element = document.querySelector(flag);
    return element
}

// return correct session container element when passed the session number
function get_session_element(session_number) {
    let flag = "ul[data-idSession='"+session_number+"']"
    , element = document.querySelector(flag);
    return element
}

// return inner html from Quill editor from event
function get_quill_text_from_event(event) {

    // Local Variables
    let el = event.target;

    // if the event originated from the editor
    if  (el.classList.contains( "ql-editor" ) ) {
        return el.innerhtml;
    } 

    // iterate through the child elements until editor is found
    while ( el = el.firstElementChild ) {
        if  (el.classList.contains( "ql-editor" ) ) {
            return el.innerhtml;
        }
    }
    // if the editor isn't found
    return "Quill editor not found"
}



// Checkbox functions
// 
//
// //

// set checkbox inputs that have a value of true on page load to checked
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
// add click event to checkbox inputs that changes their value True/False depending on whether or not it is checkedc
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
// Compiles checkbox functions into one function for init()
function Checkbox_logic() {

    // run subprograms
    set_true_checkboxes_to_checked();
    change_checkbox_value_onClick();
}



// Hide Sessions that aren't in focus
//
//


// Set active hook to most recent session on page load
function setActiveSession__onPageLoad () {

    // Local Variables
    let highest = 0
    , flag__containers_session = "div[data-flag='session_cont']"

    // get list of session containers
    , elements__containers_session = document.querySelectorAll(flag__containers_session);

    // check if there are any session db yet
    if ( elements__containers_session.length != 0 ) {
        // iterate through session elements to find most recent one
        
        for ( let i = 0, session_number = 0; i < elements__containers_session.length; i++ ) {
            // find session number of current element
            session_number = parseInt(elements__containers_session[i].getAttribute("data-number_sessionCont"))
            // check if the number is the highest one
            console.log(highest, session_number)
            if ( session_number > highest ) { highest = session_number }
        }

        // Flag most recent session elements and display container

        // Session List
        let element__sessionList_mostRecent = document.querySelector("li[data-number_sessionList='" + highest + "']");
        element__sessionList_mostRecent.classList.add(className__active_sessionList);

        // Session Container
        let element__sessionCont_mostRecent = document.querySelector("div[data-number_sessionCont='" + highest + "']");
        element__sessionCont_mostRecent.classList.add(className__active)
            // Display container
            element__sessionCont_mostRecent.classList.remove(className__hidden);
    }
}

// change active class to element that was clicked on and remove from old session


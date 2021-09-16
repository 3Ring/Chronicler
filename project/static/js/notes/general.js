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

function Checkbox_logic() {

    // run subprograms
    set_true_checkboxes_to_checked();
    change_checkbox_value_onClick();
}
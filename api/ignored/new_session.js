// New Session form functions:
// variables
let form_container = document.getElementById(new_session_form_container_id)
, new_session_button = document.getElementById(new_session_button_id)
, cancel_button = document.getElementById(new_session_form_cancel_id)
, new_session_form = document.getElementById(new_session_form_id)
, game_id_input_element = document.getElementById(new_session_form_game_id)
, number_input_element = document.getElementById(new_session_form_number_id)
, title_input_element = document.getElementById(new_session_form_title_id)
, synopsis_input_element = document.getElementById(new_session_form_synopsis_id);

// create form for making new session card
new_session_button.onclick = function() {
    form_container.classList.remove(hidden_class_name);
    new_session_button.classList.add(hidden_class_name);
}

// function to remove new session form and add the button back
var cancel_new_session_func = function () {
    form_container.classList.add(hidden_class_name);
    new_session_button.classList.remove(hidden_class_name);
}
// remove form if cancel button is clicked
cancel_button.onclick = function() {
    cancel_new_session_func();
} 

// capture and send new session to server
new_session_form.addEventListener("submit", function() {
    // ensure that form is filled out correctly
    console.log("on_submit")
    if (game_id_input_element.value != '' && number_input_element.value != '' && title_input_element.value != '' && parseInt(number_input_element.value) > -1) {
        if (!document.getElementById("session_card_"+number_input_element.value)) {
            socket.emit('send_new_session', game_id_input_element.value, number_input_element.value, title_input_element.value, synopsis_input_element.value);
            cancel_new_session_func();
            return false;
        } else {
            alert("Session number must be unique");
            return false;
        }
    } else {
        alert("Must fill out required fields");
        return false;
    }
})
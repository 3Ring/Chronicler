const socket = io();

// Variables
var context_menu_class_name = "note_edit_menu_link"
, context_menu_prefix = "note_edit_menu_"
, context_menu_name = "note_edit_menu"

, edit_form_class_name = "edit_form"
, edit_form_prefix = "edit_form_"
, edit_form_text_prefix = "form_text_"
, edit_form_private_prefix = "change_private_"
, edit_form_in_character_prefix = "make_in_character_"

, hidden_class_name = "hidden"
, active_class_name = "--active"
, inner_id_prefix = "inner_"
, image_class_name = "note_edit_button"
, new_session_form_game_id = "new_session_form_game_id"
, menu_deployed = false

, new_session_form_container_id = "new_session_cont"
, new_session_button_id = "new_session_button"
, new_session_form_id = "new_session_form"
, new_session_form_number_id = "new_session_form_number"
, new_session_form_title_id = "new_session_form_title"
, new_session_form_synopsis_id = "new_session_form_synopsis"
, new_session_form_cancel_id = "cancel_new_session"

, new_note_form_id = "new_note_form"



// socket.on Functions
// 
// 
// 
// display new session card
socket.on('fill_new_session', function(new_card, number) {
    session_cards = document.getElementById('Session Cards')
    session_cards.insertAdjacentHTML('afterbegin', new_card)
});


// display new note
socket.on('fill_new_note', function(new_note, priv, session_number, in_character) {
    this_session = document.getElementById('note_list_' + session_number)
    this_session.insertAdjacentHTML('beforeend', new_note)
});

// display note edit
socket.on('fill_note_edit', function(editted_note, is_private, session_number, in_character, note_id) {
    note_location = document.getElementById("inner_" + note_id);
    note_location.innerHTML = editted_note;
});

// Remove deleted note for all users
socket.on('remove_deleted_note', function(id_num) {
    let el_to_remove = document.getElementById("note_line_" + id_num)
    el_to_remove.remove();
})




// Helper functions
//
//
//
//


function edit_note_func(id_num) {
    // send data to server
    let form = document.getElementById(edit_form_prefix + id_num);
    let note_text = document.getElementById(edit_form_text_prefix + id_num).value,
    note_private = document.getElementById(edit_form_private_prefix + id_num).value,
    note_in_character = document.getElementById(edit_form_in_character_prefix + id_num).value,
    user_id = {{current_user.id}},
    game_id = {{id}};
    socket.emit("edit_note", note_text, note_private, note_in_character, game_id, user_id, id_num);

    // removal of form logic
    toggle_form_off(id_num);
    let note = document.getElementById(inner_id_prefix + id_num);
    note.classList.remove(hidden_class_name);
    let img = document.getElementById(id_num);
    img.classList.remove(hidden_class_name);
    return false;
};

function click_inside_element( e, className ) {
  var el = e.srcElement || e.target;

  if ( el.classList.contains(className) ) {
    return el;
  } else {
    while ( el = el.parentNode ) {
      if ( el.classList && el.classList.contains(className) ) {
        return el;
      }
    }
  }
  return false;
}

function toggle_menu_off() {
    actives = document.getElementsByClassName(active_class_name)
    for (let i = 0; i < actives.length; i++) {
        actives[i].classList.add(hidden_class_name);
        actives[i].classList.remove(active_class_name);
        menu_deployed = false;
    }
}

function toggle_menu_on(element) {
    if (element.classList.contains(active_class_name)) {} else {
        element.classList.add(active_class_name);
        element.classList.remove(hidden_class_name);
        menu_deployed = true;
    }
}

function find_id(string) {
    var id = "";
    for (let i = 0; i < string.length; i++) {
        if (parseInt(string[i])) {
            id += string[i];
        }
    }
    return id;
}

function toggle_form_on(id_num) {

    let note_text = document.getElementById(inner_id_prefix + id_num);
    note_text.classList.add(hidden_class_name);
    let form = document.getElementById(edit_form_prefix + id_num);
    form.classList.remove(hidden_class_name);
    let img = document.getElementById(id_num);
    img.classList.add(hidden_class_name);
    let text_area = document.getElementById("form_text_" + id_num);
    text_area.select();
}

function toggle_form_off(id_num) {
    let form = document.getElementById(edit_form_prefix + id_num);
    form.classList.add(hidden_class_name);
}


dfjhaskl
document.addEventListener("DOMContentLoaded", function() { 

    // set the values of the checkboxes based on whether they are checked or not
    let checkboxes = document.getElementsByClassName("note_checkbox")

    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].onclick = function () {
            if (checkboxes[i].checked) {
                checkboxes[i].value = 'True';
            } else {
                checkboxes[i].value = 'False';
            }
        }
    }

    {% if current_user.id == dmid %}
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
    {% endif %}

    // New Note form functions:
    // Variables
    let new_note_form = document.getElementById(new_note_form_id)
    , new_note_form_user_id = document.getElementById('note_user_id')
    , new_note_form_note = document.getElementById('note_note')
    , new_note_form_private = document.getElementById('note_private')
    , new_note_form_in_character = document.getElementById('note_in_character')
    , new_note_form_game_id = document.getElementById('note_game_id')


    // capture and send new note to server
    new_note_form.addEventListener("submit", function() {
        console.log("test", new_note_form)
        if (!new_note_form_note) {
            alert("note cannot be empty");
            return false
        } else {
            console.log("note form submit")
            socket.emit('send_new_note'
                , new_note_form_user_id.value
                , new_note_form_game_id.value
                , new_note_form_note.value
                , new_note_form_private.value
                , new_note_form_in_character.value
            )
            return false
        }
    });

    let forms = document.getElementsByClassName(edit_form_class_name);
    for (let i = 0; i < forms.length; i++) {
        let id_num = find_id(forms[i].id);
        forms[i].addEventListener("submit", function () {
            edit_note_func(id_num)
        })
    }

    // Core functions
    function click_listener() {
        document.addEventListener("click", function(e) {
            if (click_inside_element( e, image_class_name )) {
                if (menu_deployed == false) {
                    let context_menu_element = document.getElementById(context_menu_prefix + e.target.id);
                    toggle_menu_on(context_menu_element);
                } 
            } else if (click_inside_element( e, context_menu_name )) {
                if (click_inside_element( e, context_menu_class_name )) {
                    if ( e.target.getAttribute("data-action") == "edit" ) {
                        toggle_menu_off();
                        let id_num = find_id(e.target.id);
                        toggle_form_on(id_num);
                    } else {
                        let id_num = find_id(e.target.id);
                        socket.emit("delete_note", id_num)
                    }
                }
            } else {
                toggle_menu_off();
            }
        })
    }

    function init () {
        click_listener();
    }

    init();

})


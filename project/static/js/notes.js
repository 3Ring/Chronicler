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

// , new_note_form_id = "new_note_form"
, new_note_form_id = "test_form_quill"
, quill_form_id = "test_form_quill"
, form_container_id = 'form-container';



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
    // let form = document.getElementById(edit_form_prefix + id_num)
    let note_text = document.getElementById(edit_form_text_prefix + id_num).value
    , note_private = document.getElementById(edit_form_private_prefix + id_num).value
    , note_in_character = document.getElementById(edit_form_in_character_prefix + id_num).value;


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

// Core
//
//
//
//

document.addEventListener("DOMContentLoaded", function() { 



    var test_form = document.getElementById(quill_form_id)

    , form = document.getElementById(form_container_id)
    , about = document.querySelector('input[name=about]');
    console.log("test_form: ", user_id, game_id, test_form, form, about)

    var quill = new Quill('#editor', { 
    modules: {
        toolbar: [
        ['bold', 'italic'],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        [{ list: 'ordered' }, { list: 'bullet' }]
        ]
    },
    placeholder: 'A note about this session.',
    theme: 'snow'
    });

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

    // New Note form functions:
    // Variables
    let new_note_form = document.getElementById(new_note_form_id)
    , new_note_form_private = document.getElementById('note_private')
    , new_note_form_in_character = document.getElementById('note_in_character');

    // capture and send new note to server
    new_note_form.addEventListener("submit", function(event) {
        event.preventDefault();
        let new_note_html = quill.root.innerHTML
        , new_note_private = new_note_form_private.value
        , new_note_in_character = new_note_form_in_character.value;

        if (quill.getText() == '\n') {
            alert("note cannot be empty");
            return false;
        } else {
            console.log("note form submit", user_id, game_id, new_note_html, new_note_private, new_note_in_character.value)
            socket.emit('send_new_note'
                , user_id
                , game_id
                , new_note_html
                , new_note_private
                , new_note_in_character
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

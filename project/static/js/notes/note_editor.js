// Note Editor functions
//
//
// //

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

// hide all open contextual menues
function toggle_menues_off() {

    // there should only be one, but this just makes sure
    actives = document.getElementsByClassName(className__active)
    for (let i = 0; i < actives.length; i++) {
        actives[i].classList.add(className__hidden);
        actives[i].classList.remove(className__active);
        menu_deployed = false;
    }
}

// deploy context menu
function toggle_menu_on(element) {
    if (element.classList.contains(className__active)) {} else {
        element.classList.add(className__active);
        element.classList.remove(className__hidden);
        menu_deployed = true;
    }
}
// function NewQuill(event) {

//     // Local Variables
//     let element__newQuill_private = document.querySelector(flag__newQuillPrivate);

//     // capture data
//     let new_note_html = quill.root.innerHTML
//     , new_note_private = element__newQuill_private.value

//     // check to make sure note isn't empty
//     if (quill.getText() == '\n') {
//         alert("note cannot be empty");
//         return false

//     // send data to server
//     } else {
//         socket.emit('send_new_note'
//             , user_id
//             , game_id
//             , new_note_html
//             , new_note_private
//         )
//         return false
//     }

// }
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

function Note_Editor() {
    click_listener();
    submit_listener();
}
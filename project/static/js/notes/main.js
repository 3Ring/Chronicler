// Main Function
// 
// 
// //

// Start app
function init(DM="") {

    // note editting functions
    Note_Editor();

    // general functions
    Checkbox_logic();

    // Quill functions
    NewQuill_submitListener();

    if (DM == "DM") {
        // newSession functions
        NewSessionMaker();
    }
}